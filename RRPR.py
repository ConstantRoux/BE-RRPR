from MGD import MGD


class RRPR:
    def __init__(self, H, L, q_lim):
        self.mgd = MGD(H, L, q_lim)
