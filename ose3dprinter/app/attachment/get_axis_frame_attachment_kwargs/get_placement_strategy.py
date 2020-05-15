from FreeCAD import Console, Placement, Units, Vector
from ose3dprinter.app.enums import AxisOrientation, Side
from ose3dprinter.app.model import AxisModel
from ose3dprinter.app.model.frame.angle_frame_connector import AxisSideMount


def get_placement_strategy(face_side):
    return {
        Side.BOTTOM: get_placement_for_bottom_face,
        Side.TOP: get_placement_for_top_face,
        Side.LEFT: get_placement_for_left_face,
        Side.RIGHT: get_placement_for_right_face,
        Side.FRONT: get_placement_for_front_face,
        Side.REAR: get_placement_for_rear_face,
    }[face_side]


def get_placement_for_left_face(frame):
    if frame.HasCorners:
        return get_placement_for_left_face_on_frame_with_corners(frame)
    else:
        return get_placement_for_left_face_on_frame(frame)


def get_placement_for_right_face(frame):
    if frame.HasCorners:
        return get_placement_for_right_face_on_frame_with_corners(frame)
    else:
        return get_placement_for_right_face_on_frame(frame)


def get_placement_for_left_face_on_frame(frame):
    x = frame.Shape.BoundBox.XMin
    y = frame.Shape.BoundBox.YMin
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))

    return {
        'placement': placement,
        'origin_translation_offset': Vector(-1, 0, -1),
        'orientation': AxisOrientation.Y,
        'length': frame.Size
    }


def get_placement_for_left_face_on_frame_with_corners(frame_with_corners):
    x = frame_with_corners.Shape.BoundBox.XMin
    y = calculate_y_of_y_axis_for_frame_with_corners(frame_with_corners)
    z = calculate_z_of_y_axis_for_frame_with_corners(frame_with_corners)

    placement = Placement(
        Vector(x, y, z), frame_with_corners.Placement.Rotation, Vector())

    length = calculate_y_axis_length_for_frame_with_corners(frame_with_corners)
    return {
        'placement': placement,
        'origin_translation_offset': Vector(-1, 0, -1),
        'orientation': AxisOrientation.Y,
        'length': convert_value_to_quantity(length)
    }


def get_placement_for_right_face_on_frame(frame):
    x = frame.Shape.BoundBox.XMax
    y = frame.Shape.BoundBox.YMin
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))

    return {
        'placement': placement,
        'origin_translation_offset': Vector(0, 0, -1),
        'orientation': AxisOrientation.Y,
        'length': frame.Size
    }


def get_placement_for_right_face_on_frame_with_corners(frame_with_corners):
    x = frame_with_corners.Shape.BoundBox.XMax
    y = calculate_y_of_y_axis_for_frame_with_corners(frame_with_corners)
    z = calculate_z_of_y_axis_for_frame_with_corners(frame_with_corners)

    placement = Placement(
        Vector(x, y, z), frame_with_corners.Placement.Rotation, Vector())

    length = calculate_y_axis_length_for_frame_with_corners(frame_with_corners)
    return {
        'placement': placement,
        'origin_translation_offset': Vector(0, 0, -1),
        'orientation': AxisOrientation.Y,
        'length': convert_value_to_quantity(length)
    }


def calculate_y_of_y_axis_for_frame_with_corners(frame_with_corners):
    return (
        frame_with_corners.Shape.BoundBox.YMin -
        (AxisModel.idler_box_width / 2) +
        AxisSideMount.distance_between_hole_and_outer_edge
    )


def calculate_z_of_y_axis_for_frame_with_corners(frame_with_corners):
    return (
        frame_with_corners.Shape.BoundBox.ZMax + (
            (AxisModel.idler_box_length - AxisSideMount.height) / 2)
    )


def calculate_y_axis_length_for_frame_with_corners(frame_with_corners):
    return (
        frame_with_corners.Proxy.distance_between_axis_side_mount_holes +
        AxisModel.distance_between_inner_motor_side_holes_and_outer_edge() +
        AxisModel.distance_between_idler_side_holes_and_outer_edge()
    )


def get_placement_for_front_face(frame):
    x = frame.Shape.BoundBox.Center.x
    y = frame.Proxy.YMin
    z = frame.Shape.BoundBox.ZMin
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    return {
        'placement': placement,
        'origin_translation_offset': Vector(-0.5, -1, 0),
        'orientation': AxisOrientation.Z,
        'length': frame.Size,
        'carriage_position': 90
    }


def get_placement_for_rear_face(frame):
    x = frame.Shape.BoundBox.Center.x
    y = frame.Proxy.YMax
    z = frame.Shape.BoundBox.ZMin
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    return {
        'placement': placement,
        'origin_translation_offset': Vector(-0.5, 0, 0),
        'orientation': AxisOrientation.Z,
        'length': frame.Size,
        'carriage_position': 90
    }


def get_placement_for_bottom_face(frame):
    Console.PrintMessage('Attaching axis to bottom face is not supported.\n')
    placement = Placement()
    origin_translation_offset = Vector()
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset,
        'orientation': AxisOrientation.X,
        'length': frame.Size
    }


def get_placement_for_top_face(frame):
    x = frame.Proxy.XMin
    y = frame.Shape.BoundBox.Center.y
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    origin_translation_offset = Vector(0, -0.5, 0)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset,
        'orientation': AxisOrientation.X,
        'length': frame.Size
    }


def convert_value_to_quantity(value):
    return Units.Quantity(value, Units.Length)
