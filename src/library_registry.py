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
        from builtin.lib.gualichos import (
            Gualichos, addstr_adapter, getch_adapter, clear_adapter, 
            quit_adapter, border_adapter, getkey_adapter, getstr_adapter, 
            echo_adapter, refresh_adapter, erase_adapter, addch_adapter,
            insstr_adapter, deleteln_adapter, insln_adapter, noecho_adapter,
            cbreak_adapter, keypad_adapter, getmaxyx_adapter, nocbreak_adapter
        )
        wrapper_instance = Gualichos()
        from lunfardo_types import Curro
        gualichos_functions = {
            "noecho": lambda exec_ctx: noecho_adapter(wrapper_instance),
            "cbreak": lambda exec_ctx: cbreak_adapter(wrapper_instance),
            "nocbreak": lambda exec_ctx: nocbreak_adapter(wrapper_instance),
            "keypad": lambda exec_ctx: keypad_adapter(wrapper_instance, exec_ctx.symbol_table.get("boloodean").value),
            "getmaxyx": lambda exec_ctx: getmaxyx_adapter(wrapper_instance),
            "echo": lambda exec_ctx: echo_adapter(wrapper_instance),
            "refresh": lambda exec_ctx: refresh_adapter(wrapper_instance),
            "erase": lambda exec_ctx: erase_adapter(wrapper_instance),
            "clear": lambda exec_ctx: clear_adapter(wrapper_instance),
            "addch": lambda exec_ctx: addch_adapter(wrapper_instance, exec_ctx.symbol_table.get("ch").value, exec_ctx.symbol_table.get("y_").value, exec_ctx.symbol_table.get("x").value),
            "addstr": lambda exec_ctx: addstr_adapter(wrapper_instance, exec_ctx.symbol_table.get("texto").value, exec_ctx.symbol_table.get("y_").value, exec_ctx.symbol_table.get("x").value),
            "insstr": lambda exec_ctx: insstr_adapter(wrapper_instance, exec_ctx.symbol_table.get("texto").value, exec_ctx.symbol_table.get("y_").value, exec_ctx.symbol_table.get("x").value),
            "getch": lambda exec_ctx: getch_adapter(wrapper_instance),
            "quit": lambda exec_ctx: quit_adapter(wrapper_instance),
            "border": lambda exec_ctx: border_adapter(wrapper_instance),
            "getkey": lambda exec_ctx: getkey_adapter(wrapper_instance),
            "getstr": lambda exec_ctx: getstr_adapter(wrapper_instance),
            "deleteln": lambda exec_ctx: deleteln_adapter(wrapper_instance),
            "insln": lambda exec_ctx: insln_adapter(wrapper_instance),
            
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
