from src.lunfardo_types import Boloodean
from src.lunfardo_types import VALUE_TYPES

def and_operator(left: VALUE_TYPES, right: VALUE_TYPES) -> tuple[Boloodean, None]:
    if left.value and right.value:
        return Boloodean.posta.set_context(left.context), None
    return Boloodean.trucho.set_context(left.context), None

def or_operator(left: VALUE_TYPES, right: VALUE_TYPES) -> tuple[Boloodean, None]:
    if left.value or right.value:
        return Boloodean.posta.set_context(left.context), None
    return Boloodean.trucho.set_context(left.context), None

def not_operator(value: VALUE_TYPES, _: VALUE_TYPES) -> tuple[Boloodean, None]:
    if value.value:
        return Boloodean.trucho.set_context(value.context), None
    return Boloodean.posta.set_context(value.context), None

