from .value import Value

class Boloodean(Value):

    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def is_true(self) -> bool:
        return self.value
    
    def notted(self) -> tuple["Boloodean", None]:
        if self.value:
            return Boloodean.trucho.set_context(self.context), None
        return Boloodean.posta.set_context(self.context), None

    def copy(self) -> 'Boloodean':
        copy = Boloodean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self) -> str:
        return "posta" if self.value else "trucho"

    def __repr__(self) -> str:
        return "posta" if self.value else "trucho"


Boloodean.posta = Boloodean(True)
Boloodean.trucho = Boloodean(False)
