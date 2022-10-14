import numpy as np


class MGD:
    def __init__(self, H, L):
        self.T = [None] * 5
        self.T05 = None
        self.H = H
        self.L = L

    def get_T01(self, q1):
        self.T[0] = np.matrix([ [np.cos(q1),    -np.sin(q1),    0,      self.L[0]],
                                [np.sin(q1),    np.cos(q1),     0,      0],
                                [0,             0,              1,      self.H[0]],
                                [0,             0,              0,      1]])
        return self.T[0]

    def get_T12(self, q2):
        self.T[1] = np.matrix([ [np.cos(q2),    -np.sin(q2),    0,      self.L[1]],
                                [np.sin(q2),    np.cos(q2),     0,      0],
                                [0,             0,              1,      0],
                                [0,             0,              0,      1]])
        return self.T[1]

    def get_T23(self, q3):
        self.T[2] = np.matrix([[1,      0,      0,      self.L[2]],
                               [0,      1,      0,      0],
                               [0,      0,      1,      q3],
                               [0,      0,      0,      1]])
        return self.T[2]

    def get_T34(self, q4):
        self.T[3] = np.matrix([ [np.cos(q4),    -np.sin(q4),    0,      self.L[3]],
                                [np.sin(q4),    np.cos(q4),     0,      0],
                                [0,             0,              1,      self.H[1]],
                                [0,             0,              0,      1]])
        return self.T[3]

    def get_T45(self):
        self.T[4] = np.matrix([ [1,     0,      0,      self.L[4]],
                                [0,     1,      0,      0],
                                [0,     0,      1,      0],
                                [0,     0,      0,      1]])
        return self.T[4]

    def get_T05(self, q):
        self.T05 = np.copy(self.get_T01(q[0]))
        self.T05 = np.dot(self.T05, self.get_T12(q[1]))
        self.T05 = np.dot(self.T05, self.get_T23(q[2]))
        self.T05 = np.dot(self.T05, self.get_T34(q[3]))
        self.T05 = np.dot(self.T05, self.get_T45())

        return self.T05
