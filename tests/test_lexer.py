
import sys
import pytest
from src.lexer import Lexer
from src.lunfardo_token import Token
from src.constants.tokens import *

sys.path.append(".")

def test_lexer_empty_input():
    lexer = Lexer("<test>", "")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 1
    assert tokens[0].type == TT_EOF

def test_lexer_whitespace():
    lexer = Lexer("<test>", " \t \t ")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 1
    assert tokens[0].type == TT_EOF

def test_lexer_numbers():
    lexer = Lexer("<test>", "123 123.456 789")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 4
    assert tokens[0].type == TT_INT and tokens[0].value == 123
    assert tokens[1].type == TT_FLOAT and tokens[1].value == 123.456
    assert tokens[2].type == TT_INT and tokens[2].value == 789
    assert tokens[3].type == TT_EOF

def test_lexer_operators():
    lexer = Lexer("<test>", "+-*/^()")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 8
    assert tokens[0].type == TT_PLUS
    assert tokens[1].type == TT_MINUS
    assert tokens[2].type == TT_MUL
    assert tokens[3].type == TT_DIV
    assert tokens[4].type == TT_POW
    assert tokens[5].type == TT_LPAREN
    assert tokens[6].type == TT_RPAREN
    assert tokens[7].type == TT_EOF

def test_lexer_single_char_tokens():
    lexer = Lexer("<test>", ";\n,:.{}")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 8
    assert tokens[0].type == TT_NEWLINE
    assert tokens[1].type == TT_NEWLINE
    assert tokens[2].type == TT_COMMA
    assert tokens[3].type == TT_COLON
    assert tokens[4].type == TT_DOT
    assert tokens[5].type == TT_LCURLY
    assert tokens[6].type == TT_RCURLY
    assert tokens[7].type == TT_EOF

def test_lexer_comparisons():
    lexer = Lexer("<test>", "< > <= >= == !=")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 7
    assert tokens[0].type == TT_LT
    assert tokens[1].type == TT_GT
    assert tokens[2].type == TT_LTE
    assert tokens[3].type == TT_GTE
    assert tokens[4].type == TT_EE
    assert tokens[5].type == TT_NE
    assert tokens[6].type == TT_EOF

def test_lexer_assignment():
    lexer = Lexer("<test>", "=")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 2
    assert tokens[0].type == TT_EQ
    assert tokens[1].type == TT_EOF

def test_lexer_identifiers():
    lexer = Lexer("<test>", "a_variable another_var var123")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 4
    assert tokens[0].type == TT_IDENTIFIER and tokens[0].value == "a_variable"
    assert tokens[1].type == TT_IDENTIFIER and tokens[1].value == "another_var"
    assert tokens[2].type == TT_IDENTIFIER and tokens[2].value == "var123"
    assert tokens[3].type == TT_EOF

def test_lexer_keywords():
    lexer = Lexer("<test>", "poneleque y o  entonces chau sino mientras laburo para hasta entre")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 16
    assert all(t.type == TT_KEYWORD for t in tokens[:-1])
    assert tokens[15].type == TT_EOF

def test_lexer_string():
    lexer = Lexer("<test>", '"Hola, Mundo!"')
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 2
    assert tokens[0].type == TT_STRING and tokens[0].value == "Hola, Mundo!"
    assert tokens[1].type == TT_EOF

def test_lexer_empty_string():
    lexer = Lexer("<test>", '""')
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 2
    assert tokens[0].type == TT_STRING and tokens[0].value == ""
    assert tokens[1].type == TT_EOF

def test_lexer_string_with_escaped_chars():
    lexer = Lexer("<test>", '"a \\"new\\" line\\n and a tab\\t"')
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 2
    assert tokens[0].type == TT_STRING and tokens[0].value == 'a "new" line\n and a tab\t'
    assert tokens[1].type == TT_EOF

def test_lexer_unterminated_string():
    lexer = Lexer("<test>", '"this is not closed')
    tokens, error = lexer.make_tokens()
    assert error is not None
    assert error.error_name == "Se esperaba '\"'"

def test_lexer_illegal_character():
    lexer = Lexer("<test>", "@")
    tokens, error = lexer.make_tokens()
    assert error is not None
    assert error.error_name == "Bardo de Caracter Ilegal"

def test_lexer_comment():
    lexer = Lexer("<test>", "# esto es un comentario\n123")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 3
    assert tokens[0].type == TT_NEWLINE
    assert tokens[1].type == TT_INT and tokens[1].value == 123
    assert tokens[2].type == TT_EOF

def test_lexer_comment_at_eof():
    lexer = Lexer("<test>", "123 # comment at the end")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 2
    assert tokens[0].type == TT_INT and tokens[0].value == 123
    assert tokens[1].type == TT_EOF

def test_lexer_minus_or_arrow():
    lexer = Lexer("<test>", "->")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 2
    assert tokens[0].type == TT_ARROW
    assert tokens[1].type == TT_EOF

def test_lexer_not_equals():
    lexer = Lexer("<test>", "!=")
    tokens, error = lexer.make_tokens()
    assert error is None
    assert len(tokens) == 2
    assert tokens[0].type == TT_NE
    assert tokens[1].type == TT_EOF

def test_lexer_invalid_not_equals():
    lexer = Lexer("<test>", "!")
    tokens, error = lexer.make_tokens()
    assert error is not None
    assert error.error_name == "Bardo de Caracter Esperado"
