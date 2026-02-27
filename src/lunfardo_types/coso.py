from .value import Value
from .boloodean import Boloodean
from typing import List


class Coso(Value):

    def __init__(self, elements: List) -> None:
        super().__init__()
        self.elements = elements

    def copy(self) -> 'Coso':
        copy = Coso(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self) -> bool:
        return bool(self.elements)

    def notted(self) -> tuple["Boloodean", None]:
        if self.elements:
            return Boloodean.trucho.set_context(self.context), None
        return Boloodean.posta.set_context(self.context), None

    def __str__(self) -> str:
        return f"{self.elements}"

    def __repr__(self) -> str:
        return f'[{", ".join([str(el) for el in self.elements])}]'
