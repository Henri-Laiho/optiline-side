import cv2
import numpy as np


def find_colour(CurrentFrame, HSV, LowerColour, UpperColour, Threshold):
    """
    Find Color is a function that returns a dictionary list with predefined parameters
    :param CurrentFrame: current image from which it can compare the previous and current image
    :param HSV: RGB to HSV image
    :param LowerColour: lowest color parameters
    :param UpperColour: highest color parameters
    :param Threshold: don't know exactly what it does
    :return:
    """

    # Checks if array elements lie between the elements of two other arrays
    mask = cv2.inRange(src=HSV,
                       lowerb=LowerColour,
                       upperb=UpperColour)

    # computes bitwise conjunction of the two arrays (dst = src1 & src2)
    bitwise = cv2.bitwise_and(src1=CurrentFrame,
                              src2=CurrentFrame,
                              mask=mask)

    # Applies a fixed-level threshold to each array element
    _, threshold = cv2.threshold(src=cv2.cvtColor(bitwise, cv2.COLOR_BGR2GRAY),
                                 thresh=3,
                                 maxval=255,
                                 type=cv2.THRESH_BINARY)

    # Finds contours in a binary image
    contours, _ = cv2.findContours(image=threshold,
                                   mode=cv2.RETR_LIST,
                                   method=cv2.CHAIN_APPROX_SIMPLE)

    area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)

    if area > Threshold:
        return True
    else:
        return False


class Detection(object):
    def __init__(self):
        # ===========Detection Parameters===========
        self.debug = False
        # ===========Red Parameters===========
        self.use_red = False
        self.red_threshold = 1000
        self.red_lower = np.array([160, 20, 70])
        self.red_upper = np.array([190, 255, 255])
        # ===========Blue Parameters===========
        self.use_blue = False
        self.blue_threshold = 1000
        self.blue_lower = np.array([101, 50, 38])
        self.blue_upper = np.array([110, 255, 255])

        # ===========Green Parameters===========
        self.use_green = False
        self.green_threshold = 1000
        self.green_lower = np.array([65, 60, 60])
        self.green_upper = np.array([80, 255, 255])

    def use(self, Frame=None):
        if Frame is None:
            print("[-] Frame not found at Detection.use()")
            return None

        # ===========Parameters===========
        hsv = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('hsv', hsv)

        area = {'red_area': False,
                'green_area': False,
                'blue_area': False}

        if self.use_red:
            area['red_area'] = find_colour(CurrentFrame=Frame,
                                           HSV=hsv,
                                           UpperColour=self.red_upper,
                                           LowerColour=self.red_lower,
                                           Threshold=self.red_threshold)

        if self.use_green:
            area['green_area'] = find_colour(CurrentFrame=Frame,
                                             HSV=hsv,
                                             UpperColour=self.green_upper,
                                             LowerColour=self.green_lower,
                                             Threshold=self.green_threshold)

        if self.use_blue:
            area['blue_area'] = find_colour(CurrentFrame=Frame,
                                            HSV=hsv,
                                            UpperColour=self.blue_upper,
                                            LowerColour=self.blue_lower,
                                            Threshold=self.green_threshold)
        self.debug_message(area)
        return area

    def debug_message(self, Message):
        if self.debug:
            print(Message)

    def __str__(self):
        return f'Detection:\n' \
               f'\tlower_green: {self.green_lower}\n' \
               f'\tupper_green: {self.green_upper}'
