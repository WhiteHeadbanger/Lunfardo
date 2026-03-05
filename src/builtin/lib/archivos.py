from src.rtresult import RTResult
from src.lunfardo_types import Numero, Chamuyo, Nada, Coso
from typing import IO, Any
from enum import Enum, auto

class Error(Enum):
    ARCHIVO_NO_ENCONTRADO = auto()
    BARDO_DE_PERMISO = auto()
    ES_UN_DIRECTORIO = auto()
    BARDO_DE_VALOR = auto()
    BARDO_DE_TIPO = auto()
    BARDO_UNICODE_DECODE = auto()
    BARDO_UNICODE_ENCODE = auto()
    BARDO_DE_IO = auto()
    BARDO_DE_SISTEMA = auto()

def handle_error(error: Exception) -> Error:
    if isinstance(error, FileNotFoundError):
        return Error.ARCHIVO_NO_ENCONTRADO
    elif isinstance(error, PermissionError):
        return Error.BARDO_DE_PERMISO
    elif isinstance(error, IsADirectoryError):
        return Error.ES_UN_DIRECTORIO
    elif isinstance(error, ValueError):
        return Error.BARDO_DE_VALOR
    elif isinstance(error, TypeError):
        return Error.BARDO_DE_TIPO
    elif isinstance(error, UnicodeDecodeError):
        return Error.BARDO_UNICODE_DECODE
    elif isinstance(error, UnicodeEncodeError):
        return Error.BARDO_UNICODE_ENCODE
    elif isinstance(error, IOError):
        return Error.BARDO_DE_IO
    
    return Error.BARDO_DE_SISTEMA

class Archivo:

    def __init__(self):
        self.open_files: dict[int, IO[Any]] = {}
        self.current_id: int = 0

    def open(self, path: str, mode: str = 'r', encoding: str = 'utf-8') -> tuple[int | None, Error | None]:
        result = None
        try:
            archivo = open(path, mode, encoding=encoding)
            self.open_files[self.current_id] = archivo
            self.current_id += 1
            result = self.current_id - 1
            return result, None
        except Exception as e:
            return None, handle_error(e)

    def read(self, file_id) -> tuple[str | None, Error | None]:
        result = None
        try:
            archivo = self.open_files[file_id]
            result = archivo.read()
            return result, None
        except Exception as e:
            return None, handle_error(e)

    def write(self, file_id, content: str) -> tuple[None, Error | None]:
        try:
            archivo = self.open_files[file_id]
            archivo.write(content)
            return None, None
        except Exception as e:
            return None, handle_error(e)

    def close(self, file_id) -> tuple[None, Error | None]:
        try:
            archivo = self.open_files[file_id]
            archivo.close()
            del self.open_files[file_id]
            return None, None
        except Exception as e:
            return None, handle_error(e)
        
def open_adapter(facade, path, mode='r', encoding='utf-8') -> RTResult:
    result, error = facade.open(path, mode, encoding)

    file_value = Numero(result) if result is not None else Nada.nada
    error_value = Chamuyo(error.name.lower()) if error is not None else Nada.nada

    return RTResult().success(
        Coso([file_value, error_value])
    )

def read_adapter(facade, file_id) -> RTResult:
    result, error = facade.read(file_id)

    content_value = Chamuyo(result) if result is not None else Nada.nada
    error_value = Chamuyo(error.name.lower()) if error is not None else Nada.nada

    return RTResult().success(
        Coso([content_value, error_value])
    )

def write_adapter(facade, file_id, content) -> RTResult:
    _, error = facade.write(file_id, content)

    error_value = Chamuyo(error.name.lower()) if error is not None else Nada.nada
    return RTResult().success(
        Coso([Nada.nada, error_value])
    )

def close_adapter(facade, file_id) -> RTResult:
    _, error = facade.close(file_id)

    error_value = Chamuyo(error.name.lower()) if error is not None else Nada.nada

    return RTResult().success(
        Coso([Nada.nada, error_value])
    )