#!/usr/bin/env python3
import cv2

from ClassCamera import ClassCamera, ClassAbstractHardware

# -------------------------
# Initialization
# -------------------------

camera = ClassCamera()
camera.connect(4)

# -------------------------
# Execution in cycle
# -------------------------
while True:

    success = camera.getData()
    if success:
        cv2.imshow('frame', camera.image)  # Display the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# -------------------------
# Termination
# -------------------------
camera.disconnect()
cv2.destroyAllWindows()  # Destroy all the windows
