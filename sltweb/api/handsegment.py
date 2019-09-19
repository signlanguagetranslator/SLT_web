import numpy as np
import cv2


boundaries = [
    ([160, 83, 80], [180, 255, 255])
]

def handsegment(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower, upper = boundaries[0]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(frame, lower, upper)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output = cv2.bitwise_and(mask, frame)
    # show the images
    return output