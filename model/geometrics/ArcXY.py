import matplotlib.pyplot as plt

from model.geometrics.Geometric import Geometric
import numpy as np


class ArcXY(Geometric):
    def __init__(self, law, H, L):
        super().__init__(law, H, L)

    def traj(self, A, B, C, V, theta=0):
        pass

    def plot_Q(self):
        pass

    def plot_dQ(self):
        pass

    def plot3D_Q(self):
        pass

    def get_M(self, A, B, C, V):
        # distance de l'arc r.theta
        def get_angle(v1, v2):
            v1_u = v1 / np.linalg.norm(v1)
            v2_u = v2 / np.linalg.norm(v2)
            return np.arccos(np.dot(v1_u[:, 0], v2_u[:, 0]))

        r = np.linalg.norm(C - A)
        angle = get_angle((C-A), (C-B))
        d = r * np.abs(angle)

        # abscisse curviligne et ses dérivées
        t, s_dis, s_vit, s_acc = self.law.get_s(d, V)

        # calcul de M
        M = np.zeros((3, t.shape[0]))
        M[0, :] = C[0] + r * np.cos(angle * s_dis / d + np.pi)
        M[1, :] = C[1] + r * np.sin(angle * s_dis / d)

        # calcul de dM
        # dM = (s_vit * U / d)

        # calcul de d2M
        # d2M = (s_acc * U / d)

        return t, M

    def plot_M(self, A, B, C, V):
        t, M = self.get_M(A, B, C, V)
        plt.plot(M[0], M[1])
        plt.show()

    def plot3D_M(self):
        pass


