class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def add_by(self, n):
        if isinstance(n, Number):
            return Number(self.value + n.value)

    def sub_by(self, n):
        if isinstance(n, Number):
            return Number(self.value - n.value)

    def mul_by(self, n):
        if isinstance(n, Number):
            return Number(self.value * n.value)

    def div_by(self, n):
        if isinstance(n, Number):
            return Number(self.value / n.value)

    def __repr__(self):
        return str(self.value)
