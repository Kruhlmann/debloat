from types import *
from token import *
from runtime import *

class Interpreter:
    def visit(self, node, context):
        func_name = f"visit_{type(node).__name__}"
        func = getattr(self, func_name, self.no_visit)
        return func(node, context)

    def no_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__}")

    def visit_NumberNode(self, node, context):
        result = Number(node.token.value).set_pos(node.pos_start, node.pos_end).set_context(context)
        return RuntimeResult().success(result)

    def visit_BinOpNode(self, node, context):
        res = RuntimeResult()

        l = res.register(self.visit(node.lnode, context))
        if res.error:
            return res
        r = res.register(self.visit(node.rnode, context))
        if res.error:
            return res

        if node.op.type == TT_ADD:
            result, error = l.add_by(r)
        elif node.op.type == TT_SUB:
            result, error = l.sub_by(r)
        elif node.op.type == TT_MUL:
            result, error = l.mul_by(r)
        elif node.op.type == TT_DIV:
            result, error = l.div_by(r)

        if error:
            return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RuntimeResult()
        n = res.register(self.visit(node.node, context))

        if res.error:
            return res

        error = None

        if node.op.type == TT_SUB:
            n, error = n.mul_by(Number(-1))

        if error:
            return res.failure(error)
        return res.success(n.set_pos(node.pos_start, node.pos_end))
