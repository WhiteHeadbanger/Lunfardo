from .value import Value
from .boloodean import Boloodean


class Mataburros(Value):

    def __init__(self, keys, values):
        super().__init__()
        self.keys = keys
        self.values = values

    @classmethod
    def _from_dict(cls, _dict):
        """
        Crea un Mataburros a partir de un diccionario Python estándar.

        Args:
            python_dict (dict): El diccionario de Python a convertir.

        Returns:
            Mataburros: Una instancia de Mataburros con claves y valores separados.
        """
        keys = list(_dict.keys())
        values = list(_dict.values())
        return cls(keys, values)

    def copy(self):
        copy = Mataburros(self.keys, self.values)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return (
            Boloodean(len(self.keys) > 0 and len(self.values) > 0).set_context(
                self.context
            ),
            None,
        )

    def __str__(self):
        return f'{{{", ".join([f"{k}: {v}" for k, v in zip(self.keys, self.values)])}}}'

    def __repr__(self):
        return f'{{{", ".join([f"{k}: {v}" for k, v in zip(self.keys, self.values)])}}}'
