from abc import ABC, abstractmethod
from .func_table import FuncTable
from .symbol_table import SymbolTable
from .waypoints import WaypointsDatabase


class Node(ABC):
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children if children is not None else []

    @abstractmethod
    def evaluate(self, st):
        pass


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        evaluate_children_0 = self.children[0].evaluate(st)
        evaluate_children_1 = self.children[1].evaluate(st)

        if self.value == "+":
            if evaluate_children_0[1] == evaluate_children_1[1] and not evaluate_children_0[1] == "string":
                return evaluate_children_0[0] + evaluate_children_1[0], evaluate_children_0[1]
            else:
                raise Exception("[BIN OP] Invalid operation on +")
        elif self.value == "-":
            if evaluate_children_0[1] == "INT" and evaluate_children_1[1] == "INT":
                return evaluate_children_0[0] - evaluate_children_1[0], "INT"
            else:
                raise Exception("[BIN OP] Invalid operation on -")
        elif self.value == "*":
            if evaluate_children_0[1] == "INT" and evaluate_children_1[1] == "INT":
                return evaluate_children_0[0] * evaluate_children_1[0], "INT"
            else:
                raise Exception("[BIN OP] Invalid operation on *")
        elif self.value == "/":
            if evaluate_children_0[1] == "INT" and evaluate_children_1[1] == "INT":
                return evaluate_children_0[0] // evaluate_children_1[0], "INT"
            else:
                raise Exception("[BIN OP] Invalid operation on /")
        elif self.value == "OR":
            if evaluate_children_0[1] == "INT" and evaluate_children_1[1] == "INT":
                return int(evaluate_children_0[0] or evaluate_children_1[0]), "INT"
        elif self.value == "AND":
            if evaluate_children_0[1] == "INT" and evaluate_children_1[1] == "INT":
                return int(evaluate_children_0[0] and evaluate_children_1[0]), "INT"
        elif self.value == "==":
            if evaluate_children_0[1] == evaluate_children_1[1]:
                return int(evaluate_children_0[0] == evaluate_children_1[0]), "INT"
            else:
                raise Exception("[BIN OP] Invalid operation on ==")
        elif self.value == ">":
            if evaluate_children_0[1] == evaluate_children_1[1]:
                return int(evaluate_children_0[0] > evaluate_children_1[0]), "INT"
            else:
                raise Exception("[BIN OP] Invalid operation on >")
        elif self.value == ">=":
            if evaluate_children_0[1] == evaluate_children_1[1]:
                return int(evaluate_children_0[0] >= evaluate_children_1[0]), "INT"
            else:
                raise Exception("[BIN OP] Invalid operation on >=")
        elif self.value == "<":
            if evaluate_children_0[1] == evaluate_children_1[1]:
                return int(evaluate_children_0[0] < evaluate_children_1[0]), "INT"
            else:
                raise Exception("[BIN OP] Invalid operation on <")
        elif self.value == "<=":
            if evaluate_children_0[1] == evaluate_children_1[1]:
                return int(evaluate_children_0[0] <= evaluate_children_1[0]), "INT"
            else:
                raise Exception("[BIN OP] Invalid operation on <=")
        elif self.value == "..":
            return str(evaluate_children_0[0]) + str(evaluate_children_1[0]), "STR"
        else:
            raise Exception("[BIN OP] Unknown operator")


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        evaluate = self.children[0].evaluate(st)

        if self.value == "+":
            return evaluate[0], "INT"
        elif self.value == "-":
            return -evaluate[0], "INT"
        elif self.value == "NOT":
            return int(not evaluate[0]), "INT"
        else:
            raise Exception("[UN OP] Unknown operator")


class Read(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, st):
        return int(input()), "INT"
    
class VariableDeclaration(Node):
    def __init__(self, value, children): # Value é o tipo da variável
        super().__init__(value, children)

    def evaluate(self, st):
        if len(self.children) == 2:
            value = self.children[1].evaluate(st)
            
            if self.value.upper() == "WAYPOINT":
                if value[0] not in WaypointsDatabase.waypoints:
                    raise Exception(f"Waypoint {value[0]} not exists on Database AIRAC CYCLE 2404")

            st.set(self.children[0].value, (value[0], self.value.upper()))
        else:
            if self.children[0].value in st.table:
                raise Exception(f"Variable {self.children[0].value} already defined")

            st.create(self.children[0].value, (None, self.value))


class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        return self.value, "INT"
    
class StringVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        return self.value, "STR"


class NoOp(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, st):
        pass


class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st):
        for child in self.children:
            if isinstance(child, Return):
                return child.evaluate(st)
            child.evaluate(st)


class If(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st):
        evaluate_children_0 = self.children[0].evaluate(st)

        if evaluate_children_0[0]:
            self.children[1].evaluate(st)
        elif len(self.children) == 3:
            self.children[2].evaluate(st)

class While(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st):
        evaluate_children_0 = self.children[0].evaluate(st)

        while evaluate_children_0[0]:
            self.children[1].evaluate(st)
            evaluate_children_0 = self.children[0].evaluate(st)

class Assign(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st):
        evaluate_children_1 = self.children[1].evaluate(st)
        if self.children[0].value not in st.table:
            raise Exception(f"Variable {self.children[0].value} not defined")
        
        st.set(self.children[0].value, (evaluate_children_1[0], evaluate_children_1[1]))


class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        value, type = st.get(self.value)
        if value is None:
            raise Exception(f"Variable {self.value} not defined")

        return value, type


class Print(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st):
        print(self.children[0].evaluate(st)[0]) # Returns only the value

class Return(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st):
        return self.children[0].evaluate(st)
    
class FuncDeclaration(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st):
        
        # Check if function already exists on func table
        if self.children[0].value in FuncTable.table.keys():
            raise Exception(f"Function {self.value} already defined")
        
        FuncTable.set(self.children[0].value, self)
        
class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        # Check if function exists on func table
        if self.value not in FuncTable.table:
            raise Exception(f"Function {self.value} not defined")
        
        # Verifica o número de argumentos. N na func call == n-2 na FuncDec
        funcDec = FuncTable.table.get(self.value)
        if len(funcDec.children) - 2 != len(self.children):
            raise Exception(f"Function {self.value} called with wrong number of arguments")
        
        # Cria uma nova symbol table para a chamada da função
        local_st = SymbolTable()

        # Executar os varDecs, que vai de 1 até len - 2
        for i in range(1, len(funcDec.children) - 1):
            funcDec.children[i].evaluate(local_st)
        
        i = 0
        for key in local_st.table.keys():
            local_st.set(key, self.children[i].evaluate(st))
            i += 1
            
        return funcDec.children[-1].evaluate(local_st)
