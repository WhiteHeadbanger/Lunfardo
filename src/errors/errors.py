from . import string_with_arrows
from constants.colors import ACCENT, BOLD_ACCENT, DEFAULT

class Bardo:

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
        self.accent_color = ACCENT
        self.bold_accent_color = BOLD_ACCENT
        self.default_color = DEFAULT

    def as_string(self, nested = False):
        result = f'{self.bold_accent_color}{self.error_name}: {self.accent_color}{self.details}'
        result += f'\n{self.default_color}Fichero {self.accent_color}{self.pos_start.fn}{self.default_color}, linea {self.accent_color}{self.pos_start.ln + 1}'
        result += f'\n{string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)}' 
        return result
    
class IllegalCharBardo(Bardo):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Carácter ilegal] Flaco, fijate que metiste un carácter mal', details)
        self.name = "caracter_ilegal"

class InvalidSyntaxBardo(Bardo):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Sintaxis inválida] No te entiendo nada, boludo', details)
        self.name = "sintaxis_invalida"

class ExpectedCharBardo(Bardo):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Carácter esperado] Flaco, fijate que te olvidaste de un carácter', details)
        self.name = "caracter_esperado"

class InvalidTypeBardo(Bardo):
    
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Bardo de tipo] LOCO, ENCIMA TENGO QUE ANDAR MARCANDOTE LOS BARDOS, TARADO', details)
        self.name = "bardo_de_tipo"

class InvalidIndexBardo(Bardo):
    
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Bardo de indice] Dale, una bien te pido nada mas', details)
        self.name = "bardo_de_indice"

class InvalidKeyBardo(Bardo):
    
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Bardo de clave] A ver, correte y traeme a alguien que sepa programar (y agarra el mataburros que no muerde)', details)
        self.name = "bardo_de_clave"

class InvalidValueBardo(Bardo):
    
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '\n[Bardo de valor] Sabías que los numeros NO LLEVAN LETRAS?', details)
        self.name = "bardo_de_valor"


# Run time error
class RTError(Bardo):

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Bardo en tiempo de ejecución', details)
        self.context = context

    def as_string(self, nested=False):
        result = self.generate_traceback(nested)
        result += f'{self.bold_accent_color}{self.error_name}: {self.accent_color}{self.details}'
        result += f'\n{string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)}'
        return result
    
    def generate_traceback(self, nested=False):
        result = ''
        pos = self.pos_start
        ctx = self.context
        traceback_msg = 'Seguimiento del quilombo (la llamada más reciente está última):\n'
        

        while ctx:
            result = f' {self.default_color}Fichero {self.accent_color}{pos.fn}{self.default_color}, línea {self.accent_color}{str(pos.ln + 1)}{self.default_color}, en {self.accent_color}{ctx.display_name if isinstance(ctx.display_name, str) else "<modulo>"}\n{result}'
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        if not nested:
            result = f'{traceback_msg}\n{result}'
        
        return result