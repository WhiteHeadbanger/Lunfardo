class Position:

    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char = None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
    
class Token:
    
    def __init__(self, type_, value = None, pos_start = None, pos_end = None):
        self.type = type_
        self.value = value
        
        if pos_start is not None:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end is not None:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}: {self.value}'
        
        return f'{self.type}'