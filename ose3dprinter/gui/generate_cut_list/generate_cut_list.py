from collections import OrderedDict

import FreeCAD as App
import FreeCADGui
from FreeCAD import Console
from ose3dprinter.app.enums import AxisOrientation
from ose3dprinter.app.model import FrameModel, UniversalAxisModel
from ose3dprinter.app.model.frame.angle_frame_connector import \
    AngleFrameConnector

from .copy_cut_list_to_clipboard_task_panel import \
    CopyCutListToClipboardTaskPanel
from .merge_cut_list_rows_and_format_descriptions import \
    merge_cut_list_rows_and_format_descriptions
from .save_cut_list_as_csv_task_panel import SaveCutListAsCsvTaskPanel
from .task_type import TaskType


def generate_cut_list(task_type):
    document = App.ActiveDocument
    axes_by_orientation = retrieve_axes_by_orientation_from_document(
        document)
    columns = ['Quantity', 'Description', 'Length']
    rows = transform_axes_by_orientation_into_cut_list_table_rows(
        axes_by_orientation)
    num_z_axes = len(axes_by_orientation[AxisOrientation.Z])
    rows = concatenate_heated_beds_and_spool_holder_rods_to_rows(
        rows, num_z_axes, document)
    rows = concatentate_angle_bars_to_rows(rows, document)
    merged_rows = merge_cut_list_rows_and_format_descriptions(rows)
    show_generate_cut_list_task_panel(merged_rows, columns, task_type)


def concatentate_angle_bars_to_rows(cut_list_table_rows, document):
    frame = retrieve_frame_from_document(document)
    if frame is None:
        Console.PrintMessage(
            'Frame must be added to document to add angled bars to cut list.\n')
        return cut_list_table_rows
    bracket_length = AngleFrameConnector.calculate_bracket_length(
        frame.Width, frame.Thickness)
    angle_bar_length = frame.Size - (bracket_length * 2)
    return cut_list_table_rows + [
        OrderedDict([
            ('Quantity', '12'),
            ('Description', '({} x {}) Angled Bar'.format(
                frame.Width.UserString, frame.Thickness.UserString)),
            ('Length', convert_value_to_quantity_and_format(angle_bar_length))
        ])]


def concatenate_heated_beds_and_spool_holder_rods_to_rows(cut_list_table_rows,
                                                          num_z_axes,
                                                          document):
    frame = retrieve_frame_from_document(document)
    if frame is None:
        Console.PrintMessage(
            'Frame must be added to document to calculate length of heated bed rods and spool holder rod.\n')
        return cut_list_table_rows
    frame_size = frame.Size.Value
    rod_length_equal_to_frame_length = convert_value_to_quantity_and_format(
        frame_size)
    one_inch = 25.4

    # 2 heated bed rods per pair of Z axes
    num_heated_bed_rods = (num_z_axes / 2) * 2
    log_warning_if_odd_number_of_z_axes(num_z_axes, num_heated_bed_rods)
    if num_heated_bed_rods > 0:
        cut_list_table_rows = cut_list_table_rows + [
            OrderedDict([
                ('Quantity', num_heated_bed_rods),
                ('Description', 'Heated Bed Rod'),
                ('Length', rod_length_equal_to_frame_length)
            ])
        ]
    return cut_list_table_rows + [
        OrderedDict([
            ('Quantity', '1'),
            ('Description', 'Spool Holder Rod'),
            ('Length', rod_length_equal_to_frame_length)
        ]),
        OrderedDict([
            ('Quantity', '2'),
            ('Description', 'Spool Holder Rod'),
            ('Length', convert_value_to_quantity_and_format(
                frame_size - one_inch))
        ])]


def log_warning_if_odd_number_of_z_axes(num_z_axes, num_heated_bed_rods):
    if num_z_axes % 2 == 1:
        Console.PrintWarning(
            'An odd number of {} Z axes has been detected when determining number of heated bed rods.\n'
            .format(num_z_axes))
        Console.PrintWarning('Rounding down to {} Z axes and {} heated bed rods.\n'
                             .format(num_z_axes - 1, num_heated_bed_rods))


def transform_axes_by_orientation_into_cut_list_table_rows(axes_by_orientation):
    items_with_axes = filter(filter_item_with_axes,
                             axes_by_orientation.items())
    return list(map(axes_by_orientation_item_to_cut_list_table_row,
                    items_with_axes))


def filter_item_with_axes(axes_by_orientation_item):
    axes = axes_by_orientation_item[1]
    return len(axes) > 0


def axes_by_orientation_item_to_cut_list_table_row(axes_by_orientation_item):
    orientation, axes = axes_by_orientation_item
    num_rods_per_axis = 2
    return OrderedDict([
        ('Quantity', str(len(axes) * num_rods_per_axis)),
        ('Description', '{} Axis Rod'.format(orientation.upper())),
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
    objects = get_objects_from_document(document)
    axes = list(filter(lambda o: is_axis(o), objects))
    return OrderedDict([
        (AxisOrientation.X, [a for a in axes if a.Proxy.is_x()]),
        (AxisOrientation.Y, [a for a in axes if a.Proxy.is_y()]),
        (AxisOrientation.Z, [a for a in axes if a.Proxy.is_z()])
    ])


def retrieve_frame_from_document(document):
    objects = get_objects_from_document(document)
    return next((o for o in objects if is_frame(o)), None)


def get_objects_from_document(document):
    return [] if document is None else document.Objects


def is_axis(object):
    return is_object(object, UniversalAxisModel.Type)


def is_frame(object):
    return is_object(object, FrameModel.Type)


def is_object(object, type):
    if not hasattr(object, 'Proxy'):
        return False
    return object.Proxy.Type == type


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
