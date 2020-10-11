import argparse

from Src.CameraModuls import *
from Src.MorseCode import *


def flash_circles(current_frame):
    global skipped_outliers, avg_circle, debug, box_size, buffer_size, tx_pos_buffer, skips_to_forget_buffer, outlier_distance, decoder, circle_detector_p1, circle_detector_p2_threshold, circle_max_radius, memory_weight_decrease

    # At first, we turn it into a blur
    blurred_gray_image = blur_image(Frame=current_frame)

    # Then we put on the threshold
    _, threshed_gray_image = threshold_image(Frame=blurred_gray_image, ThresholdRatio=circle_brightness_threshold)

    # Then we put the blur back on
    blur = median_blur_image(Frame=threshed_gray_image)

    # Finds all circles
    circles = get_all_circles(blur, circle_detector_p1=circle_detector_p1,
                              circle_detector_p2_threshold=circle_detector_p2_threshold,
                              circle_max_radius=circle_max_radius)

    # to Find Circles in Memory Buffer |
    avg_circle = circle_memory_buffer(tx_pos_buffer=tx_pos_buffer, avg_circle=avg_circle, Frame=current_frame,
                                      memory_weight_decrease=memory_weight_decrease, Draw=True)

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
            current_frame = cv2.rectangle(current_frame, (x - w, y - h), (x + w, y + h), green, 2)

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


def green_area(current_frame):
    global decoder, color_area_threshold

    area = 0

    # Convert BGR to HSV
    hsv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_green = np.array([65, 60, 60])
    upper_green = np.array([80, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(current_frame, current_frame, mask=mask)

    ret, thrshed = cv2.threshold(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY), 3, 255, cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(thrshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

    if area > color_area_threshold:
        cv2.putText(current_frame, 'Green Object Detected', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
        cv2.rectangle(current_frame, (5, 40), (400, 100), (0, 255, 255), 2)

        decoder.Send(True)
    else:
        decoder.Send(False)

    # Show image
    cv2.imshow("", current_frame)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This program receives text in Morse encoding via optic transmission.')
    parser.add_argument('-d', '--device', type=int, help='Code of the video device to use as input.', default=0)
    parser.add_argument('-g', '--green', action='store_true', help='Use green color pulse detection method.', default=False)
    parser.add_argument('-gt', '--green_threshold', type=int, help='How much green area is needed to register a pulse', default=1000)
    parser.add_argument('-c1', '--circle_p1', type=int, help='Flash circle detector parameter 1', default=60)
    parser.add_argument('-c2', '--circle_p2_threshold', type=int,
                        help='Flash circle detector parameter 2 (lower value = more detections)', default=12)
    parser.add_argument('-w', '--memory_weight_decrease', help='How fast are older flash circle detections forgotten',
                        default=3, type=int)
    parser.add_argument('-m', '--memory_buffer_size', help='How many old flash circle detections are kept in the memory',
                        default=10, type=int)
    parser.add_argument('-l', '--mlong', type=int, help='Morse long pulse length in frames', default=10)
    parser.add_argument('-s', '--mshort', type=int, help='Morse short pulse length in frames', default=5)
    parser.add_argument('-b', '--mblank', type=int, help='Morse gap between pulses, length in frames', default=10)
    parser.add_argument('--circle_brightness', type=int,
                        help='How bright has to be a light to be detected as a flash cirle (from 0 to 255)', default=230)

    args = parser.parse_args()

    capture = cv2.VideoCapture(0)
    height, width, channels = capture.read()[1].shape

    # Arguments
    debug = True
    use_green_color_detection = args.green
    use_box_area_average = False
    box_size = 60
    w = h = box_size

    # Green color detector arguments
    color_area_threshold = args.green_threshold

    # Averaging the circle - Variables
    tx_pos_buffer = []
    outlier_distance = 100
    skipped_outliers = 0
    skips_to_forget_buffer = 5
    avg_circle = (0, 0, 0)

    # Averaging - arguments
    buffer_size = args.memory_buffer_size
    circle_detector_p1 = args.circle_p1
    circle_detector_p2_threshold = args.circle_p2_threshold
    circle_max_radius = 600
    memory_weight_decrease = args.memory_weight_decrease
    circle_brightness_threshold = args.circle_brightness

    decoder = MorseDecoder(args.mlong, args.mshort, args.mblank)

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

        if use_green_color_detection:
            green_area(current_frame)
        else:
            flash_circles(current_frame)

        # Exits when pressed ESC
        if cv2.waitKey(1) == 27:
            print(f"\n{decoder.Get_Message()}")
            break

    capture.release()
    cv2.destroyAllWindows()
