import re

LINES = re.compile("\n")


def loads(string: str):
    """
    Load a given properties string
    :param string: properties string
    :return: Dict object
    """
    data = {}

    if not string:
        return data

    lines = LINES.split(string)
    for line in lines:
        key, value = line.split("=", 1)
        data[key] = value

    return data
