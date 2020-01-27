"""Base class for collections of commands like toolbars, menus, and context menu."""
from importlib import import_module

from .command_collection import CommandCollection

registry = import_module(
    '.OSE-3D-Printer',
    package='ose3dprinter_workbench.registry'
).registry
