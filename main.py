from Src.CameraModuls import *
from Src.MorseCode import *

if __name__ == '__main__':
    # Arguments
    capture = cv2.VideoCapture(0)
    height, width, channels = capture.read()[1].shape
    debug = True

    use_box_area_average = False
    box_size = 60
    w = h = box_size
    decoder = MorseDecoder(8, 4, 8)

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

        # Finds all circles
        circles = get_all_circles(blur)

        # to Find Circles in Memory Buffer |
        avg_circle = circle_memory_buffer(tx_pos_buffer=tx_pos_buffer, avg_circle=avg_circle, Frame=current_frame, Draw=True)

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
        if sum(avg_circle) > 0:
            # Decode signal
            x, y, r = avg_circle
            x, y, r = int(x), int(y), int(r)
            if debug:
                current_frame = cv2.rectangle(current_frame, (x-w, y-h), (x + w, y + h), green, 2)

            if use_box_area_average:
                mask = np.zeros(current_frame.shape[:2], np.uint8)
                mask[y - h:y + h, x - w:x + w] = 255
                mean = cv2.mean(blur, mask=mask)[:3]
                decoder.Send(mean[0] >= 255 / 2)
            else:
                decoder.Send(blur[y, x] >= 255 / 2)

        # ==========Other Things==========
        # Only works while debug = True
        if debug:
            cv2.imshow('Original', current_frame)
            cv2.imshow('Circle Detector', blur)

        # Exits when pressed ESC
        if cv2.waitKey(1) == 27:
            print(f"\n{decoder.Get_Message()}")
            break

    capture.release()
    cv2.destroyAllWindows()
