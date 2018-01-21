# -*- coding: utf-8 -*-
from __future__ import absolute_import


class Property(object):
    def __init__(self, string):
        self._raw_string = string
        self._key = None
        self._value = None
        self._dirty = False

        self._parse_property()

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._dirty = True

    def _parse_property(self):
        if not self._raw_string:
            return

        string = str(self._raw_string).strip()

        if not string:
            return

        self._extract_key_value(string)

    def _extract_key_value(self, string):
        line_content = string.split("=", 1)

        self._key = line_content[0].strip()

        if len(line_content) == 2:
            self._value = line_content[1].strip()
