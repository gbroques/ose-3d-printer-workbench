from collections import OrderedDict

import FreeCAD as App
from FreeCAD import Console
from osecore.app.three_dimensional_space_enums import CoordinateAxis

from ose3dprinter.model import AxisModel, FrameModel
from ose3dprinter.part import AngleFrameConnector


def build_cut_list():
    document = App.ActiveDocument
    axes_by_orientation = retrieve_axes_by_orientation_from_document(
        document)
    cut_list = transform_axes_by_orientation_into_cut_list(
        axes_by_orientation)
    num_z_axes = len(axes_by_orientation[CoordinateAxis.Z])
    cut_list = add_heated_beds_and_spool_holder_rods_to_cut_list(
        cut_list, num_z_axes, document)
    cut_list = add_angle_bars_to_cut_list(cut_list, document)
    return cut_list


def add_angle_bars_to_cut_list(cut_list_table_rows, document):
    frame = retrieve_frame_from_document(document)
    if frame is None:
        Console.PrintMessage(
            'Frame must be added to document to add angled bars to cut list.\n')
        return cut_list_table_rows
    bracket_length = AngleFrameConnector.calculate_bracket_length(
        frame.Width, frame.Thickness)
    angle_bar_length = frame.Size - (bracket_length * 2)
    return cut_list_table_rows + [
        {
            'quantity': '12',
            'description': '({} x {}) Angled Bar'.format(
                frame.Width.UserString, frame.Thickness.UserString),
            'length': convert_value_to_quantity_and_format(angle_bar_length)
        }
    ]


def add_heated_beds_and_spool_holder_rods_to_cut_list(cut_list_table_rows,
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
            {
                'quantity': num_heated_bed_rods,
                'description': 'Heated Bed Rod',
                'length': rod_length_equal_to_frame_length
            }
        ]
    return cut_list_table_rows + [
        {
            'quantity': '1',
            'description': 'Spool Holder Rod',
            'length': rod_length_equal_to_frame_length
        },
        {
            'quantity': '2',
            'description': 'Spool Holder Rod',
            'length': convert_value_to_quantity_and_format(frame_size - one_inch)
        }
    ]


def log_warning_if_odd_number_of_z_axes(num_z_axes, num_heated_bed_rods):
    if num_z_axes % 2 == 1:
        Console.PrintWarning(
            'An odd number of {} Z axes has been detected when determining number of heated bed rods.\n'
            .format(num_z_axes))
        Console.PrintWarning('Rounding down to {} Z axes and {} heated bed rods.\n'
                             .format(num_z_axes - 1, num_heated_bed_rods))


def transform_axes_by_orientation_into_cut_list(axes_by_orientation):
    items_with_axes = filter(filter_item_with_axes,
                             axes_by_orientation.items())
    return list(map(axes_by_orientation_item_to_cut_list_item,
                    items_with_axes))


def filter_item_with_axes(axes_by_orientation_item):
    axes = axes_by_orientation_item[1]
    return len(axes) > 0


def axes_by_orientation_item_to_cut_list_item(axes_by_orientation_item):
    orientation, axes = axes_by_orientation_item
    num_rods_per_axis = 2
    return {
        'quantity': str(len(axes) * num_rods_per_axis),
        'description': '{} Axis Rod'.format(orientation.upper()),
        'length': get_axis_length_for_cut_list(axes[0], orientation)
    }


def get_axis_length_for_cut_list(axis, orientation):
    """
    See notes at:
        https://docs.google.com/presentation/d/1-tsozcFWVngwjjhr9Mp4843hSGy8iQDH__hKvnzkPew/edit
    """
    one_inch = 25.4
    axis_length = axis.Length.Value
    if orientation == CoordinateAxis.X:
        four_inches = one_inch * 4
        return convert_value_to_quantity_and_format(axis_length + four_inches)
    if orientation == CoordinateAxis.Y:
        return axis.Length.UserString
    elif orientation == CoordinateAxis.Z:
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


def retrieve_axes_by_orientation_from_document(document):
    objects = get_objects_from_document(document)
    axes = list(filter(lambda o: is_axis(o), objects))
    return OrderedDict([
        (CoordinateAxis.X, [a for a in axes if a.Proxy.is_x()]),
        (CoordinateAxis.Y, [a for a in axes if a.Proxy.is_y()]),
        (CoordinateAxis.Z, [a for a in axes if a.Proxy.is_z()])
    ])


def retrieve_frame_from_document(document):
    objects = get_objects_from_document(document)
    return next((o for o in objects if is_frame(o)), None)


def get_objects_from_document(document):
    return [] if document is None else document.Objects


def is_axis(obj):
    return is_object(obj, AxisModel.Type)


def is_frame(obj):
    return is_object(obj, FrameModel.Type)


def is_object(obj, type):
    if not hasattr(obj, 'Proxy'):
        return False
    return obj.Proxy.Type == type
