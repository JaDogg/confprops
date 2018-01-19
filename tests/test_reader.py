from __future__ import absolute_import

import confprops.reader as reader
from tests.testing_utils import TestCase


class ReaderTestCase(TestCase):
    """
    Test Plan
    -----------

    * Empty -> Return Empty Dict
    * None -> Return Empty Dict
    * Mixed line endings \r, \r\n, \n  | a=b\nc=d\r\ne=f\rg=h
    * Empty lines should be ignored  a=b\n\nc=d
    * Unicode Files
    * Single line file key=value
    * Two lines a=b\nc=d
    * No Equal sign in string 'a'
    """

    loads_tests = [
        ("", {}, "Empty -> Return Empty Dict"),

        (None, {}, "None -> Return Empty Dict"),

        ("key=value", {'key': 'value'}, "Single line file key=value"),

        ("a=b", {'a': 'b'}, "Single line file a=b"),

        ("a=b\nc=d", {'a': 'b', 'c': 'd'}, "Two lines a=b\\nc=d"),

        ("a=b\nc=d\r\ne=f\rg=h", {'a': 'b', 'c': 'd', 'e': 'f', 'g': 'h'},
         "Mixed line endings \\r, \\r\\n, \\n a=b\\nc=d\\r\\ne=f\\rg=h"),

        ("a=b\n\nc=d", {'a': 'b', 'c': 'd'},
         "Empty lines should be ignored  a=b\\n\\nc=d"),

        ("a", {'a': None}, "No Equal sign in string 'a'")
    ]

    def test_loads_function(self):
        for inp, expected, message in self.loads_tests:
            actual = reader.loads(inp)
            self.assert_dict_equal(expected, actual)
