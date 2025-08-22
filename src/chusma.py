from .context import Context
from .interpreter import Interpreter
from .lunfardo_types import Chamuyo

class Chusma:

    def __init__(self, interpreter: Interpreter, context: Context, res) -> None:
        self.interpreter = interpreter
        self.context = context
        self.res = res
        self.title = Chamuyo("[Lunfardo Chusma]")
        self.matear_func = context.symbol_table.get("matear")

    def print_internals(self) -> None:
        raw_symbols: dict = self.context.symbol_table.symbols

        # print title
        self.res.register(self.matear_func.execute([self.title], self.context, self))

        # print symbols
        for sym, value in raw_symbols.items():
            self.res.register(self.matear_func.execute([Chamuyo(f'{sym}: {value}')], self.context, self))