
import cv2
import pickle

class CameraObject(object):
    def __init__(self, camera_settings):

        self.cap_index = camera_settings['camera_index']
        self.cap = cv2.VideoCapture(self.cap_index)

        # load homography from the file
        self.homography = pickle.load(open(camera_settings['homography_file'], "rb" ))

        print(self.homography)
        # set the camera resolution according the right settings
        camera_width = camera_settings["desired_width"]
        camera_height = camera_settings["desired_height"]
        ret = self.cap.set(3,camera_width); # width
        ret = self.cap.set(4,camera_height); # height

    # from camera coodinate system to table
    def get_transformed_point(self, x, y):
        new_x = (self.homography[0][0]*x + self.homography[0][1]*y + self.homography[0][2])/(self.homography[2][0]*x + self.homography[2][1]*y + self.homography[2][2])
        new_y = (self.homography[1][0]*x + self.homography[1][1]*y + self.homography[1][2])/(self.homography[2][0]*x + self.homography[2][1]*y + self.homography[2][2])
        return (math.floor(new_x), math.floor(new_y))

    def grab_image(self):
        return self.cap.read()

    def release(self):
        self.cap.release()
