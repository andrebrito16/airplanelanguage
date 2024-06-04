import sys

from compiler.compiler import Parser
from compiler.symbol_table import SymbolTable
from compiler.waypoints import WaypointsDatabase

if __name__ == "__main__":
    args = sys.argv[1]

    file = open(args, "r")

    raw_input = file.read()

    WaypointsDatabase.initialize()


    calculator = Parser()
    symbol_table = SymbolTable()

    calculator.run(raw_input).evaluate(symbol_table)
