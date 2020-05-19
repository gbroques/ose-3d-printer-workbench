from ose3dprinter.gui.create_cut_list_task_panel import \
    create_copy_cut_list_to_clipboard_task_panel
from ose3dprinter.gui.icon import get_icon_path

from .handle_cut_list_command_activation import \
    handle_cut_list_command_activation


class CopyCutListToClipboardCommand:
    """
    Command to copy cut-list to clipboard
    """

    NAME = 'CopyCutListToClipboard'

    def Activated(self):
        handle_cut_list_command_activation(
            create_copy_cut_list_to_clipboard_task_panel)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('edit-copy.svg'),
            'MenuText': 'Copy Cut List to Clipboard',
            'ToolTip': 'Copy Cut List to Clipboard'
        }