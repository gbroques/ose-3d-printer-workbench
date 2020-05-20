from math import degrees

from FreeCAD import Vector


def place_shapes(shapes, placement):
    for shape in shapes:
        place_shape(shape, placement)


def place_shape(shape, placement):
    """Apply a placement to a given shape.

    See Part::TopoShapePy Class Reference:
        https://www.freecadweb.org/api/db/d71/classPart_1_1TopoShapePy.html

    :param part: A part.
    :type part: Part::TopoShapePy
    :param placement: Placement to apply to part
    :type placement: FreeCAD.Placement
    """
    rotation = placement.Rotation
    shape.rotate(Vector(), rotation.Axis, degrees(rotation.Angle))

    translation = placement.Base
    shape.translate(translation)
