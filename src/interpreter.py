from rtresult import RTResult
from constants.tokens import *
from lunfardo_types import Numero, Nada
from errors.errors import RTError
from context import Context
from nodes import *
from typing import Union, NoReturn

LunfardoNode = Union[NumeroNode, ChamuyoNode, CosoNode, MataburrosNode, PoneleQueAccessNode,
                     PoneleQueAssignNode, BinOpNode, UnaryOpNode, SiNode, ParaNode,
                     MientrasNode, LaburoDefNode, ChetoDefNode, MethodCallNode,
                     InstanceNode, InstanceVarAssignNode, InstanceVarAccessNode,
                     CallNode, DevolverNode, ContinuarNode, RajarNode, ImportarNode]

class Interpreter:
    """
    Executes Lunfardo programs by interpreting the Abstract Syntax Tree (AST).

    This class contains methods to visit and evaluate different types of nodes
    in the AST, implementing the runtime behavior of Lunfardo programs. It
    handles variable assignments, function calls, arithmetic operations,
    control structures, and other language features defined in the Lunfardo
    specification.
    """

    def visit(self, node: LunfardoNode, context: Context) -> RTResult:
        """
        Visit and evaluate a node in the Abstract Syntax Tree.

        Args:
            node: The AST node to visit.
            context: The current execution context.

        Returns:
            The result of evaluating the node.
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node: LunfardoNode, context: Context) -> NoReturn:
        """
        Raise an exception for nodes without a defined visit method.

        Args:
            node: The AST node without a visit method.
            context: The current execution context.

        Raises:
            Exception: Indicating that no visit method is defined for the node type.
        """
        raise Exception(f"No se encuentra definido ningun 'visit_{type(node).__name__}' metodo")
    
    def visit_NumeroNode(self, node: NumeroNode, context: Context) -> RTResult:
        """
        Evaluate a NumeroNode (number literal) in the AST.

        Args:
            node: The NumeroNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing the Numero value.
        """
        return RTResult().success(
            Numero(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_ChamuyoNode(self, node: ChamuyoNode, context: Context) -> RTResult:
        """
        Evaluate a ChamuyoNode (string literal) in the AST.

        Args:
            node: The ChamuyoNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing the Chamuyo value.
        """
        from lunfardo_types import Chamuyo
        
        return RTResult().success(
            Chamuyo(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_PoneleQueAccessNode(self, node: PoneleQueAccessNode, context: Context) -> RTResult:
        """
        Evaluate a PoneleQueAccessNode (variable access) in the AST.

        Args:
            node: The PoneleQueAccessNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing the variable's value or RTError if not found.
        """
        res = RTResult()
        var_name = node.var_name_tok.value
        
        # Try getting the variable from the current context
        value = context.symbol_table.get(var_name)
        if value is None:
            # Determine where to start the module search:
            # If context has no modules, traverse from the parent; otherwise, start from the current context.
            search_context = context.parent if not context.modules else context
            value = Interpreter.find_in_parent_module(var_name, search_context)

        # If the variable still isn't found, return a failure response
        if value is None:
            return res.failure(RTError(
                node.pos_start, 
                node.pos_end,
                f"'{var_name}' no está definido",
                context
            ))
        
        #value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        value = value.set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    
    @staticmethod
    def find_in_parent_module(var_name: str, start_context: Context):
        """
        Traverse up from the given context until we find a module with submodules,
        then search its submodules for the variable.
        """
        parent_module = start_context
        # Traverse up until we find a module that has modules
        while parent_module and not parent_module.modules:
            parent_module = parent_module.parent

        if parent_module:
            for mod in parent_module.modules.values():
                value = mod.context.symbol_table.get(var_name)
                if value is not None:
                    return value
        return None
    
    def visit_PoneleQueAssignNode(self, node: PoneleQueAssignNode, context: Context) -> RTResult:
        """
        Evaluate a PoneleQueAssignNode (variable assignment) in the AST.

        Args:
            node: The PoneleQueAssignNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing the assigned value.
        """
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        
        if res.should_return():
            return res
        
        context.symbol_table.set(var_name, value)
        return res.success(value)
    
    def visit_AccessAndAssignNode(self, node: AccessAndAssignNode, context: Context) -> RTResult:
        """
        Evaluate an AccessAndAssignNode (variable assignment) in the AST.

        Args:
            node: The AccessAndAssignNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing the assigned value.
        """
        res = RTResult()
        var_name = node.var_name_tok.value

        if not context.symbol_table.get(var_name):
            return res.failure(
                RTError(
                    node.var_name_tok.pos_start,
                    node.var_name_tok.pos_end,
                    f"'{var_name}' no está definido",
                    context
                )
            )
        
        value = res.register(self.visit(node.value_node, context))
        
        if res.should_return():
            return res
        
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node: BinOpNode, context: Context) -> RTResult:
        """
        Evaluate a BinOpNode (binary operation) in the AST.

        This method handles various binary operations including:
        - Arithmetic: addition, subtraction, multiplication, division, power
        - Comparison: equality, inequality, less than, greater than, etc.
        - Logical: 'y' (and), 'o' (or)

        Args:
            node: The BinOpNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing the outcome of the binary operation or RTError if an error occurs.
        """
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))

        if res.should_return():
            return res
        
        right = res.register(self.visit(node.right_node, context))
        if res.should_return():
            return res

        error = None
        result = None
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)

        elif node.op_tok.type == TT_MINUS:
            result, error = left.subtracted_by(right)
        
        elif node.op_tok.type == TT_MUL:
            result, error = left.multiplied_by(right)
        
        elif node.op_tok.type == TT_DIV:
            result, error = left.divided_by(right)
        
        elif node.op_tok.type == TT_POW:
            result, error = left.powered_by(right)
        
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        
        elif node.op_tok.matches(TT_KEYWORD, 'y'):
            result, error = left.anded_by(right)
        
        elif node.op_tok.matches(TT_KEYWORD, 'o'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        
        return res.success(result.set_pos(node.pos_start, node.pos_end).set_context(context))

    def visit_UnaryOpNode(self, node: UnaryOpNode, context: Context) -> RTResult:
        """
        Evaluate a UnaryOpNode in the AST.

        Handles unary operations such as negation and logical NOT ('truchar').

        Args:
            node: The UnaryOpNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing the outcome of the unary operation.
        """
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return():
            return res
        
        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multiplied_by(Numero(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'truchar'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        
        return res.success(number.set_pos(node.pos_start, node.pos_end).set_context(context))
    
    def visit_SiNode(self, node: SiNode, context: Context) -> RTResult:
        """
        Evaluate a SiNode (if statement) in the AST.

        Processes conditional statements, including 'si' (if), 'osi' (elif),
        and 'sino' (else) clauses.

        Args:
            node: The SiNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing the value of the executed branch.
        """
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            
            if res.should_return():
                return res
            
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))

                if res.should_return():
                    return res
                
                return res.success(Nada.nada if should_return_null else expr_value)
        
        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))

            if res.should_return():
                return res
            
            return res.success(Nada.nada if should_return_null else expr_value)
        
        return res.success(Nada.nada)
    
    def visit_ParaNode(self, node: ParaNode, context: Context) -> RTResult:
        """
        Evaluate a ParaNode (for loop) in the AST.

        Executes a for loop, iterating from a start value to an end value,
        with an optional step value. Handles both numeric and custom iterable types.

        Args:
            node: The ParaNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing either Nada.nada if should_return_null
                    is True, or a Coso (list) of elements generated during iteration.

        Note:
            - Supports both positive and negative step values.
            - Handles continue and break statements within the loop.
            - Creates a new variable in the context for each iteration.
        """
        from lunfardo_types import Coso
        res = RTResult()
        elements = []
        
        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return():
            return res
        
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return():
            return res
        
        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return():
                return res
        else:
            step_value = Numero(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Numero(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue is False and res.loop_should_break is False:
                return res
            
            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)
            
        return res.success(
            Nada.nada if node.should_return_null else
            Coso(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_MientrasNode(self, node: MientrasNode, context: Context) -> RTResult:
        """
        Evaluate a MientrasNode (while loop) in the AST.

        Executes a while loop, repeatedly evaluating the condition and executing
        the body until the condition becomes false.

        Args:
            node: The MientrasNode to evaluate.
            context: The current execution context.

        Returns:
            RTResult: A runtime result containing either Nada.nada if should_return_null
                    is True, or a Coso (list) of elements generated during iteration.

        Note:
            - Supports break and continue statements within the loop.
            - Accumulates results of each iteration in a list if not returning Nada.
        """
        from lunfardo_types import Coso
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))

            if res.should_return():
                return res
            
            if not condition.is_true():
                break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue is False and res.loop_should_break is False:
                return res
            
            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)
        
        return res.success(
            Nada.nada if node.should_return_null else
            Coso(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_LaburoDefNode(self, node: LaburoDefNode, context: Context) -> RTResult:
        """
        Visit and interpret a LaburoDefNode (function definition node) in the Lunfardo language.

        This method creates a Laburo (function) object from the given LaburoDefNode, evaluates
        default argument values, and sets the function in the current context if it's not a method.

        Args:
            node (LaburoDefNode): The function definition node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the created Laburo object.

        Note:
            - Evaluates default argument values.
            - Sets the function in the context's symbol table if it's not a method.
        """
        from lunfardo_types import Laburo
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks.keys()]
        
        # Evaluate default values
        arg_values = []
        for arg_value in node.arg_name_toks.values():
            if arg_value:
                evaluated_value = res.register(self.visit(arg_value, context))
                if res.should_return(): return res
                arg_values.append(evaluated_value)
            else:
                arg_values.append(None)

        func_value = Laburo(func_name, body_node, arg_names, arg_values, node.should_auto_return).set_pos(node.pos_start, node.pos_end)
        func_value.is_method = node.is_method

        if not node.is_method:
            context.symbol_table.set(func_name, func_value)

        """ if node.var_name_tok:
            context.symbol_table.set(func_name, func_value) """
        
        return res.success(func_value)
    
    def visit_ChetoDefNode(self, node: ChetoDefNode, context: Context) -> RTResult:
        """
        Visit and interpret a ChetoDefNode (class definition node) in the Lunfardo language.

        This method creates a Cheto (class) object from the given ChetoDefNode, processes the
        'arranque' (constructor) method if present, and adds all defined methods to the class.

        Args:
            node (ChetoDefNode): The class definition node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the created Cheto object.

        Notes:
            - The 'arranque' method, if present, is treated as the class constructor.
            - All methods, including 'arranque', are marked as instance methods.
            - The class is added to the current context's symbol table.
        """
        from lunfardo_types import Cheto, Laburo
        res = RTResult()

        class_name = node.var_name_tok.value
        methods = {}
        parent_class = None

        # Process parent class, if any.
        if node.parent_class:
            parent_class_name = node.parent_class.value
            parent_class = context.symbol_table.get(parent_class_name)
            if not parent_class and context.modules:
                parent_class = context.get_module(parent_class_name)
                if not parent_class:
                    return res.failure(RTError(
                        node.pos_start,
                        node.pos_end,
                        f"'{parent_class_name}' no está definido",
                        context
                    ))
            
            if not isinstance(parent_class, Cheto):
                return res.failure(RTError(
                    node.pos_start,
                    node.pos_end,
                    f"'{parent_class_name}' no es un cheto",
                    context
                ))

        # Process methods
        for method_node in node.methods:
            method_value = res.register(self.visit(method_node, context))
            if res.should_return():
                return res
            if not isinstance(method_value, Laburo):
                return res.failure(RTError(
                    method_node.pos_start,
                    method_node.pos_end,
                    f"Se esperaba un laburo para el método '{method_node.var_name_tok.value}', pero se obtuvo '{type(method_value)}'",
                    context
                ))
            methods[method_node.var_name_tok.value] = method_value

        # Process constructor arranque method
        if node.arranque_method:
            arranque_method_value = res.register(self.visit(node.arranque_method, context))
            if res.should_return():
                return res
            if not isinstance(arranque_method_value, Laburo):
                return res.failure(RTError(
                    node.arranque_method.pos_start,
                    node.arranque_method.pos_end,
                    f"Se esperaba un laburo para el método '{node.arranque_method.var_name_tok.value}', pero se obtuvo '{type(node.arranque_method)}'",
                    context
                ))
            methods[node.arranque_method.var_name_tok.value] = arranque_method_value
        
        # Create the cheto definition
        cheto_value = Cheto(class_name, methods, context, parent_class).set_pos(node.pos_start, node.pos_end)
        context.symbol_table.set(class_name, cheto_value)

        return res.success(cheto_value)
    
    def visit_CallNode(self, node: CallNode, context: Context) -> RTResult:
        """
        Visit and interpret a CallNode (function call node) in the Lunfardo language.

        This method evaluates the callable object and its arguments, then executes the call.

        Args:
            node (CallNode): The function or method call node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the value returned by the call.

        Notes:
            - The callable object and all arguments are evaluated in the current context.
            - The return value is copied and its position and context are set before being returned.
        """
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return():
            return res
        
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res
            
        return_value = res.register(value_to_call.execute(args, context))
        if res.should_return():
            return res
        
        #return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return_value = return_value.set_pos(node.pos_start, node.pos_end).set_context(context)
        
        return res.success(return_value)
    
    def visit_MethodCallNode(self, node: MethodCallNode, context: Context) -> RTResult:
        """
        Visit and interpret a MethodCallNode (object method call node) in the Lunfardo language.

        This method evaluates the object, retrieves the specified method, and executes it with
        the given arguments.

        Args:
            node (MethodCallNode): The method call node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the value returned by the method call.

        Notes:
            - The object must be an instance of Cheto (class object).
            - The method is retrieved from the object using the method name.
            - The object itself is passed as the first argument to the method.
            - All other arguments are evaluated in the current context before being passed to the method.
        """
        from lunfardo_types import Chamuyo
        from lunfardo_types.cheto import ChetoInstance

        res = RTResult()

        base_object_name = node.object_tok.value
        access_chain = node.access_chain
        method_name = node.method_name_tok.value

        # Evaluate arguments
        args = []
        for arg_node in node.arg_nodes:
            arg_value = res.register(self.visit(arg_node, context))
            if res.should_return():
                return res
            args.append(arg_value)

        current_value = context.symbol_table.get(base_object_name)
        if not current_value:
            return res.failure(RTError(
                node.pos_start,
                node.pos_end,
                f"'{base_object_name}' no está definido",
                context
            ))
        
        # access_chain NO DEBE contener el nombre del método en el último índice.
        # sólo debe contener las variables que están entre base_object_name y method_name
        for access_token in access_chain:
            if isinstance(current_value, ChetoInstance):
                var_name = access_token.value
                current_value = current_value.get_instance_var(var_name)
                if current_value is None:
                    return res.failure(RTError(
                        node.pos_start,
                        node.pos_end,
                        f"La variable de instancia '{var_name}' no pudo ser encontrada en '{base_object_name}'",
                        context
                    ))
            
            else:
                return res.failure(RTError(
                    node.pos_start,
                    node.pos_end,
                    f"No se puede acceder al atributo '{access_token.value}' porque no pertenece a ninguna instancia de objeto",
                    context
                ))

        if not isinstance(current_value, ChetoInstance):
            return res.failure(RTError(
                node.pos_start,
                node.pos_end,
                f"'{base_object_name}' no es una instancia de un cheto",
                context
            ))

        # Call the method
        return_value = res.register(current_value.execute([Chamuyo(method_name)] + args, context))
        if res.should_return():
            return res
        
        return_value = return_value.set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_InstanceNode(self, node: InstanceNode, context: Context) -> RTResult:
        """
        Visit and interpret an InstanceNode (object instantiation node) in the Lunfardo language.

        This method creates a new instance of a Cheto (class) object, initializes it using the
        'arranque' method if present, and returns the new instance.

        Args:
            node (InstanceNode): The object instantiation node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the newly created instance.

        Notes:
            - The class must exist in the current context and be a Cheto object.
            - All arguments for the instance creation are evaluated in the current context.
            - If an 'arranque' method exists, it's called with the new instance as the first argument,
            followed by any additional arguments provided during instantiation.
        """
        from lunfardo_types import Cheto
        res = RTResult()

        class_name = node.class_name_tok.value
        class_value = context.symbol_table.get(class_name)

        if not class_value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"La clase '{class_name}' no está definida",
                context
            ))
        
        if not isinstance(class_value, Cheto):
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{class_name}' no es un cheto",
                context
            ))
        
        # Evaluate arguments
        args = []
        for arg_node in node.arg_nodes:
            arg_value = res.register(self.visit(arg_node, context))
            if res.should_return():
                return res
            args.append(arg_value)
        
        # Create the instance
        instance = res.register(class_value.create_instance(args, context))

        if res.should_return():
            return res
        
        #instance = instance.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(instance)
    
    def visit_InstanceVarAssignNode(self, node: InstanceVarAssignNode, context: Context) -> RTResult:
        """
        Visit and interpret an InstanceVarAssignNode (instance variable assignment node) in the Lunfardo language.

        This method evaluates the value to be assigned, retrieves the current context of the object,
        and sets the instance variable with the evaluated value.

        Args:
            node (InstanceVarAssignNode): The instance variable assignment node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the assigned instance variable value.

        Notes:
            - The assigned value is evaluated in the current context.
            - The instance variable is set in the object's own context.
            - The returned value is a copy of the assigned value, with position and context set.
        """
        from lunfardo_types.cheto import ChetoInstance
        res = RTResult()

        object_name = node.object_tok.value
        var_name = node.var_name_tok.value

        object_value = context.symbol_table.get(object_name)
        if not object_value:
            return res.failure(RTError(
                node.pos_start,
                node.pos_end,
                f"'{object_name}' no está definido",
                context
            ))
        
        if not isinstance(object_value, ChetoInstance):
            return res.failure(RTError(
                node.pos_start,
                node.pos_end,
                f"'{object_name}' no es una instancia de un cheto",
                context
            ))

        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        object_value.set_instance_var(var_name, value)
        return res.success(value)
    
    def visit_InstanceVarAccessNode(self, node: InstanceVarAccessNode, context: Context) -> RTResult:
        """
        Visit and interpret an InstanceVarAccessNode (instance variable access node) in the Lunfardo language.

        This method retrieves the value of an instance variable from a specified object.

        Args:
            node (InstanceVarAccessNode): The instance variable access node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the value of the accessed instance variable.

        Notes:
            - The method retrieves the object's context from the current symbol table.
            - If the instance variable is not defined, an RTError is returned.
            - The returned value is a copy of the instance variable, with position and context set.
        """
        from lunfardo_types.cheto import ChetoInstance
        res = RTResult()
        base_object_name = node.object_tok.value
        access_chain = node.access_chain

        current_value = context.symbol_table.get(base_object_name)
        if not current_value:
            return res.failure(RTError(
                node.pos_start,
                node.pos_end,
                f"'{base_object_name}' no está definido",
                context
            ))
        
        for access_token in access_chain:
            if isinstance(current_value, ChetoInstance):
                var_name = access_token.value
                current_value = current_value.get_instance_var(var_name)
                if current_value is None:
                    return res.failure(RTError(
                        node.pos_start,
                        node.pos_end,
                        f"La variable de instancia '{var_name}' no fue encontrada en '{base_object_name}'",
                        context
                    ))
            
            else:
                return res.failure(RTError(
                    node.pos_start,
                    node.pos_end,
                    f"No se puede acceder al atributo '{access_token.value}' porque no pertenece a ninguna instancia de cheto",
                    context
                ))
        
        current_value = current_value.set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(current_value)
    
    def visit_InstanceVarAccessAndAssignNode(self, node: InstanceVarAccessAndAssignNode, context: Context) -> RTResult:
        from lunfardo_types.cheto import ChetoInstance
        res = RTResult()

        base_object_name = node.instance_var_name_tok.value
        access_chain = node.access_chain.copy()
        var_to_assign = access_chain.pop().value

        current_value = context.symbol_table.get(base_object_name)
        if not current_value:
            return res.failure(RTError(
                node.pos_start,
                node.pos_end,
                f"'{base_object_name}' no está definido",
                context
            ))
        
        for access_token in access_chain:
            if isinstance(current_value, ChetoInstance):
                var_name = access_token.value
                current_value = current_value.get_instance_var(var_name)
                if current_value is None:
                    return res.failure(RTError(
                        node.pos_start,
                        node.pos_end,
                        f"La variable de instancia '{var_name}' no existe",
                        context
                    ))
                var_to_assign = var_name
            
            else:
                return res.failure(RTError(
                    node.pos_start,
                    node.pos_end,
                    f"No se puede acceder al atributo '{access_token.value}' porque no pertenece a ninguna instancia de cheto",
                    context
                ))
        
        new_value = res.register(self.visit(node.value_node, context))
        if res.should_return():
            return res
        
        current_value.set_instance_var(var_to_assign, new_value)
        return res.success(new_value)
    
    def visit_DevolverNode(self, node: DevolverNode, context: Context) -> RTResult:
        """
        Visit and interpret a DevolverNode (return node) in the Lunfardo language.

        This method evaluates the expression to be returned, if any, and signals a return operation.

        Args:
            node (DevolverNode): The return node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the value to be returned.

        Notes:
            - If no expression is provided, returns Nada (None) value.
            - Uses success_return to signal a return operation.
        """
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            
            if res.should_return():
                return res
        else:
            value = Nada.nada

        return res.success_return(value)
    
    def visit_ContinuarNode(self, node: ContinuarNode, context: Context) -> RTResult:
        """
        Visit and interpret a ContinuarNode (continue node) in the Lunfardo language.

        This method signals a continue operation in a loop.

        Args:
            node (ContinuarNode): The continue node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, signaling a continue operation.
        """
        return RTResult().success_continue()
    
    def visit_RajarNode(self, node: RajarNode, context: Context) -> RTResult:
        """
        Visit and interpret a RajarNode (break node) in the Lunfardo language.

        This method signals a break operation in a loop.

        Args:
            node (RajarNode): The break node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, signaling a break operation.
        """
        return RTResult().success_break()

    def visit_CosoNode(self, node: CosoNode, context: Context) -> RTResult:
        """
        Visit and interpret a CosoNode (list node) in the Lunfardo language.

        This method creates a Coso (list) object by evaluating each element node
        and adding it to the list.

        Args:
            node (CosoNode): The list node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the created Coso object.

        Notes:
            - Each element in the list is evaluated in the current context.
            - The resulting Coso object is set with the current context and position.
        """
        from lunfardo_types import Coso
        res = RTResult()

        elements = []
        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            Coso(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_MataburrosNode(self, node: MataburrosNode, context: Context) -> RTResult:
        """
        Visit and interpret a MataburrosNode (dictionary node) in the Lunfardo language.

        This method creates a Mataburros (dictionary) object by evaluating each key-value pair
        and adding them to the dictionary.

        Args:
            node (MataburrosNode): The dictionary node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the created Mataburros object.

        Notes:
            - Both keys and values are evaluated in the current context.
            - The resulting Mataburros object is set with the current context and position.
        """
        from lunfardo_types import Mataburros, Laburo
        res = RTResult()

        mataburros = Mataburros()

        for key_node, value_node in node.pairs:
            key = res.register(self.visit(key_node, context))
            if res.should_return():
                return res
            
            value = res.register(self.visit(value_node, context))
            if res.should_return():
                return res
            
            if isinstance(key, Laburo):
                return res.failure(
                    RTError(
                        key.pos_start,
                        key.pos_end,
                        "'laburo' no es hashable",
                        context
                    )
                )
            
            mataburros.set_pair(key, value)
            
        return res.success(
            mataburros.set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_ImportarNode(self, node: ImportarNode, context: Context) -> RTResult:
        """
        Visit and interpret an ImportarNode (import node) in the Lunfardo language.

        This method imports a module by executing the file.

        Args:
            node (ImportarNode): The import node to interpret.
            context (Context): The current execution context.

        Returns:
            RTResult: The result of the interpretation, containing the imported module.
        """

        from constants import BUILTINS
        res = RTResult()
        
        try: 
            module_name = node.module_name_node.var_name_tok.value
        except AttributeError: 
            return res.failure(RTError(
                node.pos_start,
                node.pos_end,
                'El nombre del módulo debe ser un identificador',
                context
            ))
        
        ejecutar_func = context.symbol_table.get("ejecutar").set_pos(node.pos_start, node.pos_end)
        
        module = res.register(self.visit_ChamuyoNode(ChamuyoNode(node.module_name_node.var_name_tok), context))
        if res.should_return():
            return res
        
        module.value += ".lunf"
        import_value = res.register(ejecutar_func.execute([module], context))
        if res.should_return():
            return res
        
        if module_name in BUILTINS:
            # Delegate library-specific handling.
            lib_result = Interpreter.handle_library_import(module_name, node, import_value.context, context)
            if lib_result.error:
                return res.failure(lib_result.error)
        
        context.add_module({module_name: import_value})
        
        return res.success(import_value)
    
    def visit_ProbaSiBardeaNode(self, node: ProbaSiBardeaNode, context: Context) -> RTResult:
        res = RTResult()

        try_value = res.register(self.visit(node.try_body_node, context))
        if res.should_return():
            if res.error is not None:
                if res.error.name == node.bardo_name:
                    except_value = res.register(self.visit(node.except_body_node, context))
                    
                    if res.should_return():
                        return res
                    
                    return res.success(except_value)
                return res
            return res
        return res.success(try_value)
    
    def visit_BardeaNode(self, node: BardeaNode, context: Context) -> RTResult:
        res = RTResult()
        from errors import (
            IllegalCharBardo,
            InvalidSyntaxBardo,
            ExpectedCharBardo,
            InvalidTypeBardo,
            InvalidIndexBardo,
            InvalidKeyBardo,
            InvalidValueBardo
        )

        AVAILABLE_BARDOS = {
            'caracter_ilegal': IllegalCharBardo,
            'sintaxis_invalida': InvalidSyntaxBardo,
            'caracter_esperado': ExpectedCharBardo,
            'bardo_de_tipo': InvalidTypeBardo,
            'bardo_de_indice': InvalidIndexBardo,
            'bardo_de_clave': InvalidKeyBardo,
            'bardo_de_valor': InvalidValueBardo
        }
        
        bardo_msg = res.register(self.visit(node.bardo_msg_node, context))
        if res.should_return():
            return res
        
        bardo_name = node.bardo_name_tok.value
        return res.failure(
            AVAILABLE_BARDOS[bardo_name](
                node.pos_start,
                node.pos_end,
                f"{bardo_msg.value}"
            )
        )
        


    @staticmethod
    def handle_library_import(lib_name: str, node: ImportarNode, module_context: Context, context: Context) -> RTResult:
        """
        Handles library-specific initialization logic in a generic way
        using a registry of library handlers.

        Args:
            lib_name (str): The name of the library.
            node (ImportarNode): The import node from the AST.
            module_context (Context): The module's execution context.
            context (Context): The parent context.

        Returns:
            RTResult: Success or failure based on the library handling.
        """
        from library_registry import get_library_handler
        
        res = RTResult()
        handler = get_library_handler(lib_name)
        if handler:
            return handler(module_context, node, context)
        
        return res.success(Nada.nada)





