class SymbolTable:
    def __init__(self):
        self.table = {}

    def get(self, key):
        return self.table.get(key, None)
    
    def set(self, key, value):
        self.table[key] = value

    def create(self, key, type):
        self.table[key] = (None, type)
