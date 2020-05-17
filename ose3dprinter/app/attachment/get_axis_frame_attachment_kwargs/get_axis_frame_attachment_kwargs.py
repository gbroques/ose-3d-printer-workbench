from FreeCAD import Vector
from ose3dprinter.app.attachment.attachment_error import AttachmentError
from ose3dprinter.app.enums import Axis, Side
from ose3dprinter.app.model import FrameModel
from ose3dprinter.app.shape.face import (is_face_parallel_to_xy_plane,
                                         is_face_parallel_to_xz_plane,
                                         is_face_parallel_to_yz_plane)
from Part import Face

from .get_placement_strategy import get_placement_strategy


def get_axis_frame_attachment_kwargs(frame,
                                     selected_frame_face,
                                     axis_orientation):
    """
    Get the length, placement, and origin translation offset for
    creating a axis object attached to a selected frame face.
    """
    _validate_frame_and_face(frame, selected_frame_face, axis_orientation)
    face_side = frame.Proxy.get_face_side(
        selected_frame_face, axis_orientation)
    placement_strategy = get_placement_strategy(face_side)
    result = placement_strategy(frame)
    result['side'] = face_side
    return result


def _validate_frame_and_face(frame, face, axis_orientation):
    if not isinstance(face, Face):
        raise AttachmentError('Selected element is not a face')
    if not _is_frame(frame):
        raise AttachmentError('Must select frame')
    if _is_frame_rotated(frame):
        raise AttachmentError('Frame is rotated')
    if not frame.HasCorners and not _is_outer_face(face, frame):
        raise AttachmentError('Must select outer face of frame')
    face_side = frame.Proxy.get_face_side(face, axis_orientation)
    if face_side == Side.BOTTOM:
        raise AttachmentError(
            'Cannot attach axis to bottom side of frame')
    if face_side is None:
        raise AttachmentError('Must select outer face of frame')
    attachable_axis_orientation = _get_orientation_of_attachable_axis(face)
    if attachable_axis_orientation != axis_orientation:
        raise AttachmentError('Attachable "{}" axis orientation of face doesn\'t match "{}" axis orientation'.format(
            attachable_axis_orientation, axis_orientation))
    return frame, face


def _is_frame_rotated(frame):
    rotation = frame.Placement.Rotation
    return rotation.Axis != Vector(0, 0, 1) or rotation.Angle != 0


def _is_outer_face(face, frame):
    outer_faces = frame.Proxy.get_outer_faces()
    return any(map(lambda f: f.isEqual(face), outer_faces))


def _get_orientation_of_attachable_axis(face):
    """
    Returns the orientation of which axis is attachable to the face.
    """
    d = _get_is_face_parallel_to_plane_by_axis_orientation()
    for axis_orientation, is_face_parallel_to_plane in d.items():
        if is_face_parallel_to_plane(face):
            return axis_orientation
    return None


def _get_is_face_parallel_to_plane_by_axis_orientation():
    return {
        Axis.X: is_face_parallel_to_xy_plane,
        Axis.Y: is_face_parallel_to_yz_plane,
        Axis.Z: is_face_parallel_to_xz_plane
    }


def _is_frame(obj):
    return (
        obj.TypeId == 'Part::FeaturePython' and
        obj.Proxy.Type == FrameModel.Type
    )
