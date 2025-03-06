from .value import Value
from .boloodean import Boloodean


class Mataburros(Value):

    def __init__(self, size=16):
        super().__init__()
        self.size = size # tamaño inicial
        self.buckets = [[] for _ in range(size)] # lista de listas para manejar colisiones
        self.count = 0 # cantidad de elementos almacenados

    def _hash(self, key):
        """ Genera un índice para una clave """
        return hash(key) % self.size
    
    def set_pair(self, key, value):
        """ Inserta o actualiza un valor asociado a una clave """
        index = self._hash(key.value)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k.value == key.value:
                # Reemplaza el valor si la clave ya existe
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
        self.count += 1

        # si la carga supera el 70%, redimensionamos
        if self.count / self.size > 0.7:
            self._resize()

    def get_value(self, key):
        """ Obtiene el valor asociado a una clave """
        index = self._hash(key.value)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k.value == key.value:
                return v
            
        return None
    
    def del_key(self, key):
        """ Elimina un valor por su clave """
        index = self._hash(key.value)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k.value == key.value:
                del bucket[i]
                self.count -= 1
                return True
        
        return False
    
    def _resize(self):
        """ Duplica el tamaño del mataburros y reubica los elementos """
        new_size = self.size * 2
        new_buckets = [[] for _ in range(new_size)]

        for bucket in self.buckets:
            for key, value in bucket:
                index = hash(key) % new_size
                new_buckets[index].append((key, value))
        
        self.size = new_size
        self.buckets = new_buckets


    @classmethod
    def from_dict(cls, _dict):
        """
        Crea un Mataburros a partir de un diccionario Python estándar.

        Args:
            python_dict (dict): El diccionario de Python a convertir.

        Returns:
            Mataburros: Una instancia de Mataburros con claves y valores separados.
        """
        from . import Chamuyo
        instance = cls(size=len(_dict) * 2) 
        for key, value in _dict.items():
            instance.set_pair(Chamuyo(key), value)
        return instance

    def copy(self):
        copy = Mataburros(self.size)
        copy.buckets = self.buckets
        copy.count = self.count
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return (
            Boloodean(self.count > 0).set_context(
                self.context
            ),
            None,
        )

    def __str__(self):
        elements = []
        for bucket in self.buckets:
            elements.extend([f"{repr(k)}: {repr(v)}" for k, v in bucket])
        return "{" + ", ".join(elements) + "}"

    def __repr__(self):
        elements = []
        for bucket in self.buckets:
            elements.extend([f"{repr(k)}: {repr(v)}" for k, v in bucket])
        return "{" + ", ".join(elements) + "}"
