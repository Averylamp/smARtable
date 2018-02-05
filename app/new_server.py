from flask import Flask, render_template, request, jsonify
from computer_vision.camera_api import *
from information import information_class as info 
from flask_socketio import SocketIO

import os, json
import cv2
import threading

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/config/settings.json", "r") as f:
    json_settings = json.load(f)

camera = CameraObject(json_settings["camera_settings"])

# get the screen height and width
SCREEN_WIDTH = json_settings["screen_settings"]["width"]
SCREEN_HEIGHT = json_settings["screen_settings"]["height"]
TARGET_SIZE = json_settings["screen_settings"]["target_size"]

LAST_CLICKED_POSITION = None

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on("connect")
def connect():
    print("A new client has connected")

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

@socketio.on('get_point')
def get_point():
    global LAST_CLICKED_POSITION
    if LAST_CLICKED_POSITION is not None:
        point = [LAST_CLICKED_POSITION[0],LAST_CLICKED_POSITION[1]]
    else:
        # point = [2,2]
        point = camera.get_box_of_interest()
        if point is None:
            point = [2,2]
    return emit("get_point", jsonify(result=point))

@app.route('/set_background')
def set_background():
    ret, img = camera.grab_image()
    cv2.imwrite(dir_path+"/background/{}.png".format(camera.camera_name), img)
    return emit("set_background", jsonify(result=ret))

@socketio.on('get_screen')
def get_screen():
    global LAST_CLICKED_POSITION
    if LAST_CLICKED_POSITION is not None:
        corners = [0,0,LAST_CLICKED_POSITION[0],LAST_CLICKED_POSITION[1]]
    else:
        corners = [0,0,0,0]
    return emit("get_screen", jsonify(result=corners))

@app.route("/test")
def test():
    x = int(request.args.get('x', 0, type=int))
    y = int(request.args.get('y', 0, type=int))
    print(x,y)
    point = [x,y]
    data = {"x":x, "y":y}
    return socketio.emit("message", data, broadcast=True) 

@socketio.on('set_click')
def set_click():
    global LAST_CLICKED_POSITION
    x = request.args.get('x', 0, type=int)
    y = request.args.get('y', 0, type=int)
    LAST_CLICKED_POSITION = [x,y]
    print(LAST_CLICKED_POSITION)
    return emit("set_click", jsonify(result=True))

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

def send_item_info(item):
    emit("information", info.get_product_info(item))

@socketio.on("echo")
def debug(msg):
    print(msg)
    socketio.emit(msg['title'], msg['data'], broadcast=True)

@socketio.on("message")
def debug(msg):
    print(msg)
    socketio.emit("message", msg)

if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=False, threaded=True)
