"""
Main execution module for the Lunfardo programming language.

This module contains the global symbol table setup, execution function,
and the main REPL (Read-Eval-Print Loop) for the Lunfardo interpreter.
"""
import argparse
import os
import sys
from pathlib import Path
from lexer import Lexer
from lunfardo_parser import Parser
from lunfardo_types import Curro, Boloodean, Nada
from interpreter import Interpreter, SymbolTable
from context import Context
from typing import Tuple

############### Global symbol table setup ###############
global_symbol_table = SymbolTable()
# Bools and null
global_symbol_table.set("nada", Nada.nada)
global_symbol_table.set("posta", Boloodean.posta)
global_symbol_table.set("trucho", Boloodean.trucho)
# I/O
global_symbol_table.set("matear", Curro.matear)
global_symbol_table.set("morfar", Curro.morfar)
# Types
global_symbol_table.set("es_num", Curro.es_num)
global_symbol_table.set("es_chamu", Curro.es_chamu)
global_symbol_table.set("es_coso", Curro.es_coso)
global_symbol_table.set("es_laburo", Curro.es_laburo)
global_symbol_table.set("es_mataburros", Curro.es_mataburros)
global_symbol_table.set("chamu", Curro.chamu)
global_symbol_table.set("num", Curro.num)
# Coso related
global_symbol_table.set("guardar", Curro.guardar)
global_symbol_table.set("insertar", Curro.insertar)
global_symbol_table.set("cambiaso", Curro.cambiaso)
global_symbol_table.set("sacar", Curro.sacar)
global_symbol_table.set("extender", Curro.extender)
# Mataburros related
global_symbol_table.set("agarra_de", Curro.agarra_de)
global_symbol_table.set("metele_en", Curro.metele_en)
global_symbol_table.set("borra_de", Curro.borra_de)
global_symbol_table.set("existe_clave", Curro.existe_clave)
# Misc
global_symbol_table.set("linpiavidrios", Curro.limpiavidrios)
global_symbol_table.set("winpiavidrios", Curro.limpiavidrios)
global_symbol_table.set("longitud", Curro.longitud)
global_symbol_table.set("ejecutar", Curro.ejecutar)
global_symbol_table.set("renuncio", Curro.renuncio)
global_symbol_table.set("contexto", Curro.contexto_global)
global_symbol_table.set("asciiAchamu", Curro.asciiAchamu)


def execute(fn, text, cwd = None, file_path = None, parent_context = None) -> Tuple:
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
    context.symbol_table = global_symbol_table
    if parent_context:
        context.parent = parent_context
    
    result = interpreter.visit(ast.node, context)

    return result.value, result.error


def run() -> None:
    """
    Run the Lunfardo REPL (Read-Eval-Print Loop).

    This function provides an interactive prompt for executing Lunfardo code.
    """
    default_color = '\x1b[;;m'
    while True:
        text = input(f"{default_color}Lunfardo > ")
        if text.strip() == "":
            continue

        result, error = execute(fn = "<stdin>", text = text, cwd = os.getcwd())

        if error:
            print(error.as_string())
        elif result is None and error is None:
            continue
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Ejecutá código Lunfardo desde un archivo o iniciá el REPL.")
    parser.add_argument("archivo", nargs="?", help="Ruta del archivo Lunfardo a ejecutar.")
    args = parser.parse_args()

    if args.archivo:
        script_path = os.path.abspath(args.archivo)
        if not os.path.isfile(script_path):
            print(f"Error: No se encontró el archivo {script_path}")
            sys.exit(1)
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                code = f.read()
            file_path = Path(script_path)
            _result, _error = execute(fn = file_path, text = code, cwd = file_path.parent)

            if _error:
                print(_error.as_string())
            """ elif _result:
                if len(_result.elements) == 1:
                    print(repr(_result.elements[0]))
                else:
                    print(repr(_result)) """

        except FileNotFoundError:
            print(f"Error: Archivo '{args.archivo}' no se encuentra.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
    else:
        run()
