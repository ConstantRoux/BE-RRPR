from trajectories.Helix import Helix
from trajectories.Line import Line
import numpy as np

if __name__ == '__main__':
    # rrpr = RRPR(np.array([1, 1]), np.array([1, 1, 1, 1, 1]), [[0., 2*np.pi], [0., 2*np.pi], [-5., 5.], [0., 2*np.pi]])
    # rrpr.mgd.plot()

    l = Line(0.03, np.array([1, 1]), np.array([3, 3, 3, 3, 3]))
    # l.plot_s(5, 5)
    A = np.array([[3], [3], [3]])
    B = np.array([[7], [3], [3]])
    V = 1

    # l.plot3D_M(A, B, V, theta=-np.pi/2)
    # l.plot_s(A, B, V)
    # l.plot_M(A, B, V)
    l.plot_Q(A, B, V, theta=0)
    l.plot3D_Q(A, B, V, theta=0)

    h = Helix(0.03, np.array([1, 1]), np.array([3, 3, 3, 3, 3]))
    h.plot3D_Q(A, 8, V, 1, 0.5)
