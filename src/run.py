from lexer import Lexer
from lunfardo_parser import Parser
from lunfardo_types import Number, BuiltInFunction
from interpreter import Interpreter, SymbolTable
from context import Context

global_symbol_table = SymbolTable()
global_symbol_table.set("nada", Number.null) #null, none
global_symbol_table.set("posta", Number.true) #true
global_symbol_table.set("trucho", Number.false) #false
global_symbol_table.set("matear", BuiltInFunction.print)
global_symbol_table.set("morfar", BuiltInFunction.input)
global_symbol_table.set("linpiavidrios", BuiltInFunction.clear)
global_symbol_table.set("winpiavidrios", BuiltInFunction.clear)
global_symbol_table.set("es_num", BuiltInFunction.is_number)
global_symbol_table.set("es_chamu", BuiltInFunction.is_string)
global_symbol_table.set("es_coso", BuiltInFunction.is_list)
global_symbol_table.set("es_laburo", BuiltInFunction.is_function)
global_symbol_table.set("guardar", BuiltInFunction.append)
global_symbol_table.set("sacar", BuiltInFunction.pop)
global_symbol_table.set("extender", BuiltInFunction.extend)

global_symbol_table.set("str", BuiltInFunction.str)
global_symbol_table.set("int", BuiltInFunction.int)



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
        elif result:
            print(repr(result))

if __name__ == '__main__':
    run()