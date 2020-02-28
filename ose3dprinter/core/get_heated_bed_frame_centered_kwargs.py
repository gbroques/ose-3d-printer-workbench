from FreeCAD import Placement, Vector, Rotation


def get_heated_bed_frame_centered_kwargs(frame):
    x = frame.Shape.BoundBox.Center.x
    y = frame.Shape.BoundBox.Center.y
    z = frame.Shape.BoundBox.ZMin
    placement = Placement(Vector(x, y, z), Rotation())
    origin_translation_offset = Vector(0.5, 0.5, 0)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }
