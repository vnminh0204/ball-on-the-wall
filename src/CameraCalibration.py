import cv2
import numpy as np

from DetectBallPosition import *


class CameraCalibration:
    def __init__(self):
        self.circles = np.zeros((4, 2), np.int)
        self.counter = 0
        # self.cap = cv2.VideoCapture(0)

    def mousePoints(self, event, x, y, flags, params):
        global counter
        if event == cv2.EVENT_LBUTTONDOWN:
            self.circles[self.counter] = x, y
            self.counter += 1
            print(self.circles)


# When everything done, release the capture


    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()
