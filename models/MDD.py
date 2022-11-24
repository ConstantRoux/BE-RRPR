import numpy as np


class MDD:
    def __init__(self, L):
        self.L = L

    def get_jacobienne(self, q):
        P12 = self.L[1] * np.sin(q[0]) + self.L[2] * np.cos(q[1]) * np.sin(q[0]) + self.L[2] * np.sin(q[1]) * np.cos(q[0]) + self.L[3] * np.cos(q[1]) * np.sin(q[0]) + self.L[3] * np.sin(q[1]) * np.cos(q[0])
        P22 = self.L[2] * np.cos(q[1]) * np.sin(q[0]) + self.L[2] * np.sin(q[1]) * np.cos(q[0]) + self.L[3] * np.sin(q[0]) * np.cos(q[1]) + self.L[3] * np.sin(q[1]) * np.cos(q[0])
        P11 = self.L[1] * np.cos(q[0]) + self.L[2] * np.cos(q[1]) * np.cos(q[0]) - self.L[2] * np.sin(q[1]) * np.sin(q[0]) + self.L[3] * np.cos(q[1]) * np.cos(q[0]) - self.L[3] * np.sin(q[1]) * np.sin(q[0])
        P21 = self.L[2] * np.cos(q[1]) * np.cos(q[0]) - self.L[2] * np.sin(q[1]) * np.sin(q[0]) + self.L[3] * np.cos(q[1]) * np.cos(q[0]) - self.L[3] * np.sin(q[1]) * np.sin(q[0])

        J = np.array([
            [-P12, -P22, 0, 0],
            [P11, P21, 0, 0],
            [0, 0, 1, 0],
            [1, 1, 0, 1]])

        return J



