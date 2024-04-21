from lexer import Lexer
from lunfardo_parser import Parser
from lunfardo_types import Number, BuiltInFunction
from interpreter import Interpreter, SymbolTable
from context import Context

global_symbol_table = SymbolTable()
global_symbol_table.set("nada", Number.null) #null, none
global_symbol_table.set("posta", Number.true) #true
global_symbol_table.set("trucho", Number.false) #false
global_symbol_table.set("matear", BuiltInFunction.matear)
global_symbol_table.set("morfar", BuiltInFunction.morfar)
global_symbol_table.set("linpiavidrios", BuiltInFunction.limpiavidrios)
global_symbol_table.set("winpiavidrios", BuiltInFunction.limpiavidrios)
global_symbol_table.set("es_num", BuiltInFunction.es_num)
global_symbol_table.set("es_chamu", BuiltInFunction.es_chamu)
global_symbol_table.set("es_coso", BuiltInFunction.es_coso)
global_symbol_table.set("es_laburo", BuiltInFunction.es_laburo)
global_symbol_table.set("guardar", BuiltInFunction.guardar)
global_symbol_table.set("sacar", BuiltInFunction.sacar)
global_symbol_table.set("extender", BuiltInFunction.extender)

global_symbol_table.set("chamu", BuiltInFunction.chamu)
global_symbol_table.set("num", BuiltInFunction.chamu)



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