
import Part
from FreeCAD import Vector

from .angled_bar_orientation import AngledBarOrientation
from .rotate_and_translate_part import rotate_and_translate_part


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

        d = get_angled_bar_rotation_and_translation(orientation, length, width)
        rotate_and_translate_part(refined_angled_bar, d)

        return refined_angled_bar


def fuse_parts(*parts):
    return reduce(lambda union, part: union.fuse(part), parts)


def get_angled_bar_rotation_and_translation(orientation, length, width):
    d = get_rotation_and_translation_by_orientation(length, width)
    return d[orientation]


def get_rotation_and_translation_by_orientation(length, width):
    return {
        AngledBarOrientation.BOTTOM_FRONT_FLAT: {
            'rotate_args': [Vector(), Vector(0, 0, 1), 0],
            'translation': Vector()
        },
        AngledBarOrientation.BOTTOM_LEFT_FLAT: {
            'rotate_args': [Vector(), Vector(0, 0, -1), 90],
            'translation': Vector(0, length, 0)
        },
        AngledBarOrientation.BOTTOM_REAR_FLAT: {
            'rotate_args': [Vector(), Vector(0, 0, 1), 180],
            'translation': Vector(length, width, 0)
        },
        AngledBarOrientation.BOTTOM_RIGHT_FLAT: {
            'rotate_args': [Vector(), Vector(0, 0, 1), 90],
            'translation': Vector(width, 0, 0)
        },
        AngledBarOrientation.TOP_FRONT_FLAT: {
            'rotate_args': [Vector(), Vector(1, 0, 0), 270],
            'translation': Vector(0, 0, width)
        },
        AngledBarOrientation.TOP_LEFT_FLAT: {
            'rotate_args': [
                [Vector(), Vector(0, 0, 1), 90],
                [Vector(), Vector(0, 1, 0), 180]
            ],
            'translation': Vector(0, 0, width)
        },
        AngledBarOrientation.TOP_REAR_FLAT: {
            'rotate_args': [Vector(), Vector(1, 0, 0), 180],
            'translation': Vector(0, width, width)
        },
        AngledBarOrientation.TOP_RIGHT_FLAT: {
            'rotate_args': [
                [Vector(), Vector(0, 0, 1), 90],
                [Vector(), Vector(0, -1, 0), 90]
            ],
            'translation': Vector(width, 0, width)
        },
        AngledBarOrientation.FRONT_LEFT_UPRIGHT: {
            'rotate_args': [Vector(), Vector(0, 1, 0), 90],
            'translation': Vector(0, 0, length)
        },
        AngledBarOrientation.FRONT_RIGHT_UPRIGHT: {
            'rotate_args': [Vector(), Vector(0, -1, 0), 90],
            'translation': Vector(width, 0, 0)
        },
        AngledBarOrientation.REAR_LEFT_UPRIGHT: {
            'rotate_args': [
                [Vector(), Vector(0, 1, 0), 90],
                [Vector(), Vector(0, 0, -1), 90]
            ],
            'translation': Vector(0, width, length)
        },
        AngledBarOrientation.REAR_RIGHT_UPRIGHT: {
            'rotate_args':  [
                [Vector(), Vector(0, -1, 0), 90],
                [Vector(), Vector(0, 0, 1), 90]
            ],
            'translation': Vector(width, width, 0)
        }
    }
