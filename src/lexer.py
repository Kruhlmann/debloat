from token import *
from types import *
from error import IllegalTokenError
from position import Position
from parser import Parser
from interpreter import Interpreter
from context import Context
from scope import Scope

class Lexer:
    def __init__(self, fname, source):
        self.source = source
        self.fname = fname
        self.pos = Position(-1, 0, -1, fname, source)
        self.current_symbol = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_symbol)
        self.current_symbol = self.source[self.pos.index] if self.pos.index < len(self.source) else None

    def make_tokens(self):
        tokens = []

        while self.current_symbol != None:
            if self.current_symbol in " \t":
                self.advance()
            elif self.current_symbol in DIGITS:
                tokens.append(self.make_number())
            elif self.current_symbol in LETTERS + "_":
                tokens.append(self.make_identifier())
            elif self.current_symbol == "+":
                tokens.append(Token(TT_ADD, pos_start=self.pos))
                self.advance()
            elif self.current_symbol == "-":
                tokens.append(Token(TT_SUB, pos_start=self.pos))
                self.advance()
            elif self.current_symbol == "*":
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_symbol == "/":
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_symbol == "^":
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_symbol == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_symbol == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_symbol == "!":
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)
            elif self.current_symbol == "=":
                tokens.append(self.make_equals())
            elif self.current_symbol == "<":
                tokens.append(tself.make_less_than())
            elif self.current_symbol == ">":
                tokens.append(tself.make_greater_than())
            else:
                pos_start = self.pos.copy()
                illegal_symbol = self.current_symbol
                self.advance()
                return [], IllegalTokenError(pos_start, self.pos, f"'{illegal_symbol}'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_s = ""
        dot_c = 0
        pos_start = self.pos.copy()

        while self.current_symbol != None and self.current_symbol in DIGITS + ".":
            if self.current_symbol == ".":
                if dot_c == 1:
                    break
                dot_c += 1
                num_s += "."
            else:
                num_s += self.current_symbol
            self.advance()
        if dot_c == 0:
            return Token(TT_INT, int(num_s), pos_start, self.pos)
        else:
            return Token(TT_DEC, float(num_s), pos_start, self.pos)

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_symbol != None and self.current_symbol in LETTERS_DIGITS + "_":
            id_str += self.current_symbol
            self.advance()

        token_type = TT_KEY if id_str in KEYWORDS else TT_ID
        return Token(token_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_symbol == "=":
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        invalid_symbol = self.current_symbol
        self.advance()
        return None, ExpectedSymbolError(pos_start, self.pos, f"Unxpected symbol '{invalid_symbol}', expected '='")

    def make_equals(self):
        token_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_symbol == "=":
            self.advance()
            token_type = TT_EE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        token_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_symbol == "=":
            self.advance()
            token_type = TT_LTE

        return Token(token_type, pos_start=pos_start, pos_end=pos_end)

    def make_greater_than(self):
        token_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_symbol == "=":
            self.advance()
            token_type = TT_GTE

        return Token(token_type, pos_start=pos_start, pos_end=pos_end)


def lex(fname):
    source = open(fname, "r").read().rstrip("\r\n")
    lexer = Lexer(fname, source)
    tokens, error = lexer.make_tokens()

    if error:
        return None, error

    parser = Parser(tokens)
    tree = parser.parse()

    if tree.error:
        return None, tree.error

    global_scope = Scope()
    global_scope.set("NULL", Number(0))
    global_scope.set("TRUE", Number(1))
    global_scope.set("FALSE", Number(0))

    interpreter = Interpreter()
    context = Context("<main>")
    context.scope = global_scope
    result = interpreter.visit(tree.node, context)

    return result.value, result.error
