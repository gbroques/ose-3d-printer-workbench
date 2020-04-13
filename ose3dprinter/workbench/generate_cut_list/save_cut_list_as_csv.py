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
            'MenuText': 'Save Axis Rod Cut List as CSV',
            'ToolTip': 'Save Axis Rod Cut List as CSV'
        }
