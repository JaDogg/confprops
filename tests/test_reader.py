from __future__ import absolute_import
from tests.testing_utils import TestCase, mock

import confprops.reader as reader


class ReaderTestCase(TestCase):
    """
    Test Plan
    -----------

    * Empty -> Return Empty Dict
    * None -> Return Empty Dict
    * Mixed line endings \r, \r\n, \n
    * Unicode Files
    * Single line file key=value
    * Two lines a=b\nc=d
    * No Equal sign in a
    """

    loads_tests = [
        ("", {}, "Empty -> Return Empty Dict"),
        (None, {}, "None -> Return Empty Dict"),
        ("key=value", {'key': 'value'}, "Single line file key=value"),
        ("a=b", {'a': 'b'}, "Single line file a=b"),
        ("a=b\nc=d", {'a': 'b', 'c': 'd'}, "Two lines a=b\\nc=d"),
    ]

    def test_loads_function(self):
        for inp, expected, message in self.loads_tests:
            actual = reader.loads(inp)
            self.assert_dict_equal(expected, actual)
