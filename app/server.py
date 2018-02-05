import os, json
from flask import Flask, render_template, request, jsonify
from computer_vision.camera_api import *
from computer_vision.camera_processes import *
import cv2
import threading
import time
from flask_socketio import SocketIO
from information import information_class as info

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/config/settings.json", "r") as f:
    json_settings = json.load(f)

camera_settings = json_settings["camera_settings"]
cameras = []
for camera_setting in camera_settings:
    cameras.append(CameraObject(camera_setting))
    # set_background(len(cameras) - 1)
    print("Camera {} Created ".format(len(cameras)))

# get the screen height and width
SCREEN_WIDTH = json_settings["screen_settings"]["width"]
SCREEN_HEIGHT = json_settings["screen_settings"]["height"]
TARGET_SIZE = json_settings["screen_settings"]["target_size"]

LAST_CLICKED_POSITION = None
main_camera = cameras[0]

app = Flask(__name__)
socketio = SocketIO(app)

# this is the main display
@app.route('/')
def main():
    global SCREEN_HEIGHT, SCREEN_WIDTH
    return render_template('index.html',
                            screen_width=SCREEN_WIDTH,
                            screen_height=SCREEN_HEIGHT)
@app.route('/blank/')
def blank_screen():
    global SCREEN_HEIGHT, SCREEN_WIDTH
    return render_template('blank_index.html',
                            screen_width=SCREEN_WIDTH,
                            screen_height=SCREEN_HEIGHT)

# this is the main display
@app.route('/calibrate_tester_page/')
def calibrate_tester_page():
    return render_template('calibrate_tester.html',
                            screen_width=SCREEN_WIDTH,
                            screen_height=SCREEN_HEIGHT)

@app.route('/set_camera/<camera_number>')
def set_camera(camera_number = 0):
    global main_camera
    global cameras
    main_camera = cameras[camera_number]
    return "Successful set"

@app.route('/get_point/')
def get_point():
    global LAST_CLICKED_POSITION, main_camera, cameras
    if LAST_CLICKED_POSITION is not None:
        point = [LAST_CLICKED_POSITION[0],LAST_CLICKED_POSITION[1]]
    else:
        # point = [2,2]
        camera_number = request.args.get('camera_number', 0, type=int)
        main_camera = cameras[camera_number]
        point = cameras[camera_number].get_box_of_interest(THRESH=150, KERNEL=(30,30))
        print("Setting new point with camera {}".format(camera_number))
        if point is None:
            point = [2,2]
    return jsonify(result=point)

@app.route('/set_backgrounds/')
def set_all_backgrounds():
    for i in range(len(cameras)):
        set_background(i)
    return "Setting backgrounds success"

@app.route('/set_background/<camera_number>')
def set_background(camera_number = 0):
    global cameras
    print("Setting background for camera: {}".format(camera_number))
    try:
        ret, img = cameras[camera_number].grab_image()
        cv2.imwrite(dir_path+"/config/{}/background.png".format(cameras[camera_number].camera_name), img)
        print("Wrote background image to:  " + dir_path+"/config/{}/background.png".format(cameras[camera_number].camera_name))
        return "Wrote background image to:  " + dir_path+"/config/{}/background.png".format(cameras[camera_number].camera_name)
    except:
        return "Writing new background image failed"

@app.route('/get_screen/')
def get_screen():
    global LAST_CLICKED_POSITION
    if LAST_CLICKED_POSITION is not None:
        corners = [0,0,LAST_CLICKED_POSITION[0],LAST_CLICKED_POSITION[1]]
    else:
        corners = [0,0,0,0]
    return jsonify(result=corners)

@app.route('/set_click/')
def set_click():
    global LAST_CLICKED_POSITION
    x = request.args.get('x', 0, type=int)
    y = request.args.get('y', 0, type=int)
    LAST_CLICKED_POSITION = [x,y]
    print(LAST_CLICKED_POSITION)
    return jsonify(result=True)


# calibrate is functional
@app.route('/calibrate/')
def calibrate():
    global SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_SIZE
    # relead on a refresh because this potentially takes fine tuning
    with open(dir_path + "/config/settings.json", "r") as f:
        json_settings = json.load(f)

    # get the screen height and width
    SCREEN_WIDTH = json_settings["screen_settings"]["width"]
    SCREEN_HEIGHT = json_settings["screen_settings"]["height"]
    TARGET_SIZE = json_settings["screen_settings"]["target_size"]

    return render_template('calibrate.html',
                            screen_width=SCREEN_WIDTH,
                            screen_height=SCREEN_HEIGHT,
                            target_size=TARGET_SIZE)

def main_loop():
    global cameras
    while True:
        print("working")
        # point = filter_best_point(cameras, THRESH=150, KERNEL=(30,30))
        point = cameras[0].get_box_of_interest(THRESH=150, KERNEL=(30,30))
        if point is not None:
            socketio.emit("get_point", {"result":[point[0],point[1]]}, broadcast=True)
            print(point)
        # only update every X second(s)
        # s = get_item_class(cameras)
        # r = info.get_product_info(s)
        # res = {"direction":"top","top":5,"left":10,"result":r}
        # socketio.emit("information", res, broadcast=True)
        time.sleep(1)

if __name__ == '__main__':
    my_thread = threading.Thread(target=main_loop)
    my_thread.start()
    socketio.run(app)
    app.run(debug=False, threaded=True)
