from .cut_list_task_panel_factory import CutListTaskPanelFactory
from .cut_list_task_type import CutListTaskType


def create_save_cut_list_to_file_task_panel(
        cut_list_items,
        merge_cut_list_items_by_length=False,
        note=None):
    factory = CutListTaskPanelFactory(
        cut_list_items,
        merge_cut_list=merge_cut_list_items_by_length,
        note=note)
    return factory.create(CutListTaskType.SaveToFile)
