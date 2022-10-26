import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from MGI import MGI
import math


class MGD:
    def __init__(self, H, L, q_lim):
        self.T = [None] * 5
        self.T05 = None
        self.H = H
        self.L = L
        self.q_lim = q_lim
        self.mgi = MGI(L, H)

    def get_T01(self, q1):
        self.T[0] = np.matrix([[np.cos(q1), -np.sin(q1), 0, self.L[0]],
                               [np.sin(q1), np.cos(q1), 0, 0],
                               [0, 0, 1, self.H[0]],
                               [0, 0, 0, 1]])
        return self.T[0]

    def get_T12(self, q2):
        self.T[1] = np.matrix([[np.cos(q2), -np.sin(q2), 0, self.L[1]],
                               [np.sin(q2), np.cos(q2), 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
        return self.T[1]

    def get_T23(self, q3):
        self.T[2] = np.matrix([[1, 0, 0, self.L[2]],
                               [0, 1, 0, 0],
                               [0, 0, 1, q3],
                               [0, 0, 0, 1]])
        return self.T[2]

    def get_T34(self, q4):
        self.T[3] = np.matrix([[np.cos(q4), -np.sin(q4), 0, self.L[3]],
                               [np.sin(q4), np.cos(q4), 0, 0],
                               [0, 0, 1, self.H[1]],
                               [0, 0, 0, 1]])
        return self.T[3]

    def get_T45(self):
        self.T[4] = np.matrix([[1, 0, 0, self.L[4]],
                               [0, 1, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
        return self.T[4]

    def get_T0k(self, q, k):
        funcs = [self.get_T01, self.get_T12, self.get_T23, self.get_T34, self.get_T45]
        T0k = np.identity(4)
        for i in range(0, k):
            if i == 4:
                T0k = np.dot(T0k, funcs[i]())
            else:
                T0k = np.dot(T0k, funcs[i](q[i]))
        return T0k

    def get_T05(self, q):
        self.T05 = self.get_T0k(q, 5)
        return self.T05

    def plot(self):
        f, ax = plt.subplots()
        ax_q = [None] * 4
        sl_q = [None] * 4
        ax = plt.axes(projection='3d')
        f.subplots_adjust(left=0.30)

        q = np.array([self.q_lim[0][0], self.q_lim[1][0], self.q_lim[2][0], self.q_lim[3][0]])

        def draw():
            labels = ['O_0', 'O_1', 'O_2', 'O_3', 'O_4', 'O_5']
            c_r = np.zeros((12, 3))
            for i in range(2, 12, 2):
                c_r[i] = np.transpose(self.get_T0k(q, int(i / 2))[:-1, 3])
                c_r[i, 2] = c_r[i - 1, 2]
                c_r[i + 1] = np.transpose(self.get_T0k(q, int(i / 2))[:-1, 3])

            for i, txt in enumerate(labels):
                ax.text(c_r[2 * i + 1, 0], c_r[2 * i + 1, 1], c_r[2 * i + 1, 2], txt, color='red')
                if i == 5:
                    self.get_T05(q)
                    theta = math.atan2(self.T05[1, 0], self.T05[0, 0])
                    X = self.T05[0, 3]
                    Y = self.T05[1, 3]
                    Z = self.T05[2, 3]

                    ((q1, q2, q3, q4),
                     (q1_bis, q2_bis, q3, q4_bis)) = self.mgi.getQi(X, Y, Z, theta)

                    print("%.2f" % q1, "%.2f" % q2, "%.2f" % q3, "%.2f" % q4)
                    print("%.2f" % q1_bis, "%.2f" % q2_bis, "%.2f" % q3, "%.2f" % q4_bis)
                    print()

                    ax.text(c_r[2 * i + 1, 0], c_r[2 * i + 1, 1], c_r[2 * i + 1, 2]-0.5, r'$\theta={:.1f}, X={:.1f}, '
                                                                                         r'Y={:.1f}, '
                                                                                         r'Z={:.1f}$'.format(theta * 180. / np.pi,
                                                                                                             X, Y, Z))
            ax.plot3D(c_r[:, 0], c_r[:, 1], c_r[:, 2], linewidth='10')

        draw()

        def update(value):
            for i in range(4):
                q[i] = sl_q[i].val
            ax.clear()
            draw()

        # sliders
        for i in range(4):
            ax_q[i] = f.add_axes([0.05 + 0.05 * i, 0.1, 0.0225, 0.8])
            sl_q[i] = Slider(
                ax=ax_q[i],
                label='q' + str(i + 1),
                valmin=self.q_lim[i][0],
                valmax=self.q_lim[i][1],
                valinit=self.q_lim[i][0],
                orientation="vertical")
            sl_q[i].on_changed(update)

        plt.show()
