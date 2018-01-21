import sys
from functools import wraps


def unescape_(string):
    if sys.version[0] == "2":
        return string.decode("string_escape")
    else:
        return string.encode("utf-8").decode("unicode_escape")


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


def merge_dictionary(destination, source):
    for key, value in source.items():
        destination[key] = value
    return destination


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
    def remove_brackets(*atoms):
        return atoms[1:-1],

    @staticmethod
    def debug(*atoms):
        print(atoms)
        return atoms