import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# set the resolution
ret = cap.set(3,960); # width
ret = cap.set(4,540); # height

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    print("HEIGHT: {}, WIDTH: {}".format(len(frame), len(frame[0])))
    cv2.imshow('original', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
