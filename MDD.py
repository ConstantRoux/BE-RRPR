import numpy as np


class MDD:

    def __init__(self, L):
        self.J = np.matrix([
            [0, 0, 0, 0],
            [L[0] + L[1] + L[2] + L[3], L[1] + L[2] + L[3], 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 0, 1]
        ])

    def getJacobienne(self):
        return self.J

    def getJacobienneInv(self):
        return np.linalg.inv(self.J)
