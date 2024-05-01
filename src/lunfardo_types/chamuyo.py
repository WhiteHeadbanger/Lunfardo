from .value import Value
from .numero import Numero

class Chamuyo(Value):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Chamuyo):
            return Chamuyo(self.value + other.value).set_context(self.context), None
        
        return None, Value.illegal_operation(self, other)
    
    def multiplied_by(self, other):
        if isinstance(other, Numero):
            return Chamuyo(self.value * other.value).set_context(self.context), None
        
        return None, Value.illegal_operation(self, other)
    
    def get_comparison_eq(self, other):
        if isinstance(other, (Chamuyo, Numero)):
            return Numero(int(self.value == other.value)).set_context(self.context), None
    
        return None, Value.illegal_operation(self.pos_start, other.pos_end)
    
    def get_comparison_ne(self, other):
        if isinstance(other, (Chamuyo, Numero)):
            return Numero(int(self.value != other.value)).set_context(self.context), None
    
        return None, Value.illegal_operation(self.pos_start, other.pos_end)
    
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = Chamuyo(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return f'"{self.value}"'

    def __repr__(self):
        return f'"{self.value}"'