import numpy as np
import cv2
import time
import math
import json
import os
from computer_vision.camera_api import *
import pickle

'''
    Click the points in order from 0 to 3 as they appear in the webcam screen.
'''

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/config/settings.json", "r") as f:
    json_settings = json.load(f)

# get the screen height and width
SCREEN_WIDTH = json_settings["screen_settings"]["width"]
SCREEN_HEIGHT = json_settings["screen_settings"]["height"]

capture_object = CameraObject(json_settings["camera_settings"])

HOMOGRAPHY_POINT_COUNTER = 0
points = []

# will hold the mapping
M = None

def get_transformed_point(x, y, M):
    new_x = (M[0][0]*x + M[0][1]*y + M[0][2])/(M[2][0]*x + M[2][1]*y + M[2][2])
    new_y = (M[1][0]*x + M[1][1]*y + M[1][2])/(M[2][0]*x + M[2][1]*y + M[2][2])
    return (math.floor(new_x), math.floor(new_y))

def mouse_listener(event, x, y, flags, param):
    global HOMOGRAPHY_POINT_COUNTER
    global M
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        cv2.circle(frame,(x,y),10,(0,255,0),-1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str(HOMOGRAPHY_POINT_COUNTER),(x,y), font, 2, (255,255,255),2,cv2.LINE_AA)
        cv2.imshow("image", frame)
        HOMOGRAPHY_POINT_COUNTER += 1

# create the windows
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_listener)

ret, frame = capture_object.grab_image()
cv2.imshow("image", frame)

# variables defined for the mapping later
w_size = int(SCREEN_WIDTH/4)
h_size = int(SCREEN_HEIGHT/4)

# HOMOGRAPHY CALIBRATION
while M is None:

    k = cv2.waitKey(1) & 0xFF

    # take picture and restart calibration
    if k == ord("f"):
        print("Taking picture and starting over.")
        ret, frame = capture_object.grab_image()
        cv2.imshow("image", frame)
        HOMOGRAPHY_POINT_COUNTER = 0
        points = []

    # q means quit
    elif k == ord("q"):
        break

    # when all points are found
    if HOMOGRAPHY_POINT_COUNTER == 4:

        # do the transformation
        pts1 = np.float32(points)
        pts2 = np.float32([
            [(SCREEN_WIDTH/2.0)-w_size,(SCREEN_HEIGHT/2.0)-h_size],
            [(SCREEN_WIDTH/2.0)+w_size,(SCREEN_HEIGHT/2.0)-h_size],
            [(SCREEN_WIDTH/2.0)-w_size,(SCREEN_HEIGHT/2.0)+h_size],
            [(SCREEN_WIDTH/2.0)+w_size,(SCREEN_HEIGHT/2.0)+h_size]])

        M = cv2.getPerspectiveTransform(pts1,pts2)
        filename = json_settings["camera_settings"]["homography_file"]
        pickle.dump(M, open(filename, "wb"))
        print("Saving {} and exiting.".format(filename))

# When everything done, release everything
capture_object.release()
cv2.destroyAllWindows()