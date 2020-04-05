import Part
from FreeCAD import Vector

from .angle_frame_connector import AngleFrameConnector
from .angled_bar import AngledBar
from .angled_bar_orientation import AngledBarOrientation
from .corner import Corner


class AngledBarFrame:
    """Frame made from 12 angled bars connected by angle frame connectors."""

    @staticmethod
    def make(side, width, thickness):
        """Make a frame from from 12 angled bars connected by angle frame connectors.
        No welding or epoxy required, and the frame can be disassembled.

        :param side: Side or dimension of frame
                     from one corner to the opposite corner.
        :type side: float
        :param width: Width of angled bar.
        :type width: float
        :param thickness: Thickness of each angled bar.
        :type thickness: float
        :return: A frame made up of angled bars,
                 connected by angle frame connectors.
        :rtype: Part.Shape
        """
        bracket_length = AngleFrameConnector.calculate_bracket_length(
            width, thickness)

        bar_length = side - (bracket_length * 2)

        rear_translation = bar_length + bracket_length
        rear_bar_translation = rear_translation + thickness

        parts = []

        # ----------------
        # | Bottom Parts |
        # ----------------
        bottom_bar_orientations = [
            AngledBarOrientation.BOTTOM_REAR_FLAT,
            AngledBarOrientation.BOTTOM_RIGHT_FLAT,
            AngledBarOrientation.BOTTOM_FRONT_FLAT,
            AngledBarOrientation.BOTTOM_LEFT_FLAT
        ]
        bottom_corners = [
            Corner.BOTTOM_LEFT_REAR,
            Corner.BOTTOM_RIGHT_REAR,
            Corner.BOTTOM_RIGHT_FRONT,
            Corner.BOTTOM_LEFT_FRONT
        ]
        bottom_part_args = [
            bar_length,
            width,
            thickness,
            bottom_bar_orientations,
            bottom_corners,
            bracket_length,
            rear_translation,
            rear_bar_translation
        ]

        bottom_corners, bottom_bars = make_bottom_or_top_of_angled_frame(
            *bottom_part_args)
        parts.extend(bottom_corners)
        parts.extend(bottom_bars)

        # ----------------------------
        # | Four Upright Angled Bars |
        # ----------------------------
        front_left_upright_bar = AngledBar.make(
            bar_length, width, thickness, AngledBarOrientation.FRONT_LEFT_UPRIGHT)
        front_left_upright_bar.translate(Vector(
            thickness,
            thickness,
            bracket_length))

        front_right_upright_bar = AngledBar.make(
            bar_length, width, thickness, AngledBarOrientation.FRONT_RIGHT_UPRIGHT)
        front_right_upright_bar.translate(Vector(
            rear_bar_translation,
            thickness,
            bracket_length))

        rear_left_upright_bar = AngledBar.make(
            bar_length, width, thickness, AngledBarOrientation.REAR_LEFT_UPRIGHT)
        rear_left_upright_bar.translate(Vector(
            thickness,
            rear_bar_translation,
            bracket_length))

        rear_right_upright_bar = AngledBar.make(
            bar_length, width, thickness, AngledBarOrientation.REAR_RIGHT_UPRIGHT)
        rear_right_upright_bar.translate(Vector(
            rear_bar_translation,
            rear_bar_translation,
            bracket_length))

        upright_angled_bars = [
            front_left_upright_bar,
            front_right_upright_bar,
            rear_left_upright_bar,
            rear_right_upright_bar
        ]

        parts.extend(upright_angled_bars)

        # -------------
        # | Top Parts |
        # -------------
        top_bar_orientations = [
            AngledBarOrientation.TOP_REAR_FLAT,
            AngledBarOrientation.TOP_RIGHT_FLAT,
            AngledBarOrientation.TOP_FRONT_FLAT,
            AngledBarOrientation.TOP_LEFT_FLAT
        ]
        top_corners = [
            Corner.TOP_LEFT_REAR,
            Corner.TOP_RIGHT_REAR,
            Corner.TOP_RIGHT_FRONT,
            Corner.TOP_LEFT_FRONT
        ]
        top_part_args = [
            bar_length,
            width,
            thickness,
            top_bar_orientations,
            top_corners,
            bracket_length,
            rear_translation,
            rear_bar_translation
        ]
        top_corners, top_bars = make_bottom_or_top_of_angled_frame(
            *top_part_args)

        for top_corner in top_corners:
            top_corner_offset = bar_length + bracket_length - width
            top_corner.translate(Vector(0, 0, top_corner_offset))

        for top_bar in top_bars:
            top_bar_offset = bar_length + bracket_length
            top_bar.translate(Vector(0, 0, top_bar_offset))

        parts.extend(top_corners)
        parts.extend(top_bars)

        return Part.makeCompound(parts)


def make_bottom_or_top_of_angled_frame(bar_length,
                                       width,
                                       thickness,
                                       bar_orientations,
                                       corners,
                                       bracket_length,
                                       rear_translation,
                                       rear_bar_translation):
    left_rear_corner = corners[0]
    right_rear_corner = corners[1]
    right_front_corner = corners[2]
    left_front_corner = corners[3]

    rear_bar_orientation = bar_orientations[0]
    right_bar_orientation = bar_orientations[1]
    front_bar_orientation = bar_orientations[2]
    left_bar_orientation = bar_orientations[3]

    rear_corner_translation = rear_translation - width

    left_rear_connector = AngleFrameConnector.make(
        width, thickness, left_rear_corner)
    left_rear_connector.translate(Vector(
        0, rear_corner_translation, 0))

    rear_bar = AngledBar.make(
        bar_length, width, thickness, rear_bar_orientation)
    rear_bar.translate(Vector(
        bracket_length,
        rear_bar_translation,
        thickness))

    right_rear_connector = AngleFrameConnector.make(
        width, thickness, right_rear_corner)
    right_rear_connector.translate(
        Vector(rear_corner_translation, rear_corner_translation, 0))

    right_bar = AngledBar.make(
        bar_length, width, thickness, right_bar_orientation)
    right_bar.translate(Vector(
        rear_bar_translation,
        bracket_length,
        thickness))

    right_front_connector = AngleFrameConnector.make(
        width, thickness, right_front_corner)
    right_front_connector.translate(
        Vector(rear_corner_translation, 0, 0))

    front_bar = AngledBar.make(
        bar_length, width, thickness, front_bar_orientation)
    front_bar.translate(Vector(
        bracket_length,
        thickness,
        thickness))

    left_front_connector = AngleFrameConnector.make(
        width, thickness, left_front_corner)

    left_bar = AngledBar.make(
        bar_length, width, thickness, left_bar_orientation)
    left_bar.translate(Vector(
        thickness,
        bracket_length,
        thickness))

    return [
        left_rear_connector,
        right_rear_connector,
        right_front_connector,
        left_front_connector
    ], [
        rear_bar,
        right_bar,
        front_bar,
        left_bar
    ]
