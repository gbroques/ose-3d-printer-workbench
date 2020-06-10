from FreeCAD import Console, Placement, Units, Vector
from ose3dprinter.part.frame.angle_frame_connector import AxisSideMount
from ose3dprinter.part import Axis
from osecore.app.three_dimensional_space_enums import CoordinateAxis, Side


def get_placement_strategy(face_side):
    return {
        Side.BOTTOM: _get_placement_for_bottom_face,
        Side.TOP: _get_placement_for_top_face,
        Side.LEFT: _get_placement_for_left_face,
        Side.RIGHT: _get_placement_for_right_face,
        Side.FRONT: _get_placement_for_front_face,
        Side.REAR: _get_placement_for_rear_face,
    }[face_side]


def _get_placement_for_left_face(frame):
    if frame.HasCorners:
        return _get_placement_for_left_face_on_frame_with_corners(frame)
    else:
        return _get_placement_for_left_face_on_frame(frame)


def _get_placement_for_right_face(frame):
    if frame.HasCorners:
        return _get_placement_for_right_face_on_frame_with_corners(frame)
    else:
        return _get_placement_for_right_face_on_frame(frame)


def _get_placement_for_left_face_on_frame(frame):
    x = frame.Shape.BoundBox.XMin
    y = frame.Shape.BoundBox.YMin
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))

    return {
        'placement': placement,
        'origin_translation_offset': Vector(-1, 0, -1),
        'orientation': CoordinateAxis.Y,
        'length': frame.Size
    }


def _get_placement_for_left_face_on_frame_with_corners(frame_with_corners):
    x = frame_with_corners.Shape.BoundBox.XMin
    y = _calculate_y_of_y_axis_for_frame_with_corners(frame_with_corners)
    z = _calculate_z_of_y_axis_for_frame_with_corners(frame_with_corners)

    placement = Placement(
        Vector(x, y, z), frame_with_corners.Placement.Rotation, Vector())

    length = _calculate_y_axis_length_for_frame_with_corners(
        frame_with_corners)
    return {
        'placement': placement,
        'origin_translation_offset': Vector(-1, 0, -1),
        'orientation': CoordinateAxis.Y,
        'length': _convert_value_to_quantity(length)
    }


def _get_placement_for_right_face_on_frame(frame):
    x = frame.Shape.BoundBox.XMax
    y = frame.Shape.BoundBox.YMin
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))

    return {
        'placement': placement,
        'origin_translation_offset': Vector(0, 0, -1),
        'orientation': CoordinateAxis.Y,
        'length': frame.Size
    }


def _get_placement_for_right_face_on_frame_with_corners(frame_with_corners):
    x = frame_with_corners.Shape.BoundBox.XMax
    y = _calculate_y_of_y_axis_for_frame_with_corners(frame_with_corners)
    z = _calculate_z_of_y_axis_for_frame_with_corners(frame_with_corners)

    placement = Placement(
        Vector(x, y, z), frame_with_corners.Placement.Rotation, Vector())

    length = _calculate_y_axis_length_for_frame_with_corners(
        frame_with_corners)
    return {
        'placement': placement,
        'origin_translation_offset': Vector(0, 0, -1),
        'orientation': CoordinateAxis.Y,
        'length': _convert_value_to_quantity(length)
    }


def _calculate_y_of_y_axis_for_frame_with_corners(frame_with_corners):
    return (
        frame_with_corners.Shape.BoundBox.YMin -
        (Axis.idler_box_width / 2) +
        AxisSideMount.distance_between_hole_and_outer_edge
    )


def _calculate_z_of_y_axis_for_frame_with_corners(frame_with_corners):
    return (
        frame_with_corners.Shape.BoundBox.ZMax + (
            (Axis.idler_box_length - AxisSideMount.height) / 2)
    )


def _calculate_y_axis_length_for_frame_with_corners(frame_with_corners):
    return (
        frame_with_corners.Proxy.distance_between_axis_side_mount_holes +
        Axis.distance_between_inner_motor_side_holes_and_outer_edge() +
        Axis.distance_between_idler_side_holes_and_outer_edge()
    )


def _get_placement_for_front_face(frame):
    x = frame.Shape.BoundBox.Center.x
    y = frame.Proxy.YMin
    z = frame.Shape.BoundBox.ZMin
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    return {
        'placement': placement,
        'origin_translation_offset': Vector(-0.5, -1, 0),
        'orientation': CoordinateAxis.Z,
        'length': frame.Size,
        'carriage_position': 90
    }


def _get_placement_for_rear_face(frame):
    x = frame.Shape.BoundBox.Center.x
    y = frame.Proxy.YMax
    z = frame.Shape.BoundBox.ZMin
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    return {
        'placement': placement,
        'origin_translation_offset': Vector(-0.5, 0, 0),
        'orientation': CoordinateAxis.Z,
        'length': frame.Size,
        'carriage_position': 90
    }


def _get_placement_for_bottom_face(frame):
    Console.PrintMessage('Attaching axis to bottom face is not supported.\n')
    placement = Placement()
    origin_translation_offset = Vector()
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset,
        'orientation': CoordinateAxis.X,
        'length': frame.Size
    }


def _get_placement_for_top_face(frame):
    x = frame.Proxy.XMin
    y = frame.Shape.BoundBox.Center.y
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    origin_translation_offset = Vector(0, -0.5, 0)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset,
        'orientation': CoordinateAxis.X,
        'length': frame.Size
    }


def _convert_value_to_quantity(value):
    return Units.Quantity(value, Units.Length)
