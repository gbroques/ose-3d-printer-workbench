from ose3dprinter.app.cut_list import (convert_cut_list_to_ordered_dicts,
                                       merge_cut_list_items_by_length)

from .cut_list_task_type import CutListTaskType
from .task_panel import (CopyCutListToClipboardTaskPanel,
                         SaveCutListAsCsvTaskPanel)


class CutListTaskPanelFactory:

    def __init__(self,
                 cut_list,
                 merge_cut_list=False,
                 note=None):
        self.cut_list = convert_cut_list_to_ordered_dicts(cut_list)
        self.merge_cut_list = merge_cut_list
        self.note = note

    def create(self, cut_list_task_type):
        columns = ['Quantity', 'Description', 'Length']
        cut_list = self.cut_list
        if self.merge_cut_list:
            cut_list = merge_cut_list_items_by_length(cut_list)
        if cut_list_task_type == CutListTaskType.CopyToClipboard:
            return CopyCutListToClipboardTaskPanel(
                cut_list, columns, self.note)
        elif cut_list_task_type == CutListTaskType.SaveAsCsv:
            return SaveCutListAsCsvTaskPanel(
                cut_list, columns, self.note)
        else:
            message_template = 'Unrecognized cut list task type "{}".'
            raise ValueError(message_template.format(cut_list_task_type))
