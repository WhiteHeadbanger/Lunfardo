from lexer import Lexer
from lunfardo_parser import Parser
from lunfardo_types import Numero, Curro
from interpreter import Interpreter, SymbolTable
from context import Context

global_symbol_table = SymbolTable()
# Bools and null
global_symbol_table.set("nada", Numero.nada) #null, none
global_symbol_table.set("posta", Numero.posta) #true
global_symbol_table.set("trucho", Numero.trucho) #false
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
global_symbol_table.set("reemplazar", Curro.reemplazar)
global_symbol_table.set("sacar", Curro.sacar)
global_symbol_table.set("extender", Curro.extender)
global_symbol_table.set("longitud", Curro.longitud)
# Mataburros related
global_symbol_table.set("agarra_de", Curro.agarra_de)
global_symbol_table.set("metele_en", Curro.metele_en)
global_symbol_table.set("borra_de", Curro.borra_de)
# Misc
global_symbol_table.set("linpiavidrios", Curro.limpiavidrios)
global_symbol_table.set("winpiavidrios", Curro.limpiavidrios)
global_symbol_table.set("ejecutar", Curro.ejecutar)
global_symbol_table.set("renuncio", Curro.renuncio)

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
    context = Context('<programa>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

def run():
    while True:
        text = input('Lunfardo > ')
        if text.strip() == "":
            continue
        
        result, error = execute('<stdin>', text)

        if error:
            print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))

if __name__ == '__main__':
    run()