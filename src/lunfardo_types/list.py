from .value import Value
from .number import Number
from .string import String
from errors import RTError

from typing import List

# to avoid override List python type
class LList(Value):

    def __init__(self, elements: List):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        """ Extend a list by providing another list"""
        if isinstance(other, LList):
            new_list = self.copy()
            new_list.elements.extend(other.elements)

            return new_list, None
        
        return None, Value.illegal_operation(self, other)

    def multiplied_by(self, other):
        """ Multiply the values in a list by a number. """
        if isinstance(other, Number):
            if other.value < 0:
                return None, Value.illegal_operation(self, other)
            new_list = self.copy()
            new_list.elements.clear()
            for _ in range(other.value):
                new_list.elements.extend(self.elements)
            return new_list, None
        
        return None, Value.illegal_operation(self, other)
    
    def subtracted_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except IndexError:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    f"Element at the index {other.value} could not be removed from the list because the index is out of bounds.",
                    self.context
                )
        
        if isinstance(other, LList):
            new_list = self.copy()

            if not other.elements:
                return new_list, None
            
            def _value(value):
                for i, el in enumerate(new_list.elements):
                    if new_list.elements[i].value == value:
                        new_list.elements.pop(i)
                        break

            def _elements(elements):
                return self.subtracted_by(elements)

            attr_map = {
                'value': _value,
                'elements': _elements    
            }

            for _, el in enumerate(other.elements):
                attr = getattr(el, 'value', 'elements')
                
                if isinstance(attr, (int, str)):
                    attr_map['value'](attr)
                elif isinstance(attr, list):
                    attr_map['elements'](attr)
                
            return new_list, None
        
        else:
            return None, Value.illegal_operation(self, other)
    
    def divided_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except IndexError:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    f"Element at the index {other.value} could not be returned from the list because the index is out of bounds.",
                    self.context
                )
        
        else:
            return None, Value.illegal_operation(self, other)
        
    def copy(self):
        copy = LList(self.elements[:])
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
                
    def __repr__(self):
        return f'[{", ".join([str(el) for el in self.elements])}]'