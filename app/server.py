import os, json
from flask import Flask, render_template, request, jsonify
from computer_vision.camera_api import *
import cv2
import threading

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/config/settings.json", "r") as f:
    json_settings = json.load(f)

# get the screen height and width
SCREEN_WIDTH = json_settings["screen_settings"]["width"]
SCREEN_HEIGHT = json_settings["screen_settings"]["height"]
TARGET_SIZE = json_settings["screen_settings"]["target_size"]

LAST_CLICKED_POSITION = None

app = Flask(__name__)

# this is the main display
@app.route('/')
def main():
    return render_template('index.html',
                            screen_width=SCREEN_WIDTH,
                            screen_height=SCREEN_HEIGHT)

# this is the main display
@app.route('/calibrate_tester_page/')
def calibrate_tester_page():
    return render_template('calibrate_tester.html',
                            screen_width=SCREEN_WIDTH,
                            screen_height=SCREEN_HEIGHT)

@app.route('/get_point/')
def get_point():
    global LAST_CLICKED_POSITION
    if LAST_CLICKED_POSITION is not None:
        point = [LAST_CLICKED_POSITION[0],LAST_CLICKED_POSITION[1]]
    else:
        point = [-1,-1]
    return jsonify(result=point)

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

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
