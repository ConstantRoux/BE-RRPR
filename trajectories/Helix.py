import numpy as np
from matplotlib import pyplot as plt


class Helix:
    def __init__(self, Te):
        self.Te = Te

    def get_M(self, A, H, V, r, p, s=1):
        # abscisse curviligne et ses dérivées
        c = np.sqrt(r**2 + p**2)
        d = np.sqrt(r**2 + p**2) * np.abs(H-A[2]) / p
        t, s_dis, s_vit, s_acc = self.get_s(V, d)

        # calcul de M
        M = np.zeros((3, t.shape[0]))
        M[0] = A[0] + r * np.cos(s_dis / c)
        M[1] = A[1] + s * r * np.sin(s_dis / c)
        M[2] = A[2] + p * s_dis / c

        f, ax = plt.subplots()
        ax = plt.axes(projection='3d')

        ax.plot3D(M[0], M[1], M[2])
        ax.text(A[0, 0], A[1, 0], A[2, 0],
                r'A({:.1f},{:.1f},{:.1f})'.format(A[0, 0], A[1, 0], A[2, 0]))
        plt.show()

        return t, M

    def get_s(self, V, d):
        t, s_dis = self.__get_s_dis(V, d)
        t, s_vit = self.__get_s_vit(V, d)
        t, s_acc = self.__get_s_acc(V, d)

        return t, s_dis, s_vit, s_acc

    def __get_s_dis(self, V, d):
        # time
        t1 = d / V
        t2 = 2 * t1
        t = np.arange(0, t2 + self.Te, self.Te)
        t[-1] = t2

        # abscisse rectiligne
        s_t = np.zeros((t.shape[0],))
        s_t[0:int(t.shape[0] / 2)] = V / (t1 * 2) * t[0:int(t.shape[0] / 2)] ** 2
        s_t[int(t.shape[0] / 2):] = -V / (t1 * 2) * t[int(t.shape[0] / 2):] ** 2 + 2 * V * t[int(t.shape[0] / 2):] - d

        return t, s_t

    def __get_s_vit(self, V, d):
        # time
        t1 = d / V
        t2 = 2 * t1
        t = np.arange(0, t2 + self.Te, self.Te)
        t[-1] = t2

        # abscisse rectiligne
        sd_t = np.zeros((t.shape[0],))
        sd_t[0:int(t.shape[0] / 2)] = V / t1 * t[0:int(t.shape[0] / 2)]
        sd_t[int(t.shape[0] / 2):] = -V / t1 * t[int(t.shape[0] / 2):] + 2 * V

        return t, sd_t

    def __get_s_acc(self, V, d):
        # time
        t1 = d / V
        t2 = 2 * t1
        t = np.arange(0, t2 + self.Te, self.Te)
        t[-1] = t2

        # abscisse rectiligne
        sa_t = np.zeros((t.shape[0],))
        sa_t[0:int(t.shape[0] / 2)] = V / t1
        sa_t[int(t.shape[0] / 2):] = -V / t1

        return t, sa_t

    def plot_s(self, d, V):
        fig, axs = plt.subplots(3)
        fig.suptitle('Abscisse rectiligne et ses dérivées')

        axs[0].scatter(self.__get_s_dis(d, V)[0], self.__get_s_dis(d, V)[1], s=1)
        axs[0].set_title("Abscisse rectiligne en fonction du temps")

        axs[1].scatter(self.__get_s_vit(d, V)[0], self.__get_s_vit(d, V)[1], s=1)
        axs[1].set_title("Vitesse de l'abscisse rectiligne en fonction du temps")

        axs[2].scatter(self.__get_s_acc(d, V)[0], self.__get_s_acc(d, V)[1], s=1)
        axs[2].set_title("Accélération de l'abscisse rectiligne en fonction du temps")

        fig.subplots_adjust(hspace=1)
        plt.show()