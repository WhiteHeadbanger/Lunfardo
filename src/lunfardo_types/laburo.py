from .value import Value
from lunfardo_parser import RTResult
from interpreter import SymbolTable, Interpreter
from context import Context
from errors import RTError
import os

class BaseLaburo(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<injunable>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
    
    def check_args(self, arg_names, args, arg_values = None):
        res = RTResult()

        if not arg_names:
            return res.success(None)

        if arg_values is None:
            arg_values = [None] * len(arg_names)

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start,
                self.pos_end,
                f"demasiados argumentos pasados a '{self.name}'() (esperados {len(arg_names)}, recibidos {len(args)})",
                self.context
            ))

        if len(args) < len(arg_names):
            if len(args) > len([arg_value for arg_value in arg_values if arg_value is None]):
                return res.failure(RTError(
                    self.pos_start,
                    self.pos_end,
                    f"pocos argumentos pasados a '{self.name}'() (esperados {len(arg_names)}, recibidos {len(args)})",
                    self.context
                ))

        return res.success(None)
    
    def populate_args(self, arg_names, args, exec_ctx, arg_values = None):
        for i in range(len(arg_names)):
            arg_name = arg_names[i]
            if i < len(args):
                arg_value = args[i]
            else:
                arg_value = arg_values[i]
            
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx, arg_values = None):
        res = RTResult()

        if arg_values is None:
            res.register(self.check_args(arg_names, args))
        else:
            res.register(self.check_args(arg_names, args, arg_values)) #checkear esto
        
        if res.should_return():
            return res
        
        self.populate_args(arg_names, args, exec_ctx, arg_values)

        return res.success(None)

class Laburo(BaseLaburo):

    def __init__(self, name, body_node, arg_names, arg_values, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.arg_values = arg_values
        self.should_auto_return = should_auto_return

    def execute(self, args, current_context):
        from . import Nada
        res = RTResult()
        # Cada vez que creamos una nueva funcion, es necesario crear un nuevo contexto con una nueva symbol table, que son destruidos una vez que la funcion retorna.
        interpreter = Interpreter()
        execution_context = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, execution_context, self.arg_values))
        
        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.body_node, execution_context))
        if res.should_return() and res.func_return_value is None:
            return res
        
        return_value = (value if self.should_auto_return else None) or res.func_return_value or Nada.nada
        return res.success(return_value)
    
    def copy(self):
        copy = Laburo(self.name, self.body_node, self.arg_names, self.arg_values, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    
    def __str__(self):
        return f"<laburo {self.name}>"

    def __repr__(self):
        return f"<laburo {self.name}>"

class Curro(BaseLaburo):

    def __init__(self, name):
        super().__init__(name)

    def execute(self, args, current_context):
        res = RTResult()
        execution_context = self.generate_new_context()

        method_name = f'exec_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, execution_context))
        if res.should_return():
            return res
        
        return_value = res.register(method(execution_context))
        if res.should_return():
            return res
        
        return res.success(return_value)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No exec_{self.name} method defined.')
    
    def copy(self):
        copy = Curro(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    
    def __repr__(self):
        return f"<curro {self.name}>"
    
    def __str__(self):
        return f"<curro {self.name}>"
    
    #########################################
    # MARK:CURROS (BUILT-INT FUNCTIONS)
    #########################################

    def exec_chamu(self, exec_ctx):
        from . import Chamuyo, Numero, Coso
        value = exec_ctx.symbol_table.get('value')
        
        if not value:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                f"pocos argumentos pasados en '{self.name}'() (esperados 1, recibidos 0)",
                exec_ctx
            ))
        
        if isinstance(value, Numero):
            return RTResult().success(Chamuyo(str(value.value)))
        
        if isinstance(value, Chamuyo):
            return RTResult().success(Chamuyo(value.value))
        
        if isinstance(value, Coso):
            return RTResult().success(Chamuyo(f'{value.elements}'))
        
        if isinstance(value, BaseLaburo):
            return RTResult().success(Chamuyo(str(value)))
    
    exec_chamu.arg_names = ['value']
    
    def exec_num(self, exec_ctx):
        from . import Chamuyo, Numero
        value = exec_ctx.symbol_table.get('value')
        
        if not value:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                f"pocos argumentos pasados en '{self.name}'() (esperados 1, recibidos 0)",
                exec_ctx
            ))
        
        if isinstance(value, Numero):
            return RTResult().success(Numero(new_value))
        
        if isinstance(value, Chamuyo):
            # check if string is a valid string
            try:
                new_value = int(value.value)
            except ValueError:
                try:
                    new_value = float(value.value)
                except ValueError:
                    return RTResult().failure(RTError(
                        self.pos_start,
                        self.pos_end,
                        f"Literal invalido para '{self.name}()' con base 10: '{value.value}'",
                        exec_ctx
                    ))
            
            return RTResult().success(Numero(new_value))
        
        if isinstance(value, BaseLaburo):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                f"El argumento de {self.name}() debe ser un chamuyo o un número, no un 'laburo'",
                exec_ctx
            ))
    
    exec_num.arg_names = ['value']
    
    def exec_matear(self, exec_ctx):
        from . import Coso, Mataburros, Nada
        value = exec_ctx.symbol_table.get('value')
        if value is not None:
            if isinstance(value, (Coso, Mataburros)):
                print(value)
            else:
                print(value.value)
        else:
            print()
        return RTResult().success(Nada.nada)
    
    exec_matear.arg_names = ['value']
    
    def exec_morfar(self, exec_ctx):
        from . import Chamuyo
        _prefix = exec_ctx.symbol_table.get('value')
        if _prefix is not None:
            if isinstance(_prefix, Chamuyo):
                _prefix = _prefix.value
            text = input(_prefix)
        else:
            text = input()
        return RTResult().success(Chamuyo(text))
    
    exec_morfar.arg_names = ['value']

    def exec_limpiavidrios(self, exec_ctx):
        from . import Nada
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Nada.nada)
    
    exec_limpiavidrios.arg_names = []
    
    def exec_es_num(self, exec_ctx):
        from . import Boolean, Numero
        is_number = isinstance(exec_ctx.symbol_table.get('value'), Numero)
        return RTResult().success(Boolean.posta if is_number else Boolean.trucho)
    
    exec_es_num.arg_names = ['value']
    
    def exec_es_chamu(self, exec_ctx):
        from . import Boolean, Chamuyo
        is_string = isinstance(exec_ctx.symbol_table.get('value'), Chamuyo)
        return RTResult().success(Boolean.posta if is_string else Boolean.trucho)
    
    exec_es_chamu.arg_names = ['value']
    
    def exec_es_coso(self, exec_ctx):
        from . import Boolean, Coso
        is_list = isinstance(exec_ctx.symbol_table.get('value'), Coso)
        return RTResult().success(Boolean.posta if is_list else Boolean.trucho)
    
    exec_es_coso.arg_names = ['value']
    
    def exec_es_laburo(self, exec_ctx):
        from . import Boolean
        is_func = isinstance(exec_ctx.symbol_table.get('value'), BaseLaburo)
        return RTResult().success(Boolean.posta if is_func else Boolean.trucho)
    
    exec_es_laburo.arg_names = ['value']
    
    def exec_es_mataburros(self, exec_ctx):
        from . import Boolean, Mataburros
        is_dict = isinstance(exec_ctx.symbol_table.get('value'), Mataburros)
        return RTResult().success(Boolean.posta if is_dict else Boolean.trucho)
    
    exec_es_mataburros.arg_names = ['value']
    
    def exec_guardar(self, exec_ctx):
        from . import Nada, Coso
        list_ = exec_ctx.symbol_table.get('list')
        value = exec_ctx.symbol_table.get('value')

        if not isinstance(list_, Coso):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo coso.",
                exec_ctx
            ))
        
        list_.elements.append(value)
        return RTResult().success(Nada.nada)
    
    exec_guardar.arg_names = ['list', 'value']

    def exec_insertar(self, exec_ctx):
        from . import Coso, Numero, Nada
        list_ = exec_ctx.symbol_table.get('list')
        index = exec_ctx.symbol_table.get('index')
        value = exec_ctx.symbol_table.get('value')

        if not isinstance(list_, Coso):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo coso.",
                exec_ctx
            ))
        
        if not isinstance(index, Numero):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El segundo argumento debe ser de tipo número.",
                exec_ctx
            ))
        
        try:
            list_.elements.insert(index.value, value.value)
        except TypeError:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El índice debe ser un número entero.",
                exec_ctx
            ))

        return RTResult().success(Nada.nada)
    
    exec_insertar.arg_names = ['list', 'index', 'value']

    def exec_cambiaso(self, exec_ctx):
        from . import Coso, Numero, Nada
        list_ = exec_ctx.symbol_table.get('list')
        index = exec_ctx.symbol_table.get('index')
        value = exec_ctx.symbol_table.get('value')

        if not isinstance(list_, Coso):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo coso.",
                exec_ctx
            ))
        
        if not isinstance(index, Numero):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El segundo argumento debe ser de tipo número.",
                exec_ctx
            ))
        
        try:
            list_.elements[index.value] = value.value
        except TypeError:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El índice debe ser un número entero.",
                exec_ctx
            ))
        
        return RTResult().success(Nada.nada)
        
    exec_cambiaso.arg_names = ['list', 'index', 'value']
    
    def exec_sacar(self, exec_ctx):
        from . import Numero, Coso
        list_ = exec_ctx.symbol_table.get('list')
        index = exec_ctx.symbol_table.get('index')

        if not isinstance(list_, Coso):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo coso.",
                exec_ctx
            ))
        
        if not isinstance(index, Numero):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El segundo argumento debe ser de tipo número.",
                exec_ctx
            ))
        
        try:
            popped = list_.elements.pop(index.value)
        except IndexError:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                f"Elemento con el índice {index.value} no pudo ser removido del coso porque el índice está fuera de los límites.",
                exec_ctx
            ))
        
        return RTResult().success(popped)
    
    exec_sacar.arg_names = ['list', 'index']

    def exec_extender(self, exec_ctx):
        from . import Nada, Coso
        listA = exec_ctx.symbol_table.get('listA')
        listB = exec_ctx.symbol_table.get('listB')

        if not isinstance(listA, Coso):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo coso.",
                exec_ctx
            ))

        if not isinstance(listB, Coso):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El segundo argumento debe ser de tipo coso.",
                exec_ctx
            ))
        
        listA.elements.extend(listB.elements)

        return RTResult().success(Nada.nada)

    exec_extender.arg_names = ['listA', 'listB']

    def exec_agarra_de(self, exec_ctx):
        from . import Chamuyo, Numero, Mataburros, Nada
        dict_ = exec_ctx.symbol_table.get('dict')
        key = exec_ctx.symbol_table.get('key')

        if not isinstance(dict_, Mataburros):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo mataburros.",
                exec_ctx
            ))
        
        if not isinstance(key, (Numero, Chamuyo)):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El segundo argumento debe ser de tipo número o chamuyo.",
                exec_ctx
            ))
        
        for i, dictkey in enumerate(dict_.keys):
            if dictkey.value == key.value:
                return RTResult().success(dict_.values[i])
        
        return RTResult().success(Nada.nada)

    exec_agarra_de.arg_names = ['dict', 'key']

    def exec_metele_en(self, exec_ctx):
        from . import Chamuyo, Numero, Mataburros, Nada
        dict_ = exec_ctx.symbol_table.get('dict')
        key = exec_ctx.symbol_table.get('key')
        value = exec_ctx.symbol_table.get('value')

        if not isinstance(dict_, Mataburros):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo mataburros.",
                exec_ctx
            ))
        
        if not isinstance(key, (Numero, Chamuyo)):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El segundo argumento debe ser de tipo número o chamuyo.",
                exec_ctx
            ))
        
        for i, dictkey in enumerate(dict_.keys):
            if dictkey.value == key.value:
                dict_.values[i] = value
                return RTResult().success(Nada.nada)
            
        dict_.keys.append(key)
        dict_.values.append(value)
        return RTResult().success(Nada.nada)
            
    exec_metele_en.arg_names = ['dict', 'key', 'value']

    def exec_borra_de(self, exec_ctx):
        from . import Chamuyo, Numero, Mataburros, Nada
        dict_ = exec_ctx.symbol_table.get('dict')
        key = exec_ctx.symbol_table.get('key')

        if not isinstance(dict_, Mataburros):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo mataburros.",
                exec_ctx
            ))
        
        if not isinstance(key, (Numero, Chamuyo)):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El segundo argumento debe ser de tipo número o chamuyo.",
                exec_ctx
            ))
        
        for i, dictkey in enumerate(dict_.keys):
            if dictkey.value == key.value:
                del dict_.keys[i]
                del dict_.values[i]
                return RTResult().success(Nada.nada)
            
        return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                f"El elemento con la llave {key} no pudo ser encontrado en el mataburros.",
                exec_ctx
            ))
    
    exec_borra_de.arg_names = ['dict', 'key']

    def exec_existe_clave(self, exec_ctx):
        from . import Chamuyo, Numero, Mataburros, Laburo, Curro, Nada, Boolean
        dict_ = exec_ctx.symbol_table.get('dict')
        key = exec_ctx.symbol_table.get('key')

        if not isinstance(dict_, Mataburros):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo mataburros.",
                exec_ctx
            ))
        
        if not isinstance(key, (Numero, Chamuyo, Laburo, Curro)):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El segundo argumento no puede ser de tipo Coso ó Mataburros.",
                exec_ctx
            ))
        
        for _, dictkey in enumerate(dict_.keys):
            if dictkey.value == key.value:
                return RTResult().success(Boolean.posta)
        
        return RTResult().success(Nada.nada)
    
    exec_existe_clave.arg_names = ['dict', 'key']

    def exec_longitud(self, exec_ctx):
        from . import Numero, Coso, Mataburros, Chamuyo, Nada
        arg = exec_ctx.symbol_table.get('arg')

        if not isinstance(arg, (Coso, Mataburros, Chamuyo)):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El argumento debe ser de tipo coso, mataburros o chamuyo.",
                exec_ctx
            ))
        
        if isinstance(arg, Mataburros):
            return RTResult().success(Numero(len(arg.keys)))
        
        if isinstance(arg, Chamuyo):
            return RTResult().success(Numero(len(arg.value)))
        
        if isinstance(arg, Coso):
            return RTResult().success(Numero(len(arg.elements)))
        
        return RTResult().success(Nada.nada)
        
    exec_longitud.arg_names = ['arg']

    def exec_ejecutar(self, exec_ctx):
        from . import Chamuyo, Nada
        fn = exec_ctx.symbol_table.get('fn')

        if not isinstance(fn, Chamuyo):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "El primer argumento debe ser de tipo chamuyo.",
                exec_ctx
            ))
        
        fn = fn.value
        
        from os import path
        this_file = path.abspath(__file__)
        src_dir = path.dirname(os.path.dirname(this_file))
        fn = path.join(src_dir, "examples", fn)

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                f"Uy que rompimo! No pudimos abrir el archivo \'{fn}\'\n'{e}.",
                exec_ctx
            ))
        
        from run import execute as run 
        _, error = run(fn, script)

        if error:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                f"Uy que rompimo! No pudimos terminar de ejecutar el fichero \'{fn}\'\n'{error.as_string()}",
                exec_ctx
            ))
        
        return RTResult().success(Nada.nada)

    exec_ejecutar.arg_names = ['fn']

    def exec_renuncio(self, exec_ctx):
        import sys
        return RTResult().success(sys.exit())
    
    exec_renuncio.arg_names = []

# I/O
Curro.matear          = Curro('matear')
Curro.morfar          = Curro('morfar')
# Types
Curro.es_num          = Curro('es_num')
Curro.es_chamu        = Curro('es_chamu')
Curro.es_coso         = Curro('es_coso')
Curro.es_laburo       = Curro('es_laburo')
Curro.es_mataburros   = Curro('es_mataburros')
Curro.chamu           = Curro('chamu')
Curro.num             = Curro('num')
# Coso related
Curro.guardar         = Curro('guardar')
Curro.insertar        = Curro('insertar')
Curro.cambiaso        = Curro('cambiaso')
Curro.sacar           = Curro('sacar')
Curro.extender        = Curro('extender')
Curro.longitud        = Curro('longitud')
# Mataburros related
Curro.agarra_de       = Curro('agarra_de')
Curro.metele_en       = Curro('metele_en')
Curro.borra_de        = Curro('borra_de')
Curro.existe_clave    = Curro('existe_clave')
# Misc
Curro.limpiavidrios   = Curro('limpiavidrios')
Curro.ejecutar        = Curro('ejecutar')
Curro.renuncio        = Curro('renuncio')





