from src.lunfardo_types import Boloodean, Numero, Nada, Chamuyo, Coso, Mataburros, Curro, Laburo, Cheto
from src.lunfardo_types import LUNFARDO_TYPES, VALUE_TYPES
from .op_registry import operators

def eq_operator(left: LUNFARDO_TYPES, right: LUNFARDO_TYPES) -> tuple[Boloodean, None]:
    if isinstance(left, VALUE_TYPES) and isinstance(right, VALUE_TYPES):
        if left.value == right.value:
            return Boloodean.posta.set_context(left.context), None
    
    if isinstance(left, Coso) and isinstance(right, Coso):
        if left.elements == right.elements:
            return Boloodean.posta.set_context(left.context), None
    
    if isinstance(left, Mataburros) and isinstance(right, Mataburros):
        if left.count == right.count:
            # Comparar elementos de ambos mataburros
            all_elements_equal = True
            for bucket in left.buckets:
                for key, value in bucket:
                    if right.get_value(key) != value:
                        all_elements_equal = False
                        break
                if not all_elements_equal:
                    break
            if all_elements_equal:
                return Boloodean.posta.set_context(left.context), None
            
    if isinstance(left, Curro) and isinstance(right, Curro):
        if left == right:
            return Boloodean.posta.set_context(left.context), None
        
    if isinstance(left, Laburo) and isinstance(right, Laburo):
        if left == right:
            return Boloodean.posta.set_context(left.context), None
        
    if isinstance(left, Cheto) and isinstance(right, Cheto):
        if left == right:
            return Boloodean.posta.set_context(left.context), None
    
    return Boloodean.trucho.set_context(left.context), None

def ne_operator(left: LUNFARDO_TYPES, right: LUNFARDO_TYPES) -> tuple[Boloodean, None]:
    if isinstance(left, VALUE_TYPES) and isinstance(right, VALUE_TYPES):
        if left.value != right.value:
            return Boloodean.posta.set_context(left.context), None
    
    if isinstance(left, Coso) and isinstance(right, Coso):
        if left.elements != right.elements:
            return Boloodean.posta.set_context(left.context), None
    
    if isinstance(left, Mataburros) and isinstance(right, Mataburros):
        if left.count != right.count:
            return Boloodean.posta.set_context(left.context), None
        # Comparar elementos de ambos mataburros
        all_elements_not_equal = False
        for bucket in left.buckets:
            for key, value in bucket:
                if right.get_value(key) != value:
                    all_elements_not_equal = True
                    break
            if not all_elements_not_equal:
                break
        if all_elements_not_equal:
            return Boloodean.posta.set_context(left.context), None
            
    if isinstance(left, Curro) and isinstance(right, Curro):
        if left != right:
            return Boloodean.posta.set_context(left.context), None
        
    if isinstance(left, Laburo) and isinstance(right, Laburo):
        if left != right:
            return Boloodean.posta.set_context(left.context), None
        
    if isinstance(left, Cheto) and isinstance(right, Cheto):
        if left != right:
            return Boloodean.posta.set_context(left.context), None
    
    return Boloodean.trucho.set_context(left.context), None

def lt_operator(left: Numero, right: Numero) -> tuple[Boloodean, None]:
    if left.value < right.value:
        return Boloodean.posta.set_context(left.context), None
    return Boloodean.trucho.set_context(left.context), None

def gt_operator(left: Numero, right: Numero) -> tuple[Boloodean, None]:
    if left.value > right.value:
        return Boloodean.posta.set_context(left.context), None
    return Boloodean.trucho.set_context(left.context), None

def lte_operator(left: Numero, right: Numero) -> tuple[Boloodean, None]:
    if left.value <= right.value:
        return Boloodean.posta.set_context(left.context), None
    return Boloodean.trucho.set_context(left.context), None

def gte_operator(left: Numero, right: Numero) -> tuple[Boloodean, None]:
    if left.value >= right.value:
        return Boloodean.posta.set_context(left.context), None
    return Boloodean.trucho.set_context(left.context), None



