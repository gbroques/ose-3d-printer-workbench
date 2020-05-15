from FreeCAD import Placement, Rotation, Vector

from .attachment_error import AttachmentError


def get_heated_bed_frame_axis_attachment_kwargs(frame, axis):
    _validate_axis_is_in_z_orientation(axis)
    x = frame.Shape.BoundBox.Center.x
    y = frame.Shape.BoundBox.Center.y
    z = axis.Proxy.calculate_top_of_carriage_box_for_z_axis()
    placement = Placement(Vector(x, y, z), Rotation())
    origin_translation_offset = Vector(-0.5, -0.5, 0)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }


def _validate_axis_is_in_z_orientation(z_axis):
    if not z_axis.Proxy.is_z():
        raise AttachmentError('Must select Z axis')
