class Position:
    def __init__(self, index, line, col, fname, source):
        self.index = index
        self.line = line
        self.col = col
        self.fname = fname
        self.source = source

    def advance(self, current_symbol=None):
        self.index += 1
        self.col += 1

        if current_symbol == "\n":
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.index, self.line, self.col, self.fname, self.source)
