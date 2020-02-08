from FreeCAD import Vector
from Part import Face

from .face_orientation import get_face_side, get_orientation_of_attachable_axis
from .get_outer_faces_of_frame import get_outer_faces_of_frame
from .get_placement_strategy import get_placement_strategy


def get_axis_frame_attachment_kwargs(selection, axis_orientation):
    """
    Get the length, placement, and origin translation offset for
    creating a universal axis object attached to a selected frame face.
    """
    frame, face = get_frame_and_face_from_selection(
        selection, axis_orientation)
    face_side = get_face_side(frame, face)
    placement_strategy = get_placement_strategy(face_side)
    placement, origin_translation_offset = placement_strategy(frame, face)
    return {
        'length': frame.Size,
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }


def get_frame_and_face_from_selection(selection, axis_orientation):
    """Gets a selected frame and face.

    Raises AxisFrameAttachmentError,
    if unable to get frame or face from selection.
    """
    num_selected = len(selection)
    if num_selected != 1:
        raise AxisFrameAttachmentError(
            'Selected {} instead of 1 element'.format(num_selected))
    first_selection = selection[0]
    num_sub_objects = len(first_selection.SubObjects)
    if num_sub_objects != 1:
        message_template = 'Selected object has {} sub objects instead of 1'
        raise AxisFrameAttachmentError(
            message_template.format(num_sub_objects))
    potential_face = first_selection.SubObjects[0]
    if not isinstance(potential_face, Face):
        raise AxisFrameAttachmentError('Selected element is not a face')
    face = potential_face
    potential_frame = first_selection.Object
    if potential_frame.Proxy.Type != 'OSEFrame':
        raise AxisFrameAttachmentError('Must select frame')
    frame = potential_frame
    if is_frame_rotated(frame):
        raise AxisFrameAttachmentError('Frame is rotated')
    if not is_outer_face_of_frame(face, frame):
        raise AxisFrameAttachmentError('Must select outer face of frame')
    face_side = get_face_side(frame, face)
    if face_side == 'bottom':
        raise AxisFrameAttachmentError(
            'Cannot attach axis to bottom side of frame')
    attachable_axis = get_orientation_of_attachable_axis(face)
    if attachable_axis != axis_orientation:
        message_template = 'Cannot attach {} axis to {} side of frame'
        raise AxisFrameAttachmentError(message_template.format(
            axis_orientation.upper(), face_side))
    return frame, face


def is_frame_rotated(frame):
    rotation = frame.Placement.Rotation
    return rotation.Axis != Vector(0, 0, 1) or rotation.Angle != 0


def is_outer_face_of_frame(face, frame):
    outer_faces = get_outer_faces_of_frame(frame)
    return any(map(lambda f: f.isEqual(face), outer_faces))


class AxisFrameAttachmentError(ValueError):
    """Raise when unable to attach axis to frame"""
