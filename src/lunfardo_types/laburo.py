from __future__ import annotations
from .value import Value
from .boloodean import Boloodean
from src.rtresult import RTResult
from src.symbol_table import SymbolTable
from src.context import Context
from src.errors import RTError, InvalidTypeBardo
from typing import ClassVar, TYPE_CHECKING
import os

if TYPE_CHECKING:
    from src.interpreter import Interpreter


class BaseLaburo(Value):
    def __init__(self, name: str | None = None) -> None:
        super().__init__()
        self.name = name or "<injunable>"
        self.parent_context = None

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(
            new_context.parent.symbol_table if new_context.parent else None
        )
        return new_context

    def check_args(self, arg_names, args, arg_values=None):
        res = RTResult()

        if not arg_names:
            return res.success(None)

        if arg_values is None:
            arg_values = [None] * len(arg_names)

        if len(args) > len(arg_names):
            return res.failure(
                InvalidTypeBardo(
                    self.pos_start,
                    self.pos_end,
                    f"demasiados argumentos pasados a '{self.name}'() (esperados {len(arg_names)}, recibidos {len(args)})",
                    self.context,
                )
            )

        if len(args) < len(arg_names):
            if len(args) > len(
                [arg_value for arg_value in arg_values if arg_value is None]
            ):
                return res.failure(
                    InvalidTypeBardo(
                        self.pos_start,
                        self.pos_end,
                        f"pocos argumentos pasados a '{self.name}'() (esperados {len(arg_names)}, recibidos {len(args)})",
                        self.context,
                    )
                )

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx, arg_values: list[Value] | None = None):
        res = RTResult()
        from lunfardo_types import Nada
        for i, arg in enumerate(arg_names):
            if i < len(args):
                arg_value = args[i]
            else:
                try: 
                    arg_value = arg_values[i] if arg_values is not None else None
                except TypeError: 
                    arg_value = Nada.nada

            if arg_value is None:
                return res.failure(
                    InvalidTypeBardo(
                        self.pos_start,
                        self.pos_end,
                        f"no se encontró valor para el argumento '{arg}' en '{self.name}'()",
                        exec_ctx,
                    )
                )

            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg, arg_value)
        
        return res.success(None)

    def check_and_populate_args(self, arg_names, args, exec_ctx, arg_values=None):
        res = RTResult()

        if arg_values is None:
            res.register(self.check_args(arg_names, args))
        else:
            res.register(self.check_args(arg_names, args, arg_values))  # checkear esto

        if res.should_return():
            return res

        res.register(self.populate_args(arg_names, args, exec_ctx, arg_values))
        if res.error:
            return res

        return res.success(None)


class Laburo(BaseLaburo):

    def __init__(self, name, body_node, arg_names, arg_values, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.arg_values = arg_values
        self.should_auto_return = should_auto_return
        self.global_context = None
        self.memory_address = id(self)
        self.is_method: bool = False

    def execute(self, args, current_context: Context, interpreter: Interpreter):
        from . import Nada

        res = RTResult()
        # Cada vez que creamos una nueva funcion, es necesario crear un nuevo contexto con una nueva symbol table, que son destruidos una vez que la funcion retorna.
        #interpreter = Interpreter()
        execution_context = self.generate_new_context()
        execution_context.parent = current_context

        # Combine local and global contexts into one, this fixes the issue of not being able to access variables defined in the global context from inside a method.
        execution_context.symbol_table = SymbolTable(current_context.symbol_table)

        res.register(
            self.check_and_populate_args(
                self.arg_names, args, execution_context, self.arg_values
            )
        )

        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.body_node, execution_context))
        if res.should_return() and res.func_return_value is None:
            return res

        return_value = (
            (value if self.should_auto_return else None)
            or res.func_return_value
            or Nada.nada
        )
        return res.success(return_value)
    
    def is_true(self) -> bool:
        return True

    def copy(self) -> 'Laburo':
        copy = Laburo(
            self.name,
            self.body_node,
            self.arg_names,
            self.arg_values,
            self.should_auto_return,
        )
        if hasattr(self, "is_method"):
            copy.is_method = self.is_method
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __str__(self) -> str:
        return f"<laburo {self.name}>"

    def __repr__(self) -> str:
        return f"<laburo {self.name}>"


class Curro(BaseLaburo):
    matear: ClassVar["Curro"]
    morfar: ClassVar["Curro"]
    es_num: ClassVar["Curro"]
    es_chamu: ClassVar["Curro"]
    es_coso: ClassVar["Curro"]
    es_laburo: ClassVar["Curro"]
    es_mataburros: ClassVar["Curro"]
    chamu: ClassVar["Curro"]
    num: ClassVar["Curro"]
    tipo: ClassVar["Curro"]
    guardar: ClassVar["Curro"]
    insertar: ClassVar["Curro"]
    cambiaso: ClassVar["Curro"]
    sacar: ClassVar["Curro"]
    extender: ClassVar["Curro"]
    longitud: ClassVar["Curro"]
    agarra_de: ClassVar["Curro"]
    metele_en: ClassVar["Curro"]
    borra_de: ClassVar["Curro"]
    existe_clave: ClassVar["Curro"]
    limpiavidrios: ClassVar["Curro"]
    ejecutar: ClassVar["Curro"]
    renuncio: ClassVar["Curro"]
    contexto_global: ClassVar["Curro"]
    asciiAchamu: ClassVar["Curro"]

    def __init__(self, name: str | None = None, func=None) -> None:
        super().__init__(name)
        self.func = func

    def is_true(self) -> bool:
        return True

    def execute(self, args, current_context, _) -> RTResult:
        res = RTResult()
        execution_context = self.generate_new_context()
        execution_context.parent = current_context
        
        if self.func:
            return_value = res.register(self.func(execution_context))
            if return_value is None:
                from . import Nada
                return_value = Nada.nada
        else:
            method_name = f"exec_{self.name}"
            method = getattr(self, method_name, self.no_visit_method)
            res.register(
                self.check_and_populate_args(method.__func__.arg_names, args, execution_context)
            )
            if res.should_return():
                return res
            
            return_value = res.register(method(execution_context))

        if res.should_return():
            return res

        return res.success(return_value)

    def no_visit_method(self, context) -> RTResult:
        return RTResult().failure(
            RTError(
                self.pos_start,
                self.pos_end,
                f"No exec_{self.name} method defined.",
                context,
            )
        )

    def copy(self) -> 'Curro':
        copy = Curro(self.name, self.func)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self) -> str:
        return f"<curro {self.name}>"

    def __str__(self) -> str:
        return f"<curro {self.name}>"

    #########################################
    # MARK:CURROS (BUILT-IN FUNCTIONS)
    #########################################

    def exec_chamu(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo, Numero, Coso, Nada
        from errors import InvalidTypeBardo

        value = exec_ctx.symbol_table.get("value") if exec_ctx and exec_ctx.symbol_table else None

        if not value or value == Nada.nada:
            return RTResult().failure(
                InvalidTypeBardo(
                    self.pos_start,
                    self.pos_end,
                    f"pocos argumentos pasados en '{self.name}'() (esperados 1, recibidos 0)",
                    exec_ctx
                )
            )

        if isinstance(value, Numero):
            return RTResult().success(Chamuyo(str(value.value)))

        if isinstance(value, Chamuyo):
            return RTResult().success(Chamuyo(value.value))

        if isinstance(value, Coso):
            return RTResult().success(Chamuyo(f"{value.elements}"))

        if isinstance(value, BaseLaburo):
            return RTResult().success(Chamuyo(str(value)))
        
        return RTResult().failure(
            InvalidTypeBardo(
                value.pos_start,
                value.pos_end,
                "El valor del argumento solo puede ser numero, chamuyo, coso o laburo.",
                exec_ctx
            )
        )

    exec_chamu.arg_names = ["value"]

    def exec_num(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo, Numero, Nada
        from errors import InvalidTypeBardo, InvalidValueBardo

        value = exec_ctx.symbol_table.get("value") if exec_ctx and exec_ctx.symbol_table else None

        if not value:
            return RTResult().failure(
                InvalidTypeBardo(
                    self.pos_start,
                    self.pos_end,
                    f"pocos argumentos pasados en '{self.name}'() (esperados 1, recibidos 0)",
                    exec_ctx
                )
            )

        if isinstance(value, Numero):
            return RTResult().success(Numero(value.value))

        if isinstance(value, Chamuyo):
            # check if string is a valid string
            try:
                new_value = int(value.value)
            except ValueError:
                try:
                    new_value = float(value.value)
                except ValueError:
                    return RTResult().failure(
                        InvalidValueBardo(
                            value.pos_start,
                            value.pos_end,
                            f"Literal invalido para '{self.name}()' con base 10: '{value.value}'",
                            exec_ctx
                        )
                    )

            return RTResult().success(Numero(new_value))

        if isinstance(value, BaseLaburo):
            return RTResult().failure(
                InvalidTypeBardo(
                    value.pos_start,
                    value.pos_end,
                    f"El argumento de {self.name}() debe ser un chamuyo o un número, no un 'laburo'",
                    exec_ctx
                )
            )
        
        return RTResult().success(Nada.nada)

    exec_num.arg_names = ["value"]

    def exec_matear(self, exec_ctx: Context) -> RTResult:
        from . import Coso, Mataburros, Nada

        value = exec_ctx.symbol_table.get("value") if exec_ctx and exec_ctx.symbol_table else None
        if value is not None and not isinstance(value, Nada):
            if isinstance(value, (Coso, Mataburros)):
                print(value)
            else:
                print(value.value)
        else:
            print()
        return RTResult().success(Nada.nada)

    exec_matear.arg_names = ["value"]

    def exec_morfar(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo
        from lunfardo_types import Nada

        _prefix = exec_ctx.symbol_table.get("value") if exec_ctx and exec_ctx.symbol_table else None
        if _prefix and not isinstance(_prefix, Nada):
            if isinstance(_prefix, Chamuyo):
                _prefix = _prefix.value
            text = input(_prefix)
        else:
            text = input()
        return RTResult().success(Chamuyo(text))

    exec_morfar.arg_names = ["value"]

    def exec_limpiavidrios(self, exec_ctx: Context) -> RTResult:
        from . import Nada

        os.system("cls" if os.name == "nt" else "clear")
        return RTResult().success(Nada.nada)

    exec_limpiavidrios.arg_names = []

    def exec_es_num(self, exec_ctx: Context) -> RTResult:
        from . import Numero

        is_number = isinstance(exec_ctx.symbol_table.get("value"), Numero) if exec_ctx and exec_ctx.symbol_table else False
        return RTResult().success(Boloodean.posta if is_number else Boloodean.trucho)

    exec_es_num.arg_names = ["value"]

    def exec_es_chamu(self, exec_ctx: Context) -> RTResult:
        from . import Boloodean, Chamuyo

        is_string = isinstance(exec_ctx.symbol_table.get("value"), Chamuyo) if exec_ctx and exec_ctx.symbol_table else False
        return RTResult().success(Boloodean.posta if is_string else Boloodean.trucho)

    exec_es_chamu.arg_names = ["value"]

    def exec_es_coso(self, exec_ctx: Context) -> RTResult:
        from . import Boloodean, Coso

        is_list = isinstance(exec_ctx.symbol_table.get("value"), Coso) if exec_ctx and exec_ctx.symbol_table else False
        return RTResult().success(Boloodean.posta if is_list else Boloodean.trucho)

    exec_es_coso.arg_names = ["value"]

    def exec_es_laburo(self, exec_ctx: Context) -> RTResult:
        from . import Boloodean

        is_func = isinstance(exec_ctx.symbol_table.get("value"), BaseLaburo) if exec_ctx and exec_ctx.symbol_table else False
        return RTResult().success(Boloodean.posta if is_func else Boloodean.trucho)

    exec_es_laburo.arg_names = ["value"]

    def exec_es_mataburros(self, exec_ctx: Context) -> RTResult:
        from . import Boloodean, Mataburros

        is_mataburros = isinstance(exec_ctx.symbol_table.get("value"), Mataburros) if exec_ctx and exec_ctx.symbol_table else False
        return RTResult().success(Boloodean.posta if is_mataburros else Boloodean.trucho)

    exec_es_mataburros.arg_names = ["value"]

    def exec_guardar(self, exec_ctx: Context) -> RTResult:
        from . import Nada, Coso
        from errors import InvalidTypeBardo

        list_ = exec_ctx.symbol_table.get("list") if exec_ctx and exec_ctx.symbol_table else None
        value = exec_ctx.symbol_table.get("value") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(list_, Coso):
            return RTResult().failure(
                InvalidTypeBardo(
                    list_.pos_start if list_ else self.pos_start,
                    list_.pos_end if list_ else self.pos_end,
                    "El argumento debe ser de tipo coso",
                    exec_ctx
                )
            )

        list_.elements.append(value)
        return RTResult().success(Nada.nada)

    exec_guardar.arg_names = ["list", "value"]

    def exec_insertar(self, exec_ctx: Context) -> RTResult:
        from . import Coso, Numero, Nada
        from errors import InvalidTypeBardo

        list_ = exec_ctx.symbol_table.get("list") if exec_ctx and exec_ctx.symbol_table else None
        index = exec_ctx.symbol_table.get("index") if exec_ctx and exec_ctx.symbol_table else None
        value = exec_ctx.symbol_table.get("value") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(list_, Coso):
            return RTResult().failure(
                InvalidTypeBardo(
                    list_.pos_start if list_ else self.pos_start,
                    list_.pos_end if list_ else self.pos_end,
                    "El argumento debe ser de tipo coso",
                    exec_ctx
                )
            )

        if not isinstance(index, Numero):
            return RTResult().failure(
                InvalidTypeBardo(
                    index.pos_start if index else self.pos_start,
                    index.pos_end if index else self.pos_end,
                    "El argumento debe ser de tipo numero",
                    exec_ctx
                )
            )

        try:
            list_.elements.insert(int(index.value), value)
        except TypeError:
            return RTResult().failure(
                InvalidTypeBardo(
                    index.pos_start,
                    index.pos_end,
                    "El argumento debe ser un entero.",
                    exec_ctx
                )
            )

        return RTResult().success(Nada.nada)

    exec_insertar.arg_names = ["list", "index", "value"]

    def exec_cambiaso(self, exec_ctx: Context) -> RTResult:
        from . import Coso, Numero, Nada
        from errors import InvalidIndexBardo, InvalidTypeBardo

        list_ = exec_ctx.symbol_table.get("list") if exec_ctx and exec_ctx.symbol_table else None
        index = exec_ctx.symbol_table.get("index") if exec_ctx and exec_ctx.symbol_table else None
        value = exec_ctx.symbol_table.get("value") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(list_, Coso):
            return RTResult().failure(
                InvalidTypeBardo(
                    list_.pos_start if list_ else self.pos_start,
                    list_.pos_end if list_ else self.pos_end,
                    "El argumento debe ser de tipo coso",
                    exec_ctx
                )
            )

        if not isinstance(index, Numero):
            return RTResult().failure(
                InvalidTypeBardo(
                    index.pos_start if index else self.pos_start,
                    index.pos_end if index else self.pos_end,
                    "El argumento debe ser de tipo numero",
                    exec_ctx
                )
            )

        try:
            list_.elements[int(index.value)] = value
        except TypeError:
            return RTResult().failure(
                InvalidTypeBardo(
                    index.pos_start,
                    index.pos_end,
                    "El argumento debe ser un entero.",
                    exec_ctx
                )
            )
        except IndexError:
            return RTResult().failure(
                InvalidIndexBardo(
                    index.pos_start,
                    index.pos_end,
                    f"Elemento con el índice '{index.value}' no pudo ser reemplazado del coso porque el índice está fuera de los límites.",
                    exec_ctx
                )
            )

        return RTResult().success(Nada.nada)

    exec_cambiaso.arg_names = ["list", "index", "value"]

    def exec_sacar(self, exec_ctx: Context) -> RTResult:
        from . import Numero, Coso
        from errors import InvalidIndexBardo, InvalidTypeBardo

        list_ = exec_ctx.symbol_table.get("list") if exec_ctx and exec_ctx.symbol_table else None
        index = exec_ctx.symbol_table.get("index") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(list_, Coso):
            return RTResult().failure(
                InvalidTypeBardo(
                    list_.pos_start if list_ else self.pos_start,
                    list_.pos_end if list_ else self.pos_end,
                    "El argumento debe ser de tipo coso.",
                    exec_ctx
                )
            )

        if not isinstance(index, Numero):
            return RTResult().failure(
                InvalidTypeBardo(
                    index.pos_start if index else self.pos_start,
                    index.pos_end if index else self.pos_end,
                    "El argumento debe ser de tipo numero.",
                    exec_ctx
                )
            )

        try:
            popped = list_.elements.pop(int(index.value))
        except IndexError:
            return RTResult().failure(
                InvalidIndexBardo(
                    self.pos_start,
                    self.pos_end,
                    f"Elemento con el índice '{index.value}' no pudo ser removido del coso porque el índice está fuera de los límites.",
                    exec_ctx
                )
            )

        return RTResult().success(popped)

    exec_sacar.arg_names = ["list", "index"]

    def exec_extender(self, exec_ctx: Context) -> RTResult:
        from . import Nada, Coso
        from errors import InvalidTypeBardo

        listA = exec_ctx.symbol_table.get("listA") if exec_ctx and exec_ctx.symbol_table else None
        listB = exec_ctx.symbol_table.get("listB") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(listA, Coso):
            return RTResult().failure(
                InvalidTypeBardo(
                    listA.pos_start if listA else self.pos_start,
                    listA.pos_end if listA else self.pos_end,
                    "El argumento debe ser de tipo coso.",
                    exec_ctx
                )
            )

        if not isinstance(listB, Coso):
            return RTResult().failure(
                InvalidTypeBardo(
                    listB.pos_start if listB else self.pos_start,
                    listB.pos_end if listB else self.pos_end,
                    "El argumento debe ser de tipo coso.",
                    exec_ctx
                )
            )

        listA.elements.extend(listB.elements)

        return RTResult().success(Nada.nada)

    exec_extender.arg_names = ["listA", "listB"]

    def exec_agarra_de(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo, Numero, Mataburros, Nada
        from errors import InvalidTypeBardo

        dict_ = exec_ctx.symbol_table.get("dict") if exec_ctx and exec_ctx.symbol_table else None
        key = exec_ctx.symbol_table.get("key") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(dict_, Mataburros):
            return RTResult().failure(
                InvalidTypeBardo(
                    dict_.pos_start if dict_ else self.pos_start,
                    dict_.pos_end if dict_ else self.pos_end,
                    "El argumento debe ser de tipo mataburros",
                    exec_ctx
                )
            )

        if not isinstance(key, (Numero, Chamuyo)):
            return RTResult().failure(
                InvalidTypeBardo(
                    key.pos_start if key else self.pos_start,
                    key.pos_end if key else self.pos_end,
                    "El argumento debe ser de tipo numero o chamuyo.",
                    exec_ctx
                )
            )

        value = dict_.get_value(key)
        if value is not None:
            return RTResult().success(value)

        return RTResult().success(Nada.nada)

    exec_agarra_de.arg_names = ["dict", "key"]

    def exec_metele_en(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo, Numero, Mataburros, Nada
        from errors import InvalidTypeBardo

        dict_ = exec_ctx.symbol_table.get("dict") if exec_ctx and exec_ctx.symbol_table else None
        key = exec_ctx.symbol_table.get("key") if exec_ctx and exec_ctx.symbol_table else None
        value = exec_ctx.symbol_table.get("value") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(dict_, Mataburros):
            return RTResult().failure(
                InvalidTypeBardo(
                    dict_.pos_start if dict_ else self.pos_start    ,
                    dict_.pos_end if dict_ else self.pos_end,
                    "El argumento debe ser de tipo mataburros",
                    exec_ctx
                )
            )

        if not isinstance(key, (Numero, Chamuyo)):
            return RTResult().failure(
                InvalidTypeBardo(
                    key.pos_start if key else self.pos_start,
                    key.pos_end if key else self.pos_end,
                    "El argumento debe ser de tipo numero o chamuyo.",
                    exec_ctx
                )
            )

        dict_.set_pair(key, value)
        return RTResult().success(Nada.nada)

    exec_metele_en.arg_names = ["dict", "key", "value"]

    def exec_borra_de(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo, Numero, Mataburros, Nada
        from errors import InvalidTypeBardo, InvalidKeyBardo

        dict_ = exec_ctx.symbol_table.get("dict") if exec_ctx and exec_ctx.symbol_table else None
        key = exec_ctx.symbol_table.get("key") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(dict_, Mataburros):
            return RTResult().failure(
                InvalidTypeBardo(
                    dict_.pos_start if dict_ else self.pos_start,
                    dict_.pos_end if dict_ else self.pos_end,
                    "El argumento debe ser de tipo mataburros",
                    exec_ctx
                )
            )

        if not isinstance(key, (Numero, Chamuyo)):
            return RTResult().failure(
                InvalidTypeBardo(
                    key.pos_start if key else self.pos_start,
                    key.pos_end if key else self.pos_end,
                    "El argumento debe ser de tipo numero o chamuyo.",
                    exec_ctx
                )
            )

        deleted = dict_.del_key(key)
        if deleted:
            return RTResult().success(Nada.nada)
        
        return RTResult().failure(
            InvalidKeyBardo(
                key.pos_start,
                key.pos_end,
                f"El elemento con la clave {key} no pudo ser encontrado en el mataburros.",
                exec_ctx
            )
        )

    exec_borra_de.arg_names = ["dict", "key"]

    def exec_existe_clave(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo, Numero, Mataburros, Nada, Boloodean
        from errors import InvalidTypeBardo

        dict_ = exec_ctx.symbol_table.get("dict") if exec_ctx and exec_ctx.symbol_table else None
        key = exec_ctx.symbol_table.get("key") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(dict_, Mataburros):
            return RTResult().failure(
                InvalidTypeBardo(
                    dict_.pos_start if dict_ else self.pos_start,
                    dict_.pos_end if dict_ else self.pos_end,
                    "El argumento debe ser de tipo mataburros",
                    exec_ctx
                )
            )

        if not isinstance(key, (Numero, Chamuyo, Nada, Boloodean)):
            return RTResult().failure(
                InvalidTypeBardo(
                    key.pos_start if key else self.pos_start,
                    key.pos_end if key else self.pos_end,
                    "El argumento debe ser de tipo numero, chamuyo, nada o boloodean",
                    exec_ctx
                )
            )

        if dict_.get_value(key) is not None:
            return RTResult().success(Boloodean.posta)
        
        return RTResult().success(Nada.nada)

    exec_existe_clave.arg_names = ["dict", "key"]

    def exec_longitud(self, exec_ctx: Context) -> RTResult:
        from . import Numero, Coso, Mataburros, Chamuyo, Nada
        from errors import InvalidTypeBardo

        arg = exec_ctx.symbol_table.get("arg") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(arg, (Coso, Mataburros, Chamuyo)):
            return RTResult().failure(
                InvalidTypeBardo(
                    arg.pos_start if arg else self.pos_start,
                    arg.pos_end if arg else self.pos_end,
                    "El argumento debe ser de tipo coso, chamuyo o mataburros",
                    exec_ctx
                )
            )

        if isinstance(arg, Mataburros):
            return RTResult().success(Numero(arg.count))

        if isinstance(arg, Chamuyo):
            return RTResult().success(Numero(len(arg.value)))

        if isinstance(arg, Coso):
            return RTResult().success(Numero(len(arg.elements)))

        return RTResult().success(Nada.nada)

    exec_longitud.arg_names = ["arg"]

    def exec_ejecutar(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo
        from errors import InvalidTypeBardo, FileNotFoundBardo

        fn = exec_ctx.symbol_table.get("fn") if exec_ctx and exec_ctx.symbol_table else None

        if not isinstance(fn, Chamuyo):
            return RTResult().failure(
                InvalidTypeBardo(
                    fn.pos_start if fn else self.pos_start,
                    fn.pos_end if fn else self.pos_end,
                    "El argumento debe ser de tipo chamuyo",
                    exec_ctx
                )
            )

        fn = fn.value

        from pathlib import Path
        cwd = exec_ctx.get_cwd() or "."
        current_dir = Path(cwd)
        file_path = current_dir / fn

        try:
            with open(file_path, "r", encoding='utf-8') as f:
                script = f.read()
        except FileNotFoundError:
            parent_dir = current_dir
            while parent_dir.name != 'src':
                parent_dir = parent_dir.parent
            
            file_path = parent_dir / 'builtin' / fn

            try:
                with open(file_path, "r", encoding='utf-8') as f:
                    script = f.read()
            except FileNotFoundError:
                return RTResult().failure(
                    FileNotFoundBardo(
                        self.pos_start,
                        self.pos_end,
                        fn,
                        exec_ctx
                    )
                )

        from src.lunfardo import Lunfardo

        result, error, _ = Lunfardo().execute(file_path, script, str(current_dir), parent_context=exec_ctx)

        if error:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Uy que rompimo! No pudimos terminar de ejecutar el fichero '{fn}'\n'{error.as_string(nested=True)}",
                    exec_ctx,
                )
            )

        return RTResult().success(result)

    exec_ejecutar.arg_names = ["fn"]

    def exec_renuncio(self, exec_ctx: Context) -> RTResult:
        import sys

        return RTResult().success(sys.exit())

    exec_renuncio.arg_names = []

    def exec_contexto_global(self, exec_ctx: Context) -> RTResult:
        from . import Mataburros, Boloodean

        _local = exec_ctx.symbol_table.get("local") if exec_ctx and exec_ctx.symbol_table else None
        if isinstance(_local, Boloodean):
            if not _local.value:
                current_context = exec_ctx
                while current_context.parent is not None:
                    current_context = current_context.parent
            else:
                current_context = exec_ctx

        if current_context.symbol_table is not None:
            ctx = Mataburros.from_dict(current_context.symbol_table.symbols)
        else:
            ctx = Mataburros.from_dict({})
        return RTResult().success(ctx)
    
    exec_contexto_global.arg_names = ['local']

    def exec_asciiAchamu(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Chamuyo, Numero
        from errors import InvalidTypeBardo

        code = exec_ctx.symbol_table.get("ascii_code") if exec_ctx and exec_ctx.symbol_table else None
        if not isinstance(code, Numero):
            return RTResult().failure(
                InvalidTypeBardo(
                    code.pos_start if code else self.pos_start,
                    code.pos_end if code else self.pos_end,
                    "El argumento debe ser de tipo numero",
                    exec_ctx
                )
            )
        
        code = int(code.value)

        return RTResult().success(Chamuyo(chr(code)))
    
    exec_asciiAchamu.arg_names = ['ascii_code']

    def exec_tipo(self, exec_ctx: Context) -> RTResult:
        from src.lunfardo_types import Boloodean, Chamuyo, Cheto, Coso, Mataburros, Nada, Numero

        obj = exec_ctx.symbol_table.get('obj') if exec_ctx and exec_ctx.symbol_table else None
        if isinstance(obj, Boloodean):
            return RTResult().success(Chamuyo('Boloodean'))
        if isinstance(obj, Chamuyo):
            return RTResult().success(Chamuyo('Chamuyo'))
        if isinstance(obj, Cheto):
            return RTResult().success(Chamuyo('Cheto'))
        if isinstance(obj, Coso):
            return RTResult().success(Chamuyo('Coso'))
        if isinstance(obj, Curro):
            return RTResult().success(Chamuyo('Curro'))
        if isinstance(obj, Laburo):
            return RTResult().success(Chamuyo('Laburo'))
        if isinstance(obj, Mataburros):
            return RTResult().success(Chamuyo('Mataburros'))
        if isinstance(obj, Nada):
            return RTResult().success(Chamuyo('Nada'))
        if isinstance(obj, Numero):
            return RTResult().success(Chamuyo('Numero'))

        return RTResult().success(Nada.nada)
    
    exec_tipo.arg_names = ['obj']

# I/O
Curro.matear = Curro("matear")
Curro.morfar = Curro("morfar")
# Types
Curro.es_num = Curro("es_num")
Curro.es_chamu = Curro("es_chamu")
Curro.es_coso = Curro("es_coso")
Curro.es_laburo = Curro("es_laburo")
Curro.es_mataburros = Curro("es_mataburros")
Curro.chamu = Curro("chamu")
Curro.num = Curro("num")
Curro.tipo = Curro('tipo')
# Coso related
Curro.guardar = Curro("guardar")
Curro.insertar = Curro("insertar")
Curro.cambiaso = Curro("cambiaso")
Curro.sacar = Curro("sacar")
Curro.extender = Curro("extender")
Curro.longitud = Curro("longitud")
# Mataburros related
Curro.agarra_de = Curro("agarra_de")
Curro.metele_en = Curro("metele_en")
Curro.borra_de = Curro("borra_de")
Curro.existe_clave = Curro("existe_clave")
# Misc
Curro.limpiavidrios = Curro("limpiavidrios")
Curro.ejecutar = Curro("ejecutar")
Curro.renuncio = Curro("renuncio")
Curro.contexto_global = Curro("contexto_global")
Curro.asciiAchamu = Curro("asciiAchamu")
