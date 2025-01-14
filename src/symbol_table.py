from typing import Optional, Any

class SymbolTable:
    """
    Manages symbol tables for variable and function scoping in Lunfardo.

    This class implements a symbol table with support for nested scopes,
    allowing for efficient symbol lookup and management across different
    levels of the program execution.
    """

    def __init__(self, parent: Optional["SymbolTable"] = None) -> None:
        """
        Initialize a new SymbolTable.

        Args:
            parent (SymbolTable, optional): Parent symbol table for nested scopes.
        """
        self.symbols = {}
        self.parent = parent

    #TODO: getters y setters pythonicos.
    def get(self, name: str) -> Any | None:
        """
        Retrieve a symbol's value from the current or parent scopes.

        Args:
            name (str): The name of the symbol to retrieve.

        Returns:
            The value associated with the symbol, or None if not found.
        """
        value = self.symbols.get(name, None)
        if value is None and self.parent is not None:
            return self.parent.get(name)
        
        return value
    
    def set(self, name: str, value) -> None:
        """
        Set a symbol's value in the current scope.

        Args:
            name (str): The name of the symbol.
            value: The value to associate with the symbol.
        """
        self.symbols[name] = value

    def remove(self, name) -> None:
        """
        Remove a symbol from the current scope.

        Args:
            name (str): The name of the symbol to remove.
        """
        del self.symbols[name]