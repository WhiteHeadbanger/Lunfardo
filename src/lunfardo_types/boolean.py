from .value import Value

class Boolean(Value):

    def __init__(self, value):
        super().__init__()
        self.value = value
    
class Posta(Boolean):

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "posta"
    
    def __repr__(self):
        return "posta"
    
    def is_true(self):
        return True
    
    def copy(self):
        copy = Posta(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
class Trucho(Boolean):

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "trucho"
    
    def __repr__(self):
        return "trucho"
    
    def is_true(self):
        return False
    
    def copy(self):
        copy = Trucho(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
Posta.posta = Posta(True)
Trucho.trucho = Trucho(False)
