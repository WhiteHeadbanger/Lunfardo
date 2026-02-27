import curses
from rtresult import RTResult
from lunfardo_types import Numero, Chamuyo, Coso, Nada

# Facade
class Gualichos:
    def __init__(self) -> None:
        self.ventana = curses.initscr()

    ##### WINDOW/SCREEN METHODS #####
    def noecho(self) -> None:
        curses.noecho()

    def cbreak(self) -> None:
        curses.cbreak()

    def nocbreak(self) -> None:
        curses.nocbreak()

    def keypad(self, boolean) -> None:
        self.ventana.keypad(boolean)

    def getmaxyx(self) -> tuple[int, int]:
        return self.ventana.getmaxyx()
    
    def echo(self) -> None:
        curses.echo()

    def refresh(self) -> None:
        self.ventana.refresh()

    def erase(self) -> None:
        self.ventana.erase()
    
    def clear(self) -> None:
        self.ventana.clear()
        self.ventana.refresh()

    def border(self) -> None:
        self.ventana.border()
        self.ventana.refresh()

    ##### INPUT METHODS #####
    def getch(self) -> int:
        return self.ventana.getch()
    
    def getkey(self) -> str:
        return self.ventana.getkey()
    
    def getstr(self) -> str:
        return self.ventana.getstr().decode("utf-8")
    
    ##### OUTPUT METHODS #####
    def addch(self, ch, y = None, x = None) -> None:
        if y is not None and x is not None:
            self.ventana.addch(y, x, ch)
        else:
            self.ventana.addch(ch)
        self.ventana.refresh()

    def addstr(self, texto, y = None, x = None) -> None:
        if y is not None and x is not None:
            self.ventana.addstr(y, x, texto)
        else:
            self.ventana.addstr(texto)
        self.ventana.refresh()

    def insstr(self, texto, y = None, x = None) -> None:
        if y is not None and x is not None:
            self.ventana.insstr(y, x, texto)
        else:
            self.ventana.insstr(texto)
        self.ventana.refresh()

    def deleteln(self) -> None:
        self.ventana.deleteln()
        self.ventana.refresh()

    def insln(self) -> None:
        self.ventana.insln()
        self.ventana.refresh()

    def quit(self) -> None:
        curses.nocbreak()
        self.ventana.keypad(False)
        curses.echo()
        curses.endwin()

# Adapter functions
def noecho_adapter(facade) -> RTResult:
    facade.noecho()
    return RTResult().success(Nada.nada)

def cbreak_adapter(facade) -> RTResult:
    facade.cbreak()
    return RTResult().success(Nada.nada)

def nocbreak_adapter(facade) -> RTResult:
    facade.nocbreak()
    return RTResult().success(Nada.nada)

def keypad_adapter(facade, boolean) -> RTResult:
    facade.keypad(boolean)
    return RTResult().success(Nada.nada)

def getmaxyx_adapter(facade) -> RTResult:
    y, x = facade.getmaxyx()
    return RTResult().success(Coso([Numero(y), Numero(x)]))

def echo_adapter(facade) -> RTResult:
    facade.echo()
    return RTResult().success(Nada.nada)

def refresh_adapter(facade) -> RTResult:
    facade.refresh()
    return RTResult().success(Nada.nada)

def erase_adapter(facade) -> RTResult:
    facade.erase()
    return RTResult().success(Nada.nada)

def clear_adapter(facade) -> RTResult:
    facade.clear()
    return RTResult().success(Nada.nada)

def border_adapter(facade) -> RTResult:
    facade.border()
    return RTResult().success(Nada.nada)

def getch_adapter(facade) -> RTResult:
    value = facade.getch()
    return RTResult().success(Numero(value))

def getkey_adapter(facade) -> RTResult:
    value = facade.getkey()
    return RTResult().success(Chamuyo(value))

def getstr_adapter(facade) -> RTResult:
    value = facade.getstr()
    return RTResult().success(Chamuyo(value))

def addch_adapter(facade, ch, y = None, x = None) -> RTResult:
    if y is not None and x is not None:
        facade.addch(ch, int(y), int(x))
    else:
        facade.addch(ch)
    return RTResult().success(Nada.nada)

def addstr_adapter(facade, text: str, y = None, x = None) -> RTResult:
    if y is not None and x is not None:
        facade.addstr(text, int(y), int(x))
    else:
        facade.addstr(text)
    return RTResult().success(Nada.nada)

def insstr_adapter(facade, text, y = None, x = None) -> RTResult:
    if y is not None and x is not None:
        facade.insstr(text, int(y), int(x))
    else:
        facade.insstr(text)
    return RTResult().success(Nada.nada)

def deleteln_adapter(facade) -> RTResult:
    facade.deleteln()
    return RTResult().success(Nada.nada)

def insln_adapter(facade) -> RTResult:
    facade.insln()
    return RTResult().success(Nada.nada)

def quit_adapter(facade) -> RTResult:
    facade.quit()
    return RTResult().success(Nada.nada)