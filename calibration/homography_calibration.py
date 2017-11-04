import numpy as np
import cv2
import time
import pygame
from game import Player
################################

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('Test')

# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()


# Create the player paddle object
player = Player(0, 0)
player.setPosition(900,540)

all_sprite_list.add(player)

clock = pygame.time.Clock()
################################





cap = cv2.VideoCapture(1)

# set the resolution
ret = cap.set(3,960); # width
ret = cap.set(4,540); # height

# resolution of tv
# 1920 x 1080

counter = 0
points1 = []


# will hold the mapping
M = None

last_position = None



def get_transformed_point(x, y, M):
    new_x = (M[0][0]*x + M[0][1]*y + M[0][2])/(M[2][0]*x + M[2][1]*y + M[2][2])
    new_y = (M[1][0]*x + M[1][1]*y + M[1][2])/(M[2][0]*x + M[2][1]*y + M[2][2])
    return (new_x, new_y)

def mouse_listener(event, x, y, flags, param):
    global counter
    global M

    if event == cv2.EVENT_LBUTTONDOWN:
        print("Original: ({}, {})".format(x,y))
        if M is not None:
            p = get_transformed_point(x,y,M)
            last_position = p
            player.setPosition(p[0],p[1])
            print("Transformed: ({}, {})".format(p[0],p[1]))
        else:
            print("Transformed: None")

        points1.append([x, y])

        cv2.circle(frame,(x,y),10,(0,255,0),-1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str(counter),(x,y), font, 2, (255,255,255),2,cv2.LINE_AA)

        counter += 1

# create the windows
cv2.namedWindow("image")
cv2.namedWindow("final")

cv2.setMouseCallback("image", mouse_listener)

ret, frame = cap.read()
cv2.imshow('image', frame)

width = 1920
height = 1080
w_size = int(width/4)
h_size = int(height/4)


# calibration proceedure
k = None
while True:

    k = cv2.waitKey(1) & 0xFF

    if k == ord('f'):
        ret, frame = cap.read()
        counter = 0
        points1 = []

    cv2.imshow('image', frame)

    if counter == 4:
        # do the transformation
        print(points1)
        pts1 = np.float32(points1)
        pts2 = np.float32([
            [(width/2.0)-w_size,(height/2.0)-h_size],
            [(width/2.0)+w_size,(height/2.0)-h_size],
            [(width/2.0)-w_size,(height/2.0)+h_size],
            [(width/2.0)+w_size,(height/2.0)+h_size]])

        # pts2 = np.float32([
        #     [,],
        #     [],
        #     [],
        #     [])

        M = cv2.getPerspectiveTransform(pts1,pts2)

        break


    if k == ord('q'):
        break

    all_sprite_list.update()

    screen.fill(BLACK)

    pygame.draw.rect(screen, (255,255,255), [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 25)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

while True:
    k = cv2.waitKey(1) & 0xFF

    ret, frame = cap.read()
    cv2.imshow('image', frame)
    final = cv2.warpPerspective(frame,M,(width,height))
    cv2.imshow('final', final)

    time.sleep(0.01)

    # print(M)

    if k == ord('q'):
        break
    all_sprite_list.update()

    screen.fill(BLACK)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

pygame.quit()
