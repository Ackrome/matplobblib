__version__ = "0.4.1"

import importlib as _importlib
from .forall import *

submodules = [
    'tvims',
    'aisd',
    'ml',
    'nm',
    'tod',
    'tobd',
    'nlp',
    'cv'
    ]
def __dir__():
    return submodules

def __getattr__(name):
    if name in submodules:
        return _importlib.import_module(f'matplobblib.{name}')
