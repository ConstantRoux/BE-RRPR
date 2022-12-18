import numpy as np


class MGI:

    def __init__(self, H, L):
        self.H = H
        self.L = L
        self.Qi = np.zeros((4, 2))

    def get_Qi(self, X, Y, Z, theta):
        self.update_Qi(X, Y, Z, theta)
        return self.Qi[:, 0], self.Qi[:, 1]

    def fix_singularities(self, Q, theta):
        for i in range(Q.shape[1]):
            if Q[0, i] != Q[0, i]:
                if i == Q.shape[1] - 1:
                    Q[0, i] = Q[0, i - 1]
                else:
                    Q[0, i] = Q[0, i + 1]
                Q[3, i] = (theta - Q[0, i] - Q[1, i]) % (2 * np.pi)
        return Q

    def update_Qi(self, X, Y, Z, theta):
        # calcul de q2
        w1 = Y - self.L[4] * np.sin(theta)
        w2 = -self.L[0] + X - self.L[4] * np.cos(theta)
        z = self.L[2] + self.L[3]
        c2 = (w1 * w1 + w2 * w2 - self.L[1] * self.L[1] - z * z) / (2 * z * self.L[1])
        self.Qi[1, 0] = (np.arctan2(np.sqrt(1 - c2 * c2), c2)) % (2 * np.pi)
        self.Qi[1, 1] = (np.arctan2(-np.sqrt(1 - c2 * c2), c2)) % (2 * np.pi)

        # calcul de q1
        if X - self.L[4] * np.cos(theta) == self.L[0] and Y - self.L[4] * np.sin(theta) == 0:
            print("Singularité 1 !")
            self.Qi[0, 0] = None
            self.Qi[0, 1] = None
        else:
            x1 = Y - self.L[4] * np.sin(theta)
            x2 = self.L[0] - X + self.L[4] * np.cos(theta)
            y1 = -x2
            y2 = x1
            z1 = self.L[1] * np.cos(self.Qi[1, 0]) + self.L[2] + self.L[3]
            z1_bis = self.L[1] * np.cos(self.Qi[1, 1]) + self.L[2] + self.L[3]
            z2 = -self.L[1] * np.sin(self.Qi[1, 0])
            z2_bis = -self.L[1] * np.sin(self.Qi[1, 1])

            c12 = (z2 * x1 - z1 * x2) / (x1 * y2 - x2 * y1)
            s12 = (z1 * y2 - z2 * y1) / (x1 * y2 - x2 * y1)
            c12_bis = (z2_bis * x1 - z1_bis * x2) / (x1 * y2 - x2 * y1)
            s12_bis = (z1_bis * y2 - z2_bis * y1) / (x1 * y2 - x2 * y1)

            self.Qi[0, 0] = (np.arctan2(s12, c12) - self.Qi[1, 0]) % (2.0 * np.pi)
            self.Qi[0, 1] = (np.arctan2(s12_bis, c12_bis) - self.Qi[1, 1]) % (2.0 * np.pi)

        if (X - self.L[4] * np.cos(theta) - self.L[0])**2 + (Y - self.L[4] * np.sin(theta))**2 == (self.L[1] + self.L[2] + self.L[3])**2:
            print("Singularité 2 !")

        # calcul de q4
        self.Qi[3, 0] = (theta - self.Qi[0, 0] - self.Qi[1, 0]) % (2 * np.pi)
        self.Qi[3, 1] = (theta - self.Qi[0, 1] - self.Qi[1, 1]) % (2 * np.pi)

        # calcul de q3
        self.Qi[2, 0] = Z - self.H[0] - self.H[1]
        self.Qi[2, 1] = Z - self.H[0] - self.H[1]
