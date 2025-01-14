from src.lunfardo_token import Position

def pos(ftxt: str) -> Position:
    return Position(0, 0, 0, "system", ftxt)