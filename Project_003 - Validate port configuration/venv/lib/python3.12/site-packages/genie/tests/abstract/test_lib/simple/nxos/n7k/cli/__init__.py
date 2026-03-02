from genie import abstract
abstract.declare_token(three='cli')


from .. import Ospf as BaseOspf

class Ospf(BaseOspf):
    pass
