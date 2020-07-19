"""Module for angle frame connector part class."""
from functools import reduce
from math import cos, radians, tan
from typing import Dict

import Part
from FreeCAD import Placement, Rotation, Vector
from osecore.app.shape import place_shape
from osecore.app.shape.face import make_face_from_vectors

from .axis_side_mount import AxisSideMount
from .corner import Corner, is_top_corner


class AngleFrameConnector:
    """Connects angled bars together in a cubic frame.

    An angle frame connector is made up of three brackets.
    """

    axis_side_mount_width = 5
    axis_side_mount_length = 27.75

    @classmethod
    def make(cls,
             width: float = 38.1,  # 1.5 inches
             thickness: float = 3.175,  # 1/8 inch
             corner: str = Corner.BOTTOM_LEFT_FRONT,
             with_set_screw: bool = False,
             with_filleting: bool = False) -> Part.Solid:
        """Make an angle frame connector.

        :param width: Width of the angled frame.
        :param thickness: Thickness of the angled frame.
        :param corner: Which corner to orient the angle frame connector to.
                       Defaults to bottom left front corner.
        :param with_set_screw: Whether to include set screw mechanism.
        :param with_filleting: Whether to include filleting.
        :return: Angle frame connector object.
        """
        bracket_length = cls.calculate_bracket_length(width, thickness)
        length = bracket_length + width

        angle_frame_connector = cls._make_angle_frame_connector(width,
                                                                thickness,
                                                                bracket_length,
                                                                length,
                                                                corner,
                                                                with_set_screw,
                                                                with_filleting)

        placement = _get_angle_frame_connector_placement(corner, length)
        place_shape(angle_frame_connector, placement)

        return angle_frame_connector

    @classmethod
    def _make_angle_frame_connector(cls,
                                    width,
                                    thickness,
                                    bracket_length,
                                    length,
                                    corner,
                                    with_set_screw,
                                    with_filleting):
        bracket_width = cls._calculate_bracket_width(thickness)

        angle_connector_corner = _make_angle_connector_corner(
            bracket_length, bracket_width)

        tri_bracket = make_tri_bracket(
            bracket_length,
            width,
            thickness,
            with_set_screw,
            with_filleting)

        # Top tri-bracket
        top_bracket = tri_bracket.copy()
        top_bracket.translate(Vector(0, 0, bracket_length))

        # Right tri-bracket
        right_bracket = tri_bracket.copy()
        right_bracket.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 90)
        right_bracket.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 90)
        right_bracket.translate(Vector(bracket_length, 0, 0))

        # Rear tri-bracket
        rear_bracket = tri_bracket.copy()
        rear_bracket.rotate(Vector(0, 0, 0), Vector(-1, 0, 0), 90)
        rear_bracket.rotate(Vector(0, 0, 0), Vector(0, -1, 0), 90)
        rear_bracket.translate(Vector(0, bracket_length, 0))

        parts = [
            angle_connector_corner, top_bracket, right_bracket, rear_bracket
        ]

        if is_top_corner(corner):
            axis_side_mount = AxisSideMount.make(
                cls.axis_side_mount_width,
                cls.axis_side_mount_length,
                corner)

            parts.append(axis_side_mount)

        angle_frame_connector = reduce(
            lambda union, part: union.fuse(part), parts)

        # removeSplitter() refines shape
        return angle_frame_connector.removeSplitter()

    @classmethod
    def calculate_bracket_length(cls, width: float, thickness: float) -> float:
        """Calculate the length of the bracket.

        :param width: Width of the angled frame.
        :param thickness: Thickness of the angled frame.
        :return: Length of one of the three brackets that make up an
                 angle frame connector.
        """
        return width + (thickness * 2)

    @classmethod
    def _calculate_bracket_width(cls, thickness: float) -> float:
        return thickness * 3

    @classmethod
    def distance_between_axis_side_mount_holes_and_frame(cls) -> float:
        """Calculate distance between the axis side mount holes and frame.

        :return: Distance between the axis side mount holes and frame.
        """
        return AxisSideMount.calculate_distance_between_holes_and_connector(
            cls.axis_side_mount_length)

    @classmethod
    def calculate_y_axis_overhang_distance(cls) -> float:
        """Calculate distance of y axis over-hang.

        :return: Distance of y axis over-hang.
        """
        return AxisSideMount.calculate_overhang_distance(
            cls.axis_side_mount_length)


def make_tri_bracket(width: float,
                     height: float,
                     thickness: float,
                     with_set_screw: bool = False,
                     with_filleting: bool = False) -> Part.Solid:
    """Make tri-bracket.

    Three tri-brackets make up the angle frame connector.

    :param width: Width of bracket.
    :param height: Height of bracket.
    :param thickness: Thickness of bracket
    :param with_set_screw: Whether to include set screw mechanism.
    :param with_filleting: Whether to include filleting.
    :return: Tri-bracket object.
    """
    set_screw_block_width = 20

    outer_vectors = _get_outer_points(width,
                                      thickness,
                                      set_screw_block_width,
                                      with_set_screw)

    inner_vectors = _get_inner_points(width, thickness)

    inner_face = make_face_from_vectors(inner_vectors)
    outer_face = make_face_from_vectors(outer_vectors)

    inner_solid = inner_face.extrude(Vector(0, 0, height))
    outer_solid = outer_face.extrude(Vector(0, 0, height))

    bracket = outer_solid.cut(inner_solid)

    if with_set_screw:
        bracket = _cut_screw_screw(bracket,
                                   width,
                                   height,
                                   thickness,
                                   set_screw_block_width)

    if with_filleting:
        return _fillet_bracket(bracket, height)
    else:
        return bracket


def _fillet_bracket(bracket, height):
    top_wires_parallel_to_xy_plane = _find_top_wires_parallel_to_xy_plane(
        bracket, height)
    return reduce(
        lambda b, wire: b.makeFillet(1.0, wire.Edges),
        top_wires_parallel_to_xy_plane,
        bracket)


def _find_top_wires_parallel_to_xy_plane(bracket, height):
    wires_parallel_to_xy_plane = filter(
        _is_wire_parallel_to_xy_plane, bracket.Wires)
    is_top_shape = _get_is_top_shape(height)
    return filter(
        is_top_shape, wires_parallel_to_xy_plane)


def _get_is_top_shape(height):
    return lambda shape: shape.BoundBox.ZMax == height


def _is_wire_parallel_to_xy_plane(wire):
    return wire.BoundBox.ZMin == wire.BoundBox.ZMax


def _get_outer_points(width,
                      thickness,
                      set_screw_block_width,
                      with_set_screw):
    side = thickness * 3
    bottom_left = Vector(0, 0, 0)
    top_left = Vector(0, width, 0)
    top_left_mid = Vector(side, width, 0)

    outer_points = [
        bottom_left,
        top_left,
        top_left_mid
    ]

    if not with_set_screw:
        mid = Vector(side, side, 0)
        outer_points.append(mid)
    else:
        outer_points.extend([
            Vector(side, side + set_screw_block_width, 0),
            Vector(side + set_screw_block_width, side, 0)
        ])

    top_right_mid = Vector(width, side, 0)
    bottom_right = Vector(width, 0, 0)
    outer_points.extend([
        top_right_mid,
        bottom_right
    ])

    return outer_points


def _get_inner_points(width, thickness):
    length = width - thickness
    side = thickness * 2
    bottom_left_inner = Vector(thickness, thickness, 0)
    top_left_inner = Vector(thickness, length, 0)
    top_left_mid_inner = Vector(side, length, 0)
    mid_inner = Vector(side, side, 0)
    top_right_mid_inner = Vector(length, side, 0)
    bottom_right_inner = Vector(length, thickness, 0)

    return [
        bottom_left_inner,
        top_left_inner,
        top_left_mid_inner,
        mid_inner,
        top_right_mid_inner,
        bottom_right_inner
    ]


def _cut_screw_screw(bracket,
                     width,
                     height,
                     thickness,
                     set_screw_block_width):
    # M6 Hex Socket Set Screw specifications:
    # https://www.bolts-library.org/en/parts/names/HexSocketSetScrew.html
    screw_diameter = 6  # Diameter of M6 hex socket set screw
    screw_radius = screw_diameter / 2.0

    # M6 Nut specifications:
    # https://www.bolts-library.org/en/parts/names/MetricHexagonNut.html
    nut_diameter = 10  # Diameter of M6 hex nut
    nut_radius = nut_diameter / 2.0

    nut_height = 5.2  # Height of M6 hex nut

    nut_thickness = nut_radius - screw_radius
    set_screw_cutout_height = height / 2.0 + screw_radius + nut_thickness

    wiggle_room = 1  # Space between nut and cutout
    set_screw_cutout_length = nut_diameter + wiggle_room
    set_screw_cutout = _make_set_screw_cutout(
        set_screw_cutout_length, nut_height, set_screw_cutout_height)
    z = height - set_screw_cutout_height
    set_screw_cutout.translate(Vector(thickness * 2, thickness * 2, z))
    bracket = bracket.cut(set_screw_cutout)

    cylinder = _make_cylinder(screw_radius, set_screw_block_width)
    bracket_with_hole = _cut_set_screw_hole(
        bracket, height, thickness, cylinder)

    ramp_height = height - set_screw_cutout_height
    bracket = _fuse_nut_ramps_to_bracket(bracket_with_hole,
                                         thickness,
                                         set_screw_cutout_length,
                                         nut_height,
                                         ramp_height)

    return bracket


def _make_set_screw_cutout(length: float, nut_height: float, height: float):
    """Make set screw cutout.

    Set screw cutout is in the shape of a pentagon or home plate in baseball.
    """
    box = Part.makeBox(length, nut_height, height)
    rotation = 45
    box.rotate(Vector(0, 0, 0), Vector(0, 0, -1), rotation)
    offset = length * cos(radians(rotation))
    box.translate(Vector(0, offset, 0))

    # Right Triangle
    bottom_left = Vector(0, 0, 0)
    top_left = Vector(0, offset, 0)
    bottom_right = Vector(offset, 0, 0)
    vectors = [
        bottom_left,
        top_left,
        bottom_right
    ]
    face = make_face_from_vectors(vectors)
    right_triangle = face.extrude(Vector(0, 0, height))

    return box.fuse(right_triangle)


def _cut_set_screw_hole(bracket,
                        height,
                        thickness,
                        cylinder):
    translation = thickness * 3
    z = height / 2.0
    cylinder.translate(Vector(translation, translation, z))
    return bracket.cut(cylinder)


def _make_cylinder(radius, height):
    cylinder = Part.makeCylinder(
        radius, height, Vector(), Vector(1, 0, 0))
    rotation = 45
    cylinder.rotate(Vector(), Vector(0, 0, 1), rotation)
    offset = cos(radians(rotation)) * radius
    cylinder.translate(Vector(offset, offset, 0))
    return cylinder


def _fuse_nut_ramps_to_bracket(bracket: Part.Solid,
                               thickness: float,
                               set_screw_cutout_length: float,
                               set_screw_cutout_width: float,
                               ramp_height: float) -> Part.Solid:
    """Fuse nut ramps to bracket so nut doesn't spin when tightening screw.

    ::

        |\
        | \
        |__\

    :param bracket: Bracket
    :param thickness: Thickness
    :param set_screw_cutout_length: Length of set screw cutout
    :param set_screw_cutout_width: Width of set screw cutout
    :param ramp_height: Height of ramp.
    """
    ramp_length = set_screw_cutout_length / 2.0
    ramp_angle = (180 - 120) / 2  # Hexagonal nuts have 120 degree angles
    # opposite = tan(theta) * adjacent (toa in soh-cah-toa rule)
    height = tan(radians(ramp_angle)) * ramp_length
    # Right Triangle
    bottom_left = Vector(0, 0, 0)
    top_left = Vector(0, 0, height)
    bottom_right = Vector(ramp_length, 0, 0)
    vectors = [
        bottom_left,
        top_left,
        bottom_right
    ]
    face = make_face_from_vectors(vectors)

    rotation = 45
    left_ramp = face.extrude(Vector(0, set_screw_cutout_width, 0))
    right_ramp = left_ramp.copy()

    left_ramp.rotate(Vector(0, 0, 0), Vector(0, 0, -1), rotation)
    right_ramp.rotate(Vector(0, 0, 0), Vector(0, 0, -1), 180 + rotation)

    cutout_length_offset = set_screw_cutout_length * cos(radians(rotation))
    left_ramp.translate(Vector(
        thickness * 2,
        (thickness * 2) + cutout_length_offset,
        ramp_height))

    cutout_width_offset = set_screw_cutout_width * cos(radians(rotation))
    right_ramp.translate(Vector(
        (thickness * 2) + cutout_length_offset + cutout_width_offset,
        (thickness * 2) + cutout_width_offset,
        ramp_height))

    bracket = bracket.fuse(left_ramp)
    return bracket.fuse(right_ramp)


def _make_angle_connector_corner(bracket_length, bracket_width):
    box = Part.makeBox(bracket_length, bracket_length, bracket_length)

    inner_box = box.copy()
    inner_box.translate(Vector(bracket_width, bracket_width, bracket_width))

    return box.cut(inner_box)


def _get_angle_frame_connector_placement(corner: str, length: float) -> Placement:
    d = _get_placement_by_corner(length)
    return d[corner]


def _get_placement_by_corner(length: float) -> Dict[str, Placement]:
    return {
        Corner.BOTTOM_LEFT_FRONT: Placement(),
        Corner.BOTTOM_LEFT_REAR: Placement(
            Vector(0, length, 0),
            Rotation(-90, 0, 0)
        ),
        Corner.BOTTOM_RIGHT_REAR: Placement(
            Vector(length, length, 0),
            Rotation(180, 0, 0)
        ),
        Corner.BOTTOM_RIGHT_FRONT: Placement(
            Vector(length, 0, 0),
            Rotation(90, 0, 0)
        ),
        Corner.TOP_LEFT_FRONT: Placement(
            Vector(0, 0, length),
            Rotation(0, 90, 0)
        ),
        Corner.TOP_LEFT_REAR: Placement(
            Vector(0, length, length),
            Rotation(-90, 90, 0)
        ),
        Corner.TOP_RIGHT_REAR: Placement(
            Vector(length, length, length),
            Rotation(90, 180, 0)
        ),
        Corner.TOP_RIGHT_FRONT: Placement(
            Vector(length, 0, length),
            Rotation(0, 180, 0)
        )
    }
