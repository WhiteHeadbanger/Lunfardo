from .value import Value

class Nada(Value):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_comparison_eq(self, other):
        from . import Numero, Chamuyo, Nada, Boolean
        if isinstance(other, (Numero, Boolean, Chamuyo, Nada)):
            return Boolean(self.value == other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def get_comparison_ne(self, other):
        from . import Numero, Chamuyo, Nada, Boolean
        if isinstance(other, (Numero, Boolean, Chamuyo, Nada)):
            return Boolean(self.value != other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)

    def __str__(self):
        return "nada"
    
    def __repr__(self):
        return "nada"
    
    def copy(self):
        copy = Nada(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
Nada.nada = Nada(None)