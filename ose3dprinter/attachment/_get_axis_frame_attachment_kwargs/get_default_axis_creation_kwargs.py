from osecore.app.three_dimensional_space_enums import CoordinateAxis, Side


def get_default_axis_creation_kwargs(axis_orientation: str) -> dict:
    """Get default kwargs to create an axis with when not attaching to a frame.

    :param axis_orientation: Orientation of axis.
    :return: Default kwargs to create an axis with when not attaching to a frame.
    """
    return {
        'orientation': axis_orientation,
        'side': _get_default_side(axis_orientation)
    }


def _get_default_side(axis_orientation):
    return {
        CoordinateAxis.X: Side.TOP,
        CoordinateAxis.Y: Side.LEFT,
        CoordinateAxis.Z: Side.FRONT
    }[axis_orientation]
