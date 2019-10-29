from types import *
from token import *

class Interpreter:
    def visit(self, node):
        func_name = f"visit_{type(node).__name__}"
        func = getattr(self, func_name, self.no_visit)
        return func(node)

    def no_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__}")

    def visit_NumberNode(self, node):
        return Number(node.token.value).set_pos(node.pos_start, node.pos_end)

    def visit_BinOpNode(self, node):
        l = self.visit(node.lnode)
        r = self.visit(node.rnode)
        print(l)
        print(r)

        if node.op.type == TT_ADD:
            result = l.add_by(r)
        elif node.op.type == TT_SUB:
            result = l.sub_by(r)
        elif node.op.type == TT_MUL:
            result = l.mul_by(r)
        elif node.op.type == TT_DIV:
            result = l.div_by(r)

        return result.set_pos(node.pos_start, node.pos_end)

    def visit_UnaryOpNode(self, node):
        n = self.visit(node.node)

        if node.op == TT_SUB:
            n = n.mul_by(Number(-1))
        return n.set_pos(node.pos_start, node.pos_end);
