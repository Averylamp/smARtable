
import cv2
import pickle
import threading
import math
import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class CameraObject(object):
    def __init__(self, camera_settings, SCREEN_WIDTH = 1920, SCREEN_HEIGHT = 1080):

        self.cap_index = camera_settings['camera_index']
        self.cap = cv2.VideoCapture(self.cap_index)
        self.camera_name = camera_settings["camera_name"]
        # self.background_image_path = camera_settings["background_subtract"]

        # load homography from the file
        self.homography = pickle.load(open(camera_settings['homography_file'], "rb" ))
        self.inv_homography = pickle.load(open(camera_settings['inv_homography_file'], "rb" ))

        # print(self.homography)
        # set the camera resolution according the right settings
        camera_width = camera_settings["desired_width"]
        camera_height = camera_settings["desired_height"]
        ret = self.cap.set(3,camera_width); # width
        ret = self.cap.set(4,camera_height); # height

        self.last_clicked_position = None

        # create the mask
        ret, frame = self.grab_image()
        self.mask = np.zeros((len(frame),len(frame[0])), dtype=np.uint8) # height, width
        corners = []
        corners.append(self.get_inv_transformed_point(0,0))
        corners.append(self.get_inv_transformed_point(SCREEN_WIDTH,0))
        corners.append(self.get_inv_transformed_point(SCREEN_WIDTH,SCREEN_HEIGHT))
        corners.append(self.get_inv_transformed_point(0,SCREEN_HEIGHT))
        cv2.fillConvexPoly(self.mask, np.array(corners, np.int32), 255)

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.mask = self.mask.astype(np.uint8)


    # from camera coodinate system to table
    def get_transformed_point(self, x, y):
        new_x = (self.homography[0][0]*x + self.homography[0][1]*y + self.homography[0][2])/(self.homography[2][0]*x + self.homography[2][1]*y + self.homography[2][2])
        new_y = (self.homography[1][0]*x + self.homography[1][1]*y + self.homography[1][2])/(self.homography[2][0]*x + self.homography[2][1]*y + self.homography[2][2])
        return (math.floor(new_x), math.floor(new_y))

    # from table coordinates to camera coordinates
    def get_inv_transformed_point(self, x, y):
        new_x = (self.inv_homography[0][0]*x + self.inv_homography[0][1]*y + self.inv_homography[0][2])/(self.inv_homography[2][0]*x + self.inv_homography[2][1]*y + self.inv_homography[2][2])
        new_y = (self.inv_homography[1][0]*x + self.inv_homography[1][1]*y + self.inv_homography[1][2])/(self.inv_homography[2][0]*x + self.inv_homography[2][1]*y + self.inv_homography[2][2])
        return (math.floor(new_x), math.floor(new_y))

    def grab_image(self):
        ret, img = self.cap.read()
        return (ret, img)

    def release(self):
        self.cap.release()

    def mouse_listener(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.last_clicked_position = [x, y]
            print(self.last_clicked_position)

    def get_cropped_polgon_region(self, image, corners):

        mask = np.zeros((len(image),len(image[0])), dtype=image.dtype) # height, width
        cv2.fillConvexPoly(mask, np.array(corners, np.int32), 255)
        mask = mask.astype(np.uint8)

        return self.get_masked_section(image, mask)

    def get_masked_section(self, image, mask):
        output = image.copy()
        for i in range(len(image)):
            for j in range(len(image[0])):
                if mask[i][j] != 255:
                    output[i][j] = 0
        return output

    def get_box_of_interest(self, THRESH=100, KERNEL=(30,30)):
        background = cv2.imread("config/{}/background.png".format(self.camera_name))
        ret, frame = self.grab_image()

        difference = np.absolute(np.subtract(frame, background))

        # filter the image
        kernel = np.ones(KERNEL,np.uint8)
        filtered = cv2.erode(difference,kernel,iterations=1)
        kernel = np.ones(KERNEL,np.uint8)
        filtered = cv2.dilate(filtered,kernel,iterations=1)

        # convert to grayscale
        filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

        # set as 0 for this range
        filtered = np.where(np.logical_and(0<=filtered, filtered<=THRESH), 0, filtered)
        filtered = np.where(np.logical_and(THRESH<filtered, filtered<=255), 255, filtered)

        cv2.imwrite("config/{}/filtered.png".format(self.camera_name), filtered)

        im2, contours, hierarchy = cv2.findContours(filtered,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        best_density = 0.0
        best_size = 0.0
        best_contour = None
        for contour in contours:
            # get the bounding rect
            x, y, w, h = cv2.boundingRect(contour)

            corners = []
            corners.append(self.get_transformed_point(x,y))
            corners.append(self.get_transformed_point(x,y+h))
            corners.append(self.get_transformed_point(x+w,y))
            corners.append(self.get_transformed_point(x+w,y+h))

            valid_corners = True

            # make sure it isn't off the screen
            for corner in corners:
                if corner[0] < 0 or corner[0] > self.SCREEN_WIDTH or corner[1] < 0 or corner[1] > self.SCREEN_HEIGHT:
                    valid_corners = False
                    break

            size = w*h
            # for size
            if size >= best_size and valid_corners:
                best_size = size
                best_contour = contour

        # density based code
            # if size > 100:
            #     density = 0.0
            #     count = 0.0
            #     for i in range(y,y+h):
            #         for j in range(x,x+w):
            #             count += im2[i][j] / 255.0
            #     density = count / (w*h)
            #     if density >= best_density:
            #         best_density = density
            #         best_contour = contour

        if best_contour is not None:
            x, y, w, h = cv2.boundingRect(best_contour)
            center = (x+w//2,y+h//2)

            # draw a green rectangle and blue circle
            expansion = 20
            cv2.rectangle(frame, (x-expansion, y-expansion), (x+w+expansion, y+h+expansion), (0, 255, 0), 2)
            radius = 5
            cv2.circle(frame, center, radius, (255, 0, 0), 10)
            cv2.imwrite("config/{}/current_frame.png".format(self.camera_name), frame)

            return self.get_transformed_point(center[0], center[1])
        else:
            return None

    def get_latest_position(self):
        return self.last_clicked_position
