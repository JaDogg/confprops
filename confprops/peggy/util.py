# -*- coding: utf-8 -*-
from __future__ import absolute_import

import ast
from functools import wraps


def unescape_(string):
    return ast.literal_eval('"""' + string + '"""')


def escape(string):
    return repr(str(string))[1:-1]


def memoize_(func):
    data_store = dict()

    @wraps(func)
    def wrapper_function(*args):
        if args not in data_store:
            data_store[args] = func(*args)
        return data_store[args]

    return wrapper_function


def flatten(items):
    for item in items:
        if isinstance(item, (tuple, list)):
            for item_ in flatten(item):
                yield item_
        else:
            yield item


class TupleUtilsMixin(object):
    @staticmethod
    def kill(*_):
        return ()

    @staticmethod
    def join(*atoms):
        return "".join(atoms),

    @staticmethod
    def to_int(value):
        return int(value),

    @staticmethod
    def unescape(value):
        return unescape_(value),

    @staticmethod
    def build_tuple(*atoms):
        return atoms,

    @staticmethod
    def hug(*atoms):
        return atoms,

    @staticmethod
    def remove_surrounding(*atoms):
        return atoms[1:-1]

    @staticmethod
    def debug(*atoms):
        print(atoms)
        return atoms
