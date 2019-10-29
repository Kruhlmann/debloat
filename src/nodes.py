class NumberNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"

class BinOpNode:
    def __init__(self, lnode, op, rnode):
        self.lnode = lnode
        self.op = op
        self.rnode = rnode
        self.pos_start = self.lnode.pos_start
        self.pos_end = self.rnode.pos_end

    def __repr__(self):
        return f"({self.lnode}, {self.op}, {self.rnode})"

class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node
        self.pos_start = self.op.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.op}, {self.node})"

class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.pos_start = var_name_token.pos_start
        self.pos_end = var_name_token.pos_end

class VarAssignNode:
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.value_node.pos_end
