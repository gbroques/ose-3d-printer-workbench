from ose3dprinter.app.enums import AxisOrientation

from .x_axis_face_side_strategy import XAxisFaceSideStrategy
from .y_axis_face_side_strategy import YAxisFaceSideStrategy
from .z_axis_face_side_strategy import ZAxisFaceSideStrategy


class FaceSideStrategyFactory:

    @staticmethod
    def create(axis_orientation):
        if axis_orientation == AxisOrientation.X:
            return XAxisFaceSideStrategy()
        elif axis_orientation == AxisOrientation.Y:
            return YAxisFaceSideStrategy()
        elif axis_orientation == AxisOrientation.Z:
            return ZAxisFaceSideStrategy()
        else:
            raise ValueError(
                'Unrecognized {} axis orientation'.format(axis_orientation))
