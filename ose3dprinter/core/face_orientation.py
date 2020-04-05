from FreeCAD import Console

from .enums import AxisOrientation, Side, Plane
from .get_outer_faces_of_cnc_cut_frame import get_outer_faces_of_cnc_cut_frame
from .is_face_parallel_to_plane import (is_face_parallel_to_xy_plane,
                                        is_face_parallel_to_xz_plane,
                                        is_face_parallel_to_yz_plane)
from .model.frame.angle_frame_connector import AngleFrameConnector


def get_face_side(frame, face):
    attachable_axis_orientation = get_orientation_of_attachable_axis(face)
    if attachable_axis_orientation is None:
        return None
    if frame.HasCorners:
        return get_face_side_for_frame_with_corners(frame,
                                                    face,
                                                    attachable_axis_orientation)
    else:
        return get_face_side_for_cnc_cut_frame(frame,
                                               face,
                                               attachable_axis_orientation)


def get_face_side_for_frame_with_corners(frame_with_corners,
                                         face,
                                         attachable_axis_orientation):
    plane = _get_plane(attachable_axis_orientation)
    thickness = frame_with_corners.Thickness.Value
    if plane == Plane.XY:
        value = face.Surface.Position.z

        upper_bound = frame_with_corners.Proxy.ZMax
        lower_bound = upper_bound - thickness
        if between_bounds(value, lower_bound, upper_bound):
            return Side.TOP
    elif plane == Plane.YZ:
        value = face.Surface.Position.x

        lower_bound = frame_with_corners.Shape.BoundBox.XMin
        upper_bound = lower_bound + thickness + \
            AngleFrameConnector.axis_side_mount_width
        if between_bounds(value, lower_bound, upper_bound):
            return Side.LEFT

        upper_bound = frame_with_corners.Shape.BoundBox.XMax
        lower_bound = upper_bound - thickness - \
            AngleFrameConnector.axis_side_mount_width
        if between_bounds(value, lower_bound, upper_bound):
            return Side.RIGHT
    elif plane == Plane.XZ:
        value = face.Surface.Position.y

        lower_bound = frame_with_corners.Proxy.YMin
        upper_bound = lower_bound + thickness
        if between_bounds(value, lower_bound, upper_bound):
            return Side.FRONT

        upper_bound = frame_with_corners.Proxy.YMax
        lower_bound = upper_bound - thickness
        if between_bounds(value, lower_bound, upper_bound):
            return Side.REAR
    else:
        Console.PrintWarning('{} is not a valid plane.\n'.format(plane))
        return None


def get_face_side_for_cnc_cut_frame(cnc_cut_frame,
                                    face,
                                    attachable_axis_orientation):
    attachable_axis_orientation = get_orientation_of_attachable_axis(face)
    if attachable_axis_orientation is None:
        return None
    sides_by_axis_orientation = _get_sides_by_axis_orientation()
    lower_side, upper_side = sides_by_axis_orientation[attachable_axis_orientation]
    face_closest_to_origin = _get_face_closest_to_origin(
        cnc_cut_frame, attachable_axis_orientation)
    if face.isEqual(face_closest_to_origin):
        return lower_side
    else:
        return upper_side


def get_orientation_of_attachable_axis(face):
    """
    Returns the orientation of which axis is attachable to the face.
    """
    d = _get_is_face_parallel_to_plane_by_axis_orientation()
    for axis_orientation, is_face_parallel_to_plane in d.iteritems():
        if is_face_parallel_to_plane(face):
            return axis_orientation
    Console.PrintWarning('Face not parallel to XY, XZ, or YZ plane.\n')
    return None


def _get_is_face_parallel_to_plane_by_axis_orientation():
    return {
        AxisOrientation.X: is_face_parallel_to_xy_plane,
        AxisOrientation.Y: is_face_parallel_to_yz_plane,
        AxisOrientation.Z: is_face_parallel_to_xz_plane
    }


def _get_plane(axis_orientation):
    return {
        AxisOrientation.X: Plane.XY,
        AxisOrientation.Y: Plane.YZ,
        AxisOrientation.Z: Plane.XZ
    }[axis_orientation]


def _get_is_face_parallel_to_plane(axis_orientation):
    d = _get_is_face_parallel_to_plane_by_axis_orientation()
    return d[axis_orientation]


def _get_sides_by_axis_orientation():
    return {
        AxisOrientation.X: (Side.BOTTOM, Side.TOP),
        AxisOrientation.Y: (Side.LEFT, Side.RIGHT),
        AxisOrientation.Z: (Side.FRONT, Side.REAR)
    }


def _get_face_closest_to_origin(cnc_cut_frame, axis_orientation):
    """
    Get the face closest to the origin based on axis orientation.

    For example, if the axis orientation is x,
    then the face closest to the origin is the bottom face.
    """
    is_face_parallel_to_plane = _get_is_face_parallel_to_plane(
        axis_orientation)

    outer_faces = get_outer_faces_of_cnc_cut_frame(cnc_cut_frame)

    outer_faces_parallel_to_plane = filter(
        is_face_parallel_to_plane, outer_faces)
    sorted_faces_by_position = _sort_faces_by_surface_position(
        outer_faces_parallel_to_plane, axis_orientation)
    return sorted_faces_by_position[0]


def _sort_faces_by_surface_position(faces, axis_orientation):
    """
    If orientation of axis is x, then sort faces by z
    If orientation of axis is y, then sort faces by x
    If orientation of axis is z, then sort faces by y
    """
    axis_orientation_index = [
        AxisOrientation.X,
        AxisOrientation.Y,
        AxisOrientation.Z
    ].index(axis_orientation)
    position_index = ((axis_orientation_index - 1) + 3) % 3
    return sorted(faces, key=lambda f: f.Surface.Position[position_index])


def between_bounds(value, lower_bound, upper_bound):
    is_between_bounds = lower_bound < value < upper_bound
    return (
        isclose(value, lower_bound) or
        is_between_bounds or
        isclose(value, upper_bound)
    )


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """
    TODO: Replace with math.isclose in python 3.5
    Sources:
        https://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
        https://docs.python.org/3/whatsnew/3.5.html#pep-485-a-function-for-testing-approximate-equality
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
