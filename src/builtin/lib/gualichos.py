import curses
from lunfardo_parser import RTResult

# Facade
class Gualichos:
    def __init__(self):
        self.ventana = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.ventana.keypad(True)

    def addstr(self, texto):
        self.ventana.addstr(texto)
        self.ventana.refresh()

    def getch(self):
        return self.ventana.getch()

    def clear(self):
        self.ventana.clear()
        self.ventana.refresh()

    def quit(self):
        curses.nocbreak()
        self.ventana.keypad(False)
        curses.echo()
        curses.endwin()

# Adapter functions
def addstr_adapter(facade, text):
    facade.addstr(text)
    return RTResult().success(None)

def getch_adapter(facade):
    value = facade.getch()
    return RTResult().success(value)

def clear_adapter(facade):
    facade.clear()
    return RTResult().success(None)

def quit_adapter(facade):
    facade.quit()
    return RTResult().success(None)