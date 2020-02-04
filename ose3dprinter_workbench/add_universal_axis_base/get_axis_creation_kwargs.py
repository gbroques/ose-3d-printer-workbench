from .face_orientation import get_face_orientation_name
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
    face_orientation_name = get_face_orientation_name(frame, face)
    placement_strategy = get_placement_strategy(face_orientation_name)
    placement, translation_reference_point = placement_strategy(frame, face)
    return {
        'length': frame.Size,
        'placement': placement,
        'translation_reference_point': translation_reference_point
    }
