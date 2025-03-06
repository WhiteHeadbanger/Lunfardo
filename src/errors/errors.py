from . import string_with_arrows

class Error:

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFichero {self.pos_start.fn}, linea {self.pos_start.ln + 1}'
        result += f'\n{string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)}' 
        return result
    
class IllegalCharError(Error):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '[Carácter ilegal] Flaco, fijate que metiste un carácter mal', details)

class InvalidSyntaxError(Error):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '[Sintaxis inválida] No te entiendo nada, boludo', details)

class ExpectedCharError(Error):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '[Carácter esperado] Flaco, fijate que te olvidaste de un carácter', details)

class TypeError(Error):
    
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '[Tipo incorrecto] LOCO, ENCIMA TENGO QUE ANDAR MARCANDOTE LOS ERRORES, TARADO', details)

# Run time error
class RTError(Error):

    __traceback_count__ = 0

    def __new__(cls, *args, **kwargs):
        cls.__traceback_count__ += 1
        instance = super().__new__(cls)
        return instance

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Error en tiempo de ejecución', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += f'\n{string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)}'
        return result
    
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context
        previous_fn = None
        traceback_msg = 'Seguimiento del quilombo (la llamada más reciente está primero):\n'

        while ctx:
            if pos.fn != previous_fn:
                result = f' Fichero {pos.fn}, línea {str(pos.ln + 1)}, en {ctx.display_name}\n{result}'
            previous_fn = pos.fn
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        
        if RTError.__traceback_count__ > 1:
            RTError.__traceback_count__ -= 1
            return result

        return f'{traceback_msg}\n{result}'