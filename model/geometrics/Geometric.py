from abc import ABC, abstractmethod
import numpy as np
from matplotlib import pyplot as plt, animation
from matplotlib.widgets import Slider
from model.models.MDD import MDD
from model.models.MGD import MGD


class Geometric(ABC):
    def __init__(self, law, H, L):
        self.law = law
        self.H = H
        self.L = L

    @abstractmethod
    def traj(self):
        pass

    @abstractmethod
    def is_reachable(self):
        pass

    def plot_Q(self, t, q, q_bis):
        fig, axs = plt.subplots(4)
        fig.suptitle(r'Trajectoire des courbes en $q$ en fonction du temps')
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

    def plot_dQ(self, t, dq, dq_bis):
        fig, axs = plt.subplots(4)
        fig.suptitle(r'Trajectoire des courbes en $\dot{q}$ en fonction du temps')
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

    def plot3D_Q(self, t, M, q, q_bis, step=1):
        f, ax = plt.subplots()
        f.suptitle(r'Visualisation du bras manipulateur lors de la trajectoire en 3D')
        ax_q = [None]
        sl_q = [None]
        ax = plt.axes(projection='3d')
        ax.set_aspect('equal')
        f.subplots_adjust(left=0.1)

        mgd = MGD(self.H, self.L, None)
        mgd2 = MGD(self.H, self.L, None)
        j = np.array([0])

        def update(value):
            j[0] = sl_q.val
            ax.clear()
            ax.set_aspect('equal')
            draw()

        def draw():
            ax.scatter(M[0, ::step], M[1, ::step], M[2, ::step], color='red', s=0.5)

            ax.text(M[0, 0], M[1, 0], M[2, 0], 'A', color='red')

            ax.text(M[0, -1], M[1, -1], M[2, -1], 'B', color='red')

            labels = [r'$O_0$', r'$O_1$', r'$O_2$', r'$O_3$', r'$O_4$', r'$O_5$']
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

            ax.axes.set_xlim3d(left=np.min(M[0]), right=np.max(M[0]))
            ax.axes.set_ylim3d(bottom=np.min(M[1]), top=np.max(M[1]))
            ax.axes.set_zlim3d(bottom=0, top=5)
            ax.plot3D(c_r[:, 0], c_r[:, 1], c_r[:, 2], linewidth='2', color='blue')
            ax.plot3D(c_r2[:, 0], c_r2[:, 1], c_r2[:, 2], linewidth='2', color='green')

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

    @abstractmethod
    def get_M(self):
        pass

    def plot_M(self, t, M, dM, d2M):
        fig, axs = plt.subplots(3, 3)
        fig.suptitle(r'Trajectoire du point $M$ et ses dérivées sur chaque axe en fonction du temps')

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

    def plot3D_M(self, t, M, theta):
        f, ax = plt.subplots()
        f.suptitle(r'Visualisation de la trajectoire du point $M$ en 3D')
        ax = plt.axes(projection='3d')
        ax.set_aspect('equal')
        ax.axes.set_xlim3d(left=np.min(M[0]), right=np.max(M[0]))
        ax.axes.set_ylim3d(bottom=np.min(M[1]), top=np.max(M[1]))
        ax.axes.set_zlim3d(bottom=0, top=5)
        ax.scatter(M[0, ::3], M[1, ::3], M[2, ::3], s=2)
        ax.scatter(M[0, 0], M[1, 0], M[2, 0], color='red')
        ax.text(M[0, 0], M[1, 0], M[2, 0] - 0.1, 'A({:.1f},{:.1f},{:.1f})'.format(M[0, 0], M[1, 0], M[2, 0]))
        ax.scatter(M[0, -1], M[1, -1], M[2, -1], color='red')
        ax.text(M[0, -1], M[1, -1], M[2, -1] - 0.1, 'B({:.1f},{:.1f},{:.1f})'.format(M[0, -1], M[1, -1], M[2, -1]))
        data, = ax.plot([M[0, 0], M[0, 0] + 0.1 * np.cos(theta)], [M[1, 0], M[1, 0] + 0.1 * np.sin(theta)],
                        [M[2, 0], M[2, 0]], 'b')

        def animate(i):
            data.set_data([M[0, i], M[0, i] + 0.1 * np.linalg.norm(M[:, 0] - M[:, -1]) * np.cos(theta)], [M[1, i], M[1, i] + 0.1 * np.linalg.norm(M[:, 0] - M[:, -1]) * np.sin(theta)])
            data.set_3d_properties([M[2, i], M[2, i]])
            return data,

        anim = animation.FuncAnimation(f, animate, frames=t.shape[0], interval=self.law.Te, blit=True)

        plt.show()

    def plot_theta(self, t, theta):
        f, ax = plt.subplots()
        f.suptitle(r'Trajectoire de $\theta$ en fonction du temps')
        vec = np.ones((t.shape[0],)) * theta
        ax.axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        plt.scatter(t, vec)
        plt.show()

    def plot_O5(self, t, q, dq, dM):
        mdd = MDD(self.L)
        dx = np.zeros((4, q.shape[1]))
        for i in range(q.shape[1]):
            dx[:, i] = np.dot(mdd.get_jacobienne(q[:, i]), dq[:, i])

        fig, axs = plt.subplots(3, 2)
        fig.suptitle(r'Comparaison de la vitesse du point $O_5$ obtenue avec la jacobienne avec la vitesse attendue en fonction du temps')
        axs[0, 0].scatter(t, dx[0, :], s=2)
        axs[0, 0].set_title('x\'(t)')
        axs[0, 0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[1, 0].scatter(t, dx[1, :], s=2)
        axs[1, 0].set_title('y\'(t)')
        axs[1, 0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[2, 0].scatter(t, dx[2, :], s=2)
        axs[2, 0].set_title('z\'(t)')
        axs[2, 0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[0, 1].scatter(t, dM[0], s=2)
        axs[0, 1].set_title('x\'(t) attendu')
        axs[0, 1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[1, 1].scatter(t, dM[1], s=2)
        axs[1, 1].set_title('y\'(t) attendu')
        axs[1, 1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        axs[2, 1].scatter(t, dM[2], s=2)
        axs[2, 1].set_title('z\'(t) attendu')
        axs[2, 1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')

        fig.subplots_adjust(hspace=0.5, wspace=0.25)
        plt.show()