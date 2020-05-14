from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.app.exceptions import AttachmentError
from ose3dprinter.app.is_face_parallel_to_plane import \
    is_face_parallel_to_xy_plane
from ose3dprinter.app.model import UniversalAxisModel
from Part import Face


def get_extruder_x_axis_carriage_attachment_kwargs(universal_axis, face):
    validate_axis_and_face(universal_axis, face)
    x = (
        universal_axis.Shape.BoundBox.XMin +
        universal_axis.Proxy.calculate_carriage_box_x()
    )
    y = universal_axis.Shape.BoundBox.YMin
    z = face.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation())
    origin_translation_offset = Vector(0, 0, 0)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }


def validate_axis_and_face(axis, face):
    if not isinstance(face, Face):
        raise AttachmentError('Selected element is not a face')
    if axis.Proxy.Type != UniversalAxisModel.Type:
        raise AttachmentError('Must select universal axis')
    if not is_face_parallel_to_xy_plane(face):
        raise AttachmentError('Face must be parallel to XY plane')

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
