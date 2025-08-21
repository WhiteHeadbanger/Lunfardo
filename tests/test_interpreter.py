import sys
import pytest
from src.lunfardo import Lunfardo
from src.interpreter import Interpreter

sys.path.append(".")

class InterpreterTester(Interpreter):

    def __init__(self):
        super().__init__()
        self.captured_result = None

    def visit(self, node, context):
        result = super().visit(node, context)
        self.captured_result = result
        return result

    

@pytest.fixture
def lunfardo_instance():
    return Lunfardo()

def test_interpreter_numero_expression(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute(fn="<test>", text="123", interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == 123

def test_interpreter_chamuyo_expression(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", '"hola"', interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == "hola"

def test_interpreter_suma(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", "1 + 2", interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == 3

def test_interpreter_resta(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", "2 - 1", interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == 1

def test_interpreter_multiplicacion(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", "2 * 3", interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == 6

def test_interpreter_division(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", "4 / 2", interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == 2

def test_interpreter_potencia(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", "2 ^ 3", interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == 8

def test_interpreter_unario_negativo(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", "-1", interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == -1

def test_interpreter_asignacion_acceso_variable(lunfardo_instance: Lunfardo):
    code = '''
    poneleque var = 10
    var
    '''
    result, error, interp = lunfardo_instance.execute("<test>", code, interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[0].value == 10

def test_interpreter_si_declaracion(lunfardo_instance: Lunfardo):
    code = '''
    si posta entonces
    devolver 1
    chau
    '''
    result, error, interp = lunfardo_instance.execute("<test>", code, interpreter_cls = InterpreterTester)
    assert error is None
    assert interp.captured_result.func_return_value.value == 1

def test_interpreter_si_sino_declaracion(lunfardo_instance: Lunfardo):
    code = '''
    si trucho entonces
    devolver 1
    sino
    devolver 2
    chau
    '''
    result, error, interp = lunfardo_instance.execute("<test>", code, interpreter_cls = InterpreterTester)
    assert error is None
    assert interp.captured_result.func_return_value.value == 2

def test_interpreter_bucle_para(lunfardo_instance: Lunfardo):
    code = '''
    poneleque a = 0
    para i = 1 hasta 5 entonces
    a = a + i
    chau
    a
    '''
    result, error, interp = lunfardo_instance.execute("<test>", code, interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[-1].value == 10

def test_interpreter_bucle_mientras(lunfardo_instance: Lunfardo):
    code = '''
    poneleque a = 0
    mientras a < 5 entonces
    a = a + 1
    chau
    a
    '''
    result, error, interp = lunfardo_instance.execute("<test>", code, interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[-1].value == 5

def test_interpreter_definicion_llamada_laburo(lunfardo_instance: Lunfardo):
    code = '''
    laburo my_func(a, b)
    devolver a + b
    chau
    my_func(3, 4)
    '''
    result, error, interp = lunfardo_instance.execute("<test>", code, interpreter_cls = InterpreterTester)
    assert error is None
    assert result.elements[-1].value == 7

def test_interpreter_expresion_coso(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", "[1, 2, 3]", interpreter_cls = InterpreterTester)
    assert error is None
    assert len(result.elements[0].elements) == 3

def test_interpreter_expresion_mataburros(lunfardo_instance: Lunfardo):
    result, error, interp = lunfardo_instance.execute("<test>", '{"a": 1, "b": 2}', interpreter_cls = InterpreterTester)
    from src.lunfardo_types.chamuyo import Chamuyo
    assert error is None
    assert result.elements[0].count == 2
    assert result.elements[0].get_value(Chamuyo("a")).value == 1
    assert result.elements[0].get_value(Chamuyo("b")).value == 2
