import numpy as np
import cv2

cap = cv2.VideoCapture(1)

WIDTH = 720//2
HEIGHT = 1280//2

LABEL_NUM = 0
FOLDER = "original"

# set the desired resolution (must be the same aspect ratio based on experience(?))
ret = cap.set(3,WIDTH); # width
ret = cap.set(4,HEIGHT); # height

# create the windows
cv2.namedWindow("original")

index = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # print("HEIGHT: {}, WIDTH: {}".format(len(frame), len(frame[0])))
    cv2.imshow('original', frame)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('f'):
        # save the image to the correct folder
        cv2.imwrite("classes/{}/{}.jpg".format(FOLDER, index), frame)
        index += 1
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
