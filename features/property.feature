Feature: Property
  Property represents a single line in a properties file

  Scenario Outline: Single line property can be extracted
    Given '<raw_string>' to Property
    When Property is created
    Then it should parse input into key='<key>' and value='<value>'

    Examples: Basic Examples
      | raw_string | key | value |
      | "a=b   "   | a   | b     |
      | key=value  | key | value |
      | " a  = b"  | a   | b     |

    Examples: Negative Examples
      | raw_string | key  | value |
      | ""         | None | None  |
      | "    "     | None | None  |
      | "a"        | a    | None  |
      | "a="       | a    | ""    |
      | " a "      | a    | None  |
      | " \t a \t" | a    | None  |

    Examples: Weird Cases
      | raw_string | key   | value |
      | "1=Hello"  | "1"   | Hello |
      | 1          | "1"   | None  |
      | [1]        | "[1]" | None  |