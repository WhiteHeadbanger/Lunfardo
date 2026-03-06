from src.context import Context
from src.interpreter import Interpreter
from src.lunfardo_types import Chamuyo, Curro
from src.rtresult import RTResult

class Chusma:
    TITLE = "Chusmeando"
    PROMPT_LINE = "[Presioná Enter para seguir]"
    MIN_NAME_COL = 20  # minimum width for the variable name column
    MIN_TYPE_COL = 12
    VAR_PREFIX = "  "  # two spaces so it appears as "│   <var_name> → ..."

    def __init__(self, interpreter: Interpreter, context: Context, res: RTResult) -> None:
        self.interpreter = interpreter
        self.context = context
        self.res = res
        self.matear_func: Curro | None = context.symbol_table.get("matear") if context.symbol_table else None
        self.tipo_func: Curro | None = context.symbol_table.get("tipo") if context.symbol_table else None

    def print_internals(self) -> None:
        frame_name = getattr(self.context, "display_name", self.context.get_file())
        raw_symbols: dict = self.context.symbol_table.symbols if self.context.symbol_table else {}

        # dynamic padding: name column width and box inner width
        name_col = max(self.MIN_NAME_COL, max((len(str(s)) for s in raw_symbols.keys()), default=0))
        type_col = self.MIN_TYPE_COL

        # build content lines (without borders)
        lines = []
        lines.append(f"Frame: {frame_name}")
        for sym, value in raw_symbols.items():
            # Execute the 'tipo' laburo within the Lunfardo context
            if self.tipo_func is not None:
                type_value = self.res.register(self.tipo_func.execute([value], self.context, None))
                type_value_str = f'[{type_value}]'
                # Build the whole line
                lines.append(f"{self.VAR_PREFIX}{sym:<{name_col}}{type_value_str:<{type_col}} → {str(value)}")
            else:
                lines.append(f"{self.VAR_PREFIX}{sym:<{name_col}} → {str(value)}")
        lines.append("")  # visual separator before the prompt
        lines.append(self.PROMPT_LINE)

        # inner width: the longest line
        inner_width = max(len(line) for line in lines)
        # ensure the top bar with title has space for at least "─[" + TITLE + "]─"
        inner_width = max(inner_width, len(self.TITLE) + 1)

        # print box
        self._out(self._top_line(self.TITLE, inner_width))
        for line in lines:
            self._out(self._content_line(line, inner_width))
        self._out(self._bottom_line(inner_width))

        # Pause
        morfar_func = self.context.symbol_table.get("morfar") if self.context.symbol_table else None
        if morfar_func is not None:
            self.res.register(morfar_func.execute([], self.context, None))

    def _top_line(self, title: str, inner_width: int) -> str:
        # it is required that the sum of: "─[" + title + "]" + padding "─" == inner_width + 2  (the +2 accounts for the side spaces used in content lines: "│ " + ... + " │")
        fixed = len(title) + 3  # "─[" + title + "]"
        dashes = max(0, inner_width + 2 - fixed)
        return f"┌─[{title}]{'─' * dashes}┐"

    def _bottom_line(self, inner_width: int) -> str:
        return f"└{'─' * (inner_width + 2)}┘"

    def _content_line(self, text: str, inner_width: int) -> str:
        # format: "│ " + content.ljust(inner_width) + " │"
        return f"│ {text.ljust(inner_width)} │"

    def _out(self, text: str) -> None:
        if self.matear_func is not None:
            self.res.register(self.matear_func.execute([Chamuyo(text)], self.context, None))
