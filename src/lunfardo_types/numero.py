from errors import RTError
from .value import Value
from .boolean import Boolean

class Numero(Value):

    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def added_to(self, other):
        if isinstance(other, Numero):
            return Numero(self.value + other.value).set_context(self.context), None
        
        return None, Value.illegal_operation(self, other)
    
    def subtracted_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value - other.value).set_context(self.context), None
        
        return None, Value.illegal_operation(self, other)
    
    def multiplied_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value * other.value).set_context(self.context), None
        
        return None, Value.illegal_operation(self, other)
    
    def divided_by(self, other):
        if isinstance(other, Numero):
            if other.value == 0:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    'Division por cero',
                    self.context
                )
            return Numero(self.value / other.value).set_context(self.context), None 
        
        return None, Value.illegal_operation(self, other)
    
    def powered_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value ** other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def get_comparison_eq(self, other):
        if isinstance(other, (Numero, Boolean)):
            return Boolean(self.value == other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def get_comparison_ne(self, other):
        if isinstance(other, (Numero, Boolean)):
            return Boolean(self.value != other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def get_comparison_lt(self, other):
        if isinstance(other, Numero):
            return Boolean(self.value < other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def get_comparison_gt(self, other):
        if isinstance(other, Numero):
            return Boolean(self.value > other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def get_comparison_lte(self, other):
        if isinstance(other, Numero):
            return Boolean(self.value <= other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def get_comparison_gte(self, other):
        if isinstance(other, Numero):
            return Boolean(self.value >= other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def anded_by(self, other):
        if isinstance(other, (Numero, Boolean)):
            return Boolean(self.value and other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    def ored_by(self, other):
        if isinstance(other, (Numero, Boolean)):
            return Boolean(self.value or other.value).set_context(self.context), None
    
        return None, Value.illegal_operation(self, other)
    
    #Deprecated. There's Posta and Trucho boolean types now, instead of just numbers so it doesn't make sense to have this method.
    def notted(self):
        if isinstance(self, Numero):
            return Boolean(not self.value).set_context(self.context), None
    
    def is_true(self):
        return Boolean(self.value != 0).set_context(self.context), None
    
    def copy(self):
        copy = Numero(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)