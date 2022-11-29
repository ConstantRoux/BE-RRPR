from model.commands import SpeedTriangleLaw
from model.geometrics.ArcXY import ArcXY
import numpy as np


if __name__ == '__main__':
    # variables
    A = np.array([[2], [0], [3]])
    B = np.array([[4], [-2], [3]])
    C = np.array([[4], [0], [3]])
    theta = np.pi / 4
    V = 1
    Te = 0.01
    H = np.array([1, 1])
    L = np.array([2, 4, 2, 2, 2])

    # vue MGD
    mgd = MGD(H, L, [[0., 2*np.pi], [0., 2*np.pi], [-5., 5.], [0., 2*np.pi]])
    mgd.plot3D()

    # loi de commande
    law = SpeedTriangleLaw(Te)
    law.plot_s(np.linalg.norm(B - A), V)

    # droite
    l = Line(law, H, L)
    l.plot_M(A, B, V)
    l.plot3D_M(A, B, V, theta)
    l.plot_Q(A, B, V, theta=theta)
    l.plot_dQ(A, B, V, theta=theta)
    l.plot3D_Q(A, B, V, theta=theta)

    # cercle
    c = ArcXY(law, H, L)
    c.plot3D_Q(A, B, C, V, False, theta=theta)
