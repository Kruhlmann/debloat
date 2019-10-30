from token import *
from nodes import *
from error import InvalidSyntaxError

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advancements = 0

    def register(self, res):
        self.advancements += res.advancements
        if res.error:
            self.error = res.error
        return res.node

    def register_advancement(self):
        self.advancements += 1

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advancements == 0:
            self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())

        if res.error:
            return res

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op, right)

        return res.success(left)

    def comp_expr(self):
        res = ParseResult()

        if self.current_token.matches(TT_KEY, "NOT"):
            op = self.current_token
            res.register_advancement()
            self.advance
            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Unexpected token '{token.type}', expected operator or identifier"))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_ADD, TT_SUB))

    def atom(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (TT_INT, TT_DEC):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))
        elif token.type == TT_ID:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))
        elif token.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected token '{self.current_token.type}', expected ')' in parenthetical")
                return res.failure(error)

        error = InvalidSyntaxError(token.pos_start, token.pos_end, f"Unexpected token '{token.type}', expected operator or identifier")
        return res.failure(error)

    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (TT_ADD, TT_SUB):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_POW))

    def expr(self):
        res = ParseResult()
        if self.current_token.matches(TT_KEY, "SET"):
            res.register_advancement()
            self.advance()

            if self.current_token.type != TT_ID:
                error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected token '{self.current_token.type}', expected identifier")
                return res.failure(error)

            var_name = self.current_token
            res.register_advancement()
            self.advance()

            if self.current_token.type != TT_EQ:
                error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected token '{self.current_token.type}', expected '=''")
                return res.failure(error)

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if (res.error):
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEY, "AND"), (TT_KEY, "OR"))))

        if res.error:
            error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected token '{self.current_token.type}', expected 'SET', operator or identifier")
            return res.failure(error)
        return res.success(node)

    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != TT_EOF:
            error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected token '{self.current_token.type}', expected expression")
            return res.failure(error)
        return res
