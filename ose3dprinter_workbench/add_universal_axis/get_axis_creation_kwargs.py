from FreeCAD import Console, Vector

from .get_outer_faces_of_frame import get_outer_faces_of_frame
from .get_placement_strategy import get_placement_strategy
from .validate_frame_face_selection import get_frame_and_face_from_selection


def get_axis_creation_kwargs(selection):
    """
    Get the length, placement, and translation reference point for
    creating a universal axis object attached to a selected frame face.
    """
    frame, face = get_frame_and_face_from_selection(selection)
    if frame is None and face is None:
        return {}
    orientation = get_face_orientation(face)
    if orientation is None:
        return {}
    face_closest_to_origin = get_face_closest_to_origin(frame, orientation)
    lower, upper = get_placement_strategy(orientation)
    placement = translation_reference_point = None
    if face.isEqual(face_closest_to_origin):
        placement, translation_reference_point = lower(frame, face)
    else:
        placement, translation_reference_point = upper(frame, face)
    return {
        'length': frame.Size,
        'placement': placement,
        'translation_reference_point': translation_reference_point
    }


def get_face_closest_to_origin(frame, orientation):
    """Get the face closest to the origin based on orientation,
    where the origin is defined as the point (0, 0, 0).

    For example, if the orientation is z,
    then the face closest to the origin is the bottom face.
    """
    predicate_by_orientation = {
        'x': is_face_parallel_to_yz_plane,
        'y': is_face_parallel_to_xz_plane,
        'z': is_face_parallel_to_xy_plane
    }
    is_face_oriented_in_plane = predicate_by_orientation[orientation]

    outer_faces = get_outer_faces_of_frame(frame)

    outer_plane_faces = filter(is_face_oriented_in_plane, outer_faces)
    sorted_faces_by_position = sort_faces_by_surface_position(
        outer_plane_faces, orientation)
    return sorted_faces_by_position[0]


def sort_faces_by_surface_position(faces, orientation):
    position_index = ['x', 'y', 'z'].index(orientation)
    return sorted(faces, key=lambda f: f.Surface.Position[position_index])


def get_face_orientation(face):
    if is_face_parallel_to_yz_plane(face):
        return 'x'
    if is_face_parallel_to_xz_plane(face):
        return 'y'
    if is_face_parallel_to_xy_plane(face):
        return 'z'
    Console.PrintWarning('Face not parallel to YZ, XZ, or XY plane.\n')
    return None


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
