from ose3dprinter.gui.resources import get_resource_path

from .generate_cut_list import generate_cut_list
from .task_type import TaskType


class CopyCutListToClipboard:
    """
    Command to copy cut-list to clipboard
    """

    NAME = 'CopyCutListToClipboard'

    def Activated(self):
        generate_cut_list(TaskType.CopyToClipboard)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('edit-copy.svg'),
            'MenuText': 'Copy Cut List to Clipboard',
            'ToolTip': 'Copy Cut List to Clipboard'
        }
