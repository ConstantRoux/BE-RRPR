from abc import ABC, abstractmethod


class Law(ABC):
    def __init__(self, Te):
        self.Te = Te

    @abstractmethod
    def get_s(self, d, V):
        pass

    @abstractmethod
    def _get_s_dis(self, V, d):
        pass

    @abstractmethod
    def _get_s_vit(self, V, d):
        pass

    @abstractmethod
    def _get_s_acc(self, V, d):
        pass

    @abstractmethod
    def plot_s(self, d, V):
        pass
