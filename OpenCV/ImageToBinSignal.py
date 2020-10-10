import cv2
import numpy as np

cap = cv2.VideoCapture(0)
height, width, channels = cap.read()[1].shape
box_size = 100

x = int(width / 2 - box_size / 2)
y = int(height / 2 - box_size / 2)
w = h = box_size

while (True):
    gray = cv2.medianBlur(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY), 5)
    gray = cv2.medianBlur(gray, 5)
    ret, gray = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    image = cv2.rectangle(gray, (x, y), (x + w, y + h), 255, 2)

    mask = np.zeros(image.shape[:2], np.uint8)
    mask[y:y + h, x:x + w] = 255

    mean = cv2.mean(image, mask=mask)[:3]

    if mean[0] >= 255/2:
        print(1)
    else:
        print(0)

    # Displaying the image
    cv2.imshow("img", image)

    if cv2.waitKey(1) == 27:  # esc Key
        break

cap.release()
cv2.destroyAllWindows()
