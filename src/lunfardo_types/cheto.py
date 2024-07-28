from .value import Value
from lunfardo_parser import RTResult
from interpreter import SymbolTable, Interpreter
from context import Context
from errors import RTError

class Cheto(Value):
    
    def __init__(self, name, methods):
        super().__init__()
        self.name = name
        self.methods = methods

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def copy(self):
        copy = Cheto(self.name, self.methods)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return f'Cheto({self.name}, {self.methods})'