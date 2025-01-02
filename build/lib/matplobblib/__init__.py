import importlib as _importlib
from .forall import *

submodules = [
    'tvims',
    'aisd',
    'econometrics',
    'ml'
]
def __dir__():
    return submodules

def __getattr__(name):
    if name in submodules:
        return _importlib.import_module(f'matplobblib.{name}')
