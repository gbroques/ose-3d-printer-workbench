from ose3dprinter.app.enums import AxisOrientation, Plane, Side
from ose3dprinter.app.future import isclose
from ose3dprinter.app.get_outer_faces import (get_outer_faces_of_angled_bar,
                                              get_outer_faces_of_corner)
from ose3dprinter.app.model.frame.angle_frame_connector import \
    AngleFrameConnector

from .filter_faces_parallel_to_plane import filter_faces_parallel_to_plane


def get_faces_for_side_of_frame_with_corners(frame_with_corners,
                                             side):
    """TODO: Doesn't include faces of angle frame connector tabs

    :param frame_with_corners: Frame object with HasCorners property = True
    :type frame_with_corners: Document object
    :param side: Side of frame.
    :type side: See Side enum.
    :return: List of faces within bound of side for a frame with corners.
    :rtype: List[Part.Faces]
    """
    corners = _get_corners(frame_with_corners)
    outer_corner_faces = map(get_outer_faces_of_corner, corners)
    corner_faces = _flatten(outer_corner_faces)

    angled_bars = _get_angled_bars(frame_with_corners)
    outer_angle_bar_faces = map(get_outer_faces_of_angled_bar, angled_bars)
    angle_bar_faces = _flatten(outer_angle_bar_faces)

    faces = corner_faces + angle_bar_faces

    plane = _get_plane_from_side(side)
    faces_parallel_to_side = filter_faces_parallel_to_plane(
        faces, plane)

    faces_within_bound_of_side = filter(
        lambda f: _is_face_within_bounds_of_side(f, frame_with_corners, side),
        faces_parallel_to_side)
    return list(faces_within_bound_of_side)


def _flatten(list_of_lists):
    return [val for sublist in list_of_lists for val in sublist]


def _get_corners(frame_with_corners):
    return filter(
        lambda s: _is_solid_corner(s, frame_with_corners),
        frame_with_corners.Shape.Solids)


def _get_angled_bars(frame_with_corners):
    return filter(
        lambda s: _is_solid_angled_bar(s, frame_with_corners),
        frame_with_corners.Shape.Solids)


def _is_solid_corner(solid, frame):
    return not _is_solid_angled_bar(solid, frame)


def _is_solid_angled_bar(solid, frame):
    return (
        _is_solid_top_or_bottom_angled_bar(solid, frame) or
        _is_solid_upright_angled_bar(solid, frame)
    )


def _is_solid_upright_angled_bar(solid, frame):
    bracket_length = AngleFrameConnector.calculate_bracket_length(
        frame.Width, frame.Thickness)
    lower_bound = frame.Shape.BoundBox.ZMin + bracket_length.Value
    upper_bound = frame.Shape.BoundBox.ZMax - bracket_length.Value

    return (
        isclose(lower_bound, solid.BoundBox.ZMin) and
        isclose(upper_bound, solid.BoundBox.ZMax)
    )


def _is_solid_top_or_bottom_angled_bar(solid, frame):
    frame_center = frame.Shape.BoundBox.Center
    solid_center = solid.CenterOfMass
    return (
        isclose(frame_center.x, solid_center.x) or
        isclose(frame_center.y, solid_center.y)
    )


def _get_plane_from_side(side):
    return {
        Side.BOTTOM: Plane.XY,
        Side.TOP: Plane.XY,
        Side.LEFT: Plane.YZ,
        Side.RIGHT: Plane.YZ,
        Side.FRONT: Plane.XZ,
        Side.REAR: Plane.XZ
    }[side]


def _is_face_within_bounds_of_side(face, frame, side):
    axis_orientation = get_axis_orientation(side)
    face_side = frame.Proxy.get_face_side(face, axis_orientation)
    return face_side == side


def get_axis_orientation(side):
    return {
        Side.BOTTOM: AxisOrientation.X,
        Side.TOP: AxisOrientation.X,
        Side.LEFT: AxisOrientation.Y,
        Side.RIGHT: AxisOrientation.Y,
        Side.FRONT: AxisOrientation.Z,
        Side.REAR: AxisOrientation.Z,
    }[side]
