import argparse
import base64
import json
import sys
import functools
import requests



def generate_json_data(image_filename, output_filename):
    """Translates the input file into a json output file.

    Args:
        input_file: a file object, containing lines of input to convert.
        output_filename: the name of the file to output the json to.
    """
    request_list = []

    DETECTION_TYPES = [
    'FACE_DETECTION:10',
    'CROP_HINTS:10',
    'LOGO_DETECTION:10',
    'LABEL_DETECTION:10',
    'TEXT_DETECTION:10',
    'WEB_DETECTION:10'
    ]
    features = "4:10"
    with open(image_filename, 'rb') as image_file:
        content_json_obj = {
            'content': base64.b64encode(image_file.read()).decode('UTF-8')
        }

    feature_json_obj = []
    for detectionType in DETECTION_TYPES:
        feature, max_results = detectionType.split(':', 1)
        feature_json_obj.append({
            'type': feature,
            'maxResults': int(max_results),
        })

    request_list.append({
        'features': feature_json_obj,
        'image': content_json_obj,
    })

    with open(output_filename, 'w') as output_file:
        json.dump({'requests': request_list}, output_file)


def get_google_analysis(image_filename):
    # Will give a response in the form of a dictionary with
    #    ["crop"] = approximate bounding box (x,y,width,height) if not found
    #    ["items"] = possible names of the item
    #    ["best_guess"] = Hopefully string readible title for the object

    output_filename = "google_image_data.json"

    generate_json_data(image_filename, output_filename)
    data = open(output_filename, 'rb').read()

    response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyBgalC41vkCLty97Je2bmgd9nXH8GeIyJA', data=data, headers={'Content-Type': 'application/json'})

    response_json = response.json()["responses"][0]
    results = {}

    if "cropHintsAnnotation" in response_json:
        vertices = response_json["cropHintsAnnotation"]["cropHints"][0]["boundingPoly"]["vertices"]
        print("Raw Cropping Vertices --- {}".format(vertices))
        x_vars = []
        y_vars = []
        for vertex_pair in vertices:
            x_vars.append(vertex_pair.get("x", 0))
            y_vars.append(vertex_pair.get("y", 0))

        results["crop"] = (min(x_vars), min(y_vars), max(x_vars) - min(x_vars),max(y_vars) - min(y_vars))
    else:
        results["crop"] = (0,0,0,0)
    best_guess = ""
    items = set()

    if "labelAnnotations" in response_json:
        entities = list(functools.reduce(lambda a, b: a + b ,map(lambda x: x.get("description").lower().split(" "), filter(lambda d: "description" in d, response_json["labelAnnotations"]))))
        items.update(entities)
        best_guess = response_json["labelAnnotations"][0]["description"]

    if "webDetection" in response_json:
        if "webEntities" in response_json["webDetection"]:
            entities = list(functools.reduce(lambda a, b: a + b ,map(lambda x: x.get("description").lower().split(" "), filter(lambda d: "description" in d, response_json["webDetection"]["webEntities"]))))
            items.update(entities)
        if "bestGuessLabels" in response_json["webDetection"]:
            best_guess = response_json["webDetection"]["bestGuessLabels"][0]["label"]


    results["items"] = list(items)
    results["best_guess"] = best_guess
    return results


# result = get_google_analysis("coffee.jpg")
