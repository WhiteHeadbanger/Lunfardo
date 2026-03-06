from src.errors import RTError
from typing import Callable

class OperatorRegistry:
    def __init__(self) -> None:
        self._ops = {}

    def register(self, op, left_type, right_type, fn) -> None:
        self._ops[(op, left_type, right_type)] = fn

    def dispatch(self, op, left, right, ctx=None):
        key = (op, type(left), type(right))
        if key not in self._ops:
            return None, RTError(
                pos_start=left.pos_start,
                pos_end=right.pos_end,
                details=f"Operación '{op}' no soportada entre "
                f"{type(left).__name__} y {type(right).__name__}",
                context=ctx,
            )
        
        fn: Callable = self._ops.get(key)
        return fn(left, right)

operators = OperatorRegistry()


