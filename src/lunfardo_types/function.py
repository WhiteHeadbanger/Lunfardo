from .value import Value
from lunfardo_parser import RTResult
from interpreter import SymbolTable, Interpreter
from context import Context
from errors import RTError


class Function(Value):

    def __init__(self, name, body_node, arg_names):
        super().__init__()
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args, current_context):
        res = RTResult()
        # Cada vez que creamos una nueva funcion, es necesario crear un nuevo contexto con una nueva symbol table, que son destruidos una vez que la funcion retorna.
        interpreter = Interpreter()
        context = Context(self.name, self.context, self.pos_start)
        context.symbol_table = SymbolTable(context.parent.symbol_table)

        if len(args) > len(self.arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"too many args passed into '{self.name}' (expected {len(self.arg_names)}, got {len(args)})",
                self.context
            ))
        
        if len(args) < len(self.arg_names):
            return res.failure(RTError(
                self.pos_start,
                self.pos_end,
                f"too few args passed into '{self.name}' (expected {len(self.arg_names)}, got {len(args)})",
                self.context
            ))
        
        for i, arg_name in enumerate(self.arg_names):
            arg_value = args[i]
            arg_value.set_context(context)
            context.symbol_table.set(arg_name, arg_value)
        
        value = res.register(interpreter.visit(self.body_node, context))
        if res.error:
            return res
        
        return res.success(value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    
    def __repr__(self):
        return f"<laburo {self.name}>"




