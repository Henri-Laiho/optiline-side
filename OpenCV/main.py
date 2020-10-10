import cv2

if __name__ == '__main__':
    # Arguments
    capture = cv2.VideoCapture(0)
    debug = True

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

        # ==========For Debuging==========
        # Only works while debug = True
        if debug:
            cv2.imshow('Blurred Gray Image', blurred_gray_image)
            cv2.imshow('Threshed Gray Image', threshed_gray_image)
            cv2.imshow('Threshed Gray Image', threshed_gray_image)

        # ==========Other Things==========
        # Prints out all circles
        if circles is not None:
            circle_count = 0
            for circle in circles[0, :]:
                circle_count += 1
                x = circle[0]
                y = circle[1]
                w = h = int(x * y)
                print(f"Circle{circle_count} at:\n"
                      f"\tX: {x}"
                      f"\tY: {y}")
                cv2.imshow("img", current_frame)
        # Exits when pressed ESC
        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
