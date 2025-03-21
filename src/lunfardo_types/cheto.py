from .value import Value
from .laburo import Laburo
from rtresult import RTResult
from errors import RTError
from context import Context
from symbol_table import SymbolTable

class Cheto(Value):
    
    def __init__(self, name, methods, parent_context = None, parent_class = None):
        super().__init__()
        self.name = name
        self.methods: dict = methods
        self.parent_context = parent_context
        self.parent_class = parent_class
        self.context = Context(f"<cheto {self.name}>", parent_context)
        self.context.symbol_table = SymbolTable(parent_context.symbol_table if parent_context else None)

    def create_instance(self, args, call_context):
        """
        Creates a new cheto instance
        """
        res = RTResult()
        instance = ChetoInstance(self, call_context)

        # Inherit instance variables from parent class
        if self.parent_class:
            res_parent_instance = self.parent_class.create_instance(args if args else [], call_context)
            instance.instance_vars.update(res_parent_instance.value.instance_vars)

        # Call the arranque method if it exists
        arranque_method = self.methods.get("arranque")
        if arranque_method:
            res.register(self.call_method(instance, "arranque", args, call_context))
            if res.should_return():
                return res
            
        return res.success(instance)
    
    def get_method(self, method_name):
        """
        Retrieves a method from the cheto definition
        """
        method = self.methods.get(method_name)
        if not method and self.parent_class:
            method = self.parent_class.get_method(method_name)
        return method
    
    def call_method(self, instance, method_name, args, call_context):
        """
        Calls a method on a cheto's instance
        """
        res = RTResult()
        method = self.get_method(method_name)

        if not method:
            return res.failure(RTError(
                self.pos_start,
                self.pos_end,
                f"Método '{method_name}' no se encuentra en cheto '{self.name}'",
                call_context
            ))
        
        # Create a new execution context for the method call
        method_context = Context(f"<método {method_name}>", call_context)
        method_context.symbol_table = SymbolTable(call_context.symbol_table)

        # Set 'mi' in the method's context
        method_context.symbol_table.set("mi", instance)

        # Prepare arguments for the method call
        res.register(method.check_and_populate_args(method.arg_names, [instance] + args, method_context))
        if res.should_return():
            return res

        # Execute the method
        return_value = res.register(method.execute([instance] + args, method_context))
        if res.should_return():
            return res
        
        return res.success(return_value)

    def copy(self):
        """
        Creates a copy of the cheto definition
        """
        copy = Cheto(self.name, self.methods, self.parent_context, self.parent_class)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return f"<cheto {self.name}>"
    
    def __repr__(self):
        return f'Cheto({self.name}, {self.methods})'
    
class ChetoInstance(Value):
    """
    Represents an instance of a cheto in Lunfardo
    """
    def __init__(self, cheto, call_context):
        super().__init__()
        self.cheto = cheto
        self.name = cheto.name
        self.instance_vars = {}
        self.context = Context(f"<instancia de {cheto.name}>", call_context)
        self.context.symbol_table = SymbolTable(call_context.symbol_table)
        self.set_pos(cheto.pos_start, cheto.pos_end)

    def get_method(self, method_name):
        """
        Retrieves a method from the cheto definition
        """
        method = self.methods.get(method_name)
        if not method and self.parent_class:
            method = self.parent_class.get_method(method_name)
        return method

    def get_instance_var(self, var_name):
        """
        Retrieves an instance variable, including inherited variables.
        If the variable is not found, it tries to retrieve a method.
        If the method is also not found, None is returned.
        """
        value = self.instance_vars.get(var_name)
        if value is None and self.cheto.parent_class:
            parent_instance = self.cheto.parent_class.create_instance([], self.context).value
            value = parent_instance.get_instance_var(var_name)

        if value is None:
            method = self.cheto.get_method(var_name)
            if method:
                return method
        return value
    
    def set_instance_var(self, var_name, value):
        """
        Sets an instance variable
        """
        self.instance_vars[var_name] = value

    def execute(self, args, call_context):
        """
        Handles method calls on the instance
        """
        res = RTResult()

        if not args:
            return res.failure(RTError(
                self.pos_start,
                self.pos_end,
                "Se requiere el nombre del método",
                call_context
            ))
        
        method_name = args[0].value
        return self.cheto.call_method(self, method_name, args[1:], call_context)
    
    def copy(self):
        """
        Creates a copy of the instance
        """
        copy = ChetoInstance(self.cheto, self.context)
        copy.instance_vars = self.instance_vars.copy()
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return f"ChetoInstance({self.cheto.name})"
    
    def __str__(self):
        return f"<instancia de {self.cheto.name}>"