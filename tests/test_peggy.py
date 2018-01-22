# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

from confprops.peggy.peggy import Label
from confprops.peggy.util import memoize_, TupleUtilsMixin, escape, flatten


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

    def test_peggy_tuple_util_mixin(self):
        mixin = TupleUtilsMixin()
        self.assertEqual(mixin.kill(1, 2, 3), ())
        self.assertEqual(mixin.kill(1), ())
        self.assertEqual(mixin.kill(), ())
        self.assertEqual(mixin.join(""), ("",))
        self.assertEqual(mixin.join(), ("",))
        self.assertEqual(mixin.join("A", "B"), ("AB",))
        self.assertEqual(mixin.remove_surrounding(1, 2, 3), (2,))
        self.assertEqual(mixin.debug(1, 2, 3), (1, 2, 3))
        self.assertEqual(mixin.build_tuple(1, 2, 3), ((1, 2, 3),))
        self.assertEqual(mixin.build_tuple(1), ((1,),))
        self.assertEqual(mixin.build_tuple(), ((),))

    def test_peggy_string_escape(self):
        self.assertEqual(escape(""), "")
        self.assertEqual(escape("A"), "A")
        self.assertEqual(escape("a\nb"), "a\\nb")
        self.assertEqual(escape("a\rb"), "a\\rb")

    def test_flatten(self):
        self.assertEqual(list(flatten([1, 2, 3])), [1, 2, 3])
        self.assertEqual(list(flatten([1, (2, 3)])), [1, 2, 3])
        self.assertEqual(list(flatten([1, ([2], [3])])), [1, 2, 3])
