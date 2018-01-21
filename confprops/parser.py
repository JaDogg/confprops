# -*- coding: utf-8 -*-
from __future__ import absolute_import

import ast
import re

from confprops.properties import Property

LINES = re.compile("\n|\r\n|\r")


def loads(string):
    """
    Load a given properties string
    :param string: properties string
    :return: Dict object
    """
    data = {}

    if not string:
        return data

    lines = LINES.split(string)
    _parse_property_text_lines(data, lines)

    return data


def _parse_property_text_lines(data, lines):
    for line in lines:
        if not line:
            continue
        _parse_property(data, line)


def _parse_property(data, line):
    prop = Property(line)
    data[prop.key] = prop.value


def parse_any(text):
    """
    Parse a given string to a Python object or return a stripped string
    :param text: Text containing Python object or some text data
    :return: Python object parsed from ast.literal_eval or
    """
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError) as _:
        return text.strip()
