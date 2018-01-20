# -*- coding: <encoding name> -*-
from __future__ import absolute_import


class Property(object):
    def __init__(self, string):
        self._raw_string = string
        self._key = None
        self.value = None

        self._parse_property()

    @property
    def key(self):
        return self._key

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
            self.value = line_content[1].strip()
