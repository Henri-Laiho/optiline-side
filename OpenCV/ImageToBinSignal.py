import cv2
import numpy as np
import wave, struct

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

decrypt = {v: k for k, v in MORSE_CODE_DICT.items()}

cap = cv2.VideoCapture(0)
height, width, channels = cap.read()[1].shape
box_size = 100

x = int(width / 2 - box_size / 2)
y = int(height / 2 - box_size / 2)
w = h = box_size

sampleRate = 44100.0  # hertz
duration = 1.0  # seconds
frequency = 440.0  # hertz
obj = wave.open('sound.wav', 'w')
obj.setnchannels(1)  # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)

lastFrameWasOn = False
lastFrameWasOff = False
onTime = 0
offTime = 0


long = 10
short = 5
blank = 10

currentWord = ""
message = []

while (True):
    gray = cv2.medianBlur(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY), 5)
    gray = cv2.medianBlur(gray, 5)
    ret, gray = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    image = cv2.rectangle(gray, (x, y), (x + w, y + h), 255, 2)

    mask = np.zeros(image.shape[:2], np.uint8)
    mask[y:y + h, x:x + w] = 255

    mean = cv2.mean(image, mask=mask)[:3]

    if mean[0] >= 255 / 2:
        #print(1)
        lastFrameWasOn = True
        onTime += 1

        if lastFrameWasOff:
            if offTime >= blank:
                print()
            lastFrameWasOff = False
        offTime = 0

    else:
        #print(0)
        lastFrameWasOff = True
        offTime += 1

        if lastFrameWasOn:
            if onTime >= long:
                print("-", end="")
                currentWord += "-"
            elif onTime >= short:
                print(".", end="")
                currentWord += "."
            lastFrameWasOn = False
            onTime = 0

        if offTime >= blank:
            if currentWord != "":
                message.append(currentWord)
                currentWord = ""

    # Displaying the image
    cv2.imshow("img", image)

    if cv2.waitKey(1) == 27:  # esc Key
        #print(f"\n{message}")
        text_message = ""

        for i in message:
            text_message += decrypt[i]
        print(f"\n{text_message}")
        break

cap.release()
cv2.destroyAllWindows()
