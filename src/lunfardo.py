"""
Main execution module for the Lunfardo programming language.

This module contains the global symbol table setup, execution function,
and the main REPL (Read-Eval-Print Loop) for the Lunfardo interpreter.
"""

from pathlib import Path
from typing import Tuple
from lexer import Lexer
from lunfardo_parser import Parser
from lunfardo_types import Curro, Boloodean, Nada
from interpreter import Interpreter
from symbol_table import SymbolTable
from context import Context

class Lunfardo:

    def __init__(self) -> None:
        self.global_symbol_table = SymbolTable()
        self._setup_global_symbol_table()

    def _setup_global_symbol_table(self) -> None:
        self.global_symbol_table.set("nada", Nada.nada)
        self.global_symbol_table.set("posta", Boloodean.posta)
        self.global_symbol_table.set("trucho", Boloodean.trucho)
        # I/O
        self.global_symbol_table.set("matear", Curro.matear)
        self.global_symbol_table.set("morfar", Curro.morfar)
        # Types
        self.global_symbol_table.set("es_num", Curro.es_num)
        self.global_symbol_table.set("es_chamu", Curro.es_chamu)
        self.global_symbol_table.set("es_coso", Curro.es_coso)
        self.global_symbol_table.set("es_laburo", Curro.es_laburo)
        self.global_symbol_table.set("es_mataburros", Curro.es_mataburros)
        self.global_symbol_table.set("chamu", Curro.chamu)
        self.global_symbol_table.set("num", Curro.num)
        # Coso related
        self.global_symbol_table.set("guardar", Curro.guardar)
        self.global_symbol_table.set("insertar", Curro.insertar)
        self.global_symbol_table.set("cambiaso", Curro.cambiaso)
        self.global_symbol_table.set("sacar", Curro.sacar)
        self.global_symbol_table.set("extender", Curro.extender)
        # Mataburros related
        self.global_symbol_table.set("agarra_de", Curro.agarra_de)
        self.global_symbol_table.set("metele_en", Curro.metele_en)
        self.global_symbol_table.set("borra_de", Curro.borra_de)
        self.global_symbol_table.set("existe_clave", Curro.existe_clave)
        # Misc
        self.global_symbol_table.set("linpiavidrios", Curro.limpiavidrios)
        self.global_symbol_table.set("winpiavidrios", Curro.limpiavidrios)
        self.global_symbol_table.set("longitud", Curro.longitud)
        self.global_symbol_table.set("ejecutar", Curro.ejecutar)
        self.global_symbol_table.set("renuncio", Curro.renuncio)
        self.global_symbol_table.set("contexto", Curro.contexto_global)
        self.global_symbol_table.set("asciiAchamu", Curro.asciiAchamu)

    @staticmethod
    def execute(self, fn: str, text: str, cwd: str = None, file_path: str = None, parent_context: Context = None) -> Tuple:
        """
        Execute Lunfardo code.

        Args:
            fn (str): The filename or source identifier.
            text (str): The Lunfardo code to execute.

        Returns:
            tuple: A tuple containing the execution result and any error encountered.
        """
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        if error:
            return None, error

        # Generate AST
        parser = Parser(tokens)
        ast, eof = parser.parse()

        # Fixing bug with only EOF token
        if eof:
            return None, None

        if ast.error:
            return None, ast.error

        # Run
        interpreter = Interpreter()
        context = Context(fn, cwd = cwd, file = file_path)
        context.symbol_table = self.global_symbol_table
        if parent_context:
            context.parent = parent_context
        
        result = interpreter.visit(ast.node, context)

        return result.value, result.error

    def execute_file(self, script_path: str) -> None:
        """Execute a Lunfardo file."""
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                code = f.read()
            file_path = Path(script_path)
            result, error = self.execute(fn=file_path, text=code, cwd=file_path.parent)

            if error:
                print(error.as_string())

        except FileNotFoundError:
            print(f"Error: File '{script_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def run_repl(self) -> None:
        """Run the Lunfardo REPL (Read-Eval-Print Loop)."""
        default_color = "\x1b[;;m"
        while True:
            try:
                text = input(f"{default_color}Lunfardo > ")
            except KeyboardInterrupt:
                print("\nExiting REPL.")
                break

            if text.strip() == "":
                continue

            result, error = self.execute(fn="<stdin>", text=text, cwd=os.getcwd())

            if error:
                print(error.as_string())
            elif result:
                print(repr(result.elements[0]) if len(result.elements) == 1 else repr(result))