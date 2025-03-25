"""
Context module for the Lunfardo programming language.

This module defines the Context class, which represents the execution context
for Lunfardo code, including scope and symbol table information.
"""

from typing import Optional

class Context:
    """
    Represents an execution context in the Lunfardo language.

    The Context class maintains information about the current scope,
    including its parent context and symbol table.
    """

    from lunfardo_token import Position

    def __init__(self, display_name: str, parent: Optional["Context"] = None, parent_entry_pos: Optional[Position] = None, cwd: str | None = None, file: str | None = None) -> None:
        """
        Initialize a Context object.

        Args:
            display_name (str): A name for this context, used for display purposes.
            parent (Context, optional): The parent context, if any.
            parent_entry_pos (Position, optional): The position where this context was entered in the parent context.
            cwd (str, optional): The current working directory for this context.
            file (str, optional): The filename associated with this context.
        """
        self._display_name = display_name
        self._parent = parent
        self._parent_entry_pos = parent_entry_pos
        self._cwd = cwd
        self._file = file
        self._symbol_table = None

    @property
    def display_name(self) -> str:
        """
        Get the display name for this context.

        Returns:
            str: The display name.
        """
        return self._display_name
    
    @property
    def parent(self) -> Optional["Context"]:
        """
        Get the parent context for this context.

        Returns:
            Context: The parent context.
        """
        return self._parent
    
    @property
    def parent_entry_pos(self) -> Optional["Position"]:
        """
        Get the position where this context was entered in the parent context.

        Returns:
            Position: The position where this context was entered.
        """
        return self._parent_entry_pos
    
    @property
    def cwd(self) -> str | None:
        """
        Get the current working directory for this context.

        Returns:
            str: The current working directory.
        """

        return self._cwd
    
    @property
    def file(self) -> str | None:
        """
        Get the filename associated with this context.

        Returns:
            str: The filename.
        """
        return self._file
    
    @property
    def symbol_table(self):
        """
        Get the symbol table for this context.

        Returns:
            SymbolTable: The symbol table.
        """
        return self._symbol_table
    
    @display_name.setter
    def display_name(self, value: str) -> None:
        """
        Set the display name for this context.

        Args:
            value (str): The new display name.
        """
        if value is None:
            value = ""
        
        if not isinstance(value, str):
            raise TypeError("Context display name must be a string.")
        
        self._display_name = value

    @parent.setter
    def parent(self, value: "Context") -> None:
        """
        Set the parent context for this context.

        Args:
            value (Context): The new parent context.
        """
        if not isinstance(value, Context):
            raise TypeError("Context parent must be a Context object.")
        
        self._parent = value

    @parent_entry_pos.setter
    def parent_entry_pos(self, value) -> None:
        """
        Set the position where this context was entered in the parent context.

        Args:
            value (Position): The new entry position.
        """
        from lunfardo_token import Position

        if not isinstance(value, Position):
            raise TypeError("Context parent entry position must be a Position object.")
        
        self._parent_entry_pos = value

    @cwd.setter
    def cwd(self, value: str) -> None:
        """
        Set the current working directory for this context.

        Args:
            value (str): The new working directory.
        """
        if value is None:
            value = ""

        if not isinstance(value, str):
            raise TypeError("Context working directory must be a string.")
        
        self._cwd = value

    @file.setter
    def file(self, value: str) -> None:
        """
        Set the filename associated with this context.

        Args:
            value (str): The new filename.
        """
        if value is None:
            value = ""

        if not isinstance(value, str):
            raise TypeError("Context filename must be a string.")
        
        self._file = value

    @symbol_table.setter
    def symbol_table(self, value) -> None:
        """
        Set the symbol table for this context.

        Args:
            value (SymbolTable): The new symbol table.
        """
        from symbol_table import SymbolTable
        
        if not isinstance(value, SymbolTable):
            raise TypeError("Context symbol table must be a SymbolTable object.")
        
        self._symbol_table = value