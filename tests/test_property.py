# -*- coding: utf-8 -*-
from __future__ import absolute_import

from confprops.properties import Property
from tests.testing_utils import TestCase


class PropertyTestCase(TestCase):
    def test_setting_key_is_not_allowed(self):
        prop = Property("a=b")

        def assign_value():
            prop.key = "new_value"

        self.assertRaises(AttributeError, assign_value)
