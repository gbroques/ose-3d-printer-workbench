"""
Contains command registry,
and base class for collections of commands like toolbars.
"""
from importlib import import_module

from .command_collection import CommandCollection

command_registry = import_module(
    '.OSE_3D_Printer',
    package='ose3dprinter.gui.command_registry'
).command_registry
