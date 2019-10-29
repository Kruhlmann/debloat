class Scope:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, var_name):
        value = self.symbols.get(var_name, None)
        if value == None and self.parent:
            return self.parent.get(var_name)
        return value

    def set(self, var_name, value):
        self.symbols[var_name] = value

    def rem(self, var_name):
        del self.symbols[name]

