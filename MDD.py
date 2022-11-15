import numpy as np


class MDD:
    def __init__(self, L):
        self.L = L

    def getJacobienne(self, q1, q2, q3, q4):
        P22 = self.L[2] * np.cos(q2) * np.sin(q1) + self.L[2] * np.sin(q2) * np.cos(q1) + self.L[3] * np.sin(q1) * np.cos(q2) + self.L[3] * np.sin(q2) * np.cos(q1)
        P21 = self.L[2] * np.cos(q2) * np.cos(q1) - self.L[2] * np.sin(q2) * np.sin(q1) + self.L[3] * np.cos(q2) * np.cos(q1) - self.L[3] * np.sin(q2) * np.sin(q1)
        P11 = self.L[1] * np.cos(q1) + self.L[2] * np.cos(q2) * np.cos(q1) - self.L[2] * np.sin(q2) * np.sin(q1) + self.L[3] * np.cos(q2) * np.cos(q1) - self.L[3] * np.sin(q2) * np.sin(q1)
        P12 = self.L[1] * np.sin(q1) + self.L[2] * np.cos(q2) * np.sin(q1) + self.L[2] * np.sin(q2) * np.cos(q1) + self.L[3] * np.cos(q2) * np.sin(q1) + self.L[3] * np.sin(q2) * np.cos(q1)
        J = [
            [-P12, -P22, 0, 0],
            [P11, P21, 0, 0],
            [0, 0, 1, 0],
            [1, 1, 0, 1]]


        return J



