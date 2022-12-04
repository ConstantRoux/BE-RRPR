import numpy as np

from model.geometrics.Line import Line
from model.laws.SpeedTriangleLaw import SpeedTriangleLaw


def plots(A, B, V, theta, Te, H, L):
    # loi de commande
    law = SpeedTriangleLaw(Te)
    law.plot_s(np.linalg.norm(B - A), V)

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


def user_interface():
    # read L
    L = np.zeros((5,))
    L[0] = np.float64(input('Veuillez saisir la valeur de L1 (en m) : '))
    L[2] = np.float64(input('Veuillez saisir la valeur de L3 (en m) : '))
    L[3] = np.float64(input('Veuillez saisir la valeur de L4 (en m) : '))
    L[1] = L[2] + L[3]
    print('L2 = L3 + L4 = ' + str(L[1]))
    L[4] = np.float64(input('Veuillez saisir la valeur de L5 : '))

    # read H
    H = np.zeros((2,))
    H[0] = np.float64(input('Veuillez saisir la valeur de H1 (en m) : '))
    H[1] = np.float64(input('Veuillez saisir la valeur de H2 (en m) : '))

    # read Te
    Te = 0.0
    Te = np.float64(input('Veuillez saisir la valeur de Te (en s) : '))

    # read V
    V = 0.0
    V = np.float64(input('Veuillez saisir la valeur de V (en m/s) : '))

    # read A
    A = np.zeros((3, 1))
    A[0, 0] = np.float64(input('Veuillez saisir la valeur de Ax (en m) : '))
    A[1, 0] = np.float64(input('Veuillez saisir la valeur de Ay (en m) : '))
    A[2, 0] = np.float64(input('Veuillez saisir la valeur de Az (en m) : '))

    # read B
    B = np.zeros((3, 1))
    B[0, 0] = np.float64(input('Veuillez saisir la valeur de Bx (en m) : '))
    B[1, 0] = np.float64(input('Veuillez saisir la valeur de By (en m) : '))
    B[2, 0] = np.float64(input('Veuillez saisir la valeur de Bz (en m) : '))

    # read theta
    theta = 0.0
    theta = np.float64(input('Veuillez saisir la valeur de theta (en rad) : '))

    if Line(None, H, L).is_reachable(A, B, theta):
        plots(A, B, V, theta, Te, H, L)
    else:
        print("Cette trajectoire n'est pas réalisable avec ces paramètres.")


if __name__ == "__main__":
    user_interface()
