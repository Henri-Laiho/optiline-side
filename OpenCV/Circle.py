# Code moved to main.py
'''

import cv2
import numpy as np
import sys


def is_outlier(tx_pos, new_circle, threshold):
    distance = np.linalg.norm(np.subtract(tx_pos[:2], new_circle[:2]))
    # print(distance)
    return distance > threshold


cap = cv2.VideoCapture(0)

if not cap.isOpened:
    print('Unable to open camera')

buffer_size = 5
tx_pos_buffer = []

skipped_outliers = 0
skips_to_forget_buffer = 5
avg_circle = (0, 0, 0)

while (True):
    _, frame = cap.read()

    if frame is None:
        break

    gray = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 5)
    _, binary = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    blur = cv2.medianBlur(binary, 25)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=70, param2=13, minRadius=2, maxRadius=300)

    # ret=[[Xpos,Ypos,Radius],...]

    length = len(tx_pos_buffer)
    if length > 0:
        geom = [1 / 4 ** x for x in range(length)]
        # print(geom)
        avg_circle = np.sum([np.multiply(tx_pos_buffer[x], geom[length - x - 1]) for x in range(length)], axis=0) / sum(geom)
        x, y, r = avg_circle
        cv2.circle(frame, (int(x), int(y)), int(r), (0, 0, 255), 3)

    if circles is not None:
        for c1 in circles:
            for circle in c1:
                x, y, r = circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

                if length > 0 and is_outlier(avg_circle, circle, 100):
                    skipped_outliers += 1
                    if skipped_outliers > skips_to_forget_buffer:
                        tx_pos_buffer.pop(0)
                        skipped_outliers = 0
                    continue

                skipped_outliers = max(skipped_outliers-1, 0)

                tx_pos_buffer.append((x, y, r))
                if len(tx_pos_buffer) > buffer_size:
                    tx_pos_buffer.pop(0)

    cv2.imshow('Original', frame)
    cv2.imshow('Circle Detector', blur)

    if cv2.waitKey(1) == 27:  # esc Key
        break
cap.release()
cv2.destroyAllWindows()
'''
