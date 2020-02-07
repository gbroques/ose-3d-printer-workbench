from .face_orientation import get_face_side
from .get_placement_strategy import get_placement_strategy
from .validate_frame_face_selection import get_frame_and_face_from_selection


def get_axis_frame_attachment_kwargs(selection, axis_orientation):
    """
    Get the length, placement, and origin translation offset for
    creating a universal axis object attached to a selected frame face.
    """
    frame, face = get_frame_and_face_from_selection(
        selection, axis_orientation)
    if frame is None and face is None:
        return {}
    face_side = get_face_side(frame, face)
    placement_strategy = get_placement_strategy(face_side)
    placement, origin_translation_offset = placement_strategy(frame, face)
    return {
        'length': frame.Size,
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }
