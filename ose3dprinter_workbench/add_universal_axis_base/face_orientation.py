from FreeCAD import Console, Vector

from .enums import AxisOrientation, Side
from .get_outer_faces_of_frame import get_outer_faces_of_frame


def get_face_closest_to_origin(frame, axis_orientation):
    """
    Get the face closest to the origin based on axis orientation.

    For example, if the axis orientation is x,
    then the face closest to the origin is the bottom face.
    """
    is_face_parallel_to_plane = get_is_face_parallel_to_plane(axis_orientation)

    outer_faces = get_outer_faces_of_frame(frame)

    outer_faces_parallel_to_plane = filter(
        is_face_parallel_to_plane, outer_faces)
    sorted_faces_by_position = sort_faces_by_surface_position(
        outer_faces_parallel_to_plane, axis_orientation)
    return sorted_faces_by_position[0]


def sort_faces_by_surface_position(faces, axis_orientation):
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


def get_orientation_of_attachable_axis(face):
    """
    Returns the orientation of which axis is attachable to the face.
    """
    if is_face_parallel_to_xy_plane(face):
        return AxisOrientation.X
    if is_face_parallel_to_yz_plane(face):
        return AxisOrientation.Y
    if is_face_parallel_to_xz_plane(face):
        return AxisOrientation.Z
    Console.PrintWarning('Face not parallel to YZ, XZ, or XY plane.\n')
    return None


def get_is_face_parallel_to_plane(axis_orientation):
    return {
        AxisOrientation.X: is_face_parallel_to_xy_plane,
        AxisOrientation.Y: is_face_parallel_to_yz_plane,
        AxisOrientation.Z: is_face_parallel_to_xz_plane
    }[axis_orientation]


def get_face_side(frame, face):
    attachable_axis_orientation = get_orientation_of_attachable_axis(face)
    if attachable_axis_orientation is None:
        return None
    sides_by_axis_orientation = get_sides_by_axis_orientation()
    lower, upper = sides_by_axis_orientation[attachable_axis_orientation]
    face_closest_to_origin = get_face_closest_to_origin(
        frame, attachable_axis_orientation)
    if face.isEqual(face_closest_to_origin):
        return lower
    else:
        return upper


def get_sides_by_axis_orientation():
    return {
        AxisOrientation.X: (Side.BOTTOM, Side.TOP),
        AxisOrientation.Y: (Side.LEFT, Side.RIGHT),
        AxisOrientation.Z: (Side.FRONT, Side.REAR)
    }


def is_face_parallel_to_yz_plane(face):
    x_axis = Vector(1, 0, 0)
    return is_face_parallel_to_plane(face, x_axis)


def is_face_parallel_to_xz_plane(face):
    y_axis = Vector(0, 1, 0)
    return is_face_parallel_to_plane(face, y_axis)


def is_face_parallel_to_xy_plane(face):
    z_axis = Vector(0, 0, 1)
    return is_face_parallel_to_plane(face, z_axis)


def is_face_parallel_to_plane(face, axis_vector):
    return axis_vector == Vector(
        abs(round(face.Surface.Axis.x)),
        abs(round(face.Surface.Axis.y)),
        abs(round(face.Surface.Axis.z))
    )
