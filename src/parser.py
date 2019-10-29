from token import *
from nodes import *
from error import InvalidSyntaxError

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
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

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())

        if res.error:
            return res

        while self.current_token.type in ops:
            op = self.current_token
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op, right)

        return res.success(left)

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (TT_ADD, TT_SUB):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))
        elif token.type in (TT_INT, TT_DEC):
            res.register(self.advance())
            return res.success(NumberNode(token))
        elif token.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected token '{self.current_token.type}' expected ) in parenthetical")
                return res.failure(error)

        error = InvalidSyntaxError(token.pos_start, token.pos_end, f"Unexpected token '{token.type}', expected numeric literal")
        return res.failure(error)

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_POW))

    def expr(self):
        return self.bin_op(self.term, (TT_ADD, TT_SUB))

    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != TT_EOF:
            error = InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected token '{self.current_token.type}', expected expression")
            return res.failure(error)
        return res
