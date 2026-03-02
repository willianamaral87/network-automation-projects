import os
import sys
import unittest


class Test_AbstractTokens(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global test_lib
        global AbstractToken
        global LegacyToken

        from genie.abstract.token import AbstractToken, LegacyToken
        from genie.tests.abstract import test_lib

    def test_init(self):
        tk = AbstractToken(sys, legacy=LegacyToken("sys"))

        self.assertIs(tk.module, sys.modules["sys"])


class Test_AbstractTokenChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global test_lib
        global TokenChain
        global LegacyToken
        global AbstractToken

        from genie.abstract.token import TokenChain, AbstractToken, LegacyToken
        from genie.tests.abstract import test_lib

        cls.tk1 = AbstractToken(os, legacy=LegacyToken("os"))
        cls.tk2 = AbstractToken(sys, legacy=LegacyToken("sys"))
        cls.tk3 = AbstractToken(unittest, legacy=LegacyToken("unittest"))
        cls.chain = [cls.tk1, cls.tk2, cls.tk3]

    def test_init(self):
        self.assertIsNot(TokenChain()._chain, TokenChain()._chain)
        self.assertFalse(TokenChain()._chain)

        tc = TokenChain(chain=self.chain)

        self.assertIs(tc._chain, self.chain)

    def test_iterable(self):
        tc = TokenChain(chain=self.chain)

        self.assertEqual(list(tc), self.chain)

    def test_copy(self):
        tc = TokenChain(chain=self.chain)

        self.assertIsNot(tc._chain, tc.copy()._chain)

    def test_trackit(self):
        tc = TokenChain()

        import types

        dummy = types.ModuleType("dummy")
        dummy.__dict__["__abstract_token"] = self.tk1

        dummy2 = types.ModuleType("dummy2")
        dummy2.__dict__["__abstract_token"] = self.tk2

        self.assertEqual(tc._chain, [])

        with tc.track(dummy):
            with tc.track(dummy2):
                self.assertEqual(tc._chain, [self.tk1, self.tk2])

        self.assertEqual(tc._chain, [])

    def test_totuples(self):
        tc = TokenChain(chain=self.chain)

        self.assertEqual(
            tc.to_tuple(),
            (
                AbstractToken(os, legacy=LegacyToken("os")),
                AbstractToken(sys, legacy=LegacyToken("sys")),
                AbstractToken(unittest, legacy=LegacyToken("unittest")),
            ),
        )
