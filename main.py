import matplotlib.pyplot as plt

from model.gcode.GcodeInterpreter import GcodeInterpreter
from model.geometrics.ArcXY import ArcXY
import numpy as np
from model.geometrics.Line import Line
from model.laws.SpeedTriangleLaw import SpeedTriangleLaw
from model.models.MGD import MGD

if __name__ == '__main__':
    # variables
    A = np.array([[2], [0], [3]])
    B = np.array([[4], [-2], [3]])
    C = np.array([[4.], [0.], [3.]])
    theta = np.pi / 4
    V = 1
    Te = 0.01
    H = np.array([1, 1])
    L = np.array([2, 4, 2, 2, 2])

    # loi de commande
    law = SpeedTriangleLaw(Te)
    law.plot_s(np.linalg.norm(B - A), V)

    # gcode interpreter
    interpreter = GcodeInterpreter(law, H, L, V, 'input/upssitech.gcode')
    interpreter.read_lines()
    interpreter.get_commands()
    M_t = interpreter.get_M()
    f, ax = plt.subplots()
    ax = plt.axes(projection="3d")
    ax.scatter3D(M_t[0, ::6], M_t[1, ::6], M_t[2, ::6], s=1)
    plt.show()

    # vue MGD
    # mgd = MGD(H, L, [[0., 2 * np.pi], [0., 2 * np.pi], [-5., 5.], [0., 2 * np.pi]])
    # mgd.plot3D()

    # droite
    # l = Line(law, H, L)
    # l.plot_M(A, B, V)
    # l.plot3D_M(A, B, V, theta)
    # l.plot_Q(A, B, V, theta=theta)
    # l.plot_dQ(A, B, V, theta=theta)
    # l.plot3D_Q(A, B, V, theta=theta)

    # cercle
    c = ArcXY(law, H, L)
    c.plot3D_Q(A, B, C, V, False, theta=theta)
