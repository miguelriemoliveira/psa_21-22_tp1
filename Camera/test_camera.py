#!/usr/bin/env python3

# import the opencv library
import cv2

# -------------------------
# Initialization
# -------------------------

# define a video capture object
vid = cv2.VideoCapture(4)

# -------------------------
# Execution in cycle
# -------------------------

while (True):

    ret, image = vid.read()  # Capture the video frame

    cv2.imshow('frame', image)  # Display the resulting frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# -------------------------
# Termination
# -------------------------

vid.release()  # After the loop release the cap object
cv2.destroyAllWindows()  # Destroy all the windows
