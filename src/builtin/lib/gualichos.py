import curses
from rtresult import RTResult
from lunfardo_types import Numero, Chamuyo, Coso

# Facade
class Gualichos:
    def __init__(self):
        self.ventana = curses.initscr()

    ##### WINDOW/SCREEN METHODS #####
    def noecho(self):
        curses.noecho()

    def cbreak(self):
        curses.cbreak()

    def nocbreak(self):
        curses.nocbreak()

    def keypad(self, boolean):
        self.ventana.keypad(boolean)

    def getmaxyx(self):
        return self.ventana.getmaxyx()
    
    def echo(self):
        curses.echo()

    def refresh(self):
        self.ventana.refresh()

    def erase(self):
        self.ventana.erase()
    
    def clear(self):
        self.ventana.clear()
        self.ventana.refresh()

    def border(self):
        self.ventana.border()
        self.ventana.refresh()

    ##### INPUT METHODS #####
    def getch(self):
        return self.ventana.getch()
    
    def getkey(self):
        return self.ventana.getkey()
    
    def getstr(self):
        return self.ventana.getstr().decode("utf-8")
    
    ##### OUTPUT METHODS #####
    def addch(self, ch, y = None, x = None):
        if y is not None and x is not None:
            self.ventana.addch(y, x, ch)
        else:
            self.ventana.addch(ch)
        self.ventana.refresh()

    def addstr(self, texto, y = None, x = None):
        if y is not None and x is not None:
            self.ventana.addstr(y, x, texto)
        else:
            self.ventana.addstr(texto)
        self.ventana.refresh()

    def insstr(self, texto, y = None, x = None):
        if y is not None and x is not None:
            self.ventana.insstr(y, x, texto)
        else:
            self.ventana.insstr(texto)
        self.ventana.refresh()

    def deleteln(self):
        self.ventana.deleteln()
        self.ventana.refresh()

    def insln(self):
        self.ventana.insln()
        self.ventana.refresh()

    def quit(self):
        curses.nocbreak()
        self.ventana.keypad(False)
        curses.echo()
        curses.endwin()

# Adapter functions
def noecho_adapter(facade):
    facade.noecho()
    return RTResult().success(None)

def cbreak_adapter(facade):
    facade.cbreak()
    return RTResult().success(None)

def nocbreak_adapter(facade):
    facade.nocbreak()
    return RTResult().success(None)

def keypad_adapter(facade, boolean):
    facade.keypad(boolean)
    return RTResult().success(None)

def getmaxyx_adapter(facade):
    y, x = facade.getmaxyx()
    return RTResult().success(Coso([Numero(y), Numero(x)]))

def echo_adapter(facade):
    facade.echo()
    return RTResult().success(None)

def refresh_adapter(facade):
    facade.refresh()
    return RTResult().success(None)

def erase_adapter(facade):
    facade.erase()
    return RTResult().success(None)

def clear_adapter(facade):
    facade.clear()
    return RTResult().success(None)

def border_adapter(facade):
    facade.border()
    return RTResult().success(None)

def getch_adapter(facade):
    value = facade.getch()
    return RTResult().success(Numero(value))

def getkey_adapter(facade):
    value = facade.getkey()
    return RTResult().success(Chamuyo(value))

def getstr_adapter(facade):
    value = facade.getstr()
    return RTResult().success(Chamuyo(value))

def addch_adapter(facade, ch, y = None, x = None):
    if y is not None and x is not None:
        facade.addch(ch, int(y), int(x))
    else:
        facade.addch(ch)
    return RTResult().success(None)

def addstr_adapter(facade, text: str, y: int = None, x: int = None):
    facade.addstr(text, int(y), int(x))
    return RTResult().success(None)

def insstr_adapter(facade, text, y = None, x = None):
    if y is not None and x is not None:
        facade.insstr(text, int(y), int(x))
    else:
        facade.insstr(text)
    return RTResult().success(None)

def deleteln_adapter(facade):
    facade.deleteln()
    return RTResult().success(None)

def insln_adapter(facade):
    facade.insln()
    return RTResult().success(None)

def quit_adapter(facade):
    facade.quit()
    return RTResult().success(None)