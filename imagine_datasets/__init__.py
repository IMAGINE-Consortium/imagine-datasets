import os
from . import *
from ._repo_dataset import *
from .__version__ import *
from .util import show_available
import pkgutil

__all__ = []

cache_dir = os.environ.get('IMAGINE_DATASETS_CACHE_DIR', None)

for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module

