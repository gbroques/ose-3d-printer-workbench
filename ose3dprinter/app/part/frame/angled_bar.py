from functools import reduce

import Part
from FreeCAD import Placement, Rotation, Vector

from .angled_bar_orientation import AngledBarOrientation
from ose3dprinter.app.shape import place_shape


class AngledBar:

    @staticmethod
    def make(length,
             width,
             thickness,
             orientation=AngledBarOrientation.BOTTOM_FRONT_FLAT):
        """Make an angled bar with bottom-left-most corner in the origin (0, 0, 0)

        :param length: Length of angled bar.
        :type length: float
        :param width: Width of angled bar.
                    after an inner sheet is cut out of the center.
        :type width: float
        :param thickness: Thickness of angled bar.
        :type thickness: float
        :param orientation: Orientation of angled bar.
                            Must be one of AngledBarOrientation.
                            Defaults to AngledBarOrientation.BOTTOM_FRONT_FLAT.
        :type orientation: str
        :return: An angled bar.
        :rtype: Part.Shape
        """
        bottom_side = Part.makeBox(length, width, thickness)
        front_side = bottom_side.copy()
        front_side.rotate(Vector(0, 0, 0), Vector(-1, 0, 0), 90)
        front_side.translate(Vector(0, 0, width))
        angled_bar = fuse_parts(bottom_side, front_side).removeSplitter()

        # removeSplitter() refines shape
        refined_angled_bar = angled_bar.removeSplitter()

        placement = get_angled_bar_placement(orientation, length, width)
        place_shape(refined_angled_bar, placement)

        return refined_angled_bar


def fuse_parts(*parts):
    return reduce(lambda union, part: union.fuse(part), parts)


def get_angled_bar_placement(orientation, length, width):
    d = get_placement_by_orientation(length, width)
    return d[orientation]


def get_placement_by_orientation(length, width):
    return {
        AngledBarOrientation.BOTTOM_FRONT_FLAT: Placement(
            Vector(),
            Rotation()
        ),
        AngledBarOrientation.BOTTOM_LEFT_FLAT: Placement(
            Vector(0, length, 0),
            Rotation(-90, 0, 0)
        ),
        AngledBarOrientation.BOTTOM_REAR_FLAT: Placement(
            Vector(length, width, 0),
            Rotation(180, 0, 0)
        ),
        AngledBarOrientation.BOTTOM_RIGHT_FLAT: Placement(
            Vector(width, 0, 0),
            Rotation(90, 0, 0)
        ),
        AngledBarOrientation.TOP_FRONT_FLAT: Placement(
            Vector(0, 0, width),
            Rotation(0, 0, 270)
        ),
        AngledBarOrientation.TOP_LEFT_FLAT: Placement(
            Vector(0, 0, width),
            Rotation(90, 0, -180)
        ),
        AngledBarOrientation.TOP_REAR_FLAT: Placement(
            Vector(0, width, width),
            Rotation(0, 0, 180)
        ),
        AngledBarOrientation.TOP_RIGHT_FLAT: Placement(
            Vector(width, 0, width),
            Rotation(90, 0, 270)
        ),
        AngledBarOrientation.FRONT_LEFT_UPRIGHT: Placement(
            Vector(0, 0, length),
            Rotation(0, 90, 0)
        ),
        AngledBarOrientation.FRONT_RIGHT_UPRIGHT: Placement(
            Vector(width, 0, 0),
            Rotation(0, -90, 0)
        ),
        AngledBarOrientation.REAR_LEFT_UPRIGHT: Placement(
            Vector(0, width, length),
            Rotation(-90, 90, 0)
        ),
        AngledBarOrientation.REAR_RIGHT_UPRIGHT: Placement(
            Vector(width, width, 0),
            Rotation(90, -90, 0)
        )
    }
