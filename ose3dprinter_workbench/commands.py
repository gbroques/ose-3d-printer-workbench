
"""
Register commands,
and add them to toolbars, menus, sub-menus, and context menu.
"""
from .add_frame import AddFrame
from .add_universal_axis import AddUniversalAxis
from .command_registry import CommandCollection, command_registry

command_registry.register(AddFrame.NAME, AddFrame())
command_registry.register(AddUniversalAxis.NAME, AddUniversalAxis())

main_toolbar = CommandCollection('OSE 3D Printer')
main_toolbar.add(AddFrame.NAME)
main_toolbar.add(AddUniversalAxis.NAME)
