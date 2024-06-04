class FuncTable:
    table = {}
    
    def set(key, value):
        FuncTable.table[key] = value
    
    def get(key):
        return FuncTable.table[key]
