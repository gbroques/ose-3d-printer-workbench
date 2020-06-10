import FreeCADGui as Gui

from .build_cut_list import build_cut_list


def handle_cut_list_command_activation(create_cut_list_task_panel):
    cut_list = build_cut_list()
    panel = create_cut_list_task_panel(
        cut_list,
        merge_cut_list_items_by_length=True,
        note='X and Z Rod lengths adjusted by +4" and -1" respectively.')
    Gui.Control.closeDialog()
    Gui.Control.showDialog(panel)
