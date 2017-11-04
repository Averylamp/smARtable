import numpy as np
import cv2

# cameras = [1]

cap = cv2.VideoCapture(1)

# set the resolution
ret = cap.set(3,960); # width
ret = cap.set(4,540); # height

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray,100,200)

    # Display the resulting frame
    cv2.imshow('frame',edges)
    cv2.imshow('original', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
