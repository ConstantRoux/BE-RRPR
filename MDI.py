import numpy as np
import MDD


class MDI:
    def __init__(self, L):
        self.L = L

    def getConfigsPoint(self, x_point, q1, q2, q3, q4):
        q_point = np.linalg.inv(MDD.MDD.getJacobienne(q1, q2, q3, q4)) * x_point
        return q_point
