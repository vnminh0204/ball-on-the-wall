from imutils.video import VideoStream
import imutils
import cv2
import numpy as np

class DetectBallPosition():
    def __init__(self):
        self.x = 0
        self.y = 0



    def getBallPos(self, fr):
        x, y = 0, 0
        # Read camera frames
        # cap, frame = vs.read()
        # if frame is None:
        #     return None

        # Augment frames
        frame = imutils.resize(fr, width=1280, height=720)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Tennisball Parameters
        greenLower = (29, 86, 6)
        greenUpper = (64, 255, 255)

        # Look for ball
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Make contours
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        if len(cnts) > 0:
            # for c in cnts:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                return (x, y, radius)

        return None


# def calibrate():
#     corners = [0, 0, 0, 0]
#     cornerName = ("Bottom Left", "Top Left", "Top Right", "Bottom Right")
#     vs = VideoStream(src=0).start()
#     for i in range(4):
#         print("Hold ball at %s" % cornerName[i])
#         input("Press enter when ready")
#         corners[i] = getBallPos(vs)
#     print(corners)
