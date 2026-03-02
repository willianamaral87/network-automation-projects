"""
Module:
    kleenex

Authors:
    Myles Dear(mdear), CSG Test - Ottawa
    Siming Yuan (siyuan), CSG Test - Ottawa

Description:
    This module provides a framework that allows users to:

    - plug in own orchestrators that bring up dynamic device
      topologies on a variety of different backends.

    - plug in their own cleaners that prepare a physical device for testing.
"""

# metadata
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2017-2019, Cisco Systems Inc.'

from pyats.clean.bases import BaseCleaner
from pyats.clean.loader import KleenexFileLoader
from pyats.clean.schema import allowed_virtual_device_types
from pyats.clean.exceptions import YamlConfigError

from .manager import request_bringup_worker_server_shutdown, BringUp
from .bases import BringUpBase, BringUpWorkerBase
from .exceptions import TopologyDidntComeUpInTime
from .signals import SignalError
