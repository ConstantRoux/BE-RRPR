import numpy as np
from math import sin, cos


class MGD:
    def __init__(self, Q, H, L):
        self.T01 = np.matrix([[cos(Q[0]), -sin(Q[0]), 0, L[0]],
                              [sin(Q[0]), cos(Q[0]), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        self.T12 = np.matrix([[cos(Q[1]), -sin(Q[1]), 0, L[1]],
                              [sin(Q[1]), cos(Q[1]), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        self.T23 = np.matrix([[1, 0, 0, L[2]],
                              [0, 1, 0, 0],
                              [0, 0, 1, Q[2]],
                              [0, 0, 0, 1]])

        self.T34 = np.matrix([[cos(Q[3]), -sin(Q[3]), 0, L[3]],
                              [sin(Q[3]), cos(Q[3]), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        self.T45 = np.matrix([[1, 0, 0, L[4]],
                              [0, 1, 0, 0],
                              [0, 0, 1, H[0] + H[1]],
                              [0, 0, 0, 1]])

    def getPassageMatrix(self):
        return self.T01, self.T12, self.T23, self.T34, self.T45

    def getT05(self):
        T02 = np.dot(self.T01, self.T12)
        T03 = np.dot(T02, self.T23)
        T04 = np.dot(T03, self.T34)
        return np.dot(T04, self.T45)
