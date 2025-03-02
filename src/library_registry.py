from errors.errors import RTError
from lunfardo_parser import RTResult

LIBRARY_HANDLERS = {}

def register_library_handler(lib_name: str, handler):
    LIBRARY_HANDLERS[lib_name] = handler

def get_library_handler(lib_name: str):
    return LIBRARY_HANDLERS.get(lib_name, None)

# Gualichos handler.
def init_gualichos(module_context, node, context):
    res = RTResult()
    try:
        from builtin.lib.gualichos import Gualichos, addstr_adapter, getch_adapter, clear_adapter, quit_adapter
        wrapper_instance = Gualichos()
        from lunfardo_types import Curro
        gualichos_functions = {
            "addstr": lambda exec_ctx: addstr_adapter(wrapper_instance, exec_ctx.symbol_table.get("texto").value),
            "getch": lambda exec_ctx: getch_adapter(wrapper_instance),
            "clear": lambda exec_ctx: clear_adapter(wrapper_instance),
            "quit": lambda exec_ctx: quit_adapter(wrapper_instance)
        }
        for name, func in gualichos_functions.items():
            curro_instance = Curro(name, func)
            module_context.symbol_table.set(name, curro_instance)
    except ImportError as e:
        return res.failure(RTError(node.pos_start, node.pos_end, f"Error importing library 'gualichos': {str(e)}", context))
    except AttributeError:
        return res.failure(RTError(node.pos_start, node.pos_end, f"Error in library 'gualichos'", context))
    return res.success(None)


register_library_handler("gualichos", init_gualichos)
