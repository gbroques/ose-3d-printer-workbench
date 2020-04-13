from collections import OrderedDict

import FreeCAD as App
import FreeCADGui
from ose3dprinter.core.enums import AxisOrientation
from ose3dprinter.core.model import UniversalAxisModel

from .copy_cut_list_to_clipboard_task_panel import \
    CopyCutListToClipboardTaskPanel
from .save_cut_list_as_csv_task_panel import SaveCutListAsCsvTaskPanel
from .task_type import TaskType


def generate_cut_list(task_type):
    axes_by_orientation = retrieve_axes_by_orientation_from_document(
        App.ActiveDocument)
    columns = ['Quantity', 'Description', 'Length']
    rows = transform_axes_by_orientation_into_cut_list_table_rows(
        axes_by_orientation)
    show_generate_cut_list_task_panel(rows, columns, task_type)


def transform_axes_by_orientation_into_cut_list_table_rows(axes_by_orientation):
    items_with_axes = filter(filter_item_with_axes,
                             axes_by_orientation.items())
    return map(axes_by_orientation_item_to_cut_list_table_row,
               items_with_axes)


def filter_item_with_axes(axes_by_orientation_item):
    axes = axes_by_orientation_item[1]
    return len(axes) > 0


def axes_by_orientation_item_to_cut_list_table_row(axes_by_orientation_item):
    orientation, axes = axes_by_orientation_item
    num_rods_per_axis = 2
    return OrderedDict([
        ('Quantity', str(len(axes) * num_rods_per_axis)),
        ('Description', 'Rods for {} Axis'.format(orientation.upper())),
        ('Length', get_axis_length_for_cut_list(axes[0], orientation))
    ])


def get_axis_length_for_cut_list(axis, orientation):
    """
    See notes at:
        https://docs.google.com/presentation/d/1-tsozcFWVngwjjhr9Mp4843hSGy8iQDH__hKvnzkPew/edit
    """
    one_inch = 25.4
    axis_length = axis.Length.Value
    if orientation == AxisOrientation.X:
        four_inches = one_inch * 4
        return convert_value_to_quantity_and_format(axis_length + four_inches)
    if orientation == AxisOrientation.Y:
        return axis.Length.UserString
    elif orientation == AxisOrientation.Z:
        #   Only the Z1 axis (front side) needs to be shortened by an inch
        #   to allow for spool-holder rods to insert into the top of the axis.
        #
        #   For simplicity, the Z2 axis (rear side)
        #   can be shortened to the same length.
        #
        #   Ideally Z2 rod lengths are equal to the length of the frame.
        return convert_value_to_quantity_and_format(axis_length - one_inch)
    else:
        raise ValueError(
            'Unrecognized orientation "{}" passed.'.format(orientation))


def convert_value_to_quantity_and_format(value):
    return App.Units.Quantity(value, App.Units.Length).UserString


def show_generate_cut_list_task_panel(cut_list_table_rows,
                                      columns,
                                      task_type):
    FreeCADGui.Control.closeDialog()
    task_panel_factory = GenerateCutListTaskPanelFactory(
        cut_list_table_rows, columns)
    panel = task_panel_factory.create(task_type)
    FreeCADGui.Control.showDialog(panel)


def retrieve_axes_by_orientation_from_document(document):
    objects = [] if document is None else document.Objects
    axes = filter(lambda o: is_axis(o), objects)
    return OrderedDict([
        (AxisOrientation.X, list(filter(lambda a: a.Proxy.is_x(), axes))),
        (AxisOrientation.Y, list(filter(lambda a: a.Proxy.is_y(), axes))),
        (AxisOrientation.Z, list(filter(lambda a: a.Proxy.is_z(), axes)))
    ])


def is_axis(object):
    return object.Proxy.Type == UniversalAxisModel.Type


class GenerateCutListTaskPanelFactory:

    def __init__(self, cut_list_table_rows, columns):
        self.cut_list_table_rows = cut_list_table_rows
        self.columns = columns

    def create(self, task_type):
        if task_type == TaskType.CopyToClipboard:
            return CopyCutListToClipboardTaskPanel(
                self.cut_list_table_rows, self.columns)
        elif task_type == TaskType.SaveAsCsv:
            return SaveCutListAsCsvTaskPanel(
                self.cut_list_table_rows, self.columns)
        else:
            raise ValueError('Unrecognized task type "{}".'.format(task_type))
