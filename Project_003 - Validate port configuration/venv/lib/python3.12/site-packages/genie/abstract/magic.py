from __future__ import annotations

import inspect
import logging
import collections
import warnings
import importlib
from collections.abc import Mapping, MutableSequence
from collections import OrderedDict
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from genie.abstract.package import AbstractPackage
    from genie.conf.base import Device

from pyats.utils.dicts import recursive_update
from . import LEGACY_ABSTRACT_ORDER

logger = logging.getLogger(__name__)


def recursive_update_extend(a, b):
    '''recursive_update

    Recursively updates on nested dictionary a with dictionary b, but creates
    or extends a list if there is a conflict instead of overwriting. The list
    will have elements of b before the elements of a, and any duplicate values
    removed.
    '''
    if isinstance(a, Mapping) and isinstance(b, Mapping):
        for k, v in b.items():
            if isinstance(v, Mapping):
                a[k] = recursive_update_extend(a.get(k, type(v)()), v)
            elif isinstance(v, MutableSequence):
                v = v.copy()
                if k in a:
                    if isinstance(a[k], MutableSequence):
                        v.extend(a[k])
                    else:
                        v.append(a[k])
                # remove duplicates
                a[k] = list(OrderedDict.fromkeys(v))
            else:
                v = [v]
                if k in a:
                    if isinstance(a[k], MutableSequence):
                        v.extend(a[k])
                    else:
                        v.append(a[k])
                # remove duplicates
                a[k] = list(OrderedDict.fromkeys(v))
    else:
        return b
    return a


def ensure_list(a):
    if isinstance(a, MutableSequence):
        return a
    return [a]


def get_caller_stack_pkgs(stacklvl = 1):
    '''get_caller_stack_pkgs

    helper function, returns a dictionary of names/abstraction module based on
    the caller's stack frame.

    Example
    -------
        >>> import genie
        >>> import mylib as local_lib
        >>> get_caller_stack_pkgs()
        {'genie': <module genie...>,
         'local_lib': <module mylib...>,}
    '''

    # get the caller FrameInfo
    # (frame, filename, lineno, function, code_context, index)
    frame = inspect.stack()[stacklvl][0]

    # variable scope = locals + globals
    f_scope = collections.ChainMap(frame.f_locals, frame.f_globals)

    # look for imported abstract packages
    return {n: o for n, o in f_scope.items() if hasattr(o, '__abstract_pkg')}



class LookupWrapper:
    '''LookupWrapper

    Contains multiple Lookup object since each one now only contains a single
    package, to differentiate between package specific tokens.

    Arguments
    ---------
        packages (dict): dictionary of package names and their module objects.
    '''

    def __init__(self, *tokens, device=None, packages=None):
        self.tokens = tokens
        self.device = device
        self.packages = packages
        self.lookups = {}

    def __getattr__(self, attr):
        # If we get __abstract_pkg, then we have a LookupWrapper looking at us
        # We don't want that so we raise an AttributeError
        if attr == '__abstract_pkg':
            raise AttributeError

        # If the attribute is in the lookups, return it and be happy
        if attr in self.lookups:
            return self.lookups[attr]

        # If we have the attribute as a package then lets do a lookup on it
        elif attr in self.packages:
            self.lookups[attr] = Lookup(*self.tokens,
                                        device=self.device,
                                        package=self.packages[attr])
            return self.lookups[attr]

        # Otherwise, we're searching for something that doesn't exist or isn't
        # properly defined. Let's raise an error
        else:
            raise KeyError('No abstract package named "{}" in this Lookup, '
                           'found: {}'.format(attr, list(self.packages.keys())))


    def __dir__(self):
        '''__dir__

        built-in, returns the packages available for calling
        '''
        # Check if we have packages first, if not
        # then just give whatever we can.
        if hasattr(self, "packages"):
            return super().__dir__() + list(self.packages.keys())
        return super().__dir__()



class Lookup(object):
    '''Lookup

    When instanciated with a set of "token requirements", the lookup object
    allows users to dynamically reference libraries (abstraction packages).

    The concept is akin to dynamic imports. As opposed to

        >>> from genie.nxos import Ospf
        >>> from local_lib.nxos.titanium import Blah

    lookup allows the user to simply do:

        >>> import genie
        >>> import local_lib
        >>> l = Lookup('nxos', 'titanium')
        >>> l.Ospf()
        >>> l.Blah()

    where the actual import based on the given tokens will be sorted out for
    the user dynamically.

    Arguments
    ---------
        tokens (dict): token keys and values for this lookup
        packages (dict): dictionary of package names and their module object.
                         if not provided, the caller's stack is looked up for
                         all available abstraction packages.

    Examples
    --------
        >>> import my_abstracted_lib as lib
        >>> l = Lookup('nxos', 'titanium')
        >>> l.lib.module_a.module_b.MyClass()
    '''

    def __new__(cls, *args, **kwargs):
        # Allow the creator of the Lookup object to specify the stacklvl they
        # want to look into. Important for allowing LookupWrappers to function
        # correctly as they create an extra level to look into
        stacklvl = kwargs.pop('stacklvl', 2)
        if 'packages' in kwargs:
            # packages defined, wrap multiple Lookups
            return LookupWrapper(*args, **kwargs)
        elif 'package' not in kwargs:
            # no package or packages defined, get all available
            kwargs['packages'] = get_caller_stack_pkgs(stacklvl = stacklvl)
            return LookupWrapper(*args, **kwargs)
        # Normal loading with a single package
        return super().__new__(cls)

    def __init__(self,
                 *tokens,
                 package,
                 device=None):


        # extract abstract package object from given python package, and learn
        # the abstract tokens
        self.package = getattr(package, '__abstract_pkg')
        self.package.learn()
        self.tokens = {}

        # tokens for lookup
        if device:
            self.tokens = self.tokens_from_device(device,
                                                  self.package.order,
                                                  self.package.name)
        elif tokens:
            if len(tokens) == 0:
                raise TypeError('No device and no tokens given to Lookup. '
                                'At least one is required in order to peform '
                                'an abstract lookup.')
            elif len(tokens) == 1:
                if isinstance(tokens[0], (list, tuple, dict)):
                    # extract first argument
                    tokens = tokens[0]

            if isinstance(tokens, (list, tuple)):
                # convert given list/tuple into a dict using the legacy abstract
                # token order
                if self.package.order:
                    self.tokens = dict(zip(self.package.order, tokens))
                else:
                    self.tokens = dict(zip(LEGACY_ABSTRACT_ORDER, tokens))



    def __getattr__(self, attr):
        '''__getattr__

        black magic. Wraps abstraction packages with AbstractionModule - a
        dynamic search mechanism that tracks the user attribute getter path
        and returns the most complete/corresponding object.
        '''
        # AbstractedModule will chain the objects together
        # (each getattr at this level gets a new instance)
        return getattr(AbstractedModule(package=self.package,
                                        tokens=self.tokens),
                       attr)

    @classmethod
    def from_device(cls,
                    device,
                    packages=None,
                    **kwargs):
        '''from_device

        creates an abstraction Lookup object by getting the token arguments from
        a pyATS device objects.

        This api expects the device object to have an "abstraction" dictionary
        under 'custom' attribute. Eg:

        Example
        -------
            devices:
                my-device:
                    os: nxos
                    platform: n7k
                    custom:
                        abstraction:
                            platform: n9k # additional override

        Arguments
        ---------
            device (Device): pyATS topology device object
            packages (dict): dictionary of package names and their module object.
                             if not provided, the caller's stack is looked up
                             for all available abstraction packages.
            **kwargs (kwargs): any other token values to be used for lookup.
        '''

        if kwargs.pop('default_tokens', None):
            # Only warn once, not for every Lookup created
            if not getattr(cls, '_default_tokens_warn', False):
                warnings.warn('default_tokens is a deprecated argument for '
                              'Lookup.from_device(), please omit this argument '
                              'from the Lookup creation.')
                cls._default_tokens_warn = True

        # create Lookup object
        if packages:
            # LookupWrapper for multiple packages
            return cls(device=device, packages=packages)
        elif 'package' in kwargs:
            # Single package Lookup
            return cls(device=device, package=kwargs['package'])
        else:
            # The LookupWrapper will get packages from the caller stack
            return cls(device=device, stacklvl=3)

    @classmethod
    def tokens_from_device(
        cls, device: 'Device',
        token_attrs: list[str], package:str = None) -> dict[str, str]:
        """Gather tokens from device

        Parameters
        ----------
        device : Device
            Device object to gather tokens from
        token_attrs : list[str]
            List of token attributes to gather from the device
        package : str, optional
            Package to attempt to import and update tokens from, by default None

        Returns
        -------
        dict[str, str]
            Dict of tokens gathered from the device
        """
        # tokens from the testbed to apply to all devices
        tb_abstraction_info = {}
        if getattr(device, 'testbed', None):
            recursive_update_extend(
                tb_abstraction_info, getattr(device.testbed, 'abstraction', {}))
            if package:
                # update with package specific abstraction tokens defined in the testbed
                recursive_update_extend(
                    tb_abstraction_info, tb_abstraction_info.get(package, {}))

        # device specific tokens in testbed
        abstraction_info = {}
        recursive_update_extend(
            abstraction_info, getattr(device, 'abstraction', {}))

        # Since we might not have `custom` anymore, best to check if we have it
        if 'abstraction' in getattr(device, 'custom', {}):
            custom_abstract = device.custom.get('abstraction', {}).copy()
            custom_abstract.pop('order', None)
            if len(custom_abstract) > 0:
                device_name = getattr(device, 'name', device)
                warnings.warn('Abstract values defined under "custom" for '
                              'device {}'.format(device_name))
                recursive_update_extend(abstraction_info, custom_abstract)

        if package:
            # update with package specific abstraction tokens defined in the testbed
            recursive_update_extend(
                abstraction_info, abstraction_info.get(package, {}))

        # build tokens dict
        tokens = {}
        for attr in token_attrs:
            vals = []
            if attr in abstraction_info:
                vals.extend(ensure_list(abstraction_info[attr]))
            if getattr(device, attr, None) is not None:
                vals.extend(ensure_list(getattr(device, attr)))
            if attr in tb_abstraction_info:
                vals.extend(ensure_list(tb_abstraction_info[attr]))

            if vals:
                # remove duplicates, and assign list of token values to token
                # attr
                tokens[attr] = list(OrderedDict.fromkeys(vals))

        # TODO: Verify if this can be removed (pretty sure it can't be)
        # assign default values from abstract package
        if package:
            pkg = importlib.import_module(package)
            abs_pkg = getattr(pkg, '__abstract_pkg', None)
            if abs_pkg:
                for attr in abs_pkg.user_default_token_values:
                    if not attr in tokens:
                        tokens[attr] = abs_pkg.user_default_token_values[attr]
                for attr in abs_pkg.default_token_values:
                    if not attr in tokens:
                        tokens[attr] = abs_pkg.default_token_values[attr]

        return tokens


class AbstractedModule(object):
    '''AbstractedModule

    Internal class, part-two of lookup mechanism. This class is instanciated
    each time a successful package reference (through Lookup class instances)
    is done, and tracks internally user's attribute chain, used as part of the
    lookup process.

    '''

    def __init__(self, package: AbstractPackage, tokens: Dict[str, str]):
        """Create an AbstractedModule object

        Parameters
        ----------
        package (AbstractPackage):
            the abstract package to reference
        tokens (Dict[str, str]):
            sequence of tokens to perform lookup.
        """
        self._package = package
        self._tokens = tokens

        # relative path taken for this lookup: Lookup().lib.x.y.z
        # (always starts with the package name)
        self._path = package.name

    def __getattr__(self, name):
        '''__getattr__

        getattr() magic. This is where the user's attribute lookup chain is
        stored & reflected. Eg, when user look sup a.b.c.d, the referring module
        is a.b.c and the object to lookup is d.

        Logic:
            - build path around user's getattr() calls.
            - check whether the given path is a known on in this abstraction
              package
            - if it is, keep building the path.
            - else, we've hit a dead end, try to collect the object from the
              last-known module.
            - if found, return it
            - else - search unknown, raise exception.
        '''
        # build the new path from name
        path = f'{self._path}.{name}'

        # is this path still part of this package?
        if path in self._package:
            # still within the realm of this package
            self._path = path
            return self

        # no longer within a known path
        # start abstracting for a result
        return self._package.lookup(self._path, self._tokens, name)


    def __repr__(self):
        return "<%s '%s' from '%s'>" % (self.__class__.__name__,
                                            self._path,
                                            self.__file__)

    def __dir__(self):
        # include the current known path's dir() result
        return super().__dir__() + self.__getattr__('__dir__')()

    @property
    def tokens(self):
        return self._tokens