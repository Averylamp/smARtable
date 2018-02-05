from computer_vision.vision import *
import cv2

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
    x_average /= point_num
    y_average /= point_num
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
