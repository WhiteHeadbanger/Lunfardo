class NumeroNode:

    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'NumeroNode({self.tok})'

class ChamuyoNode:

    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'ChamuyoNode({self.tok})'
    
class CosoNode:

    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'CosoNode({self.element_nodes})'
    
class MataburrosNode:

    def __init__(self, keys_nodes, values_nodes, pos_start, pos_end):
        self.keys_nodes = keys_nodes
        self.values_nodes = values_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'MataburrosNode({self.keys_nodes}, {self.values_nodes})'
    
class PoneleQueAccessNode:

    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f'PoneleQueAccessNode({self.var_name_tok})'

class PoneleQueAssignNode:

    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return f'PoneleQueAssignNode({self.var_name_tok}, {self.value_node})'

    
class BinOpNode:

    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'BinOpNode({self.left_node}, {self.op_tok}, {self.right_node})'
    
class UnaryOpNode:
    
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'UnaryOpNode({self.op_tok}, {self.node})'
    
class SiNode:

    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) -1])[0].pos_end

    def __repr__(self):
        return f'SiNode({self.cases}, {self.else_case})'
    
class ParaNode:

    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'ParaNode({self.var_name_tok}, {self.start_value_node}, {self.end_value_node}, {self.step_value_node}, {self.body_node})'

class MientrasNode:

    def __init__(self, condition_node, body_node, should_return_null):
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'MientrasNode({self.condition_node}, {self.body_node})'
    
class LaburoDefNode:

    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return, is_method=False):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return
        self.is_method = is_method

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = list(self.arg_name_toks.keys())[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'LaburoDefNode({self.var_name_tok}, {self.arg_name_toks}, {self.body_node})'
    
class ChetoDefNode:
    
    def __init__(self, var_name_tok, methods, arranque_method):
        self.var_name_tok = var_name_tok
        self.methods = methods
        self.arranque_method = arranque_method
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.methods[-1].pos_end if self.methods else self.var_name_tok.pos_end

    def __repr__(self):
        return f'ChetoDefNode({self.var_name_tok}, {self.methods})'
    
class MethodCallNode:

    def __init__(self, object_tok, method_name_tok, arg_nodes):
        self.object_tok = object_tok
        self.method_name_tok = method_name_tok
        self.arg_nodes = arg_nodes

        self.pos_start = self.object_tok.pos_start
        self.pos_end = (self.arg_nodes[-1].pos_end if self.arg_nodes else self.method_name_tok.pos_end)

    def __repr__(self):
        return f'MethodCallNode({self.object_tok}, {self.method_name_tok}, {self.arg_nodes})'
    
class InstanceNode:

    def __init__(self, class_name_tok, arg_nodes = None):
        self.class_name_tok = class_name_tok
        self.arg_nodes = arg_nodes
        self.pos_start = self.class_name_tok.pos_start
        self.pos_end = self.arg_nodes[-1].pos_end if self.arg_nodes else self.class_name_tok.pos_end

    def __repr__(self):
        return f'InstanceNode({self.class_name_tok}, {self.arg_nodes})'
    
class InstanceVarAssignNode:

    def __init__(self, object_tok, var_name_tok, value_node):
        self.object_tok = object_tok
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.object_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return f'InstanceVarAssignNode({self.object_tok}, {self.var_name_tok}, {self.value_node})'

class InstanceVarAccessNode:

    def __init__(self, object_tok, var_name_tok):
        self.object_tok = object_tok
        self.var_name_tok = var_name_tok
        self.pos_start = self.object_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f'InstanceVarAccessNode({self.object_tok}, {self.var_name_tok})'
    
class CallNode:

    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

    def __repr__(self):
        return f'CallNode({self.node_to_call}, {self.arg_nodes})'
    
class DevolverNode:

    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'DevolverNode({self.node_to_return})'
    
class ContinuarNode:

    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'ContinuarNode({self.pos_start, self.pos_end})'
    
    def __str__(self):
        return f'ContinuarNode({self.pos_start, self.pos_end})'

class RajarNode:

    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'RajarNode({self.pos_start, self.pos_end})'
    
    def __str__(self):
        return f'RajarNode({self.pos_start, self.pos_end})'