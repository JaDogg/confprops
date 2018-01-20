Feature: loads()
  loads() method is capable of parsing a given string to a dictionary

  Scenario Outline: loads can parse strings to dict objects
    Given '<raw_string>' to loads
    Then loads should return '<dictionary>'

    Examples: Basic Examples
      | raw_string             | dictionary                               |
      | ""                     | {}                                       |
      | None                   | {}                                       |
      | "key=value"            | {'key': 'value'}                         |
      | "a=b"                  | {'a': 'b'}                               |
      | "a=b\nc=d"             | {'a': 'b', 'c': 'd'}                     |
      | "a=b\nc=d\r\ne=f\rg=h" | {'a': 'b', 'c': 'd', 'e': 'f', 'g': 'h'} |
      | "a=b\n\nc=d"           | {'a': 'b', 'c': 'd'}                     |
      | "a"                    | {'a': None}                              |