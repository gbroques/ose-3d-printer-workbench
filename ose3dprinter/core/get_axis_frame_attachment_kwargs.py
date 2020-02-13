from FreeCAD import Vector
from Part import Face

from .exceptions import AttachmentError
from .face_orientation import get_face_side, get_orientation_of_attachable_axis
from .get_outer_faces_of_frame import get_outer_faces_of_frame
from .get_placement_strategy import get_placement_strategy
from .model import FrameModel


def get_axis_frame_attachment_kwargs(frame, face, axis_orientation):
    """
    Get the length, placement, and origin translation offset for
    creating a universal axis object attached to a selected frame face.
    """
    validate_frame_and_face(frame, face, axis_orientation)
    face_side = get_face_side(frame, face)
    placement_strategy = get_placement_strategy(face_side)
    placement, origin_translation_offset = placement_strategy(frame, face)
    return {
        'length': frame.Size,
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }


def validate_frame_and_face(frame, face, axis_orientation):
    if not isinstance(face, Face):
        raise AttachmentError('Selected element is not a face')
    if frame.Proxy.Type != FrameModel.Type:
        raise AttachmentError('Must select frame')
    if is_frame_rotated(frame):
        raise AttachmentError('Frame is rotated')
    if not is_outer_face_of_frame(face, frame):
        raise AttachmentError('Must select outer face of frame')
    face_side = get_face_side(frame, face)
    if face_side == 'bottom':
        raise AttachmentError(
            'Cannot attach axis to bottom side of frame')
    attachable_axis = get_orientation_of_attachable_axis(face)
    if attachable_axis != axis_orientation:
        message_template = 'Cannot attach {} axis to {} side of frame'
        raise AttachmentError(message_template.format(
            axis_orientation.upper(), face_side))
    return frame, face


def is_frame_rotated(frame):
    rotation = frame.Placement.Rotation
    return rotation.Axis != Vector(0, 0, 1) or rotation.Angle != 0


def is_outer_face_of_frame(face, frame):
    outer_faces = get_outer_faces_of_frame(frame)
    return any(map(lambda f: f.isEqual(face), outer_faces))
