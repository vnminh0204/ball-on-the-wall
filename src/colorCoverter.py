from imutils.video import VideoStream
import imutils
import cv2
import numpy as np


def nothing(x):
    pass


def convertColor():
    cv2.namedWindow("HSV TrackBar")
    cv2.resizeWindow("HSV TrackBar", 500, 300)
    cv2.createTrackbar("LH", "HSV TrackBar", 0, 255, nothing)
    cv2.createTrackbar("LS", "HSV TrackBar", 0, 255, nothing)
    cv2.createTrackbar("LV", "HSV TrackBar", 0, 255, nothing)
    cv2.createTrackbar("UH", "HSV TrackBar", 255, 255, nothing)
    cv2.createTrackbar("US", "HSV TrackBar", 255, 255, nothing)
    cv2.createTrackbar("UV", "HSV TrackBar", 255, 255, nothing)
    while True:
        # Augment frames
        # frame = imutils.resize(fr, width=1280, height=720)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # GET THE DIFFERENT VALUE OF HSV
        l_h = cv2.getTrackbarPos("LH", "HSV TrackBar")
        l_s = cv2.getTrackbarPos("LS", "HSV TrackBar")
        l_v = cv2.getTrackbarPos("LV", "HSV TrackBar")

        u_h = cv2.getTrackbarPos("UH", "HSV TrackBar")
        u_s = cv2.getTrackbarPos("US", "HSV TrackBar")
        u_v = cv2.getTrackbarPos("UV", "HSV TrackBar")

        # TENNIS BALL BOUND
        tennis_lbound = np.array([l_h, l_s, l_v])
        tennis_ubound = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, tennis_lbound, tennis_ubound)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("hsv", hsv)
        cv2.imshow("mask", mask)
        cv2.imshow("res", res)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
