import os
from rtresult import RTResult
from lunfardo_types import Numero, Chamuyo, Coso, Mataburros

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
    
    def getenv(self, key: str) -> str:
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
def chdir_adapter(facade, path):
    facade.chdir(path)
    return RTResult().success(None)

def getcwd_adapter(facade):
    value = facade.getcwd()
    return RTResult().success(Chamuyo(value))

def getenv_adapter(facade, key):
    value = facade.getenv(key)
    return RTResult().success(Chamuyo(value))

def listdir_adapter(facade, path):
    value = facade.listdir(path)
    return RTResult().success(Coso([Chamuyo(item) for item in value]))

def mkdir_adapter(facade, path):
    facade.mkdir(path)
    return RTResult().success(None)

def makedirs_adapter(facade, path, exist_ok):
    facade.makedirs(path, exist_ok)
    return RTResult().success(None)

def remove_adapter(facade, path):
    facade.remove(path)
    return RTResult().success(None)

def rmdir_adapter(facade, path):
    facade.rmdir(path)
    return RTResult().success(None)

def rename_adapter(facade, old, new):
    facade.rename(old, new)
    return RTResult().success(None)

def system_adapter(facade, command):
    value = facade.system(command)
    return RTResult().success(Numero(value))

def name_adapter(facade):
    value = facade.name
    return RTResult().success(Chamuyo(value))

def environ_adapter(facade):
    value = facade.environ
    return RTResult().success(Mataburros(value.keys(), value.values()))

def sep_adapter(facade):
    value = facade.sep
    return RTResult().success(Chamuyo(value))

def pathsep_adapter(facade):
    value = facade.pathsep
    return RTResult().success(Chamuyo(value))

def curdir_adapter(facade):
    value = facade.curdir
    return RTResult().success(Chamuyo(value))

def pardir_adapter(facade):
    value = facade.pardir
    return RTResult().success(Chamuyo(value))