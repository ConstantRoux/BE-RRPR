import numpy as np
from matplotlib import pyplot as plt, animation
from matplotlib.widgets import Slider
from matplotlib.widgets import Button


class Line:
    def __init__(self, Te):
        self.Te = Te

    def traj(self, A, B, theta, V):
        pass

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

    def plot3D_M(self, A, B, V, theta=0):
        f, ax = plt.subplots()
        ax = plt.axes(projection='3d')
        f.subplots_adjust(left=0.15)
        sl, ax_sl = None, None

        t, M, _, _ = self.get_M(A, B, V)

        def draw(t_current):
            print(t_current)
            ax.scatter(A[0], A[1], A[2], color='red')
            ax.scatter(B[0], B[1], B[2], color='red')
            ax.scatter(M[0, t_current], M[1, t_current], M[2, t_current], color='blue')
            ax.plot([M[0, t_current], M[0, t_current] + 0.1*np.cos(theta)], [M[1, t_current], M[1, t_current] + 0.1 * np.sin(theta)], [M[2, t_current], M[2, t_current]], color='blue')

        def update(value):
            ax.clear()
            draw(value)

        ax_sl = f.add_axes([0.05, 0.1, 0.0225, 0.8])
        sl = Slider(ax=ax_sl,
                    label="k.Te",
                    valmin=0,
                    valmax=t.shape[0]-1,
                    valinit=0,
                    valstep=1,
                    orientation="vertical")
        sl.on_changed(update)

        draw(0)

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
