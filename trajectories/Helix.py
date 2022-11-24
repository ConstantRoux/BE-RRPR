import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from models.MGI import MGI
from models.MGD import MGD


class Helix:
    def __init__(self, Te, H, L):
        self.Te = Te
        self.H = H
        self.L = L

    def traj(self, A, H, V, r, p, s=1, theta=0):
        t, M = self.get_M(A, H, V, r, p, s=1)
        mgi = MGI(self.H, self.L)
        q = np.zeros((4, t.shape[0]))
        q_bis = np.zeros((4, t.shape[0]))
        for i in range(t.shape[0]):
            q[:, i], q_bis[:, i] = mgi.get_Qi(M[0, i], M[1, i], M[2, i], theta)
        return t, q, q_bis

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

        return t, M

    def plot3D_Q(self, A, H, V, r, p, s=1, theta=0):
        f, ax = plt.subplots()
        ax_q = [None]
        sl_q = [None]
        ax = plt.axes(projection='3d')
        f.subplots_adjust(left=0.1)

        t, q, q_bis = self.traj(A, H, V, r, p, s=1, theta=0)
        mgd = MGD(self.H, self.L, None)
        mgd2 = MGD(self.H, self.L, None)
        j = np.array([0])

        def update(value):
            j[0] = sl_q.val
            ax.clear()
            draw()

        def draw():
            labels = ['O_0', 'O_1', 'O_2', 'O_3', 'O_4', 'O_5']
            t, M = self.get_M(A, H, V, r, p, s)
            ax.scatter(M[0], M[1], M[2], color='red', s=1)
            c_r = np.zeros((12, 3))
            c_r2 = np.zeros((12, 3))
            for i in range(2, 12, 2):
                c_r[i] = np.transpose(mgd.get_T0k(q[:, j[0]], int(i / 2))[:-1, 3])
                c_r[i, 2] = c_r[i - 1, 2]
                c_r[i + 1] = np.transpose(mgd.get_T0k(q[:, j[0]], int(i / 2))[:-1, 3])

                c_r2[i] = np.transpose(mgd.get_T0k(q_bis[:, j[0]], int(i / 2))[:-1, 3])
                c_r2[i, 2] = c_r2[i - 1, 2]
                c_r2[i + 1] = np.transpose(mgd.get_T0k(q_bis[:, j[0]], int(i / 2))[:-1, 3])

            for i, txt in enumerate(labels):
                ax.text(c_r[2 * i + 1, 0], c_r[2 * i + 1, 1], c_r[2 * i + 1, 2], txt, color='blue')
                ax.text(c_r2[2 * i + 1, 0], c_r2[2 * i + 1, 1], c_r2[2 * i + 1, 2], txt, color='green')
                if i == 5:
                    mgd.get_T05(q[:, j[0]])
                    theta = math.atan2(mgd.T05[1, 0], mgd.T05[0, 0])
                    X = mgd.T05[0, 3]
                    Y = mgd.T05[1, 3]
                    Z = mgd.T05[2, 3]

                    ax.text(c_r[2 * i + 1, 0], c_r[2 * i + 1, 1], c_r[2 * i + 1, 2] - 0.5, r'$\theta={:.1f}, X={:.1f}, '
                                                                                           r'Y={:.1f}, '
                                                                                           r'Z={:.1f}$'.format(theta * 180. / np.pi, X, Y, Z))

                    mgd2.get_T05(q_bis[:, j[0]])
                    theta = math.atan2(mgd2.T05[1, 0], mgd2.T05[0, 0])
                    X = mgd2.T05[0, 3]
                    Y = mgd2.T05[1, 3]
                    Z = mgd2.T05[2, 3]

            ax.plot3D(c_r[:, 0], c_r[:, 1], c_r[:, 2], linewidth='5', color='blue')
            ax.plot3D(c_r2[:, 0], c_r2[:, 1], c_r2[:, 2], linewidth='5', color='green')

        draw()

        # slider
        ax_q = f.add_axes([0.05, 0.05, 0.0225, 0.8])
        sl_q = Slider(
            ax=ax_q,
            label='k.Te',
            valmin=0,
            valmax=t.shape[0]-1,
            valfmt='%0.0f',
            valinit=0,
            orientation="vertical")
        sl_q.on_changed(update)

        plt.show()

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