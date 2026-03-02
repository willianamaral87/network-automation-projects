from genie import abstract
abstract.declare_token(three='yang')

from .. import Ospf as BaseOspf

class Ospf(BaseOspf):
    pass
