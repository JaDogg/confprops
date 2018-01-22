# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

from confprops.peggy.peggy import *
from tests.peggy_display import *


class InfixTree(PegParser):
    def __init__(self, text):
        rules = {
            "parse": [
                ["_", "exp0", Nothing(), label("parse")]
            ],
            "exp0": [
                ["exp1", ZeroOrMore(
                    Or(
                        One(r"([+])", "_", "exp1", label("exp0_add")),
                        One(r"([-])", "_", "exp1", label("exp0_sub"))
                    )
                ), label("exp0")]
            ],
            "exp1": [
                ["exp2", ZeroOrMore(
                    Or(
                        One(r"([*])", "_", "exp2", label("exp0_mul")),
                        One(r"([/])", "_", "exp2", label("exp0_div"))
                    )
                ), label("exp1")]
            ],
            "exp2": [
                ["exp3", Optional(r"([\^])", "_", "exp2", label("exp0_pow")),
                 label("exp2")]
            ],
            "exp3": [
                [r"[\(]", "_", "exp0", r"[\)]", "_", label("exp3_paren")],
                [r"([\-])", "_", "exp1", label("exp3_neg")],
                [r"(\d+)", "_", label("exp3_int")]
            ],
            "_": [
                [r"\s*"]
            ]
        }
        PegParser.__init__(self, rules, text)

    def parse(self):
        return self.parse_rule("parse")


class TestCalculator(unittest.TestCase):
    def test_calculator(self):
        t = r"""2*5+1/2*2+3"""
        p = InfixTree(t)
        _, _, t_ = p.parse()
        display_labeled(t_)
        self.assertTrue(bool(t))

    def test_invalid_input(self):
        t = r"""ASDF"""
        p = InfixTree(t)
        _, _, t_ = p.parse()
        display_labeled(t)
