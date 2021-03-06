# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re

from confprops.peggy.util import memoize_, TupleUtilsMixin

_LABEL_FUNCTION = re.compile(r"@(?P<name>[a-zA-Z_]\w*)")

# PEG Parser
# Heavily inspired by:
# http://codereview.stackexchange.com/questions/19034/peg-parser-in-python


class PegParser(TupleUtilsMixin):
    def __init__(self, rules, text):
        self._rules = rules
        self._text = text

    def parse_text(self, start="parse"):
        _, _, tokens = self.parse_rule(start)
        return tokens

    def try_parse(self, start="parse"):
        rightmost, pos, tokens = self.parse_rule(start)
        if pos is None:
            text = self._text[:rightmost] + "<--ERROR-->" + self._text[rightmost:]
            err_text = "{sep}{sep}\n{text}\n{sep}{sep}\n".format(sep="=" * 50, text=text)
            raise ValueError("Cannot parse. Error at position {0}\n{1}".format(rightmost, err_text))
        return tokens

    @memoize_
    def parse_rule(self, rule, position=0):
        rightmost = position
        for alternative in self._rules[rule]:
            current_pos, current_values = position, ()
            for token in alternative:
                current_rightmost, current_pos, current_values = \
                    self.parse_token(token, current_pos, current_values)
                rightmost = max(rightmost, current_rightmost)
                if current_pos is None:
                    break
            else:
                return rightmost, current_pos, current_values
        return rightmost, None, ()

    def parse_token(self, token, position, values):

        if isinstance(token, Matcher):
            return token(self, position, values)

        if isinstance(token, Invoker):
            return position, position, token(*values)

        # Match a sub rule
        if token in self._rules:
            rightmost, current_pos, current_values = \
                self.parse_rule(token, position)
            return rightmost, current_pos, () if current_pos is None \
                else values + current_values

        func = self.get_callable(token)
        if func:
            return position, position, func(*values)

        # Do a regex match on current text position
        return self.match_regex(position, token, values)

    def get_callable(self, token):
        if token.startswith("@"):
            func_name = token[1:]
            func = getattr(self, func_name)
            return func
        return None

    def match_regex(self, position, token, values):
        subtext = self._text[position:]
        matched = re.match(token, subtext)

        if matched:
            new_position = position + matched.end()
            return new_position, new_position, values + matched.groups()

        return position, None, ()


class PegParserWithoutWhitespace(PegParser):
    def match_regex(self, position, token, values):
        # Skip using the rule '_', WHY: ignoring whitespace makes it easier to write
        # The grammar
        subtext = self._text[position:]
        matched = re.match(self._rules["_"][0][0] + token, subtext)

        if matched:
            new_position = position + matched.end()
            return new_position, new_position, values + matched.groups()

        return position, None, ()


class Matcher(object):
    def __init__(self, *args):
        self._atoms = args

    def __call__(self, parser, position, values):
        pass


class One(Matcher):
    def __call__(self, parser, position, values):
        Matcher.__call__(self, parser, position, values)
        current_pos, current_values = position, values
        rightmost = position
        for token in self._atoms:
            current_rightmost, current_pos, current_values = \
                parser.parse_token(token, current_pos, current_values)
            rightmost = max(position, current_rightmost)
            if current_pos is None:
                break
        else:
            return rightmost, current_pos, current_values

        return position, None, ()


class OneOrMore(One):
    def __call__(self, parser, position, values):
        Matcher.__call__(self, parser, position, values)
        current_rightmost, current_pos, current_values = position, None, values
        while True:
            prev_rightmost, prev_pos, prev_values = current_rightmost, \
                                                    current_pos, current_values
            current_rightmost, current_pos, current_values = \
                One.__call__(self, parser, current_rightmost,
                             current_values)
            if current_pos is None:
                return prev_rightmost, prev_pos, prev_values


class ZeroOrMore(OneOrMore):
    def __call__(self, parser, position, values):
        Matcher.__call__(self, parser, position, values)
        current_rightmost, current_pos, current_values = \
            OneOrMore.__call__(self, parser, position, values)

        if current_pos is None:
            return position, position, values

        return current_rightmost, current_pos, current_values


class Optional(One):
    def __call__(self, parser, position, values):
        Matcher.__call__(self, parser, position, values)
        current_rightmost, current_pos, current_values = \
            One.__call__(self, parser, position, values)

        if current_pos is None:
            return position, position, values

        return current_rightmost, current_pos, current_values


class Or(Matcher):
    def __call__(self, parser, position, values):
        Matcher.__call__(self, parser, position, values)
        for matcher in self._atoms:
            current_rightmost, current_pos, current_values \
                = matcher(parser, position, values)

            if current_pos is not None:
                return current_rightmost, current_pos, current_values

        return position, None, ()


class Not(One):
    def __call__(self, parser, position, values):
        Matcher.__call__(self, parser, position, values)
        current_rightmost, current_pos, current_values \
            = One.__call__(self, parser, position, values)

        return current_rightmost, current_rightmost if current_pos is None \
            else None, values if current_pos is None else ()


class Nothing(Not):
    def __init__(self):
        Not.__init__(self, r".")


class Invoker(object):
    def __call__(self, *values):
        pass


class Label(tuple):
    def __new__(cls, _, *args):
        return super(Label, cls).__new__(cls, tuple(args))

    def __init__(self, label_string, *_):
        super(Label, self).__init__()
        self.label = label_string

    def __add__(self, other):
        new_tuple = tuple.__add__(self, other)
        return Label(self.label, *new_tuple)

    def __radd__(self, other):
        new_tuple = tuple.__add__(other, self)
        return Label(self.label, *new_tuple)


class _LabelInvoker(Invoker):
    def __init__(self, label_str):
        self.label = label_str

    def __call__(self, *values):
        Invoker.__call__(self, *values)
        return Label(self.label, *values),


def label(label_str):
    return _LabelInvoker(label_str)
