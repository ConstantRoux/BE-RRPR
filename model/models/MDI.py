import numpy as np
from model.models.MDD import MDD


class MDI:
    def __init__(self, L):
        self.L = L
        self.mdd = MDD(L)

    def get_dq(self, dM, q):
        inv_J = np.linalg.inv(self.mdd.get_jacobienne(q))
        dq = np.dot(inv_J, np.transpose(dM))
        return dq
