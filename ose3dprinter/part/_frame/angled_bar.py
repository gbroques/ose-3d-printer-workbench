"""Module for angled bar part class."""
from functools import reduce

import Part
from FreeCAD import Placement, Rotation, Vector
from osecore.app.shape import place_shape

from .angled_bar_orientation import AngledBarOrientation


class AngledBar:
    """Angled bar of metal."""

    @staticmethod
    def make(length: float,
             width: float,
             thickness: float,
             orientation: str = AngledBarOrientation.BOTTOM_FRONT_FLAT) -> Part.Solid:
        """Make an angled bar of metal.

        :param length: Length of angled bar.
        :param width: Width of angled bar.
                    after an inner sheet is cut out of the center.
        :param thickness: Thickness of angled bar.
        :param orientation: Orientation of angled bar.
                            Must be one of AngledBarOrientation.
                            Defaults to AngledBarOrientation.BOTTOM_FRONT_FLAT.
        :return: An angled bar object.
        """
        bottom_side = Part.makeBox(length, width, thickness)
        front_side = bottom_side.copy()
        front_side.rotate(Vector(0, 0, 0), Vector(-1, 0, 0), 90)
        front_side.translate(Vector(0, 0, width))
        angled_bar = _fuse_parts(bottom_side, front_side).removeSplitter()

        # removeSplitter() refines shape
        refined_angled_bar = angled_bar.removeSplitter()

        placement = _get_angled_bar_placement(orientation, length, width)
        place_shape(refined_angled_bar, placement)

        return refined_angled_bar


def _fuse_parts(*parts):
    return reduce(lambda union, part: union.fuse(part), parts)


def _get_angled_bar_placement(orientation, length, width):
    d = _get_placement_by_orientation(length, width)
    return d[orientation]


def _get_placement_by_orientation(length, width):
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
