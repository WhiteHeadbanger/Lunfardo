from src.rtresult import RTResult
from src.lunfardo_types import Numero, Chamuyo, Nada, Coso
from typing import IO, Any
from enum import Enum, auto

class Error(Enum):
    """
    Enumeration of normalized file I/O errors exposed by the `archivos` runtime.

    These values represent Lunfardo-level error categories produced when Python
    file operations fail. The runtime maps Python exceptions to these values
    through `handle_error()` so the language receives a stable and predictable
    error set independent of the underlying OS.
    """
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
    """
    Convert a Python exception raised during file I/O into a Lunfardo `Error`.

    This function acts as a translation layer between Python's exception system
    and Lunfardo's error model. Known exception types are mapped to specific
    `Error` enum values. Any unrecognized exception falls back to
    `Error.BARDO_DE_SISTEMA`.

    Parameters
    ----------
    error
        The Python exception raised during a file operation.

    Returns
    -------
    Error
        The corresponding Lunfardo error category.
    """
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
    """
    Facade responsible for managing open files in the Lunfardo runtime.

    The class maintains an internal table of open file handles indexed by
    numeric identifiers. These identifiers are returned to the language layer
    and used for subsequent operations such as reading, writing, or closing
    the file.

    Each method returns a tuple `(result, error)` where only one value should
    be non-null:
        - On success: `(result, None)`
        - On failure: `(None, Error)`

    File handles remain valid until `close()` is called or the runtime ends.
    Currently only text mode operations are supported.
    """

    def __init__(self):
        """
        Initialize the file manager.

        Creates an empty registry of open files and prepares the internal counter
        used to assign unique identifiers to newly opened files.
        """
        self.open_files: dict[int, IO[Any]] = {}
        self.current_id: int = 0

    def _get_file(self, file_id: int) -> tuple[IO[Any] | None, Error | None]:
        """
        Retrieve an open file handle from the internal registry.

        Parameters
        ----------
        file_id
            Identifier returned by `open()`.

        Returns
        -------
        tuple
            `(file, None)` if the file exists and is open,
            `(None, Error.BARDO_DE_VALOR)` if the identifier is not valid.
        """
        file = self.open_files.get(file_id)
        if file is None:
            return None, Error.BARDO_DE_VALOR
        return file, None

    def open(self, path: str, mode: str = 'r', encoding: str = 'utf-8') -> tuple[int | None, Error | None]:
        """
        Open a file and register it in the runtime file table.

        A new numeric identifier is assigned to the opened file and returned to the
        caller. This identifier must be used for subsequent read, write, or close
        operations.

        Parameters
        ----------
        path
            Filesystem path to the file.
        mode
            File open mode (e.g. 'r', 'w', 'a').
        encoding
            Text encoding used when reading or writing.

        Returns
        -------
        tuple
            `(file_id, None)` on success or `(None, Error)` if the operation fails.
        """
        result = None
        try:
            archivo = open(path, mode, encoding=encoding)
            self.open_files[self.current_id] = archivo
            self.current_id += 1
            result = self.current_id - 1
            return result, None
        except Exception as e:
            return result, handle_error(e)

    def read(self, file_id: int) -> tuple[str | None, Error | None]:
        """
        Read the entire contents of an open file.

        The file must have been previously opened with `open()`.

        Parameters
        ----------
        file_id
            Identifier of the open file.

        Returns
        -------
        tuple
            `(content, None)` on success where `content` is a string containing the
            full file contents, or `(None, Error)` if the read operation fails.
        """
        file, err = self._get_file(file_id)
        if err:
            return None, err

        try:
            return file.read(), None
        except Exception as e:
            return None, handle_error(e)

    def write(self, file_id: int, content: str) -> tuple[None, Error | None]:
        """
        Write text content to an open file.

        The behavior depends on the mode used when opening the file
        (e.g. overwrite or append).

        Parameters
        ----------
        file_id
            Identifier of the open file.
        content
            Text content to write.

        Returns
        -------
        tuple
            `(None, None)` on success or `(None, Error)` if the write fails.
        """
        file, err = self._get_file(file_id)
        if err:
            return None, err

        try:
            file.write(content)
            return None, None
        except Exception as e:
            return None, handle_error(e)

    def close(self, file_id: int) -> tuple[None, Error | None]:
        """
        Close an open file and remove it from the runtime registry.

        After this operation the file identifier becomes invalid and cannot be
        reused for further operations.

        Parameters
        ----------
        file_id
            Identifier of the open file.

        Returns
        -------
        tuple
            `(None, None)` on success or `(None, Error)` if closing fails.
        """
        file, err = self._get_file(file_id)
        if err:
            return None, err

        try:
            file.close()
            del self.open_files[file_id]
            return None, None
        except Exception as e:
            return None, handle_error(e)
        
def open_adapter(facade: Archivo, path: str, mode: str = 'r', encoding: str = 'utf-8') -> RTResult:
    """
    Adapter that exposes `Archivo.open()` to the Lunfardo runtime.

    Converts Python values returned by the facade into Lunfardo runtime values
    and packs them into a `Coso` structure of the form:

        [file_id, error]

    Where:
        - `file_id` is a `Numero` on success or `Nada`.
        - `error` is a `Chamuyo` containing the error name or `Nada`.

    The result is wrapped inside an `RTResult` for interpreter consumption.
    """
    result, error = facade.open(path, mode, encoding)

    file_value = Numero(result) if result is not None else Nada.nada
    error_value = Chamuyo(error.name.lower()) if error is not None else Nada.nada

    return RTResult().success(
        Coso([file_value, error_value])
    )

def read_adapter(facade: Archivo, file_id: int) -> RTResult:
    """
    Adapter exposing `Archivo.read()` to the Lunfardo runtime.

    Returns a `Coso` with the structure:

        [content, error]

    Where:
        - `content` is a `Chamuyo` with the file contents or `Nada`.
        - `error` is a `Chamuyo` containing the error name or `Nada`.
    """
    result, error = facade.read(file_id)

    content_value = Chamuyo(result) if result is not None else Nada.nada
    error_value = Chamuyo(error.name.lower()) if error is not None else Nada.nada

    return RTResult().success(
        Coso([content_value, error_value])
    )

def write_adapter(facade: Archivo, file_id: int, content: str) -> RTResult:
    """
    Adapter exposing `Archivo.write()` to the Lunfardo runtime.

    Returns a `Coso` with the structure:

        [Nada, error]

    The first position is always `Nada` since write operations do not produce
    a value. If an error occurs, the second position contains the error name
    as `Chamuyo`.
    """
    _, error = facade.write(file_id, content)

    error_value = Chamuyo(error.name.lower()) if error is not None else Nada.nada
    return RTResult().success(
        Coso([Nada.nada, error_value])
    )

def close_adapter(facade: Archivo, file_id: int) -> RTResult:
    """
    Adapter exposing `Archivo.close()` to the Lunfardo runtime.

    Returns a `Coso` with the structure:

        [Nada, error]

    The first value is always `Nada`. If the close operation fails, the second
    value contains the error name as `Chamuyo`.
    """
    _, error = facade.close(file_id)

    error_value = Chamuyo(error.name.lower()) if error is not None else Nada.nada

    return RTResult().success(
        Coso([Nada.nada, error_value])
    )