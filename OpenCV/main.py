import cv2
import numpy as np

if __name__ == '__main__':
    # Arguments
    capture = cv2.VideoCapture(0)
    height, width, channels = capture.read()[1].shape
    debug = True
    default_window_name = "DEFAULT_NAME"
    square_size_big = 30
    square_size_small = 20
    color = (255, 0, 0)
    thickness = 2

    # If didn't detect camera
    if not capture.isOpened:
        print('[-] Unable to open camera')
        exit(1)

    while True:
        _, current_frame = capture.read()

        # If it doesn't get any pictures
        if current_frame is None:
            break
        # At first, we turn it into a blur
        blurred_gray_image = cv2.medianBlur(cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY), 5)

        # Then we put on the threshold
        ret, threshed_gray_image = cv2.threshold(blurred_gray_image, 230, 255, cv2.THRESH_BINARY)

        # Then we put the blur back on
        blur = cv2.medianBlur(threshed_gray_image, 33)

        # Finds all circles
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=50, param2=15, minRadius=2, maxRadius=300)

        # If it finds circles
        if circles is not None:
            new_image = cv2.medianBlur(cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY), 5)
            new_circles = np.uint16(np.around(circles))
            # Here it creates squares
            for item in new_circles[0, :]:
                # Rectangular Arguments
                starting_point = (item[0] - square_size_big, item[1] - square_size_big)
                ending_point = (item[0] + square_size_big, item[1] + square_size_big)

                # Shows new image
                rectangle_position = cv2.rectangle(new_image, starting_point, ending_point, color, thickness)
                cv2.imshow(default_window_name, rectangle_position)
            for item in new_circles[0, :]:
                hello = cv2.imshow(default_window_name, cv2.circle(new_image, (item[0], item[1]), item[2], color))

        # ==========For Debuging==========
        # Only works while debug = True
        if debug:
            cv2.imshow('Blurred Gray Image', blurred_gray_image)
            cv2.imshow('Threshed Gray Image', threshed_gray_image)
            cv2.imshow('Threshed Gray Image', threshed_gray_image)

        # ==========Other Things==========
        # Exits when pressed ESC
        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
