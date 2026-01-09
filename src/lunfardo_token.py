"""
Token and Position classes for the Lunfardo programming language.

This module defines the Token class for representing lexical tokens and
the Position class for tracking positions within the source code.
"""

from typing import Self, Optional

class Position:
    """
    Represents a position in the source code.

    Keeps track of line number, column number, and index in the source text.
    """

    def __init__(self, idx, ln, col, fn, ftxt) -> None:
        """
        Initialize a Position object.

        Args:
            idx (int): Index in the source text.
            ln (int): Line number.
            col (int): Column number.
            fn (str): Filename.
            ftxt (str): Full text of the source code.
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char = None) -> Self:
        """
        Advance the position by one character.

        Args:
            current_char (str, optional): The current character being processed.

        Returns:
            Position: The updated position.
        """
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self) -> "Position":
        """
        Create a copy of the current position.

        Returns:
            Position: A new Position object with the same values.
        """
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
    
class Token:
    """
    Represents a lexical token in the Lunfardo language.
    """
    
    def __init__(self, 
                 type_: str, 
                 value: Optional[int | float | str] = None, 
                 pos_start: Optional[Position] = None, 
                 pos_end: Optional[Position] = None, 
                 orig_pos_start: Optional[Position] = None, 
                 orig_pos_end: Optional[Position] = None
                 ) -> None:
        """
        Initialize a Token object.
        An original position is a position that was not processed by the pre-processor.
        A processed position is a position that was pre-processed.
        Lunfardo needs both so if there's an error in the code, it can mark it properly.

        Args:
            type_ (str): The type of the token.
            value (Any, optional): The value of the token.
            pos_start (Position, optional): The starting processed position of the token.
            pos_end (Position, optional): The ending processed position of the token.
            orig_pos_start (Position, optional): The starting original position of the token.
            orig_pos_end (Position, optional): The ending original position of the token.

        Returns:
            None
        """
        self.type = type_
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.orig_pos_start = orig_pos_start
        self.orig_pos_end = orig_pos_end
        
        if pos_start is not None:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end is not None:
            self.pos_end = pos_end.copy()

        if orig_pos_start is None and self.pos_start:
            self.orig_pos_start = self.pos_start
        
        if orig_pos_end is None and self.pos_end:
            self.orig_pos_end = self.pos_end

    def matches(self, type_, value) -> bool:
        """
        Check if the token matches a given type and value.

        Args:
            type_ (str): The type to match.
            value (Any): The value to match.

        Returns:
            bool: True if the token matches, False otherwise.
        """
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        val_str = f"{self.value}" if self.value is not None else ""
        # Show original position by default for error reporting clarity
        pos_str = f"@{self.orig_pos_start}" if self.orig_pos_start else ""
        return f"[{self.type}: {val_str} {pos_str}]"