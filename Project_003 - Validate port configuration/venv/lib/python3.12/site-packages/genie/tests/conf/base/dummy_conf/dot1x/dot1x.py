from genie.conf.base.base import DeviceFeature
from genie.libs.conf.dot1x.dot1x import Dot1x as Dot1xBase

class Dot1x(Dot1xBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

