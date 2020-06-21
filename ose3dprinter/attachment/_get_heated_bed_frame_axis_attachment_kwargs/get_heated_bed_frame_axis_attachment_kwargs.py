from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.model import AxisModel, FrameModel
from osecore.app.attachment import AttachmentError


def get_heated_bed_frame_axis_attachment_kwargs(frame, axis):
    _validate_frame(frame)
    _validate_axis(axis)
    x = frame.Shape.BoundBox.Center.x
    y = frame.Shape.BoundBox.Center.y
    z = axis.Proxy.calculate_top_of_carriage_box_for_z_axis()
    placement = Placement(Vector(x, y, z), Rotation())
    origin_translation_offset = Vector(-0.5, -0.5, 0)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }


def _validate_frame(frame):
    if not _is_frame(frame):
        raise AttachmentError('Must select frame')


def _validate_axis(z_axis):
    if not _is_axis(z_axis) or not z_axis.Proxy.is_z():
        raise AttachmentError('Must select Z axis')


def _is_axis(obj):
    return (
        obj.TypeId == 'Part::FeaturePython' and
        obj.Proxy.Type == AxisModel.Type
    )


def _is_frame(obj):
    return (
        obj.TypeId == 'Part::FeaturePython' and
        obj.Proxy.Type == FrameModel.Type
    )
