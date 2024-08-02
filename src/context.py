"""
Context module for the Lunfardo programming language.

This module defines the Context class, which represents the execution context
for Lunfardo code, including scope and symbol table information.
"""

class Context:
    """
    Represents an execution context in the Lunfardo language.

    The Context class maintains information about the current scope,
    including its parent context and symbol table.
    """

    def __init__(self, display_name, parent = None, parent_entry_pos = None) -> None:
        """
        Initialize a Context object.

        Args:
            display_name (str): A name for this context, used for display purposes.
            parent (Context, optional): The parent context, if any.
            parent_entry_pos (Position, optional): The position where this context was entered in the parent context.
        """
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None