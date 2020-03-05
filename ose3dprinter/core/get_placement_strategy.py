from FreeCAD import Console, Placement, Rotation, Vector

from .enums import Side
from .model.frame.angle_frame_connector import AngleFrameConnector, AxisSideMount
from .model import UniversalAxisModel


def get_placement_strategy(face_side):
    return {
        Side.BOTTOM: get_placement_for_bottom_face,
        Side.TOP: get_placement_for_top_face,
        Side.LEFT: get_placement_for_left_face,
        Side.RIGHT: get_placement_for_right_face,
        Side.FRONT: get_placement_for_front_face,
        Side.REAR: get_placement_for_rear_face,
    }[face_side]


def get_placement_for_left_face(frame, face):
    """
    Assumes Y axis
    TODO: Remove duplication between this and get_placement_for_right_face
    """
    x = frame.Shape.BoundBox.XMin
    y = frame.Shape.BoundBox.YMax
    if frame.HasCorners:
        y += UniversalAxisModel.distance_between_inner_motor_side_holes_and_outer_edge() - \
            AxisSideMount.distance_between_hole_and_outer_edge
    z = frame.Shape.BoundBox.ZMax
    if frame.HasCorners:
        axis_side_mount_height = 65.2
        z -= (axis_side_mount_height / 2)
    rotation = get_rotation_for_left_face()
    placement = Placement(
        Vector(x, y, z), rotation, Vector(0, 0, 0))
    origin_translation_offset = Vector(0, 0, 1)
    if frame.HasCorners:
        origin_translation_offset = Vector(0, 0, 0.5)
    return placement, origin_translation_offset


def get_rotation_for_left_face():
    return Rotation(-90, 0, 90)


def get_placement_for_right_face(frame, face):
    """
    Assumes Y axis
    TODO: Remove duplication between this and get_placement_for_left_face
    """
    x = frame.Shape.BoundBox.XMax
    y = frame.Shape.BoundBox.YMax
    if frame.HasCorners:
        y += UniversalAxisModel.distance_between_inner_motor_side_holes_and_outer_edge() - \
            AxisSideMount.distance_between_hole_and_outer_edge
    z = frame.Shape.BoundBox.ZMax
    if frame.HasCorners:
        z -= (AxisSideMount.height / 2)
    placement = Placement(
        Vector(x, y, z), Rotation(-90, 0, -90), Vector(0, 0, 0))
    origin_translation_offset = Vector(0, 0, 0)
    if frame.HasCorners:
        origin_translation_offset = Vector(0, 0, -0.5)
    return placement, origin_translation_offset


def get_placement_for_front_face(frame, face):
    """
    Assumes Z axis
    """
    x = frame.Shape.BoundBox.Center.x
    y = frame.Proxy.YMin
    z = frame.Shape.BoundBox.ZMax
    rotation = get_rotation_for_front_face()
    placement = Placement(
        Vector(x, y, z), rotation, Vector(0, 0, 0))
    origin_translation_offset = Vector(0.5, 0, 0)
    return placement, origin_translation_offset


def get_rotation_for_front_face():
    """
    Assumes Z axis
    """
    return Rotation(0, 90, 90)


def get_placement_for_rear_face(frame, face):
    """
    Assumes Z axis
    """
    x = frame.Shape.BoundBox.Center.x
    y = frame.Proxy.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(0, 90, -90), Vector(0, 0, 0))
    origin_translation_offset = Vector(-0.5, 0, 0)
    return placement, origin_translation_offset


def get_placement_for_bottom_face(frame, face):
    Console.PrintMessage('Attaching axis to bottom face is not supported.\n')
    placement = Placement()
    origin_translation_offset = Vector()
    return placement, origin_translation_offset


def get_placement_for_top_face(frame, face):
    """
    Assumes X axis
    """
    x = frame.Proxy.XMin
    y = frame.Shape.BoundBox.Center.y
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    origin_translation_offset = Vector(0, 0.5, 0)
    return placement, origin_translation_offset
