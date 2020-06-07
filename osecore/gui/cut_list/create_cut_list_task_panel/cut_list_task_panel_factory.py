from osecore.app.cut_list import (convert_cut_list_to_ordered_dicts,
                                  merge_cut_list_items_by_length)

from .cut_list_task_type import CutListTaskType
from .task_panel import (CopyCutListToClipboardTaskPanel,
                         SaveCutListAsCsvTaskPanel)


class CutListTaskPanelFactory:
    """Creates Cut List Task Panel objects.
    """

    def __init__(self,
                 cut_list,
                 merge_cut_list=False,
                 note=None):
        self.cut_list = _transform_cut_list(cut_list, merge_cut_list)
        self.note = note

    def create(self, cut_list_task_type):
        columns = ['Quantity', 'Description', 'Length']
        if cut_list_task_type == CutListTaskType.CopyToClipboard:
            return CopyCutListToClipboardTaskPanel(
                self.cut_list, columns, self.note)
        elif cut_list_task_type == CutListTaskType.SaveToFile:
            return SaveCutListAsCsvTaskPanel(
                self.cut_list, columns, self.note)
        else:
            message_template = 'Unrecognized cut list task type "{}".'
            raise ValueError(message_template.format(cut_list_task_type))


def _transform_cut_list(cut_list, should_merge_cut_list):
    ordered_dict_cut_list = convert_cut_list_to_ordered_dicts(cut_list)
    if should_merge_cut_list:
        return merge_cut_list_items_by_length(ordered_dict_cut_list)
    else:
        return ordered_dict_cut_list
