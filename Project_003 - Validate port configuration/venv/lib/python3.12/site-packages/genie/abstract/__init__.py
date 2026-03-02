__copyright__ = 'Cisco Systems, Inc. Cisco Confidential'

import re
import inspect
import logging

LEGACY_ABSTRACT_ORDER = ['os', 'platform', 'model']

DEFAULT_ABSTRACT_ORDER = ['origin', 'os', 'platform', 'model', 'submodel',
                          'pid', 'chassis_type', 'version', 'os_flavor', 'revision']

# These imports must be kept below the above variable definitions
# to avoid circular import errors
from .decorator import LookupDecorator as lookup  # noqa F401
from .magic import Lookup  # noqa F401
from .package import AbstractTree, AbstractPackage  # noqa F401
from .token import AbstractToken, LegacyToken  # noqa F401
from .version import VersionRange, Version  # noqa F401

_IMPORTMAP = {
    re.compile(r'^abstract(?=$|\.)'): 'genie.abstract'
}

__all__ = ['Lookup', 'LookupDecorator']

log = logging.getLogger(__name__)


def declare_package(*args, **kwargs):
    '''declare_package

    declare an abstraction package. This api should be called at the top of your
    abstraction package's __init__.py file.

    Argument
    --------
        order (tuple/list)(optional): Optional order of device tokens used to
                                      traverse the package when doing a lookup.

    Example
    -------
        >>> from genie import abstract
        >>> abstract.declare_package()
    '''

    # get the module object
    module = inspect.getmodule(inspect.stack()[1].frame)
    if not module:
        raise ValueError('Not a valid module.')

    order = args or kwargs.get('order')
    if len(args) == 1:
        if isinstance(args[0], (list, tuple)):
            order = args[0]
        elif isinstance(args[0], str) and args[0] == module.__name__:
            log.debug(
                f'ABSTRACT LEGACY {args} WARNING FOR {module.__name__} '
                f'from {module.__file__}')
            order = LEGACY_ABSTRACT_ORDER

    feature = kwargs.get('feature')
    origin = kwargs.get('origin')
    if origin and order is not None and 'origin' not in order:
        order = list(order)  # order is tuple by default
        order.insert(0, 'origin')

    # instanciate the abstraction package
    # (always delay to avoid circular reference due to recursive import)
    module.__abstract_pkg = AbstractPackage(
        module.__name__, order, delay=True, feature=feature)
    module.DEFAULT_TOKENS = module.__abstract_pkg.user_default_token_values
    if origin:
        module.__abstract_token = AbstractToken(module, {"origin": origin})


def declare_token(*args, **kwargs):
    '''declare_token

    declare an abstraction token. This api should be called at the top of your
    abstraction token module's __init__.py file. Only one token can be declared
    per module.

    Arguments
    ---------
        tokens and their matching value

    Example
    -------
        >>> from genie import abstract
        >>> abstract.declare_token(os='iosxe')
        >>> abstract.declare_token(version=abstract.VersionRange('1.0', '2.0'))
    '''

    # get the module object
    module = inspect.getmodule(inspect.stack()[1].frame)
    if not module:
        raise ValueError('Not a valid module.')

    matches = {}
    if len(args) == 1:
        if isinstance(args[0], str):
            token = LegacyToken(args[0])
            module.__abstract_token = AbstractToken(module, legacy=token)
            return
        elif isinstance(args[0], dict):
            matches.update(args[0])
    elif len(args) > 0:
        raise TypeError('declare_token does not take more than one positional '
                        'argument')

    # Ensure only one token defined
    if len(kwargs) > 1:
        raise ValueError('Only a single token can be declared')

    matches.update(kwargs)
    if 'revision' in matches:
        matches['revision'] = str(matches['revision'])

    # mark it as an abstraction token
    module.__abstract_token = AbstractToken(module, matches)
