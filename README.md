# Airplane Code Language

### Description

Aviation Code is a programming language that is designed to be very easy to read
and write. It is designed to control de Airbus FMGS (Flight Management and Guidance System)
and FCU (Flight Control Unit) of the Airbus family of aircraft. This language also implements the
Waypoint, Runway validation using AIRAC (Aeronautical Information Regulation And Control) data.

### Inspiration

I'm a big lover of aviation and specially of the Airbus family. I'm always
flying the Airbus A320 in the Microsoft Flight Simulator online at Vatsim Network.
As a part of my Computer Engineer degree, I have to develop a new language, so I decided
to created the _Airplane Code Language_.

### Language Description (EBNF)

```
BLOCK = { STATEMENT };

STATEMENT =  (  | ASSIGNMENT | WHILE | FUNCTION | IF | COMMENT | RETURN );

ASSIGNMENT = { IDENTIFIER, "->", TYPE, "=", EXPRESSION };

PARAMETER = { IDENTIFIER, "->", TYPE, {",", IDENTIFIER, "->", TYPE } };

TYPE = ( "int" | "float" | "string" | "waypoint" | "flight_level" );

WHILE = "while", "(", RELEXPRESSION, ")", "{", STATEMENT, "}";

FUNCTION = "function", IDENTIFIER, "(", [PARAMETER], ")", STATEMENT ;

IF = "if", "(", EXPRESSION, ")", STATEMENT ;

PRINT = "print", "(", EXPRESSION, ")";

RELEXPRESSION = EXPRESSION, ( "==" | "!=" | "<" | ">" | "<=" | ">=" ), EXPRESSION;

EXPRESSION = TERM, { ("+" | "-"), TERM };

TERM = FACTOR, { ("*" | "/"), FACTOR };

MATHFUNC = ( "sin" | "cos" | "tan" | "asin" | "acos" | "atan" | "sqrt" | "pow" | "log" | "exp" | "abs" | "ceil" | "floor" | "round" );

FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | "(", RELEXPR, ")" | IDENTIFIER, ["(", RELEXPR, {",", RELEXPR} ,")"] | ("MATHFUNC", "(", RELEXPR, {",", RELEXPR} ,")");

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" };

NUMBER = DIGIT, { DIGIT };

RETURN = "return", RELEXPRESSION;

DIGIT = ( "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" );

LETTER = ( "a" | "..." | "z" | "A" | "..." | "Z" );
```

### Codes example

```airplane
// This is a comment

// Define a variable with type
speed -> int = 250
altitude -> int = 35000
altitude -> flight_level = 350
vertical_speed -> int = 1250

// Define a waypoint
waypoint_1 -> waypoint = "BUXEV"

waypoint_2 -> waypoint = "QUALQUER COISA" // Throws an error because this waypoint is invalid

// Function
function climb_to_cruise_level(current_altitude, target_altitude, vertical_speed -> int) {
  original_target_altitude -> int = target_altitude
  while (current_altitude < target_altitude) {
    current_altitude += vertical_speed

    if (current_altitude - original_target_altitude < 900 || current_altitude - original_target_altitude > 1100) {
      print("Altitude indicator sound!")
    }
  }
}

print("Climbing to cruise level")
```
