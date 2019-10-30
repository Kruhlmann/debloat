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

    def pow_by(self, n):
        if isinstance(n, Number):
            return Number(self.value ** n.value).set_context(self.context), None

    def eq(self, n):
        if isinstance(n, Number):
            return Number(1 if self.value == n.value else 0).set_context(self.context), None

    def neq(self, n):
        if isinstance(n, Number):
            return Number(0 if self.value == n.value else 1).set_context(self.context), None

    def lt(self, n):
        if isinstance(n, Number):
            return Number(1 if self.value < n.value else 0).set_context(self.context), None

    def gt(self, n):
        if isinstance(n, Number):
            return Number(1 if self.value > n.value else 0).set_context(self.context), None

    def lte(self, n):
        if isinstance(n, Number):
            return Number(1 if self.value <= n.value else 0).set_context(self.context), None

    def gte(self, n):
        if isinstance(n, Number):
            return Number(1 if self.value >= n.value else 0).set_context(self.context), None

    def logic_and(self, n):
        if isinstance(n, Number):
            return Number(1 if self.value and n.value else 0).set_context(self.context), None

    def logic_or(self, n):
        if isinstance(n, Number):
            return Number(1 if self.value or n.value else 0).set_context(self.context), None

    def logic_not(self, n):
        if isinstance(n, Number):
            return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)
