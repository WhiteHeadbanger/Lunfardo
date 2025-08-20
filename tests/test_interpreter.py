import sys
import pytest
from src.lunfardo import Lunfardo

sys.path.append(".")

@pytest.fixture
def lunfardo_instance():
    return Lunfardo()

def test_interpreter_number_expression(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "123")
    assert error is None
    assert result.elements[0].value == 123

def test_interpreter_string_expression(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", '"hello"')
    assert error is None
    assert result.elements[0].value == "hello"

def test_interpreter_addition(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "1 + 2")
    assert error is None
    assert result.elements[0].value == 3

def test_interpreter_subtraction(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "2 - 1")
    assert error is None
    assert result.elements[0].value == 1

def test_interpreter_multiplication(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "2 * 3")
    assert error is None
    assert result.elements[0].value == 6

def test_interpreter_division(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "4 / 2")
    assert error is None
    assert result.elements[0].value == 2

def test_interpreter_power(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "2 ^ 3")
    assert error is None
    assert result.elements[0].value == 8

def test_interpreter_unary_minus(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "-1")
    assert error is None
    assert result.elements[0].value == -1

def test_interpreter_variable_assignment_and_access(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "poneleque my_var = 10\n my_var")
    assert error is None
    assert result.elements[0].value == 10

def test_interpreter_if_statement(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "si posta entonces\n 1\nchau")
    assert error is None
    assert result.elements[0].value == 1

def test_interpreter_if_else_statement(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "si trucho entonces \n1 \nsino\n 2 \nchau")
    assert error is None
    assert result.elements[0].value == 2

def test_interpreter_for_loop(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "poneleque a = 0\n para i = 1 hasta 5 entre 1 entonces\n a = a + i chau\n a")
    assert error is None
    assert result.elements[0].value == 10

def test_interpreter_while_loop(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "poneleque a = 0\n mientras a < 5 entonces\n a = a + 1 chau\n a")
    assert error is None
    assert result.elements[0].value == 5

def test_interpreter_function_definition_and_call(lunfardo_instance):
    code = '''
    laburo my_func(a, b)
    devolver a + b
    chau
    my_func(3, 4)
    '''
    result, error = lunfardo_instance.execute("<test>", code)
    assert error is None
    assert result.elements[0].value == 7

def test_interpreter_list_expression(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "[1, 2, 3]")
    assert error is None
    assert len(result.elements[0].elements) == 3

def test_interpreter_dict_expression(lunfardo_instance):
    result, error = lunfardo_instance.execute("<test>", "{a: 1, b: 2}")
    assert error is None
    assert len(result.elements[0].elements) == 2
