
"""
Register commands,
and add them to toolbars, menus, sub-menus, and context menu.
"""
from .add_frame import AddFrame
from .add_universal_axis import AddUniversalAxis
from .registry import CommandCollection, registry

registry.register(AddFrame.NAME, AddFrame())
registry.register(AddUniversalAxis.NAME, AddUniversalAxis())

main_toolbar = CommandCollection('OSE 3D Printer')
main_toolbar.add(AddFrame.NAME)
main_toolbar.add(AddUniversalAxis.NAME)
