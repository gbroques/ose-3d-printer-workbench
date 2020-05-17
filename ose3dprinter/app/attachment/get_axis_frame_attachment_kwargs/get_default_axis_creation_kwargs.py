from ose3dprinter.app.enums import Axis, Side


def get_default_axis_creation_kwargs(axis_orientation):
    return {
        'orientation': axis_orientation,
        'side': _get_default_side(axis_orientation)
    }


def _get_default_side(axis_orientation):
    return {
        Axis.X: Side.TOP,
        Axis.Y: Side.LEFT,
        Axis.Z: Side.FRONT
    }[axis_orientation]
