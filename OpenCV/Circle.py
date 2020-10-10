import cv2
import numpy as np
import sys

cap = cv2.VideoCapture(0)

# backSub = cv2.createBackgroundSubtractorKNN()
backSub = cv2.createBackgroundSubtractorMOG2()

if not cap.isOpened:
    print('Unable to open camera')
while (True):
    _, frame = cap.read()

    if frame is None:
        break

    gray = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 5)
    cv2.imshow('Blur&Gray', gray)

    ret, gray = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    cv2.imshow('gray', gray)

    blur = cv2.medianBlur(gray, 25)

    # fgMask = backSub.apply(gray)
    # cv2.imshow('Mask', fgMask)

    cirles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 20,
                              param1=50, param2=15, minRadius=2, maxRadius=300)
    # ret=[[Xpos,Ypos,Radius],...]
    if cirles is not None:
        print("Circle There!")
        print(cirles)
        for c1 in cirles:
            for x, y, r in c1:
                cv2.circle(blur, (x, y), r, (255, 255, 0), 4)

    cv2.imshow('video', blur)

    if cv2.waitKey(1) == 27:  # esc Key
        break
cap.release()
cv2.destroyAllWindows()
