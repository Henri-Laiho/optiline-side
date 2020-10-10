import cv2
import numpy as np


# Check if a detected circle is probably a false positive
def is_outlier(tx_pos, new_circle, threshold):
    distance = np.linalg.norm(np.subtract(tx_pos[:2], new_circle[:2]))
    # print(distance)
    return distance > threshold


if __name__ == '__main__':
    # Arguments
    capture = cv2.VideoCapture(0)
    height, width, channels = capture.read()[1].shape
    debug = True
    default_window_name = "DEFAULT_NAME"
    square_size_big = 30
    square_size_small = 20
    blue = (255, 0, 0)
    red = (0, 0, 255)
    green = (0, 255, 0)
    thickness = 2

    # Averaging the circle - Variables
    buffer_size = 10
    tx_pos_buffer = []
    outlier_distance = 100
    skipped_outliers = 0
    skips_to_forget_buffer = 5
    avg_circle = (0, 0, 0)

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
        blur = cv2.medianBlur(threshed_gray_image, 37)

        # Finds all circles
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=70, param2=13, minRadius=2, maxRadius=300)

        # Find average of the circle memory buffer
        length = len(tx_pos_buffer)
        if length > 0:
            geom = [1 / 4 ** x for x in range(length)]
            avg_circle = np.sum([np.multiply(tx_pos_buffer[x], geom[length - x - 1]) for x in range(length)],
                                axis=0) / sum(geom)
            x, y, r = avg_circle

            # draw it on the original image
            cv2.circle(current_frame, (int(x), int(y)), int(r), red, 3)

        # Draw the receiving rectangle
        if sum(avg_circle) > 0:
            x, y, r = avg_circle
            # Rectangular Arguments
            starting_point = (int(x - square_size_big), int(y - square_size_big))
            ending_point = (int(x + square_size_big), int(y + square_size_big))

            # Shows new image
            current_frame = cv2.rectangle(current_frame, starting_point, ending_point, green, thickness)

        # If it finds circles
        if circles is not None:

            new_circles = np.uint16(np.around(circles))

            for circle in new_circles[0, :]:
                x, y, r = circle
                current_frame = cv2.circle(current_frame, (x, y), r, blue, 2)

                # Record it for averaging
                if length > 0 and is_outlier(avg_circle, circle, outlier_distance):
                    skipped_outliers += 1
                    if skipped_outliers > skips_to_forget_buffer:
                        tx_pos_buffer.pop(0)
                        skipped_outliers = 0
                    continue
                skipped_outliers = max(skipped_outliers - 1, 0)

                tx_pos_buffer.append((x, y, r))
                if len(tx_pos_buffer) > buffer_size:
                    tx_pos_buffer.pop(0)

        # ==========For Debuging==========
        # Only works while debug = True
        if debug:
            cv2.imshow('Original', current_frame)
            cv2.imshow('Circle Detector', threshed_gray_image)

        # ==========Other Things==========
        # Exits when pressed ESC
        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
