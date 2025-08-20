
import sys
import pytest
from src.lexer import Lexer
from src.lunfardo_parser import Parser
from src.nodes import *

sys.path.append(".")

def test_parser_empty_input():
    lexer = Lexer("<test>", "")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert eof is True
    assert ast.node is None

def test_parser_number_expression():
    lexer = Lexer("<test>", "123")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, NumeroNode)
    assert ast.node.tok.value == 123

def test_parser_string_expression():
    lexer = Lexer("<test>", '"hello"')
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, ChamuyoNode)
    assert ast.node.tok.value == "hello"

def test_parser_addition():
    lexer = Lexer("<test>", "1 + 2")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, BinOpNode)
    assert ast.node.op_tok.type == 'PLUS'

def test_parser_subtraction():
    lexer = Lexer("<test>", "2 - 1")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, BinOpNode)
    assert ast.node.op_tok.type == 'MINUS'

def test_parser_multiplication():
    lexer = Lexer("<test>", "2 * 3")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, BinOpNode)
    assert ast.node.op_tok.type == 'MUL'

def test_parser_division():
    lexer = Lexer("<test>", "4 / 2")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, BinOpNode)
    assert ast.node.op_tok.type == 'DIV'

def test_parser_power():
    lexer = Lexer("<test>", "2 ^ 3")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, BinOpNode)
    assert ast.node.op_tok.type == 'POW'

def test_parser_unary_minus():
    lexer = Lexer("<test>", "-1")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, UnaryOpNode)
    assert ast.node.op_tok.type == 'MINUS'

def test_parser_variable_assignment():
    lexer = Lexer("<test>", "poneleque my_var = 10")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, PoneleQueAssignNode)
    assert ast.node.var_name_tok.value == "my_var"

def test_parser_variable_access():
    lexer = Lexer("<test>", "my_var")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, PoneleQueAccessNode)
    assert ast.node.var_name_tok.value == "my_var"

def test_parser_if_statement():
    lexer = Lexer("<test>", "si posta entonces\n 1\n chau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, SiNode)

def test_parser_if_else_statement():
    lexer = Lexer("<test>", "si posta entonces\n 1\n sino\n 2\nchau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, SiNode)
    assert ast.node.else_case is not None

def test_parser_for_loop():
    lexer = Lexer("<test>", "para i = 0 hasta 10 entre 1 entonces\n i\n chau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, ParaNode)

def test_parser_while_loop():
    lexer = Lexer("<test>", "mientras posta entonces\n 1\n chau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, MientrasNode)

def test_parser_function_definition():
    lexer = Lexer("<test>", "laburo my_func(a, b)\n a + b \n chau")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, LaburoDefNode)
    assert ast.node.func_name_tok.value == "my_func"

def test_parser_function_call():
    lexer = Lexer("<test>", "my_func(1, 2)")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, CallNode)
    assert ast.node.node_to_call.var_name_tok.value == "my_func"

def test_parser_list_expression():
    lexer = Lexer("<test>", "[1, 2, 3]")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, CosoNode)
    assert len(ast.node.element_nodes) == 3

def test_parser_dict_expression():
    lexer = Lexer("<test>", "{a: 1, b: 2}")
    parser = Parser(lexer.make_tokens()[0])
    ast, eof = parser.parse()
    assert isinstance(ast.node, MataburrosNode)
    assert len(ast.node.element_nodes) == 2
