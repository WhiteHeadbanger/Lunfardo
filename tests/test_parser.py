import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.lunfardo_parser import Parser
from src.constants import *
from src.lunfardo_token import Token, Position
from tests.utils import pos

def test_parser_parses_identifier():
    parser = Parser(
        [
            Token(
                TT_IDENTIFIER, 
                "foo", 
                pos_start=pos("foo")
            )
        ]
    )
    ast, eof = parser.parse()
    element_nodes = ast.node.element_nodes
    assert element_nodes[0].var_name_tok.type == TT_IDENTIFIER
    assert element_nodes[0].var_name_tok.value == "foo"

def test_parser_parses_expression():
    parser = Parser(
        [
            Token(
                TT_INT, 
                123, 
                pos_start=pos("foo")
            ), 
            Token(
                TT_PLUS, 
                "+", 
                pos_start=pos("foo")
            ), 
            Token(
                TT_INT, 
                456, 
                pos_start=pos("foo")
            )
        ]
    )
    ast, eof = parser.parse()
    element_nodes = ast.node.element_nodes

    assert element_nodes[0].left_node.tok.type == "INT"
    assert element_nodes[0].left_node.tok.value == 123
    assert element_nodes[0].op_tok.type == TT_PLUS
    assert element_nodes[0].op_tok.value == "+"
    assert element_nodes[0].right_node.tok.type == "INT"
    assert element_nodes[0].right_node.tok.value == 456