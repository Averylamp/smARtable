from computer_vision.vision import *
import cv2
import cv2.aruco as aruco
import numpy as np
import math

# this function is used to compute the best point from
def filter_best_point(camera_objects, THRESH=150, KERNEL=(30,30)):
    '''
    Pass in the camera object list to get an averaged point result.
    '''
    points = []
    for camera_object in camera_objects:
        points.append(camera_object.get_box_of_interest(THRESH=THRESH, KERNEL=KERNEL))

    # get average where the point is not none
    x_average = 0.0
    y_average = 0.0
    num_points = 0.0
    for point in points:
        if point is not None:
            num_points += 1.0
            x_average += point[0]
            y_average += point[1]
    if num_points == 0:
        return None
    x_average /= num_points
    y_average /= num_points
    return (math.floor(x_average), math.floor(y_average))

def get_item_class(camera_objects):
    # use the first camera frame to get the google vision API output
    ret, frame = camera_objects[0].grab_image()
    cv2.imwrite("temp.jpg", frame)
    result = get_google_analysis("temp.jpg")
    # result has "items" and "best_guess"
    best = result["best_guess"]
    print("Best Guess: {}".format(best))
    return best


def aruco_filtered_best_point(camera_objects):
    points = []
    for camera_object in camera_objects:

        ret, frame = camera_object.grab_image()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        parameters =  cv2.aruco.DetectorParameters_create()

        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if corners != []:
            lowest_point = [1000,1000]
            for aruco_marker in corners[0]:
                for point in aruco_marker:
                    if point[1] < lowest_point[1]:
                        lowest_point = (math.floor(point[0]), math.floor(point[1]))
            return camera_object.get_transformed_point(lowest_point[0], lowest_point[1])
    return None
