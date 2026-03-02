import unittest
import sys, os, copy
import threading

TEST_LIB_ORDER = ["one", "two", "three", "four", "five"]

# TODO: Majory of these tests were made obsolete. New tests will need to be written

class Test_AbstractModule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global test_lib
        global AbstractedModule

        from genie.abstract.magic import AbstractedModule
        from genie.abstract.package import AbstractPackage
        from genie.tests.abstract import test_lib

        cls.pkg = AbstractPackage(test_lib, order=TEST_LIB_ORDER)

    def test_getattr_simple(self):
        am = AbstractedModule(self.pkg, {'one': 'nxos', 'two': 'n7k'})
        self.assertIs(am.simple.Ospf, test_lib.simple.nxos.n7k.Ospf)

        am = AbstractedModule(self.pkg, {'one': 'nxos', 'two': 'n8k'})
        self.assertIs(am.simple.Ospf, test_lib.simple.nxos.Ospf)


    def test_getattr_complex(self):

        am = AbstractedModule(self.pkg,
                              {'one': 'token_a', 'two': 'token_b', 'three': 'token_c'})

        self.assertIs(am.complex.module_a.module_b.MyCls,
                      test_lib.complex.token_a.module_a.module_b.token_b.MyCls)

        am = AbstractedModule(self.pkg,
                              {'one': 'token_a', 'two': 'token_b', 'three': 'token_c'})
        self.assertIs(am.complex.module_a.module_b.module_c.myfile.MyCls,
                      test_lib.complex.token_a.module_a.module_b.token_b.\
                      module_c.token_c.myfile.MyCls)

    def test_get_attr_error(self):


        am = AbstractedModule(self.pkg,
                              {'one': 'token_a', 'two': 'token_b', 'three': 'token_c'})

        with self.assertRaises(LookupError):
            am.complex.b


class Test_Lookup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global test_lib
        global Lookup

        from genie.abstract.magic import Lookup
        from genie.tests.abstract import test_lib


    def test_lookup_init(self):
        l = Lookup()

        self.assertIs(type(l.tokens), tuple)
        self.assertEqual(l.packages, {'test_lib':
                                    test_lib.__dict__['__abstract_pkg'].module})

        self.assertTrue(hasattr(l, 'test_lib'))

    def test_lookup_device(self):
        class Device():
            one = 1
            two = 2
            name = "TestDevice"
            custom = {
                'abstraction': {
                    'order': ['one', 'two'],
                    'one': 100,
                    'two': 200,
                }
            }
        l = Lookup.from_device(Device())
        self.assertEqual(l.test_lib.tokens,
                         {'one': [100, 1], 'two': [200, 2], 'revision': []})

    def test_lookup_device_only_abstraction(self):
        class Device():
            one = 999
            two = 9999

        l = Lookup.from_device(Device())
        self.assertEqual(l.test_lib.tokens,
                         {'one': [999], 'two': [9999], 'revision': []})

    def test_lookup_device_only_abstraction_optionals(self):
        class Device():
            one = 999
            three = 99999

        l = Lookup.from_device(Device())
        self.assertEqual(l.test_lib.tokens,
                         {'one': [999], 'three': [99999], 'revision': []})

    def test_lookup_device_default(self):
        class Device():
            custom = {
                'abstraction': {
                    'order': ['one', 'two'],
                    'one': 100,
                    'two': 200,
                }
            }

        l = Lookup.from_device(Device())
        self.assertEqual(l.test_lib.tokens,
                         {'one': [100], 'revision': [], 'two': [200]})

    def test_lookup_device_fallback(self):
        class Device():
            one = 1
            two = 2
            custom = {
                'abstraction': {
                    'order': ['one', 'two'],
                }
            }

        l = Lookup.from_device(Device())
        self.assertEqual(l.test_lib.tokens,
                         {'one': [1], 'revision': [], 'two': [2]})

    def test_lookup_device_pkgs(self):
        class Device():
            one = 1
            two = 2
            custom = {
                'abstraction': {
                    'order': ['one', 'two'],
                }
            }

        l = Lookup.from_device(Device(),
                               packages = {'test_lib':test_lib,
                                           'abc': test_lib})

        self.assertTrue(hasattr(l, 'test_lib'))
        self.assertTrue(hasattr(l, 'abc'))

    def test_lookup_stack(self):
        class Device():
            one = 1
            two = 2
            custom = {
                'abstraction': {
                    'order': ['one', 'two'],
                }
            }

        one = test_lib
        two = test_lib
        three = test_lib
        l = Lookup.from_device(Device())

        self.assertTrue(hasattr(l, 'test_lib'))
        self.assertTrue(hasattr(l, 'one'))
        self.assertTrue(hasattr(l, 'two'))
        self.assertTrue(hasattr(l, 'three'))

    def test_lookup_pass_in_pkgs(self):
        l = Lookup(packages = {'test_lib': test_lib,
                               'abc': test_lib})

        self.assertTrue(hasattr(l, 'test_lib'))
        self.assertTrue(hasattr(l, 'abc'))

    def test_caller_stack_collection(self):

        one = test_lib
        two = test_lib
        three = test_lib
        l = Lookup()

        self.assertTrue(hasattr(l, 'test_lib'))
        self.assertTrue(hasattr(l, 'one'))
        self.assertTrue(hasattr(l, 'two'))
        self.assertTrue(hasattr(l, 'three'))

    def test_dir(self):

        one = test_lib
        two = test_lib
        three = test_lib
        l = Lookup()

        self.assertIn('one', dir(l))
        self.assertIn('two', dir(l))
        self.assertIn('three', dir(l))
        self.assertIn('test_lib', dir(l))


class Test_Threading_Errors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global threading_test_lib
        global Lookup

        from genie.abstract import Lookup
        from genie.tests.abstract import threading_test_lib

    def test_threading(self):

        class DeviceA():
            speed = 'slow'

        class DeviceB():
            speed = 'fast'

        result = []

        def func(device):
            l = Lookup.from_device(device,
                                     default_tokens = ['speed'],
                                     packages = {'test': threading_test_lib})
            result.append(l.test.api.speed())

        fast = threading.Thread(target=func, args = (DeviceA(),))
        slow = threading.Thread(target=func, args = (DeviceB(),))

        fast.start()
        slow.start()

        fast.join()
        slow.join()

        self.assertEqual(set(result), set(['fast', 'slow']))