"""
Main execution module for the Lunfardo programming language.

This module contains the global symbol table setup, execution function,
and the main REPL (Read-Eval-Print Loop) for the Lunfardo interpreter.
"""

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


def execute(fn, text) -> Tuple:
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
    context = Context("<programa>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error


def run() -> None:
    """
    Run the Lunfardo REPL (Read-Eval-Print Loop).

    This function provides an interactive prompt for executing Lunfardo code.
    """
    while True:
        text = input("Lunfardo > ")
        if text.strip() == "":
            continue

        result, error = execute("<stdin>", text)

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
    run()
