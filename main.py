from trajectories.Helix import Helix
from trajectories.Line import Line
from models.MDD import MDD
from models.MGD import MGD
import numpy as np


if __name__ == '__main__':
    # rrpr = RRPR(np.array([1, 1]), np.array([1, 1, 1, 1, 1]), [[0., 2*np.pi], [0., 2*np.pi], [-5., 5.], [0., 2*np.pi]])
    # rrpr.mgd.plot()

    # mgd = MGD(np.array([1, 1]), np.array([1, 1, 1, 1, 1]), [[0., 2*np.pi], [0., 2*np.pi], [-5., 5.], [0., 2*np.pi]])
    # mgd.plot3D()

    # l = Line(0.03, np.array([1, 1]), np.array([3, 3, 3, 3, 3]))
    # l.plot_s(5, 5)
    A = np.array([[0], [0], [2]])
    B = np.array([[4], [0], [3]])
    theta = 0
    V = 1

    # l.plot3D_M(A, B, V, theta=-np.pi/2)
    # l.plot_s(A, B, V)
    # l.plot_M(A, B, V)
    # l.plot_Q(A, B, V, theta=0)
    # l.plot3D_Q(A, B, V, theta=0)
    #
    # h = Helix(0.03, np.array([1, 1]), np.array([3, 3, 3, 3, 3]))
    # h.plot3D_Q(A, 8, V, 1, 0.5)

    l = Line(0.001, np.array([1, 1]), np.array([1, 2, 1, 1, 1]))
    l.plot3D_Q(A, B, V, theta=theta)
    l.plot_Q(A, B, V, theta=theta)
    l.plot_dQ(A, B, V, theta=theta)