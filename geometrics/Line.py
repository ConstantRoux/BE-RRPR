import numpy as np
import math
from matplotlib import pyplot as plt, animation
from matplotlib.widgets import Slider

from geometrics.Geometric import Geometric
from models.MGI import MGI
from models.MGD import MGD
from models.MDI import MDI


class Line(Geometric):
    def __init__(self, law, H, L):
        super().__init__(law, H, L)

    def traj(self, A, B, V, theta=0):
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

    def plot_Q(self, A, B, V, theta=0):
        t, q, q_bis, _, _ = self.traj(A, B, V, theta)
        fig, axs = plt.subplots(4)
        axs[0].scatter(t, q[0], c='blue', s=2)
        axs[0].scatter(t, q_bis[0], c='green', s=2)
        axs[0].legend(['q1', 'q1 bis'])
        axs[0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[1].scatter(t, q[1], c='blue', s=2)
        axs[1].scatter(t, q_bis[1], c='green', s=2)
        axs[1].legend(['q2', 'q2 bis'])
        axs[1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[2].scatter(t, q[2], c='blue', s=2)
        axs[2].scatter(t, q_bis[2], c='green', s=2)
        axs[2].legend(['q3', 'q3 bis'])
        axs[2].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[3].scatter(t, q[3], c='blue', s=2)
        axs[3].scatter(t, q_bis[3], c='green', s=2)
        axs[3].legend(['q4', 'q4 bis'])
        axs[3].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        plt.show()

    def plot_dQ(self, A, B, V, theta=0):
        t, q, q_bis, dq, dq_bis = self.traj(A, B, V, theta)
        fig, axs = plt.subplots(4)
        axs[0].scatter(t, dq[0], c='blue', s=2)
        axs[0].scatter(t, dq_bis[0], c='green', s=2)
        axs[0].legend([r'$\dot{q}_1$', r'$\dot{q}_{1bis}$'])
        axs[0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[1].scatter(t, dq[1], c='blue', s=2)
        axs[1].scatter(t, dq_bis[1], c='green', s=2)
        axs[1].legend([r'$\dot{q}_2$', r'$\dot{q}_{2bis}$'])
        axs[1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[2].scatter(t, dq[2], c='blue', s=2)
        axs[2].scatter(t, dq_bis[2], c='green', s=2)
        axs[2].legend([r'$\dot{q}_3$', r'$\dot{q}_{3bis}$'])
        axs[2].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[3].scatter(t, dq[3], c='blue', s=2)
        axs[3].scatter(t, dq_bis[3], c='green', s=2)
        axs[3].legend([r'$\dot{q}_4$', r'$\dot{q}_{4bis}$'])
        axs[3].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        plt.show()

    def plot3D_Q(self, A, B, V, theta=0):
        f, ax = plt.subplots()
        ax_q = [None]
        sl_q = [None]
        ax = plt.axes(projection='3d')
        f.subplots_adjust(left=0.1)

        t, q, q_bis, _, _ = self.traj(A, B, V, theta)
        mgd = MGD(self.H, self.L, None)
        mgd2 = MGD(self.H, self.L, None)
        j = np.array([0])

        def update(value):
            j[0] = sl_q.val
            ax.clear()
            draw()

        def draw():
            t, M, _, _ = self.get_M(A, B, V)
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
                    theta = math.atan2(mgd.T05[1, 0], mgd.T05[0, 0])
                    X = mgd.T05[0, 3]
                    Y = mgd.T05[1, 3]
                    Z = mgd.T05[2, 3]

                    ax.text(c_r[2 * i + 1, 0], c_r[2 * i + 1, 1], c_r[2 * i + 1, 2] - 0.5, r'$\theta={:.1f}, X={:.1f}, '
                                                                                           r'Y={:.1f}, '
                                                                                           r'Z={:.1f}$'.format(
                        theta * 180. / np.pi, X, Y, Z))

                    mgd2.get_T05(q_bis[:, j[0]])
                    theta = math.atan2(mgd2.T05[1, 0], mgd2.T05[0, 0])
                    X = mgd2.T05[0, 3]
                    Y = mgd2.T05[1, 3]
                    Z = mgd2.T05[2, 3]

            ax.set_aspect('equal')
            ax.axes.set_xlim3d(left=-np.sum(self.L), right=np.sum(self.L))
            ax.axes.set_ylim3d(bottom=-np.sum(self.L), top=np.sum(self.L))
            ax.axes.set_zlim3d(bottom=-np.sum(self.L), top=np.sum(self.L))
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

    def plot_M(self, A, B, V):
        fig, axs = plt.subplots(3, 3)

        t, M, dM, d2M = self.get_M(A, B, V)

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

    def plot3D_M(self, A, B, V, theta=0):
        f, ax = plt.subplots()
        ax = plt.axes(projection='3d')
        ax.set_aspect('equal')
        ax.axes.set_xlim3d(left=-np.sum(self.L), right=np.sum(self.L))
        ax.axes.set_ylim3d(bottom=-np.sum(self.L), top=np.sum(self.L))
        ax.axes.set_zlim3d(bottom=-np.sum(self.L), top=np.sum(self.L))
        t, M, _, _ = self.get_M(A, B, V)
        ax.scatter(M[0, ::3], M[1, ::3], M[2, ::3], s=2)
        ax.scatter(A[0], A[1], A[2], color='red')
        ax.text(A[0, 0], A[1, 0], A[2, 0] - 0.1, 'A({:.1f},{:.1f},{:.1f})'.format(A[0, 0], A[1, 0], A[2, 0]))
        ax.scatter(B[0], B[1], B[2], color='red')
        ax.text(B[0, 0], B[1, 0], B[2, 0] - 0.1, 'B({:.1f},{:.1f},{:.1f})'.format(B[0, 0], B[1, 0], B[2, 0]))
        data, = ax.plot([M[0, 0], M[0, 0] + 0.1 * np.cos(theta)], [M[1, 0], M[1, 0] + 0.1 * np.sin(theta)],
                        [M[2, 0], M[2, 0]], 'b')

        def animate(i):
            data.set_data([M[0, i], M[0, i] + 0.1 * np.cos(theta)], [M[1, i], M[1, i] + 0.1 * np.sin(theta)])
            data.set_3d_properties([M[2, i], M[2, i]])
            return data,

        anim = animation.FuncAnimation(f, animate, frames=t.shape[0], interval=self.law.Te, blit=True)

        plt.show()
