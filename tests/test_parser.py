
import sys
import pytest
from src.lexer import Lexer
from src.lunfardo_parser import Parser
from src.nodes import *

sys.path.append(".")

def test_parser_input_vacio():
    lexer = Lexer("<test>", "")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert eof is True
    assert ast is None

def test_parser_expresion_numero():
    lexer = Lexer("<test>", "123")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], NumeroNode)
    assert ast.node.element_nodes[0].tok.value == 123

def test_parser_expresion_chamuyo():
    lexer = Lexer("<test>", '"hola"')
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], ChamuyoNode)
    assert ast.node.element_nodes[0].tok.value == "hola"

def test_parser_addition():
    lexer = Lexer("<test>", "1 + 2")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], BinOpNode)
    assert ast.node.element_nodes[0].op_tok.type == 'PLUS'

def test_parser_subtraction():
    lexer = Lexer("<test>", "2 - 1")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], BinOpNode)
    assert ast.node.element_nodes[0].op_tok.type == 'MINUS'

def test_parser_multiplication():
    lexer = Lexer("<test>", "2 * 3")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], BinOpNode)
    assert ast.node.element_nodes[0].op_tok.type == 'MUL'

def test_parser_division():
    lexer = Lexer("<test>", "4 / 2")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], BinOpNode)
    assert ast.node.element_nodes[0].op_tok.type == 'DIV'

def test_parser_power():
    lexer = Lexer("<test>", "2 ^ 3")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], BinOpNode)
    assert ast.node.element_nodes[0].op_tok.type == 'POW'

def test_parser_unary_minus():
    lexer = Lexer("<test>", "-1")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], UnaryOpNode)
    assert ast.node.element_nodes[0].op_tok.type == 'MINUS'

def test_parser_variable_assignment():
    lexer = Lexer("<test>", "poneleque my_var = 10")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], PoneleQueAssignNode)
    assert ast.node.element_nodes[0].var_name_tok.value == "my_var"

def test_parser_variable_access():
    lexer = Lexer("<test>", "my_var")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], PoneleQueAccessNode)
    assert ast.node.element_nodes[0].var_name_tok.value == "my_var"

def test_parser_if_statement():
    lexer = Lexer("<test>", "si posta entonces\n 1\n chau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], SiNode)

def test_parser_if_else_statement():
    lexer = Lexer("<test>", "si posta entonces\n 1\n sino\n 2\nchau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], SiNode)
    assert ast.node.element_nodes[0].else_case is not None

def test_parser_for_loop():
    lexer = Lexer("<test>", "para i = 0 hasta 10 entre 1 entonces\n i\n chau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], ParaNode)

def test_parser_while_loop():
    lexer = Lexer("<test>", "mientras posta entonces\n 1\n chau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], MientrasNode)

def test_parser_function_definition():
    lexer = Lexer("<test>", "laburo my_func(a, b)\n a + b \n chau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], LaburoDefNode)
    assert ast.node.element_nodes[0].var_name_tok.value == "my_func"

def test_parser_function_call():
    lexer = Lexer("<test>", "my_func(1, 2)")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], CallNode)
    assert ast.node.element_nodes[0].node_to_call.var_name_tok.value == "my_func"

def test_parser_list_expression():
    lexer = Lexer("<test>", "[1, 2, 3]")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], CosoNode)
    assert len(ast.node.element_nodes[0].element_nodes) == 3

def test_parser_dict_expression():
    lexer = Lexer("<test>", '{"a": 1, "b": 2}')
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node.element_nodes[0], MataburrosNode)
    assert len(ast.node.element_nodes[0].pairs) == 2
