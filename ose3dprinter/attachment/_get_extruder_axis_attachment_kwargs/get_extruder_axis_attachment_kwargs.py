from FreeCAD import Placement, Rotation, Vector
from osecore.app.attachment import AttachmentError
from osecore.app.shape.face import is_face_parallel_to_xy_plane
from Part import Face

from ose3dprinter.model import AxisModel


def get_extruder_axis_attachment_kwargs(axis, selected_axis_face):
    _validate_axis_and_face(axis, selected_axis_face)
    x = (
        axis.Shape.BoundBox.XMin +
        axis.Proxy.calculate_carriage_box_x()
    )
    y = axis.Shape.BoundBox.YMin
    z = selected_axis_face.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation())
    origin_translation_offset = Vector(0, 0, 0)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }


def _validate_axis_and_face(axis, face):
    if not isinstance(face, Face):
        raise AttachmentError('Selected element is not a face')
    if not _is_axis:
        raise AttachmentError('Must select axis')
    if not is_face_parallel_to_xy_plane(face):
        raise AttachmentError('Face must be parallel to XY plane')
    if not axis.Proxy.is_x():
        raise AttachmentError('Must select X axis')

    axis_bounding_box = axis.Shape.BoundBox
    axis_left_bound = axis_bounding_box.XMin
    axis_right_bound = axis_bounding_box.XMax

    face_bounding_box = face.BoundBox
    face_left_bound = face_bounding_box.XMin
    face_right_bound = face_bounding_box.XMax

    if (face_left_bound <= axis_left_bound or
            face_right_bound >= axis_right_bound):
        raise AttachmentError('Must select carriage face')

    if axis_bounding_box.ZMin == face_bounding_box.ZMin:
        raise AttachmentError('Must select top carriage face')
    return axis, face


def _is_axis(obj):
    return (
        obj.TypeId == 'Part::FeaturePython' and
        obj.Proxy.Type == AxisModel.Type
    )
