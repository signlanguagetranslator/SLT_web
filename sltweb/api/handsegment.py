import numpy as np
import cv2
import os
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
    cv2.waitKey(0)
    # show the images
    cv2.imshow("images", output)
    return output

if __name__ == '__main__':
    filenames = os.listdir('C:/Users/them0/Desktop/졸과/개발/masking_hand_detection/photos/pink_glob/other')
    for name in filenames:

        filename = "photos/pink_glob/other/" + name
        frame = cv2.imread(filename)
        mask = handsegment(frame)
        cv2.imwrite('train_photos/other/' + name , mask)
