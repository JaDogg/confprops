from __future__ import absolute_import

import unittest

from confprops.peggy.util import memoize_
from confprops.peggy.peggy import Label


class TestPeggy(unittest.TestCase):
    def test_memoize_member_function(self):
        class SomeClass(object):
            def __init__(self):
                self._arr = []

            @memoize_
            def member(self, a_, b_):
                self._arr.append(a_)
                self._arr.append(b_)
                return [a_, b_]

        t = SomeClass()
        a = "Value a"
        b = "Value b"
        c = "Value c"
        self.assertTrue(t.member(a, b) is t.member(a, b))
        self.assertTrue(t.member(a, b) is not t.member(a, c))
        self.assertTrue(t.member(a, c) is t.member(a, c))

    def test_label_functions_add_tuples(self):
        lbl = Label("Hello", 0)
        lbl = lbl + (1, 2)
        self.assertEqual(str(lbl), "(0, 1, 2)")
        self.assertTrue(isinstance(lbl, Label))
        lbl = (-1,) + lbl
        self.assertEqual(str(lbl), "(-1, 0, 1, 2)")
        self.assertTrue(isinstance(lbl, Label))
