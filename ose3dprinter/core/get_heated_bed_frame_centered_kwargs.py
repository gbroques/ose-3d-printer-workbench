from FreeCAD import Placement, Vector, Rotation


def get_heated_bed_frame_centered_kwargs(frame):
    half_frame_size = frame.Size / 2
    z = frame.Placement.Base.z
    placement = Placement(
        Vector(half_frame_size, half_frame_size, z), Rotation())
    origin_translation_offset = Vector(0.5, 0.5, 0)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }
