from trajectories.Line import Line
import numpy as np

if __name__ == '__main__':
    # rrpr = RRPR(np.array([1, 1]), np.array([1, 1, 1, 1, 1]), [[0., 2*np.pi], [0., 2*np.pi], [-5., 5.], [0., 2*np.pi]])
    # rrpr.mgd.plot()

    l = Line(0.003, np.array([1, 1]), np.array([1, 1, 1, 1, 1]))
    # l.plot_s(5, 5)
    A = np.array([[1], [2], [0]])
    B = np.array([[1], [1], [0]])
    V = 1

    l.plot3D_M(A, B, V, theta=-np.pi/2)
    l.plot_s(A, B, V)
    l.plot_M(A, B, V)
    l.plot_Q(A, B, V)
