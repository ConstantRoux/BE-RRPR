from RRPR import RRPR
import numpy as np

if __name__ == '__main__':
    rrpr = RRPR(np.array([1, 1]), np.array([1, 1, 1, 1, 1]))
    rrpr.mgd.plot(np.array([0.24*np.pi, 0.12, -2.24, 0.8*np.pi]))
