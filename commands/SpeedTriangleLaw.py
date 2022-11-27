import numpy as np
from matplotlib import pyplot as plt

from commands.Law import Law


class SpeedTriangleLaw(Law):
    def __init__(self, Te):
        super().__init__(Te)

    def get_s(self, d, V):
        t, s_dis = self._get_s_dis(V, d)
        t, s_vit = self._get_s_vit(V, d)
        t, s_acc = self._get_s_acc(V, d)

        return t, s_dis, s_vit, s_acc

    def _get_s_dis(self, V, d):
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

    def _get_s_vit(self, V, d):
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

    def _get_s_acc(self, V, d):
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
        t, s_dis, s_vit, s_acc = self.get_s(d, V)

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
