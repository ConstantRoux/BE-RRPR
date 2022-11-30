import numpy as np

from model.gcode.Command import Command
from model.geometrics.ArcXY import ArcXY
from model.geometrics.Line import Line


class GcodeInterpreter:
    def __init__(self, law, H, L, V, path, theta=0):
        self.law = law
        self.H = H
        self.L = L
        self.V = V
        self.file = open(path, 'r')
        self.lines = None
        self.commands = None
        self.current_pos = np.array([[0], [0], [0]])
        self.theta = theta

    def get(self):
        self.read_lines()
        self.get_commands()
        t, M = self.get_M()
        q = self.get_Q()
        return t, M, q

    def read_lines(self):
        self.lines = self.file.readlines()

    def get_commands(self):
        self.commands = [None] * len(self.lines)
        for i, line in enumerate(self.lines):
            self.commands[i] = Command(line)
            self.commands[i].interpret()

    def get_M(self):
        M_t = np.zeros((3, 1))
        for command in self.commands:
            if command.type == "line":
                _, M, _, _ = Line(self.law, self.H, self.L).get_M(self.current_pos, command.B, self.V)
                M_t = np.append(M_t, M, axis=1)
            elif command.type == "clockwise":
                _, M, _, _M = ArcXY(self.law, self.H, self.L).get_M(self.current_pos, command.B, command.C, self.V, True)
                M_t = np.append(M_t, M, axis=1)
            elif command.type == "anticlockwise":
                _, M, _, _ = ArcXY(self.law, self.H, self.L).get_M(self.current_pos, command.B, command.C, self.V, False)
                M_t = np.append(M_t, M, axis=1)
            self.current_pos = command.B
        return M_t

    def get_Q(self):
        pass
