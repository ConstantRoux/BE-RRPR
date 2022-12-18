from model.geometrics.Geometric import Geometric
import numpy as np
from model.models.MDI import MDI
from model.models.MGI import MGI


class ArcXY(Geometric):
    def __init__(self, law, H, L):
        super().__init__(law, H, L)

    def traj(self, A, B, C, V, clockwise, theta=0):
        # get geometrics
        t, M, dM, d2M = self.get_M(A, B, C, V, clockwise)

        # get q
        mgi = MGI(self.H, self.L)
        q = np.zeros((4, t.shape[0]))
        q_bis = np.zeros((4, t.shape[0]))
        for i in range(t.shape[0]):
            q[:, i], q_bis[:, i] = mgi.get_Qi(M[0, i], M[1, i], M[2, i], theta)
        q = mgi.fix_singularities(q, theta)
        q_bis = mgi.fix_singularities(q_bis, theta)

        # get dq
        mdi = MDI(self.L)
        dq = np.zeros((4, t.shape[0]))
        dq_bis = np.zeros((4, t.shape[0]))
        for i in range(t.shape[0]):
            dq[:, i] = mdi.get_dq(np.append(dM[:, i], theta), q[:, i])
            dq_bis[:, i] = mdi.get_dq(np.append(dM[:, i], theta), q_bis[:, i])

        return t, q, q_bis, dq, dq_bis

    def is_reachable(self):
        pass

    def get_M(self, A, B, C, V, clockwise):
        # variables
        way = 1 if not clockwise else -1

        # distance de l'arc r.theta
        r = np.linalg.norm(C - A)
        th_A = (np.arctan2(float(A[1] - C[1]), float(A[0] - C[0])) + 2 * np.pi) % (2 * np.pi)
        th_B = (np.arctan2(float(B[1] - C[1]), float(B[0] - C[0])) + 2 * np.pi) % (2 * np.pi)
        angle = (th_B - th_A + 2 * np.pi) % (2 * np.pi)
        if clockwise:
            angle = 2 * np.pi - angle
        d = r * np.abs(angle)

        # abscisse curviligne et ses dérivées
        t, s_dis, s_vit, s_acc = self.law.get_s(d, V)

        # calcul de M
        M = np.zeros((3, t.shape[0]))
        M[0, :] = C[0] + r * np.cos(way * angle * s_dis / d + th_A)
        M[1, :] = C[1] + r * np.sin(way * angle * s_dis / d + th_A)
        M[2, :] = np.ones((1, t.shape[0])) * A[2]

        # calcul de dM
        dM = np.zeros((3, t.shape[0]))
        dM[0, :] = -way * r * angle * s_vit / d * np.sin(way * angle * s_dis / d + th_A)
        dM[1, :] = way * r * angle * s_vit / d * np.cos(way * angle * s_dis / d + th_A)

        # calcul de d2M
        d2M = np.zeros((3, t.shape[0]))
        d2M[0, :] = (-way * r * angle * s_vit / d) * (-way * r * angle * s_vit / d) * np.cos(way * angle * s_dis / d + th_A)
        d2M[1, :] = -(way * r * angle * s_vit / d) * (way * r * angle * s_vit / d) * np.sin(way * angle * s_dis / d + th_A)

        return t, M, dM, d2M
