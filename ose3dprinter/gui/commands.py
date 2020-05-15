
"""
Register commands,
and add them to toolbars, menus, sub-menus, and context menu.
"""
from .add_extruder import AddExtruder
from .add_frame import AddFrame
from .add_heated_bed import AddHeatedBed
from .add_x_axis import AddXAxis
from .add_y_axis import AddYAxis
from .add_z_axis import AddZAxis
from .command_registry import CommandCollection, command_registry
from .generate_cut_list import CopyCutListToClipboard, SaveCutListAsCsv
from .make_angle_frame_connector import MakeAngleFrameConnector


def register_commands():
    """
    Register all workbench commands.
    """
    command_registry.register(AddFrame.NAME, AddFrame())
    command_registry.register(AddXAxis.NAME, AddXAxis())
    command_registry.register(AddYAxis.NAME, AddYAxis())
    command_registry.register(AddZAxis.NAME, AddZAxis())
    command_registry.register(AddHeatedBed.NAME, AddHeatedBed())
    command_registry.register(AddExtruder.NAME, AddExtruder())
    command_registry.register(
        CopyCutListToClipboard.NAME, CopyCutListToClipboard())
    command_registry.register(SaveCutListAsCsv.NAME, SaveCutListAsCsv())
    command_registry.register(
        MakeAngleFrameConnector.NAME, MakeAngleFrameConnector())


#: Main Toolbar
main_toolbar = CommandCollection('OSE 3D Printer')
main_toolbar.add(AddFrame.NAME)
main_toolbar.add(AddXAxis.NAME)
main_toolbar.add(AddYAxis.NAME)
main_toolbar.add(AddZAxis.NAME)
main_toolbar.add(AddHeatedBed.NAME)
main_toolbar.add(AddExtruder.NAME)

#: Main Menu
main_menu = CommandCollection('OSE 3D Printer')
main_menu.add(CopyCutListToClipboard.NAME)
main_menu.add(SaveCutListAsCsv.NAME)
main_menu.add(MakeAngleFrameConnector.NAME)
