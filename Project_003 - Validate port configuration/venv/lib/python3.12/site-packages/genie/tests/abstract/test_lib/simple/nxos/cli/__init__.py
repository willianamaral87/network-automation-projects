from genie import abstract
abstract.declare_token(two='cli')


from .. import Ospf as BaseOspf

class Ospf(BaseOspf):
    pass
