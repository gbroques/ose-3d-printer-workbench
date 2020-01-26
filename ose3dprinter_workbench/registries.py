
"""
Register commands to toolbars, menus, sub-menus, and context menu.
"""
from .add_frame import AddFrame
from .add_universal_axis import AddUniversalAxis
from .command_registry import CommandRegistry

main_toolbar = CommandRegistry('OSE 3D Printer')
main_toolbar.register('AddFrame', AddFrame())
main_toolbar.register('AddUniversalAxis', AddUniversalAxis())
