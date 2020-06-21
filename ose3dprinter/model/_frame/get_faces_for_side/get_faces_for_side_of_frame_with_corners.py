from osecore.app.three_dimensional_space_enums import (CoordinateAxis, Plane,
                                                       Side)

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
    faces = frame_with_corners.Proxy.get_outer_faces()

    plane = _get_plane_from_side(side)
    faces_parallel_to_side = filter_faces_parallel_to_plane(
        faces, plane)

    faces_within_bound_of_side = filter(
        lambda f: _is_face_within_bounds_of_side(f, frame_with_corners, side),
        faces_parallel_to_side)
    return list(faces_within_bound_of_side)


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
        Side.BOTTOM: CoordinateAxis.X,
        Side.TOP: CoordinateAxis.X,
        Side.LEFT: CoordinateAxis.Y,
        Side.RIGHT: CoordinateAxis.Y,
        Side.FRONT: CoordinateAxis.Z,
        Side.REAR: CoordinateAxis.Z,
    }[side]
