from ose3dprinter.app.enums import AxisOrientation, Side


def get_default_axis_creation_kwargs(axis_orientation):
    return {
        'orientation': axis_orientation,
        'side': get_default_side(axis_orientation)
    }


def get_default_side(axis_orientation):
    return {
        AxisOrientation.X: Side.TOP,
        AxisOrientation.Y: Side.LEFT,
        AxisOrientation.Z: Side.FRONT
    }[axis_orientation]
