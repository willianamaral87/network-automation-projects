from abc import ABC


class Dot1x(ABC):
    def build_config(self, devices=None, apply=True, attributes=None,
                     **kwargs):
        pass

    def build_unconfig(self, devices=None, apply=True, attributes=None,
                       **kwargs):
        pass
