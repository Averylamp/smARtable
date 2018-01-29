import requests, json
from computer_vision.camera_api import *
import cv2, os

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/config/settings.json", "r") as f:
    json_settings = json.load(f)

capture_object = CameraObject(json_settings["camera_settings"])

def mouse_listener(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # get transormed point
        new_x, new_y = capture_object.get_transformed_point(x, y)
        # print("Original (x,y): ({},{})".format(x,y))
        # print("New (x,y): ({},{})".format(new_x,new_y))
        r = requests.get("http://localhost:5000/set_click?x={}&y={}".format(new_x,new_y))

# create the windows
window_title = capture_object.camera_name
cv2.namedWindow(window_title)
cv2.setMouseCallback(window_title, mouse_listener)

ret, frame = capture_object.grab_image()
cv2.imshow(window_title, frame)

i = 0

while True:

    k = cv2.waitKey(1) & 0xFF

    # take picture and restart calibration
    if k == ord("f"):
        ret, frame = capture_object.grab_image()
        cv2.imshow(window_title, frame)

    # q means quit
    elif k == ord("q"):
        break
