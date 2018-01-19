import sys
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

class TestCase(unittest.TestCase):
    def assert_dict_equal(self, d1, d2, msg=None):
        # Python version that is larger than 2.6
        if not (sys.version_info[0] == 2 and sys.version_info[1] <= 6):
            self.assertDictEqual(d1, d2, msg)
            return

        # Python 2.6
        if not isinstance(d1, dict):
            raise AssertionError("d1 is not a dict")
        if not isinstance(d2, dict):
            raise AssertionError("d2 is not a dict")

        if d1 != d2:
            raise AssertionError("Dictionaries are not equal:" + msg)
