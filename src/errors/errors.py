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

# Run time error
class RTError(Bardo):

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Bardo en tiempo de ejecución', details)
        self.context = context

    def as_string(self, nested=False):
        result = self.generate_traceback(nested)
        result += f'{self.bold_accent_color}{self.error_name} {self.accent_color}{self.details}'
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
    
class InvalidTypeBardo(RTError):
    
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f'LOCO, ENCIMA TENGO QUE ANDAR MARCANDOTE LOS BARDOS, TARADO: {details}', context)
        self.error_name = "[Bardo de tipo]"
        self.name = "bardo_de_tipo"
    
class MaxRecursionBardo(RTError):

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f'Capo, te fuiste de mambo con la recursión. Bajá un cambio: {details}', context)
        self.error_name = "[Límite de recursión]"
        self.name = "limite_de_recursion"

class AttributeBardo(RTError):

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f'Troesma, ese atributo no está. Lo soñaste?: {details}', context)
        self.error_name = "[Bardo de atributo]"
        self.name = "bardo_de_atributo"

class UndefinedVarBardo(RTError):

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f'Y esta variable de dónde salió? No la declaraste, flaco: {details}', context)
        self.error_name = "[Variable indefinida]"
        self.name = "variable_indefinida"

class InvalidValueBardo(RTError):
    
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f'Sabías que los números NO LLEVAN LETRAS?: {details}', context)
        self.error_name = "[Bardo de valor]"
        self.name = "bardo_de_valor"

class ZeroDivisionBardo(RTError):
    
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f'Ah, mirá qué pillo, queriendo dividir por cero. Dale, probá otra vez: {details}', context)
        self.error_name = "[División por cero]"
        self.name = "division_por_cero"

class InvalidKeyBardo(RTError):
    
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f'A ver, correte y traeme al senior que sepa programar (y agarra el mataburros que no muerde): {details}', context)
        self.error_name = "[Bardo de clave]"
        self.name = "bardo_de_clave"

class InvalidIndexBardo(RTError):
    
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f'Dale, una bien te pido nada mas: {details}', context)
        self.error_name = "[Bardo de índice]"
        self.name = "bardo_de_indice"

class FileNotFoundBardo(RTError):

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, f"Uy que rompimo! No pudimos abrir el archivo '{details}'\n El archivo no existe.", context)
        self.error_name = "[Archivo no encontrado]"
        self.name = "archivo_no_encontrado"