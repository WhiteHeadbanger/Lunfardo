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
    def as_string(self, nested = False):
        result += f'\n{string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)}' 
        return result
    
class IllegalCharError(Error):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Carácter ilegal] Flaco, fijate que metiste un carácter mal', details)

class InvalidSyntaxError(Error):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Sintaxis inválida] No te entiendo nada, boludo', details)

class ExpectedCharError(Error):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Carácter esperado] Flaco, fijate que te olvidaste de un carácter', details)

class TypeError(Error):
    
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Tipo incorrecto] LOCO, ENCIMA TENGO QUE ANDAR MARCANDOTE LOS ERRORES, TARADO', details)

# Run time error
class RTError(Error):

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Error en tiempo de ejecución', details)
        self.context = context

        result += f'{self.error_name}: {self.details}'
    def as_string(self, nested=False):
        result = self.generate_traceback(nested)
        result += f'\n{string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)}'
        return result
    
    def generate_traceback(self, nested=False):
        result = ''
        pos = self.pos_start
        ctx = self.context
        traceback_msg = 'Seguimiento del quilombo (la llamada más reciente está última):\n'
        

        while ctx:
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        if not nested:
            result = f'{traceback_msg}\n{result}'
        
        return result