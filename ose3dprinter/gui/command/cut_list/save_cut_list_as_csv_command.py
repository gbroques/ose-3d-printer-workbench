from ose3dprinter.gui.create_cut_list_task_panel import \
    create_save_cut_list_to_file_task_panel
from ose3dprinter.gui.icon import get_icon_path

from .handle_cut_list_command_activation import \
    handle_cut_list_command_activation


class SaveCutListAsCsvCommand:
    """
    Command to save cut-list as a CSV file.
    """

    NAME = 'SaveCutListAsCsv'

    def Activated(self):
        handle_cut_list_command_activation(
            create_save_cut_list_to_file_task_panel)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('document-save-as.svg'),
            'MenuText': 'Save Cut List as CSV',
            'ToolTip': 'Save Cut List as CSV'
        }
