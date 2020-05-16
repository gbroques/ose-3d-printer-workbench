import FreeCADGui as Gui

from .command.add_axis import AddXAxisCommand, AddYAxisCommand, AddZAxisCommand
from .command.add_extruder import AddExtruderCommand
from .command.add_frame import AddFrameCommand
from .command.add_heated_bed import AddHeatedBedCommand
from .command.cut_list import (CopyCutListToClipboardCommand,
                               SaveCutListAsCsvCommand)
from .command.make_angle_frame_connector import MakeAngleFrameConnectorCommand

#: Command Namespace: Must be unique to all FreeCAD workbenches.
command_namespace = 'OSE3DP'


def register_commands():
    """
    Register all workbench commands,
    and associate them to toolbars, menus, sub-menus, and context menu.
    """
    add_frame_key = register(AddFrameCommand.NAME, AddFrameCommand())
    add_x_axis_key = register(AddXAxisCommand.NAME, AddXAxisCommand())
    add_y_axis_key = register(AddYAxisCommand.NAME, AddYAxisCommand())
    add_z_axis_key = register(AddZAxisCommand.NAME, AddZAxisCommand())
    add_heated_bed_key = register(
        AddHeatedBedCommand.NAME, AddHeatedBedCommand())
    add_extruder_key = register(AddExtruderCommand.NAME, AddExtruderCommand())
    copy_cut_list_to_clipboard_key = register(
        CopyCutListToClipboardCommand.NAME, CopyCutListToClipboardCommand())
    save_cut_list_as_csv_key = register(
        SaveCutListAsCsvCommand.NAME, SaveCutListAsCsvCommand())
    make_angle_frame_connector_key = register(
        MakeAngleFrameConnectorCommand.NAME, MakeAngleFrameConnectorCommand())

    #: Main Toolbar Commands
    main_toolbar_commands = [
        add_frame_key,
        add_x_axis_key,
        add_y_axis_key,
        add_z_axis_key,
        add_heated_bed_key,
        add_extruder_key
    ]

    #: Main Menu Commands
    main_menu_commands = [
        copy_cut_list_to_clipboard_key,
        save_cut_list_as_csv_key,
        make_angle_frame_connector_key
    ]
    return main_toolbar_commands, main_menu_commands


def register(name, command):
    """Register a command via Gui.addCommand.

    FreeCAD uses the filename where Gui.addCommand is executed as a category
    to group commands together in it's UI.
    """
    key = from_command_name_to_key(name)
    Gui.addCommand(key, command)
    return key


def from_command_name_to_key(command_name):
    return '{}_{}'.format(command_namespace, command_name)
