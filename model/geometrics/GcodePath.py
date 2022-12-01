

from model.geometrics.Geometric import Geometric


class GcodePath(Geometric):
    def __init__(self, law, H, L):
        super().__init__(law, H, L)

    def traj(self):
        pass

    def is_reachable(self):
        pass

    def get_M(self):
        pass
