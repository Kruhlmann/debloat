from token import *
from error import IllegalTokenError
from position import Position
from parser import Parser
from interpreter import Interpreter

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
            elif self.current_symbol == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_symbol == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
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

    interpreter = Interpreter()
    result = interpreter.visit(tree.node)

    return result, None
