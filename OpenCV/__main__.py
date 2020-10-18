import cv2

from OpenCV.Camera.Camera import Camera
from OpenCV.Detection.Detection import Detection

if __name__ == '__main__':
    # Previous Launch settings: -c2 18 --circle_brightness 240 -l 9 -s 3 -b 20
    camera = Camera(CameraNumber=0)
    
    detection = Detection()
    detection.use_green = True
    detection.use_red = True
    detection.use_blue = True

    while camera.capture.isOpened():  # Read until video is completed
        ret, frame = camera.capture.read()  # Capture frame-by-frame
        if frame is None:
            break

        colours = detection.use(frame)

        if colours["red_area"]:
            print("[+] Saw Green!")

        if colours["green_area"]:
            print("[+] Saw blue!")

        if colours["blue_area"]:
            print("[+] Saw Blue!")

        if cv2.waitKey(1) == 27:  # Exits when pressed ESC
            break

    camera.close_camera()
