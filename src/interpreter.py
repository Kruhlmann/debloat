from types import *
from token import *
from runtime import *
from scope import Scope

class Interpreter:
    def visit(self, node, context):
        func_name = f"visit_{type(node).__name__}"
        func = getattr(self, func_name, self.no_visit)
        return func(node, context)

    def no_visit(self, node, context):
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
        elif node.op.type == TT_POW:
            result, error = l.pow_by(r)
        elif node.op.type == TT_EE:
            result, error = l.eq(r)
        elif node.op.type == TT_NE:
            result, error = l.ne(r)
        elif node.op.type == TT_LT:
            result, error = l.lt(r)
        elif node.op.type == TT_GT:
            result, error = l.gt(r)
        elif node.op.type == TT_LTE:
            result, error = l.lte(r)
        elif node.op.type == TT_GTE:
            result, error = l.gte(r)
        elif node.op.matches(TT_KEY, "AND"):
            result, error = l.logic_and(r)
        elif node.op.matches(TT_KEY, "OR"):
            result, error = l.logic_or(r)

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
        if node.op.type.matches(TT_KEYWORD, "NOT"):
            n, error = n.logic_not()

        if error:
            return res.failure(error)
        return res.success(n.set_pos(node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_token.value
        value = context.scope.get(var_name)

        if not value:
            error = RuntimeError(node.pos_start, node.pos_end, f"'{var_name}' is not defined")
            return res.failure(error)

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_token.value
        value = res.register(self.visit(node.value_node, context))

        if res.error:
            return res

        context.scope.set(var_name, value)
        return res.success(value)
