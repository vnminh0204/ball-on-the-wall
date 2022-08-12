"""
Program to detect when a ball changes its velocity in the x direction
"""
from imutils.video import VideoStream
import imutils
import cv2

bounces = 0


class Ball():
    maxnbd = 2

    def __init__(self):
        self.prevX = 600
        self.speeds = []
        self.nbd = 0

    def newX(self, x):
        global bounces
        if x == None:
            self.nbd += 1
            if self.nbd >= self.maxnbd:
                return -1
        else:
            self.speeds.append(x-self.prevX)
            self.prevX = x
            if len(self.speeds) > 1:
                if self.speeds[len(self.speeds)-2] < 0 and self.speeds[len(self.speeds)-1] > 0:
                    print(bounces)
                    print(self.speeds)
                    bounces += 1
                    return 1

        return 0

    def lived(self):
        return len(self.speeds) > 0 and self.nbd > 0


def trackBall():
    # Select camera
    vs = VideoStream(src=0).start()
    x, y = 0, 0
    currentBall = Ball()

    while True:
        # Read camera frames
        frame = vs.read()
        if frame is None:
            break

        # Augment frames
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

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
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                if currentBall.newX(x) == 1:
                    print("bounce")
            else:
                if currentBall.newX(None) == -1 and currentBall.lived():
                    print("ball lost")
                    currentBall = Ball()
        else:
            if currentBall.newX(None) == -1 and currentBall.lived():
                print("ball lost")
                currentBall = Ball()

        # Display camera frames
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break
