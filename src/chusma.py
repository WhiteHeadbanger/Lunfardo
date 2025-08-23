from .context import Context
from .interpreter import Interpreter
from .lunfardo_types import Chamuyo

class Chusma:

    def __init__(self, interpreter: Interpreter, context: Context, res) -> None:
        self.interpreter = interpreter
        self.context = context
        self.res = res
        self.matear_func = context.symbol_table.get("matear")

    def print_internals(self) -> None:
        # print title
        title = Chamuyo("┌─[Lunfardo Chusma]─────────────────────────────┐")
        self.res.register(self.matear_func.execute([title], self.context, self))

        frame_name = self.context.display_name if hasattr(self.context, "display_name") else str(self.context)
        frame_str = Chamuyo(f"│ Frame: {frame_name:<39}│")
        self.res.register(self.matear_func.execute([frame_str], self.context, self))

        raw_symbols: dict = self.context.symbol_table.symbols
        for sym, value in raw_symbols.items():
            self.res.register(self.matear_func.execute([Chamuyo(f'│   {sym:<12} → {str(value):<29}│')], self.context, self))

        # print footer
        self.res.register(self.matear_func.execute([Chamuyo("│                                               │")], self.context, self))
        self.res.register(self.matear_func.execute([Chamuyo("│ [Presioná Enter para seguir]                  │")], self.context, self))
        self.res.register(self.matear_func.execute([Chamuyo("└───────────────────────────────────────────────┘")], self.context, self))

        # call morfar
        morfar_func = self.context.symbol_table.get("morfar")
        self.res.register(morfar_func.execute([], self.context, self))