import requests, json
from computer_vision.camera_api import *
import cv2, os
import threading
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/config/settings.json", "r") as f:
    json_settings = json.load(f)


def create_tester_for_camera(camera_settings):
    print(camera_settings)
capture_objects = []
capture_objects_configs = json_settings["camera_settings"]
for camera_setting in capture_objects_configs:
    capture_objects.append(CameraObject(camera_setting))
capture_object = capture_objects[0]

def mouse_listener(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # get transormed point
        new_x, new_y = capture_object.get_transformed_point(x, y)
        # print("Original (x,y): ({},{})".format(x,y))
        # print("New (x,y): ({},{})".format(new_x,new_y))
        r = requests.get("http://localhost:5000/set_click?x={}&y={}&camera_number={}".format(new_x,new_y, capture_objects.index(capture_object)))

# create the windows
window_title = "Calibration Testing"
cv2.namedWindow(window_title)
cv2.setMouseCallback(window_title, mouse_listener)

ret, frame = capture_object.grab_image()
cv2.imshow(window_title, frame)

i = 0
current_time = time.time()

while True:

    k = cv2.waitKey(1) & 0xFF
    if time.time() - current_time > 0.25:
        current_time = time.time()
        ret, frame = capture_object.grab_image()
        cv2.imshow(window_title, frame)

    def mouse_listener(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # get transormed point
            new_x, new_y = capture_object.get_transformed_point(x, y)
            print("Original (x,y): ({},{})".format(x,y))
            print("New (x,y): ({},{})".format(new_x,new_y))
            r = requests.get("http://localhost:5000/set_click?x={}&y={}&camera_number={}".format(new_x,new_y, capture_objects.index(capture_object)))

    # take picture and restart calibration
    if k == ord("f"):
        ret, frame = capture_object.grab_image()
        cv2.imshow(window_title, frame)
    if k == ord("1"):
        r = requests.get("http://localhost:5000/set_camera/{}".format(0))
        capture_object = capture_objects[0]
        ret, frame = capture_object.grab_image()
        cv2.imshow(window_title, frame)
        cv2.setMouseCallback(window_title, mouse_listener)
    if k == ord("2"):
        if len(capture_objects) >= 2:
            r = requests.get("http://localhost:5000/set_camera/{}".format(1))
            capture_object = capture_objects[1]
            ret, frame = capture_object.grab_image()
            cv2.imshow(window_title, frame)
            cv2.setMouseCallback(window_title, mouse_listener)
    if k == ord("3"):
        if len(capture_objects) >= 3:
            r = requests.get("http://localhost:5000/set_camera/{}".format(2)) 
            capture_object = capture_objects[2]
            ret, frame = capture_object.grab_image()
            cv2.imshow(window_title, frame)
            cv2.setMouseCallback(window_title, mouse_listener)
    if k == ord("4"):
        if len(capture_objects) >= 4:
            r = requests.get("http://localhost:5000/set_camera/{}".format(3))
            capture_object = capture_objects[3]
            ret, frame = capture_object.grab_image()
            cv2.imshow(window_title, frame)
            cv2.setMouseCallback(window_title, mouse_listener)

    # q means quit
    elif k == ord("q"):
        break
