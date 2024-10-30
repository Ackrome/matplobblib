import importlib as _importlib


submodules = [
    'tvims',
    'aisd'
]
def __dir__():
    return submodules

def __getattr__(name):
    if name in submodules:
        return _importlib.import_module(f'matplobblib.{name}')
