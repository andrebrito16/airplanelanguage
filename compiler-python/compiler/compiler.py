from .node import (Assign, BinOp, Block, Identifier, If, IntVal, NoOp, Print,
                   Read, UnOp, VariableDeclaration, StringVal, FuncCall, FuncDeclaration, Return, While)
from .pre_pro import PreProcessing
from .tokenizer import Tokenizer


class Parser:
    def __init__(self) -> None:
        self.tokenizer = None

    def parse_relative_expression(self):
        node = self.parse_expression()
        token = self.tokenizer.next

        if token.type in [
            "EQUAL",
            "DIFFERENT",
            "LESS",
            "GREATER",
            "LESSE",
            "GREATERE",
        ]:
            if token.type == "EQUAL":
                self.tokenizer.next_token()
                return BinOp("==", [node, self.parse_expression()])
            elif token.type == "DIFFERENT":
                self.tokenizer.next_token()
                return BinOp("!=", [node, self.parse_expression()])
            elif token.type == "LESS":
                self.tokenizer.next_token()
                return BinOp("<", [node, self.parse_expression()])
            elif token.type == "LESSE":
                self.tokenizer.next_token()
                return BinOp("<=", [node, self.parse_expression()])
            elif token.type == "GREATER":
                self.tokenizer.next_token()
                return BinOp(">", [node, self.parse_expression()])
            elif token.type == "GREATERE":
                self.tokenizer.next_token()
                return BinOp(">=", [node, self.parse_expression()])

        return node

    def parse_bool_tem(self):
        node = self.parse_relative_expression()
        token = self.tokenizer.next

        while token.type == "AND":
            self.tokenizer.next_token()
            node = BinOp("AND", [node, self.parse_relative_expression()])
            token = self.tokenizer.next

        return node

    def parse_bool_expression(self):
        node = self.parse_bool_tem()
        
        token = self.tokenizer.next

        while token.type == "OR":
            self.tokenizer.next_token()
            node = BinOp("OR", [node, self.parse_bool_tem()])
            token = self.tokenizer.next
        
        while token.type == "DOTDOT":
            self.tokenizer.next_token()
            node = BinOp("..", [node, self.parse_bool_tem()])
            token = self.tokenizer.next

        return node

    def parse_factor(self):
        if self.tokenizer.next.type == "INT":
            node = IntVal(int(self.tokenizer.next.value))
            self.tokenizer.next_token()
            return node
        elif self.tokenizer.next.type == "ID":
            identifier = Identifier(self.tokenizer.next.value)
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "OPENBRACKET":
                return identifier
            elif self.tokenizer.next.type == "OPENBRACKET":
                self.tokenizer.next_token()
                bool_expressions = []
                if self.tokenizer.next.type != "CLOSEBRACKET":
                    bool_expressions.append(self.parse_bool_expression())
                                        
                    # Enquanto não acaba os argumentos
                    while self.tokenizer.next.type == "COMMA":
                        self.tokenizer.next_token()
                        bool_expressions.append(self.parse_bool_expression())
                        
                    if self.tokenizer.next.type != "CLOSEBRACKET":
                        raise Exception("Expected close bracket")

                    self.tokenizer.next_token()
                    return FuncCall(identifier.value, bool_expressions)
                self.tokenizer.next_token()
                return FuncCall(identifier.value, bool_expressions)
        elif self.tokenizer.next.type == "STRING":
            node = StringVal(self.tokenizer.next.value)
            self.tokenizer.next_token()
            return node
        elif self.tokenizer.next.type == "PLUS":
            self.tokenizer.next_token()
            return UnOp("+", [self.parse_factor()])
        elif self.tokenizer.next.type == "MINUS":
            self.tokenizer.next_token()
            return UnOp("-", [self.parse_factor()])
        elif self.tokenizer.next.type == "NOT":
            self.tokenizer.next_token()
            return UnOp("NOT", [self.parse_factor()])
        elif self.tokenizer.next.type == "OPENBRACKET":
            self.tokenizer.next_token()
            node = self.parse_bool_expression()
            if self.tokenizer.next.type != "CLOSEBRACKET":
                raise Exception("Expected close bracket")
            self.tokenizer.next_token()
            return node
        elif self.tokenizer.next.type == "READ":
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "OPENBRACKET":
                raise Exception("Expected open bracket")
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "CLOSEBRACKET":
                raise Exception("Expected close bracket")
            self.tokenizer.next_token()
            return Read()
        else:
            raise Exception(f"Unexpected token in parse factor GOT {self.tokenizer.next.type}")

    def parse_term(self):
        node = self.parse_factor()
        token = self.tokenizer.next

        while token.type in ["MULT", "DIV"]:
            if token.type == "MULT":
                self.tokenizer.next_token()
                node = BinOp("*", [node, self.parse_factor()])
            elif token.type == "DIV":
                self.tokenizer.next_token()
                node = BinOp("/", [node, self.parse_factor()])
            token = self.tokenizer.next

        return node

    def parse_expression(self):
        node = self.parse_term()
        token = self.tokenizer.next

        while token.type in ["PLUS", "MINUS"]:
            if token.type == "PLUS":
                self.tokenizer.next_token()
                node = BinOp("+", [node, self.parse_term()])
            elif token.type == "MINUS":
                self.tokenizer.next_token()
                node = BinOp("-", [node, self.parse_term()])
            elif token.type == "DOTDOT":
                self.tokenizer.next_token()
                node = BinOp("..", [node, self.parse_term()])
            token = self.tokenizer.next

        return node

    def parse_statement(self):
        if self.tokenizer.next.type == "NEWLINE":
            self.tokenizer.next_token()
            return NoOp()
        elif self.tokenizer.next.type == "PRINT":
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "OPENBRACKET":
                raise Exception("Expected open bracket")
            self.tokenizer.next_token()
            node = self.parse_bool_expression()
            if self.tokenizer.next.type != "CLOSEBRACKET":
                raise Exception("Expected close bracket")
            self.tokenizer.next_token()
            return Print([node])
        elif self.tokenizer.next.type == "ID":
            identifier = Identifier(self.tokenizer.next.value)
            self.tokenizer.next_token()
            
            if self.tokenizer.next.type != "ARROW" and self.tokenizer.next.type != "OPENBRACKET" and self.tokenizer.next.type != "ASSIGN":
                raise Exception(f"[LINE 173] Expected arrow or open bracket GOT {self.tokenizer.next.type}")
            if self.tokenizer.next.type == "OPENBRACKET":
                # é uma função
                self.tokenizer.next_token()
                bool_expressions = []
                if self.tokenizer.next.type != "CLOSEBRACKET":
                    bool_expressions.append(self.parse_bool_expression())
                                        
                    # Enquanto não acaba os argumentos
                    while self.tokenizer.next.type == "COMMA":
                        self.tokenizer.next_token()
                        bool_expressions.append(self.parse_bool_expression())
                        
                    
                    
                    if self.tokenizer.next.type != "CLOSEBRACKET":
                        raise Exception("Expected close bracket")

                    self.tokenizer.next_token()
                self.tokenizer.next_token()
                return FuncCall(identifier.value, bool_expressions)
            else:
                self.tokenizer.next_token()
                if self.tokenizer.next.type == "ID":
                    # Variable already declared, just reassigning
                    return Assign([identifier, self.parse_bool_expression()])
                if self.tokenizer.next.type != "TYPE":
                    raise Exception("Expected type")
                variable_type = self.tokenizer.next.value
                self.tokenizer.next_token()
                if self.tokenizer.next.type == "ASSIGN":
                    self.tokenizer.next_token()
                bool_expression = self.parse_bool_expression()
                return VariableDeclaration(variable_type, [identifier, bool_expression])
        elif self.tokenizer.next.type == "FUNCTION":
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "ID":
                raise Exception("Expected ID after function")
            identifier = Identifier(self.tokenizer.next.value)
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "OPENBRACKET":
                raise Exception("Expected open bracket")
            self.tokenizer.next_token()
            
            arguments = []
            while self.tokenizer.next.type != "CLOSEBRACKET":
                if self.tokenizer.next.type != "ID":
                    raise Exception("Expected argument identifier")
                arg_identifier = Identifier(self.tokenizer.next.value)
                self.tokenizer.next_token()
                
                if self.tokenizer.next.type == "COMMA":
                    # Argument without type annotation
                    arguments.append(VariableDeclaration(None, [arg_identifier]))
                    self.tokenizer.next_token()
                elif self.tokenizer.next.type == "ARROW":
                    # Argument with type annotation
                    self.tokenizer.next_token()
                    if self.tokenizer.next.type != "TYPE":
                        raise Exception("Expected type after '->'")
                    arg_type = self.tokenizer.next.value
                    arguments.append(VariableDeclaration(arg_type, [arg_identifier]))
                    self.tokenizer.next_token()
                    
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.next_token()
                    elif self.tokenizer.next.type != "CLOSEBRACKET":
                        raise Exception("Expected ',' or 'CLOSEBRACKET'")
                else:
                    raise Exception("Expected ',' or '->' after argument identifier")
            
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "OPENBRACE":
                raise Exception("Expected '{' after function declaration")
            self.tokenizer.next_token()
            
            blocks = []
            while self.tokenizer.next.type != "CLOSEBRACE":
                blocks.append(self.parse_statement())
            self.tokenizer.next_token()
            
            childrens = [identifier] + arguments
            childrens.append(Block(blocks))
            return FuncDeclaration(childrens)
        # ASSIGNMENT
        elif self.tokenizer.next.type == "ID":
           self.tokenizer.next_token()
           if self.tokenizer.next.type != "ARROW":
                raise Exception("Expected ARROW AFTER VAR DEC")
           self.tokenizer.next_token()
           if self.tokenizer.next.type != "TYPE":
                raise Exception("Expected TYPE AFTER VAR DEC")
           identifier = Identifier(self.tokenizer.next.value)
           self.tokenizer.next_token()
           if self.tokenizer.next.type == "ASSIGN":
                self.tokenizer.next_token()
                bool_expression = self.parse_bool_expression()
                return VariableDeclaration(arg_type, [identifier, bool_expression])
            
           return VariableDeclaration(arg_type, [identifier])
               
        elif self.tokenizer.next.type == "WHILE":
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "OPENBRACKET":
                raise Exception("Expected open bracket on while")
            bool_expression = self.parse_bool_expression()

            if self.tokenizer.next.type != "OPENBRACE":
                raise Exception("Expected { on WHILE")
            self.tokenizer.next_token()
            
            if self.tokenizer.next.type != "NEWLINE":
                raise Exception("Expected new line")
            
            blocks = []
            while self.tokenizer.next.type != "CLOSEBRACE":
                blocks.append(self.parse_statement())
            self.tokenizer.next_token()
            
            if self.tokenizer.next.type != "NEWLINE" and self.tokenizer.next.type != "EOF":
                raise Exception("Expected new line")
            return While([bool_expression, Block(blocks)])
            
        elif self.tokenizer.next.type == "IF":
            self.tokenizer.next_token()
            if self.tokenizer.next.type != "OPENBRACKET":
                raise Exception("Expected open bracket")
            bool_expression = self.parse_bool_expression()
            if self.tokenizer.next.type != "OPENBRACE":
                raise Exception("Expected newline")
            self.tokenizer.next_token()
                       
            
            blocks = []
            while self.tokenizer.next.type not in ["ELSE", "CLOSEBRACE"]:
                blocks.append(self.parse_statement())
            
            if self.tokenizer.next.type == "CLOSEBRACE":
                self.tokenizer.next_token()
                if self.tokenizer.next.type != "ELSE":
                    return If([bool_expression, Block(blocks)])

            self.tokenizer.next_token()
            if self.tokenizer.next.type != "OPENBRACE":
                raise Exception(f"Expected openbrace got {self.tokenizer.next.type}")
            
            self.tokenizer.next_token() # Skip else token
            else_blocks = []
            while self.tokenizer.next.type != "CLOSEBRACE":
                else_blocks.append(self.parse_statement())
            self.tokenizer.next_token()
            return If([bool_expression, Block(blocks), Block(else_blocks)])
        elif self.tokenizer.next.type == "RETURN":
            self.tokenizer.next_token()
            node = self.parse_bool_expression()
            if self.tokenizer.next.type != "NEWLINE":
                raise Exception("Expected new line")
            return Return([node])
        else:
            raise Exception(f"Unexpected token, in parse statement. GOT {self.tokenizer.next.type}")

    def parse_block(self):
        nodes = []
        while self.tokenizer.next.type != "EOF":
            nodes.append(self.parse_statement())

        return Block(nodes)

    def run(self, source):
        source_without_comments = PreProcessing.filter(source)

        tokenizer = Tokenizer(source_without_comments)
        tokenizer.next_token()
        self.tokenizer = tokenizer

        node_root = self.parse_block()

        if self.tokenizer.next.type != "EOF":
            raise Exception("Unexpected token in run")

        return node_root
