from lexer import Lexer
from lunfardo_parser import Parser
from lunfardo_types import Number
from interpreter import Interpreter, SymbolTable
from context import Context

global_symbol_table = SymbolTable()
global_symbol_table.set("nada", Number(0)) #null, none
global_symbol_table.set("posta", Number(1)) #true
global_symbol_table.set("trucho", Number(0)) #false


def execute(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Run
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

def run():
    while True:
        text = input('Lunfardo > ')
        result, error = execute('<stdin>', text)

        if error:
            print(error.as_string())
        else:
            print(result)

if __name__ == '__main__':
    run()