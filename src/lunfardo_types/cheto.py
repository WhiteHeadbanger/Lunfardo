from .value import Value
from src.lunfardo_parser import RTResult
from src.errors import RTError

class Cheto(Value):
    
    def __init__(self, name, methods, context, instance_vars = None):
        super().__init__()
        self.name = name
        self.methods = methods
        self.instance_vars = {} if instance_vars is None else instance_vars
        self.context = context

    def get_method(self, method_name):
        method = self.methods.get(method_name, None)
        if method:
            method.global_context = self.context
        return method
    
    def set_instance_var(self, name, value):
        self.instance_vars[name] = value

    def get_instance_var(self, name):
        return self.instance_vars.get(name)

    def execute(self, args, context):
        res = RTResult()
        
        if len(args) == 0:
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                "Method name is required for cheto object execution",
                context
            ))
        
        method_name = args[0].value
        method = self.context.symbol_table.get(method_name)
        
        if not method:
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"'{method_name}' is not a method of '{self.name}'",
                context
            ))
        
        return_value = res.register(method.execute(args[1:], self.context))
        if res.should_return(): return res
        
        return res.success(return_value)

    def copy(self):
        copy = Cheto(self.name, self.methods, self.context, self.instance_vars)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return f'Cheto({self.name}, {self.methods})'