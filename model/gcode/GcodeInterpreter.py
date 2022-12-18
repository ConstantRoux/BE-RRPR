import numpy as np

from model.gcode.Command import Command
from model.geometrics.ArcXY import ArcXY
from model.geometrics.Line import Line
from model.models.MGI import MGI


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
        t_t = np.zeros((1,))
        for command in self.commands:
            if command.type == "line":
                t, M, _, _ = Line(self.law, self.H, self.L).get_M(self.current_pos, command.B, self.V)
                M_t = np.append(M_t, M, axis=1)
                t_t = np.append(t_t, t + t_t[-1])
            elif command.type == "clockwise":
                t, M, _, _M = ArcXY(self.law, self.H, self.L).get_M(self.current_pos, command.B, command.C, self.V,
                                                                    True)
                M_t = np.append(M_t, M, axis=1)
                t_t = np.append(t_t, t + t_t[-1])
            elif command.type == "anticlockwise":
                t, M, _, _ = ArcXY(self.law, self.H, self.L).get_M(self.current_pos, command.B, command.C, self.V,
                                                                   False)
                M_t = np.append(M_t, M, axis=1)
                t_t = np.append(t_t, t + t_t[-1])
            self.current_pos = command.B
        return t_t, M_t

    def get_Q(self, t, M, theta):
        mgi = MGI(self.H, self.L)
        q = np.zeros((4, t.shape[0]))
        q_bis = np.zeros((4, t.shape[0]))
        for i in range(t.shape[0]):
            q[:, i], q_bis[:, i] = mgi.get_Qi(M[0, i], M[1, i], M[2, i], theta)
        q = mgi.fix_singularities(q, theta)
        q_bis = mgi.fix_singularities(q_bis, theta)

        return q, q_bis
