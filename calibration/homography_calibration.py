import numpy as np
import cv2
import time

cap = cv2.VideoCapture(1)

# set the resolution
ret = cap.set(3,960); # width
ret = cap.set(4,540); # height

# resolution of tv
# 1920 x 1080

def click_and_crop(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDBLCLK:
        refPt = [(x, y)]
        print(refPt)
        # cv2.circle(frame,(x,y),100,(255,0,0),-1)

    # if event == cv2.EVENT_LBUTTONDOWN:
    #     refPt = [(x, y)]
    #     print(refPt)

    # if event == cv2.EVENT_LBUTTONUP:
    #     refPt = [(x, y)]
    #     print(refPt)

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

while(True):

    ret, frame = cap.read()

    # time.sleep(0.01)

    # Capture frame-by-frame
    # ret, frame = cap.read()

    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower_range = np.array([110,50,50])
    # upper_range = np.array([130,255,255])

    # mask = cv2.inRange(hsv, lower_range, upper_range)

    # Display the resulting frame
    # cv2.imshow('original', frame)

    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
