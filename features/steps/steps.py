# -*- coding: <encoding name> -*-
from __future__ import absolute_import

import ast
from behave import *
from hamcrest import *

from confprops.properties import *
from confprops.parser import loads


def parse_any(text):
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError) as _:
        return text.strip()


@given("'{string}' to Property")
def step_given_string_to_property_constructor(context, string):
    context.string = parse_any(string)


@given("'{string}' to loads")
def step_given_string_to_loads(context, string):
    context.parsed = loads(parse_any(string))


@when("Property is created")
def step_when_property_is_created(context):
    context.property_object = Property(context.string)


@then("it should parse input into key='{key}' and value='{value}'")
def step_then_it_should_parse_into(context, key, value):
    assert_that(context.property_object.key, equal_to(parse_any(key)))
    assert_that(context.property_object.value, equal_to(parse_any(value)))


@then("loads should return '{dictionary}'")
def step_then_it_should_parse_into(context, dictionary):
    assert_that(context.parsed, equal_to(parse_any(dictionary)))
