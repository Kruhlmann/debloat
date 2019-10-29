from error import RuntimeError

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context;
        return self

    def add_by(self, n):
        if isinstance(n, Number):
            return Number(self.value + n.value).set_context(self.context), None

    def sub_by(self, n):
        if isinstance(n, Number):
            return Number(self.value - n.value).set_context(self.context), None

    def mul_by(self, n):
        if isinstance(n, Number):
            return Number(self.value * n.value).set_context(self.context), None

    def div_by(self, n):
        if isinstance(n, Number):
            if n.value == 0:
                return None, RuntimeError(n.pos_start,
                        n.pos_end,
                        "Division by zero",
                        self.context)
            return Number(self.value / n.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)
