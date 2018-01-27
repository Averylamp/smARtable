import numpy as np
import cv2
import time
import pygame, sys
import math
from pygame.locals import *

################################

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Set the title of the window
pygame.display.set_caption('smARtable')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

clock = pygame.time.Clock()
################################



cap = cv2.VideoCapture(1)

# set the resolution
ret = cap.set(3,960); # width
ret = cap.set(4,540); # height

HOMOGRAPHY_POINT_COUNTER = 0
points = []


# will hold the mapping
M = None

LAST_POSITION = (0,0)

def get_transformed_point(x, y, M):
    new_x = (M[0][0]*x + M[0][1]*y + M[0][2])/(M[2][0]*x + M[2][1]*y + M[2][2])
    new_y = (M[1][0]*x + M[1][1]*y + M[1][2])/(M[2][0]*x + M[2][1]*y + M[2][2])
    return (math.floor(new_x), math.floor(new_y))

def mouse_listener(event, x, y, flags, param):
    global HOMOGRAPHY_POINT_COUNTER
    global M
    global LAST_POSITION

    if event == cv2.EVENT_LBUTTONDOWN:
        print("Original: ({}, {})".format(x,y))
        if M is not None:
            p = get_transformed_point(x,y,M)
            LAST_POSITION = p

            # player.setPosition(p[0],p[1])

            print("Transformed: ({}, {})".format(p[0],p[1]))

        points.append([x, y])

        cv2.circle(frame,(x,y),10,(0,255,0),-1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str(HOMOGRAPHY_POINT_COUNTER),(x,y), font, 2, (255,255,255),2,cv2.LINE_AA)

        HOMOGRAPHY_POINT_COUNTER += 1

# create the windows
cv2.namedWindow("image")

# cv2.namedWindow("final")

cv2.setMouseCallback("image", mouse_listener)

ret, frame = cap.read()
cv2.imshow('image', frame)

w_size = int(SCREEN_WIDTH/4)
h_size = int(SCREEN_HEIGHT/4)


# HOMOGRAPHY CALIBRATION
while M is None:

    k = cv2.waitKey(1) & 0xFF

    # f means take new picture
    if k == ord('f'):
        ret, frame = cap.read()
        HOMOGRAPHY_POINT_COUNTER = 0
        points = []

    # q means quit
    elif k == ord('q'):
        break

    # ret, frame = cap.read()
    cv2.imshow('image', frame)

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


    # calibration picture from pygame
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 25)

    # pygame managament
    for event in pygame.event.get():
        if event.type == QUIT:
            break

    pygame.display.flip()
    clock.tick(20)

while True:
    k = cv2.waitKey(1) & 0xFF

    ret, frame = cap.read()
    cv2.imshow('image', frame)

    # calibration picture from pygame
    screen.fill(BLACK)
    pygame.draw.circle(screen, BLUE, LAST_POSITION, 25)

    # print(LAST_POSITION)

    # pygame managament
    for event in pygame.event.get():
        if event.type == QUIT:
            break

    pygame.display.flip()
    clock.tick(20)

    if k == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

pygame.quit()
sys.exit()
