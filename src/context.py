"""
Context module for the Lunfardo programming language.

This module defines the Context class, which represents the execution context
for Lunfardo code, including scope and symbol table information.
"""

from typing import Dict, Optional

class Context:
    """
    Represents an execution context in the Lunfardo language.

    The Context class maintains information about the current scope,
    including its parent context and symbol table.
    """
    
    def __init__(self, display_name, parent = None, parent_entry_pos = None, cwd = None, file = None) -> None:
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
        self.cwd = cwd
        self.file = file
        self.symbol_table = None
        self.modules = {}

    def get_cwd(self):
        """
        Retrieve the current working directory for this context.
        """
        cwd = self.cwd
        if cwd is None and self.parent:
            cwd = self.parent.get_cwd()
        return cwd

    def get_file(self) -> str | None:
        """
        Retrieve the current file for this context.
        """
        file = self.file
        if file is None and self.parent:
            file = self.parent.get_file()
        return file
    
    def get_parent(self) -> Optional["Context"]:
        """
        Retrieve the parent context for this context.
        """
        return self.parent
    
    def add_module(self, module: Dict) -> None:
        """
        Add a module to this context.
        """
        self.modules.update(module)

    def get_module(self, module_name: str):
        """
        Retrieve a module from this context.
        """
        for i, (_, v) in enumerate(self.modules.items()):
            if v.elements[i].name == module_name:
                return v.elements[i]
        return self.modules.get(module_name)
