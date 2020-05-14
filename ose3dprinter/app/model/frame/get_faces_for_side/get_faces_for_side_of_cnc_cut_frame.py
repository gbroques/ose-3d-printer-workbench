from ose3dprinter.app.enums import Plane, Side
from ose3dprinter.app.get_outer_faces import get_outer_faces_of_cnc_cut_frame
from ose3dprinter.app.is_face_parallel_to_plane import (
    is_face_parallel_to_xy_plane, is_face_parallel_to_xz_plane,
    is_face_parallel_to_yz_plane)

from .filter_faces_parallel_to_plane import filter_faces_parallel_to_plane


def get_faces_for_side_of_cnc_cut_frame(cnc_cut_frame, side):
    faces_by_side = _get_faces_by_side_for_cnc_cut_frame(cnc_cut_frame)
    return faces_by_side[side]


def _get_faces_by_side_for_cnc_cut_frame(cnc_cut_frame):
    """Gets a dictionary of outer faces of the frame by their Side.

    :param cnc_cut_frame: CNC Cut Frame (frame without corners)
    :type cnc_cut_frame: Document Object
    :return: Dictionary where the keys are a Side, and value is a list of Faces
    :rtype: dict
    """
    faces_by_side = {}
    outer_faces = get_outer_faces_of_cnc_cut_frame(cnc_cut_frame)
    for outer_face in outer_faces:
        parallel_plane = _get_parallel_plane(outer_face)
        outer_faces_parallel_to_plane = filter_faces_parallel_to_plane(
            outer_faces, parallel_plane)
        perpendicular_axis_to_plane = _get_perpendicular_axis_to_plane(
            parallel_plane)
        sorted_faces_by_position = sorted(
            outer_faces_parallel_to_plane,
            key=lambda f: getattr(f.Surface.Position, perpendicular_axis_to_plane))
        side_index = 0 if sorted_faces_by_position[0].isEqual(
            outer_face) else 1
        ordered_sides_by_plane = {
            Plane.XY: [Side.BOTTOM, Side.TOP],
            Plane.YZ: [Side.LEFT, Side.RIGHT],
            Plane.XZ: [Side.FRONT, Side.REAR]
        }
        side = ordered_sides_by_plane[parallel_plane][side_index]
        faces_by_side[side] = [outer_face]

    return faces_by_side


def _get_parallel_plane(face):
    """
    Returns which plane the face is parallel to
    """
    if is_face_parallel_to_xy_plane(face):
        return Plane.XY
    elif is_face_parallel_to_yz_plane(face):
        return Plane.YZ
    elif is_face_parallel_to_xz_plane(face):
        return Plane.XZ
    else:
        raise ValueError('Face must be parallel to XY, YZ, or XZ plane.')


def _get_perpendicular_axis_to_plane(plane):
    return {
        Plane.XY: 'z',
        Plane.YZ: 'x',
        Plane.XZ: 'y'
    }[plane]
