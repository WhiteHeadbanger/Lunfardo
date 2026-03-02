from typing import Union

from .numero import Numero
from .boloodean import Boloodean
from .nada import Nada
from .laburo import Laburo, Curro
from .chamuyo import Chamuyo
from .coso import Coso
from .mataburros import Mataburros
from .cheto import Cheto

LUNFARDO_TYPES = Union[Numero, Boloodean, Nada, Laburo, Curro, Chamuyo, Coso, Mataburros, Cheto]
VALUE_TYPES = Union[Numero, Boloodean, Nada, Chamuyo]

from src.runtime.op_registry import operators
from src.runtime.operators_arithmetic import (
        numero_plus_numero,
        numero_sub_numero,
        numero_mul_numero,
        numero_div_numero,
        numero_mod_numero,
        numero_pow_numero,
        coso_plus_coso,
        coso_mul_numero,
        coso_sub_numero,
        coso_sub_coso,
        coso_div_numero,
        chamuyo_plus_chamuyo,
        chamuyo_mul_numero
    )
from src.runtime.operators_eq import (
    eq_operator,
    ne_operator,
    lt_operator,
    gt_operator,
    lte_operator,
    gte_operator
)
from src.runtime.operators_logic import (
    and_operator,
    or_operator
)

operators.register("+", Numero, Numero, numero_plus_numero)
operators.register("-", Numero, Numero, numero_sub_numero)
operators.register("*", Numero, Numero, numero_mul_numero)
operators.register("/", Numero, Numero, numero_div_numero)
operators.register("%", Numero, Numero, numero_mod_numero)
operators.register("^", Numero, Numero, numero_pow_numero)
operators.register("+", Coso, Coso, coso_plus_coso)
operators.register("*", Coso, Numero, coso_mul_numero)
operators.register("-", Coso, Numero, coso_sub_numero)
operators.register("-", Coso, Coso, coso_sub_coso)
operators.register("/", Coso, Numero, coso_div_numero)
operators.register("+", Chamuyo, Chamuyo, chamuyo_plus_chamuyo)
operators.register("*", Chamuyo, Numero, chamuyo_mul_numero)

for t in (Numero, Boloodean, Nada, Chamuyo, Coso, Mataburros, Curro, Laburo, Cheto):
    for u in (Numero, Boloodean, Nada, Chamuyo, Coso, Mataburros, Curro, Laburo, Cheto):
        operators.register("==", t, u, eq_operator)
        operators.register("!=", t, u, ne_operator)

operators.register("<", Numero, Numero, lt_operator)
operators.register(">", Numero, Numero, gt_operator)
operators.register("<=", Numero, Numero, lte_operator)
operators.register(">=", Numero, Numero, gte_operator)

for t in (Numero, Boloodean, Nada, Chamuyo):
    for u in (Numero, Boloodean, Nada, Chamuyo):
        operators.register("y", t, u, and_operator)
        operators.register("o", t, u, or_operator)