from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from src.lunfardo_types import LUNFARDO_TYPES

# Run Time Result
class RTResult:
    """
    Represents the result of running a node in the interpreter.

    This class keeps track of the return value, error state, and loop control
    flow for the interpreted code.
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        from src.lunfardo_types import Nada
        self.value: "LUNFARDO_TYPES" = Nada.nada
        self.error = None
        self.func_return_value: "LUNFARDO_TYPES | None" = None
        self.loop_should_continue: bool = False
        self.loop_should_break: bool = False

    def register(self, res: "RTResult") -> "LUNFARDO_TYPES":
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break

        return res.value

    def success(self, value) -> Self:
        self.reset()
        self.value = value
        return self

    def success_return(self, value) -> Self:
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self) -> Self:
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self) -> Self:
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self, error) -> Self:
        self.reset()
        self.error = error
        return self

    def should_return(self) -> bool:
        return (
            self.error
            or self.func_return_value
            or self.loop_should_continue
            or self.loop_should_break
        )