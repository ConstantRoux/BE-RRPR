from model.gcode.GcodeInterpreter import GcodeInterpreter
from model.geometrics.ArcXY import ArcXY
from model.geometrics.GcodePath import GcodePath
from model.geometrics.Line import Line
from model.laws.SpeedTriangleLaw import SpeedTriangleLaw
from model.models.MGD import MGD
import numpy as np

if __name__ == '__main__':
    # variables
    A = np.array([[0], [0], [3]])
    B = np.array([[4], [4], [3]])
    AC = np.array([[2], [0], [3]])
    BC = np.array([[4], [-2], [3]])
    C = np.array([[4.], [0.], [3.]])
    theta = np.pi / 2
    V = 1
    Te = 0.01
    H = np.array([1, 1])
    L = np.array([2, 4, 2, 2, 1])

    # loi de commande
    law = SpeedTriangleLaw(Te)
    law.plot_s(np.linalg.norm(B - A), V)

    # vue MGD
    mgd = MGD(H, L, [[0., 2 * np.pi], [0., 2 * np.pi], [-5., 5.], [0., 2 * np.pi]])
    mgd.plot3D()

    # droite
    l = Line(law, H, L)
    t, M, dM, d2M = l.get_M(A, B, V)
    _, q, q_bis, dq, dq_bis = l.traj(A, B, V, theta)
    l.plot_M(t, M, dM, d2M)
    l.plot_theta(t, theta)
    l.plot3D_M(t, M, theta)
    l.plot_O5(t, q, dq, dM)
    l.plot_Q(t, q, q_bis)
    l.plot_dQ(t, dq, dq_bis)
    l.plot3D_Q(t, M, q, q_bis)

    # cercle
    L = np.array([2, 4, 2, 2, 2])
    c = ArcXY(law, H, L)
    t, M, dM, d2M = c.get_M(AC, BC, C, V, True)
    _, q, q_bis, dq, dq_bis = c.traj(AC, BC, C, V, True, theta)
    c.plot_M(t, M, dM, d2M)
    c.plot3D_M(t, M, theta)
    c.plot_Q(t, q, q_bis)
    c.plot_dQ(t, dq, dq_bis)
    c.plot3D_Q(t, M, q, q_bis)

    # gcode interpreter
    L = np.array([2, 16, 8, 8, 2])
    interpreter = GcodeInterpreter(law, H, L, V, 'input/upssitech.gcode')
    interpreter.read_lines()
    interpreter.get_commands()
    t, M = interpreter.get_M()
    q, q_bis = interpreter.get_Q(t, M, theta)
    g = GcodePath(law, H, L)
    g.plot3D_M(t, M, theta)
    g.plot3D_Q(t, M, q, q_bis, step=25)
