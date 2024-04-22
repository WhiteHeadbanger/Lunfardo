from lunfardo_parser import RTResult
from constants.tokens import *
from lunfardo_types import Numero
from errors.errors import RTError

class SymbolTable:

    def __init__(self, parent = None):
        self.symbols = {}
        self.parent = parent

    #TODO: capaz implementar getters y setters pythonicos.
    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent is not None:
            return self.parent.get(name)
        
        return value
    
    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

class Interpreter:

    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumeroNode(self, node, context):
        return RTResult().success(
            Numero(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_ChamuyoNode(self, node, context):
        from lunfardo_types import Chamuyo
        
        return RTResult().success(
            Chamuyo(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_CualcaAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))
        
        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    
    def visit_CualcaAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        
        if res.error:
            return res
        
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

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
        
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res
        
        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multiplied_by(Numero(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'truchar'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        
        return res.success(number.set_pos(node.pos_start, node.pos_end))
    
    def visit_SiNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            
            if res.error:
                return res
            
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))

                if res.error:
                    return res
                
                return res.success(Numero.nada if should_return_null else expr_value)
        
        if node.else_case:
            expr, should_return_null = node.else_case
            else_value = res.register(self.visit(expr, context))

            if res.error:
                return res
            
            return res.success(Numero.nada if should_return_null else else_value)
        
        return res.success(Numero.nada)
    
    def visit_ParaNode(self, node, context):
        from lunfardo_types import Coso
        res = RTResult()
        elements = []
        
        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error:
            return res
        
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error:
            return res
        
        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error:
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

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error:
                return res
            
        return res.success(
            Numero.nada if node.should_return_null else
            Coso(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_MientrasNode(self, node, context):
        from lunfardo_types import Coso
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))

            if res.error:
                return res
            
            if not condition.is_true():
                break

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error:
                return res
        
        return res.success(
            Numero.nada if node.should_return_null else
            Coso(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_LaburoDefNode(self, node, context):
        from lunfardo_types import Laburo
        res = RTResult()

        # si la funcion es anonima, func_name = None
        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Laburo(func_name, body_node, arg_names, node.should_return_null).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)
        
        return res.success(func_value)
    
    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error:
            return res
        
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error:
                return res
            
        return_value = res.register(value_to_call.execute(args, context))
        if res.error:
            return res
        
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        
        return res.success(return_value)
    
    def visit_CosoNode(self, node, context):
        from lunfardo_types import Coso
        res = RTResult()

        elements = [res.register(self.visit(element_node, context)) for element_node in node.element_nodes]
        if res.error:
            return res

        return res.success(
            Coso(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )





