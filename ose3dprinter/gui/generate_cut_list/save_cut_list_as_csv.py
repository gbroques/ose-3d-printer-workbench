from ose3dprinter.gui.resources import get_resource_path

from .generate_cut_list import generate_cut_list
from .task_type import TaskType


class SaveCutListAsCsv:
    """
    Command to save cut-list as a CSV file.
    """

    NAME = 'SaveCutListAsCsv'

    def Activated(self):
        generate_cut_list(TaskType.SaveAsCsv)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('document-save-as.svg'),
            'MenuText': 'Save Cut List as CSV',
            'ToolTip': 'Save Cut List as CSV'
        }
