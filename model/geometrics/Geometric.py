from abc import ABC, abstractmethod


class Geometric(ABC):
    def __init__(self, law, H, L):
        self.law = law
        self.H = H
        self.L = L

    @abstractmethod
    def traj(self):
        pass

    @abstractmethod
    def is_reachable(self):
        pass

    @abstractmethod
    def plot_Q(self):
        pass

    @abstractmethod
    def plot_dQ(self):
        pass

    @abstractmethod
    def plot3D_Q(self):
        pass

    @abstractmethod
    def get_M(self):
        pass

    @abstractmethod
    def plot_M(self):
        pass

    @abstractmethod
    def plot3D_M(self):
        pass
