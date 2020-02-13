
"""
Register commands,
and add them to toolbars, menus, sub-menus, and context menu.
"""
from .add_extruder import AddExtruder
from .add_frame import AddFrame
from .add_heated_bed import AddHeatedBed
from .add_universal_x_axis import AddUniversalXAxis
from .add_universal_y_axis import AddUniversalYAxis
from .add_universal_z_axis import AddUniversalZAxis
from .command_registry import CommandCollection, command_registry


def register_commands():
    command_registry.register(AddFrame.NAME, AddFrame())
    command_registry.register(AddUniversalXAxis.NAME, AddUniversalXAxis())
    command_registry.register(AddUniversalYAxis.NAME, AddUniversalYAxis())
    command_registry.register(AddUniversalZAxis.NAME, AddUniversalZAxis())
    command_registry.register(AddHeatedBed.NAME, AddHeatedBed())
    command_registry.register(AddExtruder.NAME, AddExtruder())


main_toolbar = CommandCollection('OSE 3D Printer')
main_toolbar.add(AddFrame.NAME)
main_toolbar.add(AddUniversalXAxis.NAME)
main_toolbar.add(AddUniversalYAxis.NAME)
main_toolbar.add(AddUniversalZAxis.NAME)
main_toolbar.add(AddHeatedBed.NAME)
main_toolbar.add(AddExtruder.NAME)
