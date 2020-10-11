import cv2
import numpy as np

default_window_name = "DEFAULT_NAME"
square_size_big = 30
square_size_small = 20
blue = (255, 0, 0)
red = (0, 0, 255)
green = (0, 255, 0)
thickness = 2


def blur_image(Frame):
    """
    blurs the image to better understand what it is
    :rtype: object
    """
    return cv2.medianBlur(cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY), 5)


def threshold_image(Frame, ThresholdRatio=230):
    """
    Makes the image black and white
    :rtype: object
    """
    return cv2.threshold(Frame, ThresholdRatio, 255, cv2.THRESH_BINARY)


def median_blur_image(Frame, BlurRatio=37):
    """
    blurs the image to better understand what it is
    :rtype: object
    """
    return cv2.medianBlur(Frame, BlurRatio)


def get_all_circles(Frame, circle_detector_p1, circle_detector_p2_threshold, circle_max_radius, min_radius=2):
    return cv2.HoughCircles(Frame,
                            cv2.HOUGH_GRADIENT, 1, 20,
                            param1=circle_detector_p1, param2=circle_detector_p2_threshold, minRadius=min_radius,
                            maxRadius=circle_max_radius)


def circle_memory_buffer(tx_pos_buffer, avg_circle, Frame, memory_weight_decrease, Draw=False):
    """
    Find average of the circle memory buffer
    :rtype: object -> tx_pos_buffer
    """
    length = len(tx_pos_buffer)
    if length > 0:
        geom = [1 / memory_weight_decrease ** x for x in range(length)]
        avg_circle = np.sum([np.multiply(tx_pos_buffer[x], geom[length - x - 1]) for x in range(length)],
                            axis=0) / sum(geom)
        x, y, r = avg_circle

        if Draw:
            cv2.circle(Frame, (int(x), int(y)), int(r), red, 3)
    return avg_circle


def is_outlier(tx_pos, new_circle, threshold):
    """
    Check if a detected circle is probably a false positive
    :rtype: object
    """
    distance = np.linalg.norm(np.subtract(tx_pos[:2], new_circle[:2]))
    # print(distance)
    return distance > threshold
