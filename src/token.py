# File:     token.py
# Author:   Andreas Kruhlmann
# Since:    OCT 28 2019

DIGITS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS_DIGITS = LETTERS + DIGITS

# Arithmetic
TT_INT = "INT"
TT_DEC = "DEC"
TT_ADD = "ADD"
TT_SUB = "SUB"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POW = "POW"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

TT_KEY = "KEY"
TT_EOF = "EOF"
TT_EQ = "EQ"
TT_ID = "ID"

KEYWORDS = [
    "SET"
]

class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = self.pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type, value):
        return self.type == type and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

