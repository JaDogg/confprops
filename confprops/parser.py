# -*- coding: <encoding name> -*-
from __future__ import absolute_import

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
