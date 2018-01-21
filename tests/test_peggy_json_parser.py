from __future__ import print_function

import json
import sys
import unittest

from confprops.peggy.peggy import PegParserWithoutWhitespace, Not, ZeroOrMore


# References : https://github.com/antlr/grammars-v4/blob/master/json/JSON.g4


class JsonParser(PegParserWithoutWhitespace):
    def __init__(self, text):
        rules = {
            "parse": [
                ["object", Not(r".")],
                ["array", Not(r".")]
            ],
            "object": [
                [r"[{]", "pair", "_",
                 ZeroOrMore(r"[,]", "pair"), r"[}]", "@dict_"],
                [r"[{]", r"[}]", "@empty_dict"]
            ],
            "array": [
                [r"[\[]", "value", "_",
                 ZeroOrMore(r"[,]", "value"), r"[\]]", "@list_"],
                [r"[\[]", r"[\]]", "@empty_list"]
            ],
            "pair": [
                ["string", r"[:]", "value", "@hug"]
            ],
            "value": [
                ["string"],
                ["number"],
                ["object"],
                ["array"],
                [r"(true)", "@special"],
                [r"(false)", "@special"],
                [r"(null)", "@special"]
            ],
            "string": [
                [r'"((?:\\.|[^"\\])*)"', "@unescape"]
            ],
            "number": [
                [r"(\d+)", "@to_int"]
            ],
            "_": [
                [r"(?:\s|\r|\n)*"]
            ]
        }
        PegParserWithoutWhitespace.__init__(self, rules, text)

    def parse(self):
        return self.try_parse()

    @staticmethod
    def dict_(*args):
        return dict(args),

    @staticmethod
    def empty_dict(*_):
        return {},

    @staticmethod
    def list_(*args):
        return list(args),

    @staticmethod
    def empty_list(*_):
        return [],

    @staticmethod
    def special(value):
        if value == "true":
            return True,
        elif value == "false":
            return False,
        elif value == "null":
            return None,

        assert False, "Invalid Special {val}".format(val=value)


class TestJsonParser(unittest.TestCase):
    def test_json_basic(self):
        objects = [
            {"he\\l\"lo": "world", "hi": {"alternative": "reality"}},
            {"null_checker": None, "hi": {"false": False, "true": True}},
            [["A"], "2", [[[]], {}]],
            {"Hello": None, "World": [[[1]]]},
            [1, 2, 3]
        ]
        for obj in objects:
            s = json.dumps(obj)
            parser = JsonParser(s)
            parsed_object, = parser.parse()
            print("Original::\n{obj}\nParsed::\n{parsed}\n\n".format(
                obj=s, parsed=json.dumps(parsed_object)))
            self.assertEqual(obj, parsed_object)

    def test_negative_tests(self):
        parser = JsonParser('{"a": xzv}')
        self.assertRaises(ValueError, parser.parse)
