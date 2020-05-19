
from ose3dprinter.app.future import isclose
from ose3dprinter.app.part import AngleFrameConnector

from .sort_faces_by_area_descending import sort_faces_by_area_descending


def get_outer_faces_of_frame_with_corners(frame_with_corners):
    # TODO: Doesn't include faces of angle frame connector tabs
    corners = _get_corners(frame_with_corners)
    outer_corner_faces = map(_get_outer_faces_of_corner, corners)
    corner_faces = _flatten(outer_corner_faces)

    angled_bars = _get_angled_bars(frame_with_corners)
    outer_angle_bar_faces = map(_get_outer_faces_of_angled_bar, angled_bars)
    angle_bar_faces = _flatten(outer_angle_bar_faces)

    return corner_faces + angle_bar_faces


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


def _get_outer_faces_of_angled_bar(angled_bar_solid):
    """Get outer faces of angled bar.

    Assumes the 2 largest faces are the outer faces of the angled bar.
    """
    faces = angled_bar_solid.Faces
    sorted_faces = sort_faces_by_area_descending(faces)
    return sorted_faces[:2]


def _get_outer_faces_of_corner(corner_solid):
    """Get outer faces of frame corner (angle frame connector).

    Assumes the 3 largest faces are the outer faces of the corner.
    """
    faces = corner_solid.Faces
    sorted_faces = sort_faces_by_area_descending(faces)
    return sorted_faces[:3]


def _flatten(list_of_lists):
    return [val for sublist in list_of_lists for val in sublist]
