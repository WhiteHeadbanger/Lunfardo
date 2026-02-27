from .value import Value
from .boloodean import Boloodean

class Chamuyo(Value):

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
    
    def is_true(self) -> bool:
        return bool(self.value)
    
    def notted(self) -> tuple["Boloodean", None]:
        if self.value:
            return Boloodean.trucho.set_context(self.context), None
        return Boloodean.posta.set_context(self.context), None
    
    def copy(self) -> 'Chamuyo':
        copy = Chamuyo(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self) -> str:
        return f'"{self.value}"'

    def __repr__(self) -> str:
        return f'"{self.value}"'

    # Format is used for debugging purposes in src/chusma.py, to correctly show the value type without double quotes.
    # Must not be used in normal Lunfardo execution
    def __format__(self, format_spec) -> str:
        return f'{self.value}'