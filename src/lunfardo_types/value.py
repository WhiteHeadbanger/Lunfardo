from abc import ABC, abstractmethod
from src.errors import RTError
from src.rtresult import RTResult
from typing import Self, Optional, Tuple


class Value(ABC):
    """
    Base class for all value types in the Lunfardo language.

    This class provides a common interface for operations, comparisons,
    and error handling for all value types.
    """

    def __init__(self) -> None:
        self.set_pos()
        self.set_context()
        
        from src.runtime.op_registry import operators
        self.operators = operators

    def set_pos(self, pos_start=None, pos_end=None) -> Self:
        """
        Set the start and end positions of this value in the source code.

        Args:
            pos_start: The starting position of the value.
            pos_end: The ending position of the value.

        Returns:
            self: The Value object for method chaining.
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None) -> Self:
        """
        Set the context for this value.

        Args:
            context: The context to set for this value.

        Returns:
            self: The Value object for method chaining.
        """
        self.context = context
        return self

    def added_to(self, other: "Value") -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform addition with another value.

        Args:
            other: The value to add to this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("+", self, other, self.context)

    def subtracted_by(
        self, other: "Value"
    ) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform subtraction with another value.

        Args:
            other: The value to add to this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("-", self, other, self.context)

    def multiplied_by(
        self, other: "Value"
    ) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform multiplication with another value.

        Args:
            other: The value to add to this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("*", self, other, self.context)

    def divided_by(self, other: "Value") -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform divition with another value.

        Args:
            other: The value to add to this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("/", self, other, self.context)

    def powered_by(self, other: "Value") -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform exponentiation with another value.

        Args:
            other: The value to add to this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("^", self, other, self.context)

    def get_comparison_eq(
        self, other: "Value"
    ) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform equality comparison with another value.

        Args:
            other: The value to compare with this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("==", self, other, self.context)

    def get_comparison_ne(
        self, other: "Value"
    ) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform negated equality comparison with another value.

        Args:
            other: The value to compare with this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("!=", self, other, self.context)

    def get_comparison_lt(
        self, other: "Value"
    ) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform less-than comparison with another value.

        Args:
            other: The value to compare with this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("<", self, other, self.context)

    def get_comparison_gt(
        self, other: "Value"
    ) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform greater-than comparison with another value.

        Args:
            other: The value to compare with this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch(">", self, other, self.context)

    def get_comparison_lte(
        self, other: "Value"
    ) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform less-than-equality comparison with another value.

        Args:
            other: The value to compare with this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("<=", self, other, self.context)

    def get_comparison_gte(
        self, other: "Value"
    ) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform greater-than-equality comparison with another value.

        Args:
            other: The value to compare with this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch(">=", self, other, self.context)

    def anded_by(self, other: "Value") -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform logical AND operation with another value.

        Args:
            other: The value to AND with this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("y", self, other, self.context)

    def ored_by(self, other: "Value") -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform logical OR operation with another value.

        Args:
            other: The value to AND with this one.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return self.operators.dispatch("o", self, other, self.context)

    
    def notted(self) -> Tuple[Optional["Value"], Optional[RTError]]:
        """
        Perform logical NOT operation on this value.

        Returns:
            A tuple containing the result and any error that occurred.
        """
        return None, self.illegal_operation(self)

    def illegal_operation(self, other=None) -> RTError:
        """
        Create an error for an illegal operation.

        Args:
            other: The other value involved in the illegal operation, if any.

        Returns:
            An RTError object describing the illegal operation.
        """
        if other is None:
            other = self

        return RTError(self.pos_start, other.pos_end, "Operación Ilegal", self.context)

    def execute(self) -> RTResult:
        """
        Execute this value (for callable types).

        Returns:
            An RTResult object containing the result of the execution.
        """
        return RTResult().failure(self.illegal_operation())

    @abstractmethod
    def copy(self) -> None:
        """
        Create a copy of this value.

        Returns:
            A copy of the Value object.
        """

    @abstractmethod
    def is_true(self) -> bool:
        """
        Determine if this value is considered true (used by the interpreter internals).

        Returns:
            A boolean indicating whether this value is considered true.
        """

    @abstractmethod
    def __str__(self) -> str:
        """
        Get the string representation of this value.

        Returns:
            A string representing this value.
        """

    @abstractmethod
    def __repr__(self) -> str:
        """
        Get the official string representation of this value.

        Returns:
            A string representing this value.
        """
