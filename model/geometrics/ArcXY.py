import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from model.geometrics.Geometric import Geometric
import numpy as np

from models.MDI import MDI
from models.MGD import MGD
from models.MGI import MGI


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

        # get dq
        mdi = MDI(self.L)
        dq = np.zeros((4, t.shape[0]))
        dq_bis = np.zeros((4, t.shape[0]))
        for i in range(t.shape[0]):
            dq[:, i] = mdi.get_dq(np.append(dM[:, i], theta), q[:, i])
            dq_bis[:, i] = mdi.get_dq(np.append(dM[:, i], theta), q_bis[:, i])

        return t, q, q_bis, dq, dq_bis

    def plot_Q(self):
        pass

    def plot_dQ(self):
        pass

    def plot3D_Q(self, A, B, C, V, clockwise, theta=0):
        f, ax = plt.subplots()
        ax_q = [None]
        sl_q = [None]
        ax = plt.axes(projection='3d')
        f.subplots_adjust(left=0.1)

        t, q, q_bis, _, _ = self.traj(A, B, C, V, clockwise, theta=0)
        mgd = MGD(self.H, self.L, None)
        mgd2 = MGD(self.H, self.L, None)
        j = np.array([0])

        def update(value):
            j[0] = sl_q.val
            ax.clear()
            draw()

        def draw():
            t, M, _, _ = self.get_M(A, B, C, V, clockwise)
            ax.scatter(M[0], M[1], M[2], color='red', s=1)

            ax.text(A[0, 0], A[1, 0], A[2, 0], 'A', color='red')

            ax.text(B[0, 0], B[1, 0], B[2, 0], 'B', color='red')

            labels = ['O_0', 'O_1', 'O_2', 'O_3', 'O_4', 'O_5']
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
                    theta = np.arctan2(mgd.T05[1, 0], mgd.T05[0, 0])
                    X = mgd.T05[0, 3]
                    Y = mgd.T05[1, 3]
                    Z = mgd.T05[2, 3]

                    ax.text(c_r[2 * i + 1, 0], c_r[2 * i + 1, 1], c_r[2 * i + 1, 2] - 0.5, r'$\theta={:.1f}, X={:.1f}, '
                                                                                           r'Y={:.1f}, '
                                                                                           r'Z={:.1f}$'.format(
                        theta * 180. / np.pi, X, Y, Z))

                    mgd2.get_T05(q_bis[:, j[0]])
                    theta = np.arctan2(mgd2.T05[1, 0], mgd2.T05[0, 0])
                    X = mgd2.T05[0, 3]
                    Y = mgd2.T05[1, 3]
                    Z = mgd2.T05[2, 3]

            ax.set_aspect('equal')
            ax.axes.set_xlim3d(left=-4, right=4)
            ax.axes.set_ylim3d(bottom=-4, top=4)
            ax.axes.set_zlim3d(bottom=-5, top=5)
            ax.plot3D(c_r[:, 0], c_r[:, 1], c_r[:, 2], linewidth='5', color='blue')
            ax.plot3D(c_r2[:, 0], c_r2[:, 1], c_r2[:, 2], linewidth='5', color='green')

        draw()

        # slider
        ax_q = f.add_axes([0.05, 0.05, 0.0225, 0.8])
        sl_q = Slider(
            ax=ax_q,
            label='k.Te',
            valmin=0,
            valmax=t.shape[0] - 1,
            valfmt='%0.0f',
            valinit=0,
            orientation="vertical")
        sl_q.on_changed(update)

        plt.show()

    def get_M(self, A, B, C, V, clockwise):
        # variables
        way = 1 if not clockwise else -1

        # distance de l'arc r.theta
        r = np.linalg.norm(C - A)
        th_A = (np.arctan2(A[1] - C[1], A[0] - C[0]) + 2 * np.pi) % (2 * np.pi)
        th_B = (np.arctan2(B[1] - C[1], B[0] - C[0]) + 2 * np.pi) % (2 * np.pi)
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

        # calcul de dM
        dM = np.zeros((3, t.shape[0]))
        dM[0, :] = -way * r * angle * s_vit / d * np.sin(way * angle * s_dis / d + th_A)
        dM[1, :] = way * r * angle * s_vit / d * np.cos(way * angle * s_dis / d + th_A)

        # calcul de d2M
        d2M = np.zeros((3, t.shape[0]))
        d2M[0, :] = (-way * r * angle * s_vit / d) * (-way * r * angle * s_vit / d) * np.cos(way * angle * s_dis / d + th_A)
        d2M[1, :] = -(way * r * angle * s_vit / d) * (way * r * angle * s_vit / d) * np.sin(way * angle * s_dis / d + th_A)

        return t, M, dM, d2M

    def plot_M(self, A, B, C, V, clockwise):
        fig, axs = plt.subplots(3, 3)

        t, M, dM, d2M = self.get_M(A, B, C, V, clockwise)

        axs[0, 0].scatter(t, M[0], s=2)
        axs[0, 0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[0, 0].set_title('x(t)')
        axs[1, 0].scatter(t, dM[0], s=2)
        axs[1, 0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[1, 0].set_title('x\'(t)')
        axs[2, 0].scatter(t, d2M[0], s=2)
        axs[2, 0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[2, 0].set_title('x\'\'(t)')

        axs[0, 1].scatter(t, M[1], s=2)
        axs[0, 1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[0, 1].set_title('y(t)')
        axs[1, 1].scatter(t, dM[1], s=2)
        axs[1, 1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[1, 1].set_title('y\'(t)')
        axs[2, 1].scatter(t, d2M[1], s=2)
        axs[2, 1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[2, 1].set_title('y\'\'(t)')

        axs[0, 2].scatter(t, M[2], s=2)
        axs[0, 2].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[0, 2].set_title('z(t)')
        axs[1, 2].scatter(t, dM[2], s=2)
        axs[1, 2].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[1, 2].set_title('z\'(t)')
        axs[2, 2].scatter(t, d2M[2], s=2)
        axs[2, 2].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[2, 2].set_title('z\'\'(t)')

        fig.subplots_adjust(hspace=0.5, wspace=0.25)
        plt.show()
    def plot3D_M(self):
        pass


