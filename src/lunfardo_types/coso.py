from .value import Value
from .numero import Numero
from .boloodean import Boloodean
from src.errors import InvalidIndexBardo, InvalidTypeBardo

from typing import List


class Coso(Value):

    def __init__(self, elements: List):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        """with list -> extend original list. Returns new list"""
        if isinstance(other, Coso):
            new_list = self.copy()
            new_list.elements.extend(other.elements)

            return new_list, None

        return None, Value.illegal_operation(self, other)

    def multiplied_by(self, other):
        """with int -> multiply by <int> the occurrences of element, sorted by original list. Returns new list."""
        if isinstance(other, Numero):
            if other.value < 0:
                return None, Value.illegal_operation(self, other)
            new_list = self.copy()
            new_list.elements.clear()
            for _ in range(other.value):
                new_list.elements.extend(self.elements)
            return new_list, None

        return None, Value.illegal_operation(self, other)

    def subtracted_by(self, other):
        """
        - with int -> remove by index (positive or negative). Returns new list
        - with list -> remove first element encountered. Returns new list
        - with function -> not supported (must use index) TODO
        """
        if isinstance(other, Numero):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except IndexError:
                return None, InvalidIndexBardo(
                    other.pos_start,
                    other.pos_end,
                    f"Elemento con el índice {other.value} no pudo ser removido del coso porque el índice está fuera de los límites.",
                    self.context,
                )

        if isinstance(other, Coso):
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

            attr_map = {"value": _value, "elements": _elements}

            for _, el in enumerate(other.elements):
                attr = getattr(el, "value", "elements")

                if isinstance(attr, (int, str)):
                    attr_map["value"](attr)
                elif isinstance(attr, list):
                    attr_map["elements"](attr)

            return new_list, None

        return None, Value.illegal_operation(self, other)

    def divided_by(self, other):
        """with int -> return element at index <int>"""
        if isinstance(other, Numero):
            try:
                return self.elements[other.value], None
            except IndexError:
                return None, InvalidIndexBardo(
                    other.pos_start,
                    other.pos_end,
                    f"Elemento con el índice {other.value} no pudo ser devuelto del coso porque el índice está fuera de los límites.",
                    self.context,
                )
            except TypeError:
                return None, InvalidTypeBardo(
                    other.pos_start,
                    other.pos_end,
                    f"Elemento con el índice {other.value} no pudo ser devuelto del coso porque el índice no es un número entero.",
                    self.context,
                )

        return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Coso(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return Boloodean(len(self.elements) > 0).set_context(self.context), None

    def __str__(self):
        return f"{self.elements}"

    def __repr__(self):
        return f'[{", ".join([str(el) for el in self.elements])}]'
