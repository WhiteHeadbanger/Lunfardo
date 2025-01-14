import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.interpreter import Interpreter
from src.nodes import NumeroNode, BinOpNode
from src.lunfardo_token import Token, Position
from src.constants import *
from src.lunfardo_types import Numero
from tests.utils import pos

def test_interpreter_executes_identifier():
    interpreter = Interpreter()
    result = interpreter.visit(
        NumeroNode(
            Token(
                TT_INT, 
                123, 
                pos_start=pos("123")
            )
        ), 
        None
    )
    assert isinstance(result.value, Numero)
    assert result.value.value == 123
    assert result.error == None

def test_interpreter_executes_expression():
    interpreter = Interpreter()
    result = interpreter.visit(
        BinOpNode(
            NumeroNode(
                Token(
                    TT_INT, 
                    123, 
                    pos_start=pos("123")
                )
            ), 
            Token(
                TT_PLUS, 
                "+", 
                pos_start=pos("+")
            ), 
            NumeroNode(
                Token(
                    TT_INT, 
                    456, 
                    pos_start=pos("456")
                )
            )
        ), 
        None
    )
    assert isinstance(result.value, Numero)
    assert result.value.value == 579