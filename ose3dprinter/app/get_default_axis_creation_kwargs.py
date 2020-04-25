from FreeCAD import Placement, Rotation, Vector

from .enums import AxisOrientation
from .get_placement_strategy import (get_rotation_for_front_face,
                                     get_rotation_for_left_face)


def get_default_axis_creation_kwargs(axis_orientation):
    rotation = get_rotation(axis_orientation)
    placement = Placement(Vector(), rotation, Vector())
    origin_translation_offset = get_origin_translation_offset(
        axis_orientation)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }


def get_rotation(axis_orientation):
    return {
        AxisOrientation.X: Rotation(),
        AxisOrientation.Y: get_rotation_for_left_face(),
        AxisOrientation.Z: get_rotation_for_front_face()
    }[axis_orientation]


def get_origin_translation_offset(axis_orientation):
    return {
        AxisOrientation.X: Vector(0, 0, 0),
        AxisOrientation.Y: Vector(-1, -1, 0),
        AxisOrientation.Z: Vector(0, -1, -1)
    }[axis_orientation]
