import Part
from FreeCAD import Vector
from ose3dprinter.app.shape.face import make_face_from_vectors
from ose3dprinter.app.model.axis import AxisModel

from .corner import Corner, is_top_corner
from .rotate_and_translate_part import rotate_and_translate_part


class AxisSideMount:
    """
    TODO: Rename to TopAngleFrameConnectorTab?
    """
    hole_radius = 3.39
    height = 65.2
    distance_between_hole_and_outer_edge = hole_radius + 5.99554
    attachment_overlap = 10.22

    @classmethod
    def make(cls, width, length, top_corner):
        """Returns which side of the angle frame connector to add the axis mount to.

        :param width: Width of axis side mount.
        :type width: float
        :param top_corner: A top corner:
                        top left front, top right front,
                        top left rear, or top right rear.
        :type top_corner: str
        :return: Axis side mount
        :rtype: Part.Shape
        """
        if not is_top_corner(top_corner):
            raise ValueError('Corner {} must be one of {}, {}, {}, or {}.'.format(
                top_corner,
                Corner.TOP_LEFT_FRONT,
                Corner.TOP_RIGHT_FRONT,
                Corner.TOP_LEFT_REAR,
                Corner.TOP_RIGHT_REAR))

        distance_from_hole_to_side = (
            cls.height - (AxisModel.distance_between_holes + (cls.hole_radius * 2))) / 2

        if length <= cls.attachment_overlap:
            raise ValueError(
                'Length {} must be greater than attachment overlap of {}.'
                .format(length, cls.attachment_overlap))
        box = cls.make_trapezoid_tab(width, length, cls.attachment_overlap)

        top_hole = Part.makeCylinder(
            cls.hole_radius, width, Vector(), Vector(0, 0, 1))
        top_hole.translate(Vector(
            distance_from_hole_to_side,
            length - cls.distance_between_hole_and_outer_edge,
            0))
        box = box.cut(top_hole)

        bottom_hole = Part.makeCylinder(
            cls.hole_radius, width, Vector(), Vector(0, 0, 1))
        bottom_hole.translate(Vector(
            cls.height - distance_from_hole_to_side,
            length - cls.distance_between_hole_and_outer_edge,
            0))
        box = box.cut(bottom_hole)

        d = get_rotation_and_translation(
            top_corner, cls.height, cls.attachment_overlap)
        rotate_and_translate_part(box, d)

        return box

    @classmethod
    def calculate_distance_between_holes_and_connector(cls, length):
        return length - cls.distance_between_hole_and_outer_edge - cls.attachment_overlap

    @classmethod
    def calculate_overhang_distance(cls, length):
        return length - cls.attachment_overlap

    @classmethod
    def make_trapezoid_tab(cls, width, length, attachment_overlap):
        """
           -------------
          /             \
         /               \
        /                 \
        |_________________|
        """
        distance_between_rear_point_and_side = 11.21
        slanted_edge_distance = 5.87

        bottom_left = Vector(0, slanted_edge_distance, 0)
        bottom_left_midpoint = Vector(0, attachment_overlap, 0)
        top_left = Vector(
            distance_between_rear_point_and_side, length, 0)
        top_right = Vector(
            cls.height - distance_between_rear_point_and_side, length, 0)
        bottom_right_midpoint = Vector(cls.height, attachment_overlap, 0)
        bottom_right = Vector(cls.height, slanted_edge_distance, 0)

        points = [
            bottom_left,
            bottom_left_midpoint,
            top_left,
            top_right,
            bottom_right_midpoint,
            bottom_right
        ]

        face = make_face_from_vectors(points)

        trapezoid = face.extrude(Vector(0, 0, width))

        slanted_edge = cls.make_slanted_edge(slanted_edge_distance, width)

        # removeSplitter() refines shape
        return trapezoid.fuse(slanted_edge).removeSplitter()

    @classmethod
    def make_slanted_edge(cls, slanted_edge_distance, width):
        """
        |\
        | \
        |  \
        |___\
        """
        a = Vector(0, slanted_edge_distance, 0)
        b = Vector(0, 0, 0)
        c = Vector(0, slanted_edge_distance, width)
        vectors = [a, b, c]
        face = make_face_from_vectors(vectors)
        return face.extrude(Vector(cls.height, 0, 0))


def get_rotation_and_translation(top_corner, height, attachment_overlap):
    d = get_rotation_and_translation_by_top_corner(height, attachment_overlap)
    return d[top_corner]


def get_rotation_and_translation_by_top_corner(height,
                                               attachment_overlap):
    return {
        Corner.TOP_LEFT_FRONT: {
            'rotate_args': [
                [Vector(), Vector(0, -1, 0), 180],
                [Vector(), Vector(0, 0, 1), 180]
            ],
            'translation': Vector(0, attachment_overlap, 0)
        },
        Corner.TOP_LEFT_REAR: {
            'rotate_args': [
                [Vector(), Vector(1, 0, 0), 90],
                [Vector(), Vector(0, 1, 0), 180]
            ],
            'translation': Vector(height, 0, attachment_overlap)
        },
        Corner.TOP_RIGHT_REAR: {
            'rotate_args': [
                [Vector(), Vector(-1, 0, 0), 90],
                [Vector(), Vector(0, -1, 0), 90],
                [Vector(), Vector(0, 0, -1), 180]
            ],
            'translation': Vector(attachment_overlap, 0, 0)
        },
        Corner.TOP_RIGHT_FRONT: {
            'rotate_args': [
                [Vector(), Vector(0, -1, 0), 90],
                [Vector(), Vector(-1, 0, 0), 180]
            ],
            'translation': Vector(0, attachment_overlap, height)
        }
    }
