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
        for frame_name, context_for_frame in zip(self.get_stack(), self.get_context_stack()):
            # :<40 -> Formats the string to a 40-character width, padding with spaces on the right.
            frame_str = Chamuyo(f"│ Frame: {str(frame_name):<39}│")
            self.res.register(self.matear_func.execute([frame_str], self.context, self))

            raw_symbols: dict = context_for_frame.symbol_table.symbols

            # print symbols
            for sym, value in raw_symbols.items():
                self.res.register(self.matear_func.execute([Chamuyo(f'│   {sym:<12} → {str(value):<29}│')], self.context, self))

        # print end
        self.res.register(self.matear_func.execute([Chamuyo("│                                               │")], self.context, self))
        self.res.register(self.matear_func.execute([Chamuyo("│ [Presioná Enter para seguir]                  │")], self.context, self))
        self.res.register(self.matear_func.execute([Chamuyo("└───────────────────────────────────────────────┘")], self.context, self))
        
        morfar_func = self.context.symbol_table.get("morfar")
        self.res.register(morfar_func.execute([], self.context, self))


    def get_stack(self):
        for frame in reversed(self.interpreter.call_stack):
            yield frame.name

    def get_context_stack(self):
        current = self.context
        while current.parent is not None:
            yield current
            current = current.parent