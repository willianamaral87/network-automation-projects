import os
import unittest
import threading
import multiprocessing

from unittest.mock import patch


TEST_LIB_ORDER = ["one", "two", "three", "four", "five"]


class Test_AbstractPackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global test_lib, threading_test_lib
        global AbstractPackage
        global package

        from genie.abstract import package
        from genie.abstract.package import AbstractPackage
        from genie.tests.abstract import test_lib, threading_test_lib

    def setUp(self):
        # reset _seen_set to enable re-discovery
        package._seen_set = set()

    def test_simple_init(self):
        obj = AbstractPackage(test_lib, order=TEST_LIB_ORDER)

        self.assertTrue(obj.matrix)
        self.assertTrue(obj.learnt)
        self.assertEqual(obj.name, test_lib.__name__)
        self.assertIs(obj.module, test_lib)

    def test_delay_init(self):
        obj = AbstractPackage(test_lib, order=TEST_LIB_ORDER, delay=True)

        self.assertFalse(obj.matrix)
        self.assertFalse(obj.learnt)
        self.assertEqual(obj.name, test_lib.__name__)
        self.assertIs(obj.module, test_lib)

    def test_learn(self):
        obj = AbstractPackage(test_lib, order=TEST_LIB_ORDER)

        self.assertEqual(
            sorted(list(obj.matrix)),
            [
                "genie.tests.abstract.test_lib",
                "genie.tests.abstract.test_lib.complex",
                "genie.tests.abstract.test_lib.complex.module_a",
                "genie.tests.abstract.test_lib.complex.module_a.module_b",
                "genie.tests.abstract.test_lib.complex.module_a.module_b.module_c",
                "genie.tests.abstract.test_lib.complex.module_a.module_b.module_c.myfile",
                "genie.tests.abstract.test_lib.decor",
                "genie.tests.abstract.test_lib.simple",
                "genie.tests.abstract.test_lib.simple.dummy_module",
                "genie.tests.abstract.test_lib.simple.show_test",
            ],
        )

        # no tokens under this abstract path
        self.assertEqual(list(obj.matrix["genie.tests.abstract.test_lib"]), [])

        self.assertEqual(
            sorted(
                obj.matrix["genie.tests.abstract.test_lib.simple"].iter_import_paths()
            ),
            [
                "",
                "iosxe",
                "iosxe.ultra",
                "iosxe.ultra.polaris_dev",
                "nxos",
                "nxos.cli",
                "nxos.n7k",
                "nxos.n7k.cli",
                "nxos.n7k.yang",
                "nxos.yang",
            ],
        )

        self.assertEqual(
            sorted(
                obj.matrix["genie.tests.abstract.test_lib.complex"].iter_import_paths()
            ),
            ["", "token_a"],
        )

        self.assertEqual(
            sorted(
                obj.matrix.nodes[
                    "genie.tests.abstract.test_lib.complex.module_a"
                ].iter_import_paths()
            ),
            ["token_a"],
        )

        self.assertEqual(
            sorted(
                obj.matrix.nodes[
                    "genie.tests.abstract.test_lib.complex.module_a.module_b"
                ].iter_import_paths()
            ),
            ["token_a", "token_a.token_b"],
        )

        self.assertEqual(
            sorted(
                obj.matrix.nodes[
                    "genie.tests.abstract.test_lib.complex.module_a.module_b.module_c"
                ].iter_import_paths()
            ),
            ["token_a.token_b", "token_a.token_b.token_c"],
        )

        self.assertEqual(
            sorted(
                obj.matrix.nodes[
                    "genie.tests.abstract.test_lib.complex.module_a.module_b.module_c.myfile"
                ].iter_import_paths()
            ),
            ["token_a.token_b.token_c"],
        )

    def test_paths(self):
        obj = AbstractPackage(test_lib, order=TEST_LIB_ORDER)

        self.assertEqual(obj.paths, [os.path.dirname(test_lib.__file__)])

    def test_lookup(self):
        obj = AbstractPackage(test_lib, order=TEST_LIB_ORDER)

        a = obj.lookup(
            "genie.tests.abstract.test_lib.simple",
            {'one': "nxos", 'two': "n7k"},
            "Ospf",
        )

        assert a is test_lib.simple.nxos.n7k.Ospf

        b = obj.lookup(
            "genie.tests.abstract.test_lib.complex.module_a",
            {'one': "token_a"},
            "MyCls",
        )

        assert b is test_lib.complex.token_a.module_a.MyCls

        c = obj.lookup(
            "genie.tests.abstract.test_lib.complex.module_a.module_b.module_c.myfile",
            {'one': "token_a", 'two': "token_b", 'three': "token_c"},
            "MyCls",
        )

        assert (
            c
            is test_lib.complex.token_a.module_a.module_b.token_b.module_c.token_c.myfile.MyCls
        )

    def test_lookup_error(self):
        obj = AbstractPackage(test_lib, order=TEST_LIB_ORDER)

        with self.assertRaises(LookupError):
            a = obj.lookup(
                "tests.abstract.test_lib.simple", {'one': "nxos", 'two': "n7k"}, "Ospfa"
            )

        with self.assertRaises(LookupError):
            a = obj.lookup(
                "tests.abstract.test_lib.simple", {'one': "nxos", 'two': "n8k"}, "Ospf"
            )

        with self.assertRaises(LookupError):
            a = obj.lookup(
                "tests.abstract.test_lib.simle", {'one': "nxos", 'two': "n7k"}, "Ospf"
            )

    def test_registration_error(self):
        from genie.tests.abstract import bad_lib

        # ! This used to raise a ValueError. The test has been changed to reflect the new
        # ! error. However, it's unclear if this is the error this test was originally
        # ! trying to test for
        with self.assertRaises(KeyError):
            bad_lib.__dict__["__abstract_pkg"].learn()

    def test_threading(self):
        result = []

        obj = AbstractPackage(threading_test_lib, order=TEST_LIB_ORDER, delay=True)

        def func(speed):
            obj.learn()
            speed_func = obj.lookup(
                "genie.tests.abstract.threading_test_lib.api", {'one': speed}, 'speed'
                )
            result.append(speed_func())

        fast = threading.Thread(target=func, args=("fast",))
        slow = threading.Thread(target=func, args=("slow",))

        fast.start()
        slow.start()

        fast.join()
        slow.join()

        self.assertEqual(set(result), set(["fast", "slow"]))

    def test_loaded_packages(self):
        from genie.conf.base import Device

        dev = Device(name='test', os='iosxe', revision=0)

        with patch("genie.abstract.package.runtime.synchro", multiprocessing.Manager()):
            try:
                # It doesn't matter that this will fail, we just need to load the parser
                dev.parse('show version')
            except Exception as e:
                ...
        from genie.abstract import AbstractTree
        self.assertIn(
            ('parser', 'show version', '|iosxe||||||||'),
            AbstractTree.loaded_packages['features'])

    def test_root_iter_import(self):
        obj = AbstractPackage(test_lib, order=TEST_LIB_ORDER)

        self.assertIn(
            "genie.tests.abstract.test_lib.simple.dummy_module", obj.matrix
        )

        from genie.tests.abstract.test_lib.simple import dummy_module
        self.assertIs(
            obj.lookup("genie.tests.abstract.test_lib.simple.dummy_module", {}, "TestClass"),
            dummy_module.TestClass,
        )