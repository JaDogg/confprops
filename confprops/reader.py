import re

LINES = re.compile("\n|\r\n|\r")


def loads(string):
    """
    Load a given properties string
    :param string: properties string
    :return: Dict object
    """
    data = {}

    if not string:
        return data

    lines = LINES.split(string)
    _parse_property_text_lines(data, lines)

    return data


def _parse_property_text_lines(data, lines):
    for line in lines:
        if not line:
            continue
        _parse_property(data, line)


def _parse_property(data, line):
    line_content = line.split("=", 1)

    if len(line_content) == 1:
        data[line_content[0]] = None
    else:
        key, value = line_content
        data[key] = value
