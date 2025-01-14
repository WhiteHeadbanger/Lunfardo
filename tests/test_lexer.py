import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.lexer import Lexer
from src.constants import *
from src.errors import IllegalCharError
from src.lunfardo_token import Position

def test_lexer_tokenizes_identifier():
    lexer = Lexer("system", "foo")
    tokens = lexer.make_tokens()
    assert len(tokens) == 2 #EOF is a Token that's always present.
    assert tokens[0][0].type == TT_IDENTIFIER
    assert tokens[0][0].value == "foo"

def test_lexer_tokenizes_keyword():
    lexer = Lexer("system", "si")
    tokens = lexer.make_tokens()
    assert len(tokens) == 2
    assert tokens[0][0].type == TT_KEYWORD
    assert tokens[0][0].value == "si"

def test_lexer_tokenizes_integer():
    lexer = Lexer("system", "123")
    tokens = lexer.make_tokens()
    assert len(tokens) == 2
    assert tokens[0][0].type == TT_INT
    assert tokens[0][0].value == 123

def test_lexer_tokenizes_string():
    lexer = Lexer("system", '"hello"')
    tokens = lexer.make_tokens()
    assert len(tokens[0]) == 2
    assert tokens[0][0].type == TT_STRING
    assert tokens[0][0].value == "hello"

def test_lexer_tokenizes_punctuation():
    lexer = Lexer("system", "(")
    tokens = lexer.make_tokens()
    assert len(tokens[0]) == 2
    assert tokens[0][0].type == TT_LPAREN
    assert tokens[0][0].value == None

def test_lexer_tokenizes_multiple_keywords():
    lexer = Lexer("system", "si no")
    tokens = lexer.make_tokens()
    assert len(tokens[0]) == 3
    assert tokens[0][0].type == TT_KEYWORD
    assert tokens[0][0].value == "si"
    assert tokens[0][1].type == TT_IDENTIFIER
    assert tokens[0][1].value == "no"
    assert tokens[0][2].type == TT_EOF
    assert tokens[0][2].value == None

def test_lexer_tokenizes_mix_of_keywords_and_identifiers():
    lexer = Lexer("system", "si foo bar")
    tokens = lexer.make_tokens()
    assert len(tokens[0]) == 4
    assert tokens[0][0].type == TT_KEYWORD
    assert tokens[0][0].value == "si"
    assert tokens[0][1].type == TT_IDENTIFIER
    assert tokens[0][1].value == "foo"
    assert tokens[0][2].type == TT_IDENTIFIER
    assert tokens[0][2].value == "bar"
    assert tokens[0][3].type == TT_EOF
    assert tokens[0][3].value == None

def test_lexer_tokenizes_keyword_followed_by_punctuation():
    lexer = Lexer("system", "si (")
    tokens = lexer.make_tokens()
    assert len(tokens[0]) == 3
    assert tokens[0][0].type == TT_KEYWORD
    assert tokens[0][0].value == "si"
    assert tokens[0][1].type == TT_LPAREN
    assert tokens[0][1].value == None
    assert tokens[0][2].type == TT_EOF
    assert tokens[0][2].value == None

def test_lexer_throws_error_on_invalid_input():
    lexer = Lexer("system", " 2_4a7 ")
    tokens, error = lexer.make_tokens()
    assert error.details == "'_'"