import numpy as np
import matplotlib.pyplot as plt


class MGD:
    def __init__(self, H, L):
        self.T = [None] * 5
        self.T05 = None
        self.H = H
        self.L = L

    def get_T01(self, q1):
        self.T[0] = np.matrix([ [np.cos(q1),    -np.sin(q1),    0,      self.L[0]],
                                [np.sin(q1),    np.cos(q1),     0,      0],
                                [0,             0,              1,      self.H[0]],
                                [0,             0,              0,      1]])
        return self.T[0]

    def get_T12(self, q2):
        self.T[1] = np.matrix([ [np.cos(q2),    -np.sin(q2),    0,      self.L[1]],
                                [np.sin(q2),    np.cos(q2),     0,      0],
                                [0,             0,              1,      0],
                                [0,             0,              0,      1]])
        return self.T[1]

    def get_T23(self, q3):
        self.T[2] = np.matrix([[1,      0,      0,      self.L[2]],
                               [0,      1,      0,      0],
                               [0,      0,      1,      q3],
                               [0,      0,      0,      1]])
        return self.T[2]

    def get_T34(self, q4):
        self.T[3] = np.matrix([ [np.cos(q4),    -np.sin(q4),    0,      self.L[3]],
                                [np.sin(q4),    np.cos(q4),     0,      0],
                                [0,             0,              1,      self.H[1]],
                                [0,             0,              0,      1]])
        return self.T[3]

    def get_T45(self):
        self.T[4] = np.matrix([ [1,     0,      0,      self.L[4]],
                                [0,     1,      0,      0],
                                [0,     0,      1,      0],
                                [0,     0,      0,      1]])
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

    def plot(self, q):
        f, ax = plt.subplots()
        ax = plt.axes(projection='3d')

        labels = ['O_0', 'O_1', 'O_2', 'O_3', 'O_4', 'O_5']
        c_r = np.zeros((12, 3))
        for i in range(2, 12, 2):
            c_r[i] = np.transpose(self.get_T0k(q, int(i / 2))[:-1, 3])
            c_r[i, 2] = c_r[i - 1, 2]
            c_r[i + 1] = np.transpose(self.get_T0k(q, int(i / 2))[:-1, 3])

        for i, txt in enumerate(labels):
            ax.text(c_r[2*i + 1, 0], c_r[2*i + 1, 1], c_r[2*i + 1, 2], txt, color='red')

        ax.plot3D(c_r[:, 0], c_r[:, 1], c_r[:, 2])
        plt.show()

