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
    placement_strategy_result = placement_strategy(frame)
    print "frame.Placement {}".format(frame.Placement)

    print "placement_strategy_result {}".format(placement_strategy_result)

    adjusted = adjust_placement_for_frame_rotation(
        placement_strategy_result, frame)
    print "adjusted {}".format(adjusted)

    return adjusted


def adjust_placement_for_frame_rotation(placement_strategy_result, frame):
    frame_rotation = frame.Placement.Rotation.toEuler()
    rotation = placement_strategy_result['placement'].Rotation.toEuler()
    new_rotation = Rotation(
        rotation[0] + frame_rotation[0],
        rotation[1] + frame_rotation[1],
        rotation[2] + frame_rotation[2])
    # Adjust placement_strategy_result['placement'].Base.y by (-math.sin(math.radians(30)) * 304.8)
    placement_strategy_result['placement'] = Placement(
        placement_strategy_result['placement'].Base, new_rotation)
    return placement_strategy_result


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


def rotate(u, angle, axis=Vector(0, 0, 1)):
    """Rotate the vector by the specified angle, around the given axis.
    If the axis is omitted, the rotation is made around the Z axis
    (on the XY plane).
    It uses a 3x3 rotation matrix.
    ::
        u_rot = R u
                (c + x*x*t    xyt - zs     xzt + ys )
        u_rot = (xyt + zs     c + y*y*t    yzt - xs ) * u
                (xzt - ys     yzt + xs     c + z*z*t)
    Where `x`, `y`, `z` indicate unit components of the axis;
    `c` denotes a cosine of the angle; `t` indicates a complement
    of that cosine; `xs`, `ys`, `zs` indicate products of the unit
    components and the sine of the angle; and `xyt`, `xzt`, `yzt`
    indicate products of two unit components and the complement
    of the cosine.
    Parameters
    ----------
    u : Base::Vector3
        The vector.
    angle : float
        The angle of rotation given in radians.
    axis : Base::Vector3, optional
        The vector specifying the axis of rotation.
        It defaults to `(0, 0, 1)`, the +Z axis.
    Returns
    -------
    Base::Vector3
        The new rotated vector.
        If the `angle` is zero, return the original vector `u`.
    """

    if angle == 0:
        return u

    # Unit components, so that x**2 + y**2 + z**2 = 1
    L = axis.Length
    x = axis.x/L
    y = axis.y/L
    z = axis.z/L

    c = math.cos(angle)
    s = math.sin(angle)
    t = 1 - c

    # Various products
    xyt = x * y * t
    xzt = x * z * t
    yzt = y * z * t
    xs = x * s
    ys = y * s
    zs = z * s

    m = FreeCAD.Matrix(c + x*x*t,   xyt - zs,   xzt + ys,   0,
                       xyt + zs,    c + y*y*t,  yzt - xs,   0,
                       xzt - ys,    yzt + xs,   c + z*z*t,  0)

    return m.multiply(u)
