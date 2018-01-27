import numpy as np
import cv2
import time
import pygame
import sys
import math
import json
import os
from colors import *
from camera_api import *
import pickle

'''
    Click the points in order from 0 to 3 as they appear in the webcam screen.
'''

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/../settings.json", "r") as f:
    json_settings = json.load(f)

# get the screen height and width
SCREEN_WIDTH = json_settings["screen_settings"]["width"]
SCREEN_HEIGHT = json_settings["screen_settings"]["height"]

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# set the title of the window
pygame.display.set_caption(json_settings["title"])
clock = pygame.time.Clock()

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

    # f means take new picture
    if k == ord("f"):
        ret, frame = capture_object.grab_image()
        HOMOGRAPHY_POINT_COUNTER = 0
        points = []

    # q means quit
    elif k == ord("q"):
        break

    # keep showing the latest frame
    cv2.imshow("image", frame)

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
        pickle.dump(M, open(json_settings["camera_settings"]["homography_file"], "wb"))

    # set the background picture
    screen.fill(BLACK)

    # pygame font
    pygame_font = pygame.font.SysFont('Arial', 100)

    top_left = [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4]
    top_right = [SCREEN_WIDTH // 4 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4]
    bottom_left = [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + SCREEN_HEIGHT // 2]
    bottom_right = [SCREEN_WIDTH // 4 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + SCREEN_HEIGHT // 2]

    pygame.draw.circle(screen, WHITE, top_left, 100)
    screen.blit(pygame_font.render('0', True, (255,0,0)), top_left)

    pygame.draw.circle(screen, WHITE, top_right, 100)
    screen.blit(pygame_font.render('1', True, (255,0,0)), top_right)

    pygame.draw.circle(screen, WHITE, bottom_left, 100)
    screen.blit(pygame_font.render('2', True, (255,0,0)), bottom_left)

    pygame.draw.circle(screen, WHITE, bottom_right, 100)
    screen.blit(pygame_font.render('3', True, (255,0,0)), bottom_right)

    # pygame managament
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    pygame.display.flip()
    clock.tick(20)

# When everything done, release everything
capture_object.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
