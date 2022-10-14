from RRPR import RRPR
import numpy as np

if __name__ == '__main__':
    rrpr = RRPR(np.array([1, 1]), np.array([1, 1, 1, 1, 1]))
    print(rrpr.mgd.get_T05(np.array([np.pi / 2, 0, 3, 0])))
