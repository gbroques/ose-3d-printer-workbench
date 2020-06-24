"""Command Registry Module
"""
import FreeCADGui as Gui

from .command import (AddExtruderCommand, AddFrameCommand, AddHeatedBedCommand,
                      AddXAxisCommand, AddYAxisCommand, AddZAxisCommand,
                      CopyCutListToClipboardCommand,
                      MakeAngleFrameConnectorCommand, SaveCutListAsCsvCommand)

#: Command Namespace
command_namespace = 'OSE3DP'


def register_commands():
    """
    Register all workbench commands,
    and associate them to toolbars, menus, sub-menus, and context menu.
    """
    add_frame_key = _register(AddFrameCommand.NAME, AddFrameCommand())
    add_x_axis_key = _register(AddXAxisCommand.NAME, AddXAxisCommand())
    add_y_axis_key = _register(AddYAxisCommand.NAME, AddYAxisCommand())
    add_z_axis_key = _register(AddZAxisCommand.NAME, AddZAxisCommand())
    add_heated_bed_key = _register(
        AddHeatedBedCommand.NAME, AddHeatedBedCommand())
    add_extruder_key = _register(AddExtruderCommand.NAME, AddExtruderCommand())
    copy_cut_list_to_clipboard_key = _register(
        CopyCutListToClipboardCommand.NAME, CopyCutListToClipboardCommand())
    save_cut_list_as_csv_key = _register(
        SaveCutListAsCsvCommand.NAME, SaveCutListAsCsvCommand())
    make_angle_frame_connector_key = _register(
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


def _register(name, command):
    key = '{}_{}'.format(command_namespace, name)
    Gui.addCommand(key, command)
    return key


__all__ = ['register_commands']
