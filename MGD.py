import numpy as np
from math import sin, cos


class MGD:
    def __init__(self, Q, h1, h2, L1, L2, L3, L4, L5):
        self.T01 = np.matrix([cos(Q[0]), -sin(Q[0]), 0, L1],
                             [sin(Q[0]), cos(Q[0]), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1])

        self.T12 = np.matrix([cos(Q[1]), -sin(Q[1]), 0, L2],
                             [sin(Q[1]), cos(Q[1]), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1])

        self.T23 = np.matrix([1, 0, 0, L3],
                             [0, 1, 0, 0],
                             [0, 0, 1, Q[2]],
                             [0, 0, 0, 1])

        self.T34 = np.matrix([cos(Q[3]), -sin(Q[3]), 0, L4],
                             [sin(Q[3]), cos(Q[3]), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1])

        self.T45 = np.matrix([1, 0, 0, L5],
                             [0, 1, 0, 0],
                             [0, 0, 1, h1 + h2],
                             [0, 0, 0, 1])

    def getPassageMatrix(self):
        return self.T01, self.T12, self.T23, self.T34, self.T45
