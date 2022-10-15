from RRPR import RRPR
import numpy as np

if __name__ == '__main__':
    rrpr = RRPR(np.array([1, 1]), np.array([1, 1, 1, 1, 1]), [[0., 2*np.pi], [0., 2*np.pi], [-5., 5.], [0., 2*np.pi]])
    rrpr.mgd.plot()
