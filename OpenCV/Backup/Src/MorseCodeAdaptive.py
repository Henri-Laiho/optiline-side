from OpenCV.Backup.Src.MorseCode import MorseDecoder
import numpy as np


class MorseDecoderAdaptive:
    MORSE_CODE_DICT = MorseDecoder.MORSE_CODE_DICT
    decrypt = MorseDecoder.decrypt

    lastFrameWasOn = False
    lastFrameWasOff = False
    onTime = 0
    offTime = 0
    pulses = []
    blanks = []
    frames = []

    def __init__(self, min_pulse_length = 2, min_blank_length = 0, max_blank_length = 40):
        self.min_pulse_length = min_pulse_length
        self.min_blank_length = min_blank_length
        self.max_blank_length = max_blank_length

    def Send(self, value):
        if value:
            self.lastFrameWasOn = True
            self.onTime += 1

            if self.lastFrameWasOff:
                if self.min_blank_length <= self.offTime:
                    self.frames.append(False)
                    self.blanks.append(self.offTime)
                self.lastFrameWasOff = False
            self.offTime = 0

        else:
            self.lastFrameWasOff = True
            self.offTime += 1

            if self.lastFrameWasOn:
                if self.min_pulse_length <= self.onTime:
                    self.frames.append(True)
                    self.pulses.append(self.onTime)
                self.lastFrameWasOn = False
                self.onTime = 0

    def Get_Message(self, debug=False):

        message = []
        local_str = ""
        if len(self.pulses) == 0:
            return ""
        mean_pulse = np.mean(self.pulses)
        np_blanks = np.array(self.blanks)
        normal_blanks = np_blanks[np.where(np_blanks < self.max_blank_length)]
        if len(normal_blanks) == 0:
            return "error: too long blanks, max blank is %s frames" % self.max_blank_length
        mean_blank = (np.mean(normal_blanks) + np.percentile(normal_blanks, 75)) / 2

        i_pulse = 0
        i_blank = 0
        for x in self.frames:
            if x:
                pulse = self.pulses[i_pulse]
                long = pulse > mean_pulse

                if long:
                    local_str += "-"
                else:
                    local_str += "."

                i_pulse += 1
            else:
                blank = self.blanks[i_blank]
                long = mean_blank < blank
                brk = self.max_blank_length < blank

                if long:
                    if len(local_str) > 0:
                        message.append(local_str)
                        local_str = ""

                i_blank += 1

        if debug:
            print(" ".join(message), end="; ")

        text_message = ""
        for i in message:
            if i in self.decrypt:
                text_message += self.decrypt[i]

        return text_message
