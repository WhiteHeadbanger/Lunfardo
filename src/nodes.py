"""
Node classes for the Abstract Syntax Tree (AST) of the Lunfardo programming language.

This module defines various node types that represent different syntactic constructs
in the Lunfardo language, forming the structure of the AST.
"""

class NumeroNode:
    """Represents a numeric literal in the AST."""

    def __init__(self, tok) -> None:
        """
        Initialize a NumeroNode.

        Args:
            tok (Token): The token representing the numeric literal.
        """
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self) -> str:
        return f'NumeroNode({self.tok})'

class ChamuyoNode:
    """Represents a string literal in the AST."""

    def __init__(self, tok) -> None:
        """
        Initialize a ChamuyoNode.

        Args:
            tok (Token): The token representing the string literal.
        """
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self) -> str:
        return f'ChamuyoNode({self.tok})'
    
class CosoNode:
    """Represents a list (coso) in the AST."""

    def __init__(self, element_nodes, pos_start, pos_end) -> None:
        """
        Initialize a CosoNode.

        Args:
            element_nodes (list): List of nodes representing the elements.
            pos_start (Position): Start position of the list.
            pos_end (Position): End position of the list.
        """
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        return f'CosoNode({self.element_nodes})'
    
class MataburrosNode:
    """Represents a dictionary (mataburros) in the AST."""

    def __init__(self, pairs, pos_start, pos_end) -> None:
        """
        Initialize a MataburrosNode.

        Args:
            keys_nodes (list): List of nodes representing the keys.
            values_nodes (list): List of nodes representing the values.
            pos_start (Position): Start position of the dictionary.
            pos_end (Position): End position of the dictionary.
        """
        self.pairs = pairs
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        return f'MataburrosNode({self.pairs})'
    
class PoneleQueAccessNode:
    """Represents a name of a variable to access its value in the AST."""

    def __init__(self, var_name_tok) -> None:
        """
        Initialize a PoneleQueAccessNode.

        Args:
            var_name_tok (Token): Token representing the name of the variable.
        """
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self) -> str:
        return f'PoneleQueAccessNode({self.var_name_tok})'

class PoneleQueAssignNode:
    """Represents a name of a variable and its value in the AST."""

    def __init__(self, var_name_tok, value_node) -> None:
        """
        Initialize a PoneleQueAssignNode.

        Args:
            var_name_tok (Token): Token representing the name of the variable.
            value_node (Node): Node representing the value of the variable.
        """
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self) -> str:
        return f'PoneleQueAssignNode({self.var_name_tok}, {self.value_node})'

class AccessAndAssignNode:
    """Represents a name of a declared variable and its value in the AST."""

    def __init__(self, var_name_tok, value_node) -> None:
        """
        Initialize an AccessAndAssignNode.

        Args:
            var_name_tok (Token): Token representing the name of the variable.
            value_node (Node): Node representing the value of the variable.
        """
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self) -> str:
        return f'AccessAndAssignNode({self.var_name_tok}, {self.value_node})'
    
class InstanceVarAccessAndAssignNode:
    """Represents a name of a declared instanced variable and its value in the AST."""

    def __init__(self, instance_var_name_tok, access_chain, value_node) -> None:
        """
        Initialize an InstanceVarAccessAndAssignNode.

        Args:
            instance_var_name_tok (Token): Token representing the first identifier.
            access_chain (List): List of tokens representing the access chain.
            value_node (Node): Node representing the value of the variable.
        """
        self.instance_var_name_tok = instance_var_name_tok
        self.access_chain = access_chain
        self.value_node = value_node
        self.pos_start = self.instance_var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self) -> str:
        return f'InstanceVarAccessAndAssignNode({self.instance_var_name_tok}, {self.access_chain}, {self.value_node})'

    
class BinOpNode:
    """Represents a Binary Operator in the AST."""

    def __init__(self, left_node, op_tok, right_node) -> None:
        """
        Initialize a PoneleQueAssignNode.

        Args:
            left_node (Node): Node representing the left operand.
            op_tok (Token): Token representing the operator.
            right_node (Node): Node representing the right operand.
        """
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self) -> str:
        return f'BinOpNode({self.left_node}, {self.op_tok}, {self.right_node})'
    
class UnaryOpNode:
    """Represents a Unary Operator in the AST."""
    
    def __init__(self, op_tok, node) -> None:
        """
        Initialize a UnaryOpNode.

        Args:
            op_tok (Token): Token representing the operator.
            node (Node): Node representing the operand.
        """
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self) -> str:
        return f'UnaryOpNode({self.op_tok}, {self.node})'
    
class SiNode:
    """Represents a si (if) statement in the AST."""

    def __init__(self, cases, else_case) -> None:
        """
        Initialize a SiNode.

        Args:
            cases (list): List of tuples (condition, body) representing the cases.
            else_case (Node): Node representing the else case.
        """
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) -1])[0].pos_end

    def __repr__(self) -> str:
        return f'SiNode({self.cases}, {self.else_case})'
    
class ParaNode:
    """Represents a para (for) statement in the AST."""

    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null) -> None:
        """
        Initialize a ParaNode.

        Args:
            var_name_tok (Token): Token representing the name of the variable.
            start_value_node (Node): Node representing the start value of the variable.
            end_value_node (Node): Node representing the end value of the variable.
            step_value_node (Node): Node representing the step value of the variable.
            body_node (Node): Node representing the body of the for loop.
            should_return_null (bool): True if the body of the for loop returns null.
        """
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self) -> str:
        return f'ParaNode({self.var_name_tok}, {self.start_value_node}, {self.end_value_node}, {self.step_value_node}, {self.body_node})'

class MientrasNode:
    """Represents a mientras (while) statement in the AST."""

    def __init__(self, condition_node, body_node, should_return_null) -> None:
        """
        Initialize a MientrasNode.

        Args:
            condition_node (Node): Node representing the condition of the while loop.
            body_node (Node): Node representing the body of the while loop.
            should_return_null (bool): True if the body of the while loop returns null.
        """
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self) -> str:
        return f'MientrasNode({self.condition_node}, {self.body_node})'
    
class LaburoDefNode:
    """Represents a laburo (function) definition in the AST."""

    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return, is_method=False) -> None:
        """
        Initialize a LaburoDefNode.

        Args:
            var_name_tok (Token): Token representing the name of the laburo.
            arg_name_toks (dict): Dictionary of tokens representing the names of the arguments.
            body_node (Node): Node representing the body of the laburo.
            should_auto_return (bool): True if the laburo should return null.
            is_method (bool): True if the laburo is a method.
        """
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

    def __repr__(self) -> str:
        return f'LaburoDefNode({self.var_name_tok}, {self.arg_name_toks}, {self.body_node})'
    
class ChetoDefNode:
    """Represents a cheto (class) definition in the AST."""
    
    def __init__(self, var_name_tok, methods, arranque_method, parent_class = None) -> None:
        """
        Initialize a ChetoDefNode.

        Args:
            var_name_tok (Token): Token representing the name of the cheto.
            methods (list): List of Nodes representing the methods of the cheto.
            arranque_method (LaburoDefNode): Node representing the "arranque" (constructor) method of the cheto.
            parent_class (Node): Node representing the parent cheto of the cheto to inherit from.
        """
        self.var_name_tok = var_name_tok
        self.methods = methods
        self.arranque_method = arranque_method
        self.parent_class = parent_class
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.methods[-1].pos_end if self.methods else self.var_name_tok.pos_end

    def __repr__(self):
        return f'ChetoDefNode({self.var_name_tok}, {self.methods})'
    
class MethodCallNode:
    """Represents a method call in the AST."""

    def __init__(self, object_tok, access_chain, method_name_tok, arg_nodes) -> None:
        """
        Initialize a MethodCallNode.

        Args:
            object_tok (Token): Token representing the object of the method call.
            method_name_tok (Token): Token representing the name of the method.
            arg_nodes (list): List of Nodes representing the arguments of the method call.
        """
        self.object_tok = object_tok
        self.access_chain = access_chain
        self.method_name_tok = method_name_tok
        self.arg_nodes = arg_nodes

        self.pos_start = self.object_tok.pos_start
        self.pos_end = (self.arg_nodes[-1].pos_end if self.arg_nodes else self.method_name_tok.pos_end)

    def __repr__(self) -> str:
        return f'MethodCallNode({self.object_tok}, {self.method_name_tok}, {self.arg_nodes})'
    
class InstanceNode:
    """Represents an instance in the AST."""

    def __init__(self, class_name_tok, arg_nodes = None) -> None:
        """
        Initialize an InstanceNode.

        Args:
            class_name_tok (Token): Token representing the name of the cheto (class).
            arg_nodes (list): List of Nodes representing the arguments of the instance.
        """
        self.class_name_tok = class_name_tok
        self.arg_nodes = arg_nodes
        self.pos_start = self.class_name_tok.pos_start
        self.pos_end = self.arg_nodes[-1].pos_end if self.arg_nodes else self.class_name_tok.pos_end

    def __repr__(self) -> str:
        return f'InstanceNode({self.class_name_tok}, {self.arg_nodes})'
    
class InstanceVarAssignNode:
    """Represents an instance variable assignment in the AST."""

    def __init__(self, object_tok, var_name_tok, value_node) -> None:
        """
        Initialize an InstanceVarAssignNode.

        Args:
            object_tok (Token): Token representing the object of the instance variable assignment.
            var_name_tok (Token): Token representing the name of the instance variable.
            value_node (Node): Node representing the value of the instance variable.
        """
        self.object_tok = object_tok
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.object_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self) -> str:
        return f'InstanceVarAssignNode({self.object_tok}, {self.var_name_tok}, {self.value_node})'

class InstanceVarAccessNode:
    """Represents an instance variable access in the AST."""

    def __init__(self, object_tok, access_chain) -> None:
        """
        Initialize an InstanceVarAccessNode.

        Args:
            object_tok (Token): Token representing the object of the instance variable access.
            var_name_tok (Token): Token representing the name of the instance variable.
        """
        self.object_tok = object_tok
        self.access_chain = access_chain
        self.pos_start = self.object_tok.pos_start
        self.pos_end = self.access_chain[-1].pos_end if access_chain else self.object_tok.pos_end

    def __repr__(self) -> str:
        return f'InstanceVarAccessNode({self.object_tok}, {self.access_chain})'
    
class CallNode:
    """Represents a call in the AST."""

    def __init__(self, node_to_call, arg_nodes) -> None:
        """
        Initialize a CallNode.

        Args:
            node_to_call (Node): Node representing the node to call.
            arg_nodes (list): List of Nodes representing the arguments of the call.
        """
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

    def __repr__(self) -> str:
        return f'CallNode({self.node_to_call}, {self.arg_nodes})'
    
class DevolverNode:
    """Represents a devolver (return) in the AST."""

    def __init__(self, node_to_return, pos_start, pos_end) -> None:
        """
        Initialize a DevolverNode.

        Args:
            node_to_return (Node): Node representing the node to devolver.
            pos_start (int): Position of the first character of the node.
            pos_end (int): Position of the last character of the node.
        """
        self.node_to_return = node_to_return
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        return f'DevolverNode({self.node_to_return})'
    
class ContinuarNode:
    """Represents a continuar (continue) in the AST."""

    def __init__(self, pos_start, pos_end):
        """
        Initialize a ContinuarNode.

        Args:
            pos_start (int): Position of the first character of the node.
            pos_end (int): Position of the last character of the node.
        """
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        return f'ContinuarNode({self.pos_start, self.pos_end})'
    
    def __str__(self) -> str:
        return f'ContinuarNode({self.pos_start, self.pos_end})'

class RajarNode:
    """Represents a rajar (break) statement in the AST."""

    def __init__(self, pos_start, pos_end) -> None:
        """
        Initialize a RajarNode.

        Args:
            pos_start (Position): Start position of the break statement.
            pos_end (Position): End position of the break statement.
        """
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        return f'RajarNode({self.pos_start, self.pos_end})'
    
    def __str__(self) -> str:
        return f'RajarNode({self.pos_start, self.pos_end})'
    
class ImportarNode:
    """Represents an import statement in the AST."""

    def __init__(self, module_name_node: ChamuyoNode) -> None:
        """
        Initialize an ImportarNode.

        Args:
            module_name_node (ChamuyoNode): Node representing the module name.
        """
        self.module_name_node = module_name_node
        self.pos_start = self.module_name_node.pos_start
        self.pos_end = self.module_name_node.pos_end

    def __repr__(self) -> str:
        return f'ImportarNode({self.module_name_node})'
    
    def __str__(self) -> str:
        return f'ImportarNode({self.module_name_node})'
    
class ProbaSiBardeaNode:
    """ Represents a try-except code block in the AST """

    def __init__(self, try_body_node, bardo_name, except_body_node) -> None:
        """
        Initialize a ProbaSiBardeaNode.

        Args:
            try_body_node (Node): Node representing the node to try
            bardo_name (str): str representing the bardo name (should be a node actually, but will be implemented later on)
            except_body_node (Node): Node representing the node to execute in case of Bardo (exception)
        """
        self.try_body_node = try_body_node
        self.except_body_node = except_body_node
        self.bardo_name = bardo_name
        self.pos_start = self.try_body_node.pos_start
        self.pos_end = self.except_body_node.pos_end

    def __repr__(self) -> str:
        return f'ProbaSiBardeaNode({self.try_body_node}, {self.except_body_node})'
    
    def __str__(self) -> str:
        return f'ProbaSiBardeaNode({self.try_body_node}, {self.except_body_node})'

class BardeaNode:
    """ Represents a raise code expression in the AST """

    def __init__(self, bardo_name_tok, bardo_msg_node) -> None:
        """
        Initialize a BardeaNode.

        Args:
            bardo_name_tok (Token): Token representing the bardo name (should be a node actually, but will be implemented later on)
            bardo_msg_node (Node): Node representing the message to pass to the bardo.
        """
        self.bardo_name_tok = bardo_name_tok
        self.bardo_msg_node = bardo_msg_node
        self.pos_start = self.bardo_name_tok.pos_start
        self.pos_end = self.bardo_msg_node.pos_end

    def __repr__(self) -> str:
        return f'BardeaNode({self.bardo_name_tok}, {self.bardo_msg_node})'
    
    def __str__(self) -> str:
        return f'BardeaNode({self.bardo_name_tok}, {self.bardo_msg_node})'
