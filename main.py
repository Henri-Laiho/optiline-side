from Hackaton.Src.CameraModuls import *

if __name__ == '__main__':
    # Arguments
    capture = cv2.VideoCapture(2)
    height, width, channels = capture.read()[1].shape
    debug = True

    # If didn't detect camera
    if not capture.isOpened:
        print('[-] Unable to open camera')
        exit(1)

    while True:
        # Gets current frame from camera
        _, current_frame = capture.read()

        # If it doesn't get any pictures
        if current_frame is None:
            break

        # At first, we turn it into a blur
        blurred_gray_image = blur_image(Frame=current_frame)

        # Then we put on the threshold
        _, threshed_gray_image = threshold_image(Frame=blurred_gray_image)

        # Then we put the blur back on
        blur = median_blur_image(Frame=threshed_gray_image)

        cv2.imshow(default_window_name, blur)

        # Finds all circles
        circles = get_all_circles(blur)

        # to Find Circles in Memory Buffer |
        circle_memory_buffer(Frame=current_frame, Draw=True)

        if circles is not None:
            new_circles = np.uint16(np.around(circles))
            for circle in new_circles[0, :]:
                x, y, r = circle
                current_frame = cv2.circle(current_frame, (x, y), r, blue, 2)

                # Record it for averaging
                if len(tx_pos_buffer) > 0 and is_outlier(avg_circle, circle, outlier_distance):
                    skipped_outliers += 1
                    if skipped_outliers > skips_to_forget_buffer:
                        tx_pos_buffer.pop(0)
                        skipped_outliers = 0
                    continue
                skipped_outliers = max(skipped_outliers - 1, 0)

                tx_pos_buffer.append((x, y, r))
                if len(tx_pos_buffer) > buffer_size:
                    tx_pos_buffer.pop(0)

        # ==========Other Things==========
        # Only works while debug = True
        if debug:
            cv2.imshow('Original', current_frame)
            cv2.imshow('Circle Detector', threshed_gray_image)

        # Exits when pressed ESC
        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
