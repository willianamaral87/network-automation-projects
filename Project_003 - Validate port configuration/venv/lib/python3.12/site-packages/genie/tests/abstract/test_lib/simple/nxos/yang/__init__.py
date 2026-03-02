from genie import abstract
abstract.declare_token(two='yang')

from .. import Ospf as BaseOspf

class Ospf(BaseOspf):
    pass
