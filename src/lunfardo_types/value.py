#TODO: implentar Value como una abstract class
from errors import RTError

class Value:

    def __init__(self):
        self.set_pos()
        self.set_context()

    #TODO: capaz implementar getters y setters pythonicos.
    def set_pos(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context = None):
        self.context = context
        return self
    
    def added_to(self, other):
        return None, self.illegal_operation(other)
    
    def subtracted_by(self, other):
        return None, self.illegal_operation(other)
    
    def multiplied_by(self, other):
        return None, self.illegal_operation(other)
    
    def divided_by(self, other):
        return None, self.illegal_operation(other)
    
    def powered_by(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)
    
    def anded_by(self, other):
        return None, self.illegal_operation(other)
    
    def ored_by(self, other):
        return None, self.illegal_operation(other)
    
    def notted(self):
        return None, self.illegal_operation()
    
    def illegal_operation(self, other = None):
        if other is None:
            other = self
        
        return RTError(
            self.pos_start,
            other.pos_end,
            'Illegal operation',
            self.context
        )
    
    def execute(self):
        return None, self.illegal_operation()
    
