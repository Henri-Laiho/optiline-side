import cv2


class Camera:
    def __init__(self, CameraNumber):
        # Create a VideoCapture object and read from input file
        # If the input is the camera, pass 0 instead of the video file name
        self.capture = cv2.VideoCapture(CameraNumber)
        if not self.capture.isOpened():
            print("[-] Error opening video stream or file")

        # ===========Camera Parameters===========
        self.camera_height = self.capture.read()[1].shape[0]
        self.camera_width = self.capture.read()[1].shape[1]
        self.camera_channels = self.capture.read()[1].shape[2]
        self.camera_FPS = self.capture.get(cv2.CAP_PROP_FPS)

        # ===========Camera Arguments===========
        self.WindowName = "Default_Window_Name"

    def close_camera(self):
        # When everything done, release the video capture object
        self.capture.release()
        print("[+] Camera released")

    def __str__(self):
        return f"Camera:\n" \
               f"\tCamera: {self.capture}\n" \
               f"\theight: {self.camera_height}\n" \
               f"\twidth: {self.camera_width}\n" \
               f"\tcamera_FPS: {self.camera_FPS}\n" \
               f"\tchannels: {self.camera_channels}\n"
