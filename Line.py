import numpy as np
from matplotlib import pyplot as plt, animation
from MGI import MGI


class Line:
    def __init__(self, Te, H, L):
        self.Te = Te
        self.H = H
        self.L = L

    def traj(self, A, B, V, theta=0):
        t, M, dM, d2M = self.get_M(A, B, V)
        mgi = MGI(self.H, self.L)
        q = np.zeros((4, t.shape[0]))
        q_bis = np.zeros((4, t.shape[0]))
        for i in range(t.shape[0]):
            q[:, i], q_bis[:, i] = mgi.get_Qi(M[0, i], M[1, i], M[2, i], theta)
        return t, q, q_bis

    def plot_Q(self, A, B, V, theta=0):
        t, q, q_bis = self.traj(A, B, V, theta)
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

    def get_M(self, A, B, V):
        # abscisse curviligne et ses dérivées
        t, s_dis, s_vit, s_acc = self.get_s(A, B, V)

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

    def plot_M(self, A, B, V, theta=0):
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
        t, M, _, _ = self.get_M(A, B, V)
        ax.scatter(M[0, ::3], M[1, ::3], M[2, ::3], s=2)
        ax.scatter(A[0], A[1], A[2], color='red')
        ax.text(A[0, 0], A[1, 0], A[2, 0] - 0.1, 'A({:.1f},{:.1f},{:.1f})'.format(A[0, 0], A[1, 0], A[2, 0]))
        ax.scatter(B[0], B[1], B[2], color='red')
        ax.text(B[0, 0], B[1, 0], B[2, 0] - 0.1, 'B({:.1f},{:.1f},{:.1f})'.format(B[0, 0], B[1, 0], B[2, 0]))
        data, = ax.plot([M[0, 0], M[0, 0] + 0.1*np.cos(theta)], [M[1, 0], M[1, 0] + 0.1 * np.sin(theta)], [M[2, 0], M[2, 0]], 'b')

        def animate(i):
            data.set_data([M[0, i], M[0, i] + 0.1*np.cos(theta)], [M[1, i], M[1, i] + 0.1 * np.sin(theta)])
            data.set_3d_properties([M[2, i], M[2, i]])
            return data,

        anim = animation.FuncAnimation(f, animate, frames=t.shape[0], interval=self.Te, blit=True)

        plt.show()

    def get_s(self, A, B, V):
        d = np.linalg.norm(B - A)
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
        sd_t[0:int(t.shape[0] / 2)] = (V / t1) * t[0:int(t.shape[0] / 2)]
        sd_t[int(t.shape[0] / 2):] = (-V / t1) * t[int(t.shape[0] / 2):] + 2 * V

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

    def plot_s(self, A, B, V):
        t, s_dis, s_vit, s_acc = self.get_s(A, B, V)

        fig, axs = plt.subplots(3)
        fig.suptitle('Abscisse rectiligne et ses dérivées')

        axs[0].scatter(t, s_dis, s=1)
        axs[0].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[0].set_title("Abscisse rectiligne en fonction du temps")

        axs[1].scatter(t, s_vit, s=1)
        axs[1].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[1].set_title("Vitesse de l'abscisse rectiligne en fonction du temps")

        axs[2].scatter(t, s_acc, s=1)
        axs[2].axvline(t[int(t.shape[0] / 2)], linestyle='dashdot', c='red')
        axs[2].set_title("Accélération de l'abscisse rectiligne en fonction du temps")

        fig.subplots_adjust(hspace=1)
        plt.show()
