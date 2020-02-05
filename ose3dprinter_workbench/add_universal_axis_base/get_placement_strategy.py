from FreeCAD import Console, Placement, Rotation, Vector

from .enums import Side


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
    """
    x = face.Placement.Base.x
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    rotation = get_rotation_for_left_face()
    placement = Placement(
        Vector(x, y, z), rotation, Vector(0, 0, 0))
    translation_reference_point = Vector(0, 0, 1)
    return placement, translation_reference_point


def get_rotation_for_left_face():
    return Rotation(-90, 0, 90)


def get_placement_for_right_face(frame, face):
    """
    Assumes Y axis
    """
    x = frame.Shape.BoundBox.XMax
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(-90, 0, -90), Vector(0, 0, 0))
    translation_reference_point = Vector(0, 0, 0)
    return placement, translation_reference_point


def get_placement_for_front_face(frame, face):
    """
    Assumes Z axis
    """
    x = face.CenterOfMass.x
    y = face.Placement.Base.y
    z = frame.Shape.BoundBox.ZMax
    rotation = get_rotation_for_front_face()
    placement = Placement(
        Vector(x, y, z), rotation, Vector(0, 0, 0))
    translation_reference_point = Vector(0.5, 0, 0)
    return placement, translation_reference_point


def get_rotation_for_front_face():
    """
    Assumes Z axis
    """
    return Rotation(0, 90, 90)


def get_placement_for_rear_face(frame, face):
    """
    Assumes Z axis
    """
    x = face.CenterOfMass.x
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(0, 90, -90), Vector(0, 0, 0))
    translation_reference_point = Vector(-0.5, 0, 0)
    return placement, translation_reference_point


def get_placement_for_bottom_face(frame, face):
    Console.PrintMessage('Attaching axis to bottom face is not supported.\n')
    placement = Placement()
    translation_reference_point = Vector()
    return placement, translation_reference_point


def get_placement_for_top_face(frame, face):
    """
    Assumes X axis
    """
    x = face.Placement.Base.x
    y = face.CenterOfMass.y
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    translation_reference_point = Vector(0, 0.5, 0)
    return placement, translation_reference_point
