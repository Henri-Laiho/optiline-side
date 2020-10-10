from OpenCV.SendCommands import move_shark_left, move_shark_right


class MorseDecoder:
    MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                       'C': '-.-.', 'D': '-..', 'E': '.',
                       'F': '..-.', 'G': '--.', 'H': '....',
                       'I': '..', 'J': '.---', 'K': '-.-',
                       'L': '.-..', 'M': '--', 'N': '-.',
                       'O': '---', 'P': '.--.', 'Q': '--.-',
                       'R': '.-.', 'S': '...', 'T': '-',
                       'U': '..-', 'V': '...-', 'W': '.--',
                       'X': '-..-', 'Y': '-.--', 'Z': '--..',
                       '1': '.----', '2': '..---', '3': '...--',
                       '4': '....-', '5': '.....', '6': '-....',
                       '7': '--...', '8': '---..', '9': '----.',
                       '0': '-----', ', ': '--..--', '.': '.-.-.-',
                       '?': '..--..', '/': '-..-.', '-': '-....-',
                       '(': '-.--.', ')': '-.--.-'}

    decrypt = {v: k for k, v in MORSE_CODE_DICT.items()}

    lastFrameWasOn = False
    lastFrameWasOff = False
    onTime = 0
    offTime = 0

    currentWord = ""
    message = []

    def __init__(self, long, short, blank):
        self.long = long
        self.short = short
        self.blank = blank

    def Send(self, value):
        if value:
            self.lastFrameWasOn = True
            self.onTime += 1

            if self.lastFrameWasOff:
                if self.offTime >= self.blank:
                    print()
                self.lastFrameWasOff = False
            self.offTime = 0

        else:
            self.lastFrameWasOff = True
            self.offTime += 1

            if self.lastFrameWasOn:
                if self.onTime >= self.long:
                    print("-", end="")
                    self.currentWord += "-"
                elif self.onTime >= self.short:
                    print(".", end="")
                    self.currentWord += "."
                self.lastFrameWasOn = False
                self.onTime = 0

            if self.offTime >= self.blank:
                if self.currentWord != "":
                    self.message.append(self.currentWord)
                    self.Move_Check()
                    self.currentWord = ""

    def Get_Message(self):
        text_message = ""

        for i in MorseDecoder.message:
            text_message += self.decrypt[i]

        return text_message

    def Move_Check(self):
        if self.currentWord == "": return

        decoded_message = self.decrypt[self.currentWord]

        if decoded_message == "L":
            print("Move L")
            move_shark_left()
            self.currentWord = ""
        elif decoded_message == "R":
            print("Move R")
            move_shark_right()
            self.currentWord = ""
