"""Base class for collections of commands like toolbars, menus, and context menu."""
from importlib import import_module

from .command_collection import CommandCollection

command_registry = import_module(
    '.OSE-3D-Printer',
    package='ose3dprinter_workbench.command_registry'
).command_registry