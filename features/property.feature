Feature: Property
  Property represents a single line in a properties file

  Scenario Outline: Single line property can be parsed
    Given '<raw_string>' to Property
    When Property is created
    Then Property should contain key='<key>' and value='<value>'

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

  Scenario Outline: Property value can be updated
    Given '<raw_string>' to Property
    When Property is created
    And value is set to '<new_value>'
    Then Property should contain key='<key>' and value='<new_value>'

    Examples: Values with different data types
      | raw_string | key | new_value       |
      | "a=b   "   | a   | x               |
      | key=value  | key | ""              |
      | " a  = b"  | a   | None            |
      | " a  = b"  | a   | []              |
      | " a  = b"  | a   | (1,)            |
      | " a  = b"  | a   | (1, {"a": "b"}) |