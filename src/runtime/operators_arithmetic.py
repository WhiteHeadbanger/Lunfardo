from src.lunfardo_types import Numero, Coso, Chamuyo
from src.errors import ZeroDivisionBardo, InvalidValueBardo, InvalidIndexBardo, InvalidTypeBardo

def numero_plus_numero(left: Numero, right: Numero) -> tuple[Numero, None]:
    return Numero(left.value + right.value).set_context(left.context), None

def numero_sub_numero(left: Numero, right: Numero) -> tuple[Numero, None]:
    return Numero(left.value - right.value).set_context(left.context), None

def numero_mul_numero(left: Numero, right: Numero) -> tuple[Numero, None]:
    return Numero(left.value * right.value).set_context(left.context), None

def numero_div_numero(left: Numero, right: Numero) -> tuple[None, ZeroDivisionBardo] | tuple[Numero, None]:
    if right.value == 0:
        return None, ZeroDivisionBardo(
            right.pos_start, right.pos_end, "Division por cero", right.context
        )
    return Numero(left.value / right.value).set_context(left.context), None

def numero_mod_numero(left: Numero, right: Numero) -> tuple[None, ZeroDivisionBardo] | tuple[Numero, None]:
    if right.value == 0:
        return None, ZeroDivisionBardo(
            right.pos_start, right.pos_end, "Modulo por cero", right.context
        )
    return Numero(left.value % right.value).set_context(left.context), None

def numero_pow_numero(left: Numero, right: Numero) -> tuple[Numero, None]:
    return Numero(left.value ** right.value).set_context(left.context), None

def coso_plus_coso(left: Coso, right: Coso) -> tuple[Coso, None]:
    new_list = left.copy()
    new_list.elements.extend(right.elements)
    return new_list, None

def coso_mul_numero(left: Coso, right: Numero) -> tuple[None, InvalidValueBardo] | tuple[Coso, None]:
    if right.value < 0:
        return None, InvalidValueBardo(
            right.pos_start, right.pos_end, "No se puede multiplicar un coso por un número negativo", right.context
        )
    new_list = left.copy()
    new_list.elements.clear()
    for _ in range(right.value):
        new_list.elements.extend(left.elements)
    return new_list, None

def coso_sub_numero(left: Coso, right: Numero) -> tuple[None, InvalidIndexBardo] | tuple[Coso, None]:
    new_list = left.copy()
    try:
        new_list.elements.pop(right.value)
        return new_list, None
    except IndexError:
        return None, InvalidIndexBardo(
            right.pos_start,
            right.pos_end,
            f"Elemento con el índice {right.value} no pudo ser removido del coso porque el índice está fuera de los límites.",
            right.context,
        )
    
def coso_sub_coso(left: Coso, right: Coso) -> tuple[Coso, None]:
    new_list = left.copy()

    if not right.elements:
        return new_list, None

    def _value(value):
        for i, el in enumerate(new_list.elements):
            if new_list.elements[i].value == value:
                new_list.elements.pop(i)
                break

    def _elements(elements):
        return coso_sub_coso(left, elements)

    attr_map = {"value": _value, "elements": _elements}

    for _, el in enumerate(right.elements):
        attr = getattr(el, "value", "elements")

        if isinstance(attr, (int, str)):
            attr_map["value"](attr)
        elif isinstance(attr, list):
            attr_map["elements"](attr)

    return new_list, None

def coso_div_numero(left: Coso, right: Numero) -> tuple[None, InvalidIndexBardo] | tuple[None, InvalidTypeBardo] | tuple[Coso, None]:
    try:
        return left.elements[right.value], None
    except IndexError:
        return None, InvalidIndexBardo(
            right.pos_start,
            right.pos_end,
            f"Elemento con el índice {right.value} no pudo ser devuelto del coso porque el índice está fuera de los límites.",
            right.context,
        )
    except TypeError:
        return None, InvalidTypeBardo(
            right.pos_start,
            right.pos_end,
            f"Elemento con el índice {right.value} no pudo ser devuelto del coso porque el índice no es un número entero.",
            right.context,
        )

def chamuyo_plus_chamuyo(left: Chamuyo, right: Chamuyo) -> tuple[Chamuyo, None]:
    return Chamuyo(left.value + right.value).set_context(left.context), None

def chamuyo_mul_numero(left: Chamuyo, right: Numero) -> tuple[Chamuyo, None]:
    return Chamuyo(left.value * right.value).set_context(left.context), None

