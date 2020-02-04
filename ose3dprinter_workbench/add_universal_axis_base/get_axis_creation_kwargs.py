from .face_orientation import (get_face_orientation,
                               get_is_face_parallel_to_plane_predicate)
from .get_outer_faces_of_frame import get_outer_faces_of_frame
from .get_placement_strategy import get_placement_strategy
from .validate_frame_face_selection import get_frame_and_face_from_selection


def get_axis_creation_kwargs(selection, axis_orientation):
    """
    Get the length, placement, and translation reference point for
    creating a universal axis object attached to a selected frame face.
    """
    frame, face = get_frame_and_face_from_selection(
        selection, axis_orientation)
    if frame is None and face is None:
        return {}
    face_orientation = get_face_orientation(face)
    if face_orientation is None:
        return {}
    face_closest_to_origin = get_face_closest_to_origin(
        frame, face_orientation)
    lower, upper = get_placement_strategy(face_orientation)
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
