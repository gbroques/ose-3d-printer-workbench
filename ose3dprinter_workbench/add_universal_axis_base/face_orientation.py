from FreeCAD import Console, Vector
from .get_outer_faces_of_frame import get_outer_faces_of_frame


def get_face_closest_to_origin(frame, face_orientation):
    """Get the face closest to the origin based on orientation,
    where the origin is defined as the point (0, 0, 0).

    For example, if the orientation is z,
    then the face closest to the origin is the bottom face.
    """
    is_face_parallel_to_plane = get_is_face_parallel_to_plane_predicate(
        face_orientation)

    outer_faces = get_outer_faces_of_frame(frame)

    outer_faces_parallel_to_plane = filter(
        is_face_parallel_to_plane, outer_faces)
    sorted_faces_by_position = sort_faces_by_surface_position(
        outer_faces_parallel_to_plane, face_orientation)
    return sorted_faces_by_position[0]


def sort_faces_by_surface_position(faces, face_orientation):
    """
    If orientation of face is x, then sort by z
    If orientation of face is y, then sort by x
    If orientation of face is z, then sort by y
    """
    face_orientation_index = ['x', 'y', 'z'].index(face_orientation)
    position_index = ((face_orientation_index - 1) + 3) % 3
    return sorted(faces, key=lambda f: f.Surface.Position[position_index])


def get_face_orientation(face):
    if is_face_parallel_to_xy_plane(face):
        return 'x'
    if is_face_parallel_to_yz_plane(face):
        return 'y'
    if is_face_parallel_to_xz_plane(face):
        return 'z'
    Console.PrintWarning('Face not parallel to YZ, XZ, or XY plane.\n')
    return None


def get_is_face_parallel_to_plane_predicate(orientation):
    return {
        'x': is_face_parallel_to_xy_plane,
        'y': is_face_parallel_to_yz_plane,
        'z': is_face_parallel_to_xz_plane
    }[orientation]


def get_face_orientation_name(frame, face):
    face_orientation = get_face_orientation(face)
    if face_orientation is None:
        return None
    lower, upper = {
        'x': ('bottom', 'top'),
        'y': ('left', 'right'),
        'z': ('front', 'rear')
    }[face_orientation]
    face_closest_to_origin = get_face_closest_to_origin(
        frame, face_orientation)
    if face.isEqual(face_closest_to_origin):
        return lower
    else:
        return upper


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
