import numpy as np
from exception.NotReachableException import NotReachableException
from model.geometrics.Geometric import Geometric
from model.models.MGI import MGI
from model.models.MDI import MDI


class Line(Geometric):
    def __init__(self, law, H, L):
        super().__init__(law, H, L)

    def traj(self, A, B, V, theta=0):
        # check if the line is possible
        if not self.is_reachable(A, B, theta):
            raise NotReachableException("Le segment [AB] n'est pas compris dans la zone atteignable par le robot.")

        # get geometrics
        t, M, dM, d2M = self.get_M(A, B, V)

        # get q
        mgi = MGI(self.H, self.L)
        q = np.zeros((4, t.shape[0]))
        q_bis = np.zeros((4, t.shape[0]))
        for i in range(t.shape[0]):
            q[:, i], q_bis[:, i] = mgi.get_Qi(M[0, i], M[1, i], M[2, i], theta)

        # get dq
        mdi = MDI(self.L)
        dq = np.zeros((4, t.shape[0]))
        dq_bis = np.zeros((4, t.shape[0]))
        for i in range(t.shape[0]):
            dq[:, i] = mdi.get_dq(np.append(dM[:, i], theta), q[:, i])
            dq_bis[:, i] = mdi.get_dq(np.append(dM[:, i], theta), q_bis[:, i])

        return t, q, q_bis, dq, dq_bis

    def is_reachable(self, A, B, theta):
        if ((A[0] - self.L[0] - self.L[4] * np.cos(theta)) ** 2 + (A[1] - self.L[4] * np.sin(theta)) ** 2) \
                > ((self.L[1] + self.L[2] + self.L[3]) ** 2):
            return False
        elif ((B[0] - self.L[0] - self.L[4] * np.cos(theta)) ** 2 + (B[1] - self.L[4] * np.sin(theta)) ** 2) \
                > ((self.L[1] + self.L[2] + self.L[3]) ** 2):
            return False
        else:
            return True

    def get_M(self, A, B, V):
        # abscisse curviligne et ses dérivées
        t, s_dis, s_vit, s_acc = self.law.get_s(np.linalg.norm(B - A), V)

        # vecteur directeur
        U = B - A

        # norme euclidienne A, B
        d = np.linalg.norm(B - A)

        # calcul de M
        M = A + (s_dis * U / d)

        # calcul de dM
        dM = (s_vit * U / d)

        # calcul de d2M
        d2M = (s_acc * U / d)

        return t, M, dM, d2M
