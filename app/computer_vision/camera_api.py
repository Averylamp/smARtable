
import cv2
import pickle
import threading
import math

class CameraObject(object):
    def __init__(self, camera_settings):

        self.cap_index = camera_settings['camera_index']
        self.cap = cv2.VideoCapture(self.cap_index)
        self.camera_name = camera_settings["camera_name"]

        # load homography from the file
        self.homography = pickle.load(open(camera_settings['homography_file'], "rb" ))

        # print(self.homography)
        # set the camera resolution according the right settings
        camera_width = camera_settings["desired_width"]
        camera_height = camera_settings["desired_height"]
        ret = self.cap.set(3,camera_width); # width
        ret = self.cap.set(4,camera_height); # height

        self.last_clicked_position = None

    # from camera coodinate system to table
    def get_transformed_point(self, x, y):
        new_x = (self.homography[0][0]*x + self.homography[0][1]*y + self.homography[0][2])/(self.homography[2][0]*x + self.homography[2][1]*y + self.homography[2][2])
        new_y = (self.homography[1][0]*x + self.homography[1][1]*y + self.homography[1][2])/(self.homography[2][0]*x + self.homography[2][1]*y + self.homography[2][2])
        return (math.floor(new_x), math.floor(new_y))

    def grab_image(self):
        return self.cap.read()

    def release(self):
        self.cap.release()

    def mouse_listener(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.last_clicked_position = [x, y]
            print(self.last_clicked_position)

    # def create_window(self):
    #     thread = threading.Thread(target=self.window_thread, args=())
    #     thread.daemon = True
    #     thread.start()

    def window_thread(self):
        # create the windows
        window_title = self.camera_name
        # cv2.startWindowThread()
        cv2.namedWindow(window_title)
        cv2.setMouseCallback(window_title, self.mouse_listener)

        ret, frame = self.grab_image()
        cv2.imshow(window_title, frame)

        while True:

            k = cv2.waitKey(1) & 0xFF

            # take picture and restart calibration
            if k == ord("f"):
                ret, frame = self.grab_image()
                cv2.imshow(window_title, frame)

            # q means quit
            elif k == ord("q"):
                break

    def get_latest_position(self):
        return self.last_clicked_position
