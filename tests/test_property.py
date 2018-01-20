# -*- coding: <encoding name> -*-
from __future__ import absolute_import

from confprops.properties import Property
from tests.testing_utils import TestCase


class PropertyTestCase(TestCase):
    def test_cannot_set_key(self):
        prop = Property("a=b")

        def assign_value():
            prop.key = "new_value"

        self.assertRaises(AttributeError, assign_value)
