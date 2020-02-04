
"""
Register commands,
and add them to toolbars, menus, sub-menus, and context menu.
"""
from .add_frame import AddFrame
from .add_heated_bed import AddHeatedBed
from .add_universal_x_axis import AddUniversalXAxis
from .command_registry import CommandCollection, command_registry

command_registry.register(AddFrame.NAME, AddFrame())
command_registry.register(AddUniversalXAxis.NAME, AddUniversalXAxis())
command_registry.register(AddHeatedBed.NAME, AddHeatedBed())

main_toolbar = CommandCollection('OSE 3D Printer')
main_toolbar.add(AddFrame.NAME)
main_toolbar.add(AddUniversalXAxis.NAME)
main_toolbar.add(AddHeatedBed.NAME)
