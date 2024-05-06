from errors import RTError
from .value import Value
from .boolean import Posta, Trucho

class Mataburros(Value):

    def __init__(self, keys, values):
        super().__init__()
        self.keys = keys
        self.values = values

    def copy(self):
        copy = Mataburros(self.keys, self.values)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        if len(self.keys) and len(self.values) > 0:
            return Posta(True).set_context(self.context), None

        return Trucho(False).set_context(self.context), None
    
    def __str__(self):
        return f'{{{", ".join([f"{k}: {v}" for k, v in zip(self.keys, self.values)])}}}'
        
    def __repr__(self):
        return f'{{{", ".join([f"{k}: {v}" for k, v in zip(self.keys, self.values)])}}}'