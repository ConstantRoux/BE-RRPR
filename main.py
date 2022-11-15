from Line import Line
from RRPR import RRPR
import numpy as np

if __name__ == '__main__':
    # rrpr = RRPR(np.array([1, 1]), np.array([1, 1, 1, 1, 1]), [[0., 2*np.pi], [0., 2*np.pi], [-5., 5.], [0., 2*np.pi]])
    # rrpr.mgd.plot()

    l = Line(0.003, np.array([1, 1]), np.array([1, 1, 1, 1, 1]))
    # l.plot_s(5, 5)
    A = np.array([[1], [1], [1]])
    B = np.array([[11], [1], [1]])
    V = 1
    # l.plot3D_M(A, B, V, theta=np.pi/2)
    l.plot_s(A, B, V)
    # l.plot_M(A, B, V)
