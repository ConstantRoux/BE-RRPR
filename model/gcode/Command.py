import numpy as np
import re


class Command:
    def __init__(self, line):
        self.line = line
        self.type = None
        self.B = np.array([[None], [None], [None]])
        self.C = np.array([[None], [None], [None]])

    def interpret(self):
        if self.line[0] != 'G':
            return -1

        if self.line[1] != '0' and self.line[1] != '1' and self.line[1] != '2' and self.line[1] != '3':
            return -2

        self.B[0] = self.get_float_param('X')
        self.B[1] = self.get_float_param('Y')
        self.B[2] = self.get_float_param('Z')
        self.C[0] = self.get_float_param('I')
        self.C[1] = self.get_float_param('J')
        self.C[2] = self.get_float_param('Z')

        if self.line[1] == '0' or self.line[1] == '1':
            self.type = "line"
        elif self.line[1] == '2':
            self.type="clockwise"
        elif self.line[1] == '3':
            self.type = "anticlockwise"

        if self.B[2, 0] is None:
            self.B[2] = 0
            self.C[2] = 0

    def get_float_param(self, letter):
        str_float = re.findall(letter + "(\d+\.\d+|\d+)", self.line)
        if len(str_float) == 0:
            return None
        else:
            return np.asarray(str_float[0], dtype=float)




