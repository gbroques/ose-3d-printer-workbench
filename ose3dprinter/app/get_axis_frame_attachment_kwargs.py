from math import degrees

from FreeCAD import Placement, Rotation, Vector
from Part import Face

from .enums import Side
from .exceptions import AttachmentError
from .face_orientation import get_face_side, get_orientation_of_attachable_axis
from .get_outer_faces import get_outer_faces_of_cnc_cut_frame
from .get_placement_strategy import get_placement_strategy
from .model import FrameModel
import FreeCAD
import math


def get_axis_frame_attachment_kwargs(frame, face, axis_orientation):
    """
    Get the length, placement, and origin translation offset for
    creating a universal axis object attached to a selected frame face.
    """
    validate_frame_and_face(frame, face, axis_orientation)
    face_side = get_face_side(frame, face)

    placement_strategy = get_placement_strategy(face_side)
    original_frame_shape = frame.Shape.copy()
    unrotated_frame_shape = get_unrotated_frame_shape(frame)
    frame.Shape = unrotated_frame_shape
    placement_strategy_result = placement_strategy(frame)
    frame.Shape = original_frame_shape
    print "frame.Placement {}".format(frame.Placement)

    print "placement_strategy_result {}".format(placement_strategy_result)

    placement = placement_strategy_result['placement']
    placement_strategy_result['placement'] = adjust_placement(
        placement, frame.Placement)

    print "adjusted placement_strategy_result {}".format(
        placement_strategy_result)

    return placement_strategy_result


def adjust_placement(axis_placement, frame_placement):
    frame_rotation = frame_placement.Rotation
    frame_rotation_matrix = Placement(Vector(), frame_rotation).toMatrix()

    axis_rotation = axis_placement.Rotation
    axis_rotation_matrix = Placement(
        Vector(), axis_rotation).toMatrix()

    rotation_matrix = frame_rotation_matrix.multiply(axis_rotation_matrix)

    rotation_matrix.move(frame_rotation.multVec(axis_placement.Base))
    return Placement(rotation_matrix)


def get_unrotated_frame_shape(frame):
    frame_shape_copy = frame.Shape.copy()
    frame_shape_copy.Placement = Placement(
        frame.Shape.Placement.Base, Rotation())
    return frame_shape_copy


def validate_frame_and_face(frame, face, axis_orientation):
    if not isinstance(face, Face):
        raise AttachmentError('Selected element is not a face')
    if frame.Proxy.Type != FrameModel.Type:
        raise AttachmentError('Must select frame')
    # if is_frame_rotated(frame):
    #     raise AttachmentError('Frame is rotated')
    if not frame.HasCorners and not is_outer_face_of_cnc_cut_frame(face, frame):
        raise AttachmentError('Must select outer face of frame')
    face_side = get_face_side(frame, face)
    if face_side == Side.BOTTOM:
        raise AttachmentError(
            'Cannot attach axis to bottom side of frame')
    if face_side is None:
        raise AttachmentError('Must select outer face of frame')
    attachable_axis = get_orientation_of_attachable_axis(face)
    if attachable_axis != axis_orientation:
        message_template = 'Cannot attach {} axis to {} side of frame'
        raise AttachmentError(message_template.format(
            axis_orientation.upper(), face_side))
    return frame, face


def is_frame_rotated(frame):
    rotation = frame.Placement.Rotation
    return rotation.Axis != Vector(0, 0, 1) or rotation.Angle != 0


def is_outer_face_of_cnc_cut_frame(face, cnc_cut_frame):
    outer_faces = get_outer_faces_of_cnc_cut_frame(cnc_cut_frame)
    return any(map(lambda f: f.isSame(face), outer_faces))
