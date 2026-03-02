import os
from rtresult import RTResult
from lunfardo_types import Numero, Chamuyo, Coso, Mataburros, Nada

# Facade
class LaCompu:
    name = os.name
    environ = os.environ # mapping, hay que convertirlo a mataburros
    sep = os.sep
    pathsep = os.pathsep
    curdir = os.curdir
    pardir = os.pardir

    def chdir(self, path: str) -> None:
        os.chdir(path)

    def getcwd(self) -> str:
        return os.getcwd()
    
    def getenv(self, key: str) -> str | None:
        return os.getenv(key)
    
    def listdir(self, path: str) -> list:
        return os.listdir(path)
    
    def mkdir(self, path: str) -> None:
        os.mkdir(path)

    def makedirs(self, path: str, exist_ok: bool = False) -> None:
        os.makedirs(path, exist_ok=exist_ok)

    def remove(self, path: str) -> None:
        os.remove(path)

    def rmdir(self, path: str) -> None:
        os.rmdir(path)

    def rename(self, old: str, new: str) -> None:
        os.rename(old, new)

    def system(self, command: str) -> int:
        return os.system(command)
    
# Adapter functions
def chdir_adapter(facade, path) -> RTResult:
    facade.chdir(path)
    return RTResult().success(Nada.nada)

def getcwd_adapter(facade) -> RTResult:
    value = facade.getcwd()
    return RTResult().success(Chamuyo(value))

def getenv_adapter(facade, key) -> RTResult:
    value = facade.getenv(key)
    return RTResult().success(Chamuyo(value))

def listdir_adapter(facade, path) -> RTResult:
    value = facade.listdir(path)
    return RTResult().success(Coso([Chamuyo(item) for item in value]))

def mkdir_adapter(facade, path) -> RTResult:
    facade.mkdir(path)
    return RTResult().success(Nada.nada)

def makedirs_adapter(facade, path, exist_ok) -> RTResult:
    facade.makedirs(path, exist_ok)
    return RTResult().success(Nada.nada)

def remove_adapter(facade, path) -> RTResult:
    facade.remove(path)
    return RTResult().success(Nada.nada)

def rmdir_adapter(facade, path) -> RTResult:
    facade.rmdir(path)
    return RTResult().success(Nada.nada)

def rename_adapter(facade, old, new) -> RTResult:
    facade.rename(old, new)
    return RTResult().success(Nada.nada)

def system_adapter(facade, command) -> RTResult:
    value = facade.system(command)
    return RTResult().success(Numero(value))

def name_adapter(facade) -> RTResult:
    value = facade.name
    return RTResult().success(Chamuyo(value))

def environ_adapter(facade) -> RTResult:
    value = facade.environ
    return RTResult().success(Mataburros.from_dict(value))

def sep_adapter(facade) -> RTResult:
    value = facade.sep
    return RTResult().success(Chamuyo(value))

def pathsep_adapter(facade) -> RTResult:
    value = facade.pathsep
    return RTResult().success(Chamuyo(value))

def curdir_adapter(facade) -> RTResult:
    value = facade.curdir
    return RTResult().success(Chamuyo(value))

def pardir_adapter(facade) -> RTResult:
    value = facade.pardir
    return RTResult().success(Chamuyo(value))