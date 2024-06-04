class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.reserved_words = {
            "print": "PRINT",
            "if": "IF",
            "else": "ELSE",
            "while": "WHILE",
            "read": "READ",
            "not": "NOT",
            "and": "AND",
            "then": "THEN",
            "local": "LOCAL",
            "function": "FUNCTION",
            "return": "RETURN",
            "string": "STRING",
            "int": "INT",
            "flight_level": "FLIGHT_LEVEL",
            "waypoint": "WAYPOINT",
        }

        self.types = {
            "int": "INT",
            "string": "STRING",
            "flight_level": "FLIGHT_LEVEL",
            "float": "FLOAT",
            "waypoint": "WAYPOINT",
        }

    def next_token(self):
        num = ""

        while (
            self.position < len(self.source)
            and self.source[self.position] in [" ", "\t"]
        ):
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
        elif self.source[self.position] == "+":
            self.next = Token("PLUS", "+")
            self.position += 1
        elif self.source[self.position] == "-":
            if self.source[self.position + 1] == ">":
                self.next = Token("ARROW", "->")
                self.position += 2
                return
            self.next = Token("MINUS", "-")
            self.position += 1
        elif self.source[self.position] == "*":
            self.next = Token("MULT", "*")
            self.position += 1
        elif self.source[self.position] == "/":
            self.next = Token("DIV", "//")
            self.position += 1
        elif self.source[self.position] == "(":
            self.next = Token("OPENBRACKET", "(")
            self.position += 1
        elif self.source[self.position] == ")":
            self.next = Token("CLOSEBRACKET", ")")
            self.position += 1
        elif self.source[self.position] == "{":
            self.next = Token("OPENBRACE", "{")
            self.position += 1
        elif self.source[self.position] == "}":
            self.next = Token("CLOSEBRACE", "}")
            self.position += 1
        elif self.source[self.position] == "\n":
            self.next = Token("NEWLINE", "\n")
            self.position += 1
        elif self.source[self.position] == "=":
            if self.source[self.position + 1] == "=":
                self.next = Token("EQUAL", "==")
                self.position += 2
                return
            self.next = Token("ASSIGN", "=")
            self.position += 1
        elif self.source[self.position] == "<" and self.source[self.position + 1] == "=":
            self.next = Token("LESSE", "<=")
            self.position += 2
        elif self.source[self.position] == "<":
            self.next = Token("LESS", "<")
            self.position += 1
        elif self.source[self.position] == ">" and self.source[self.position + 1] == "=":
            self.next = Token("GREATERE", ">=")
            self.position += 2
        elif self.source[self.position] == ">":
            self.next = Token("GREATER", ">")
            self.position += 1
        elif self.source[self.position] == ",":
            self.next = Token("COMMA", ",")
            self.position += 1
        elif self.source[self.position] == "|":
            self.position += 1
            if self.source[self.position] == "|":
                self.next = Token("OR", "||")
                self.position += 1
            else:
                raise Exception("Unexpected symbol, found only one | and expected ||")
        elif self.source[self.position] == "\"":
            self.position += 1
            while self.position < len(self.source) and self.source[self.position] != "\"":
                num += self.source[self.position]
                self.position += 1
                if self.position == len(self.source):
                    raise Exception("Unexpected EOF, STRING NOT CLOSED")
            self.position += 1
            self.next = Token("STRING", num)
        elif self.source[self.position] == ".":
            self.position += 1
            if self.source[self.position] == ".":
                self.next = Token("DOTDOT", "..")
                self.position += 1
            else:
                raise Exception("Unexpected symbol, found only one . and expected ..")
        elif self.source[self.position] in "0123456789":
            while (
                self.position < len(self.source)
                and self.source[self.position] in "0123456789"
            ):
                num += self.source[self.position]
                self.position += 1
            self.next = Token("INT", num)
        elif (
            self.source[self.position].isalpha()
            or self.source[self.position] == "_"
        ):
            while self.position < len(self.source) and (
                self.source[self.position].isalpha()
                or self.source[self.position].isdigit()
                or self.source[self.position] == "_"
            ):                
                num += self.source[self.position]
                self.position += 1
            is_reserved_world = self.reserved_words.get(num, None)
            if is_reserved_world:
                is_type = self.types.get(num, None)
                if is_type:
                    self.next = Token("TYPE", num)
                else:
                    self.next = Token(is_reserved_world, num)
            else:
                self.next = Token("ID", num)
        else:
            raise Exception("Unexpected symbol")
