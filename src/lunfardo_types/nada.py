from .value import Value
from .boloodean import Boloodean

class Nada(Value):

    def __init__(self, value: None) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return "nada"

    def __repr__(self) -> str:
        return "nada"

    def copy(self) -> 'Nada':
        copy = Nada(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return False
    
    def notted(self) -> tuple["Boloodean", None]:
        if self.value:
            return Boloodean.trucho.set_context(self.context), None
        return Boloodean.posta.set_context(self.context), None

Nada.nada = Nada(None)
