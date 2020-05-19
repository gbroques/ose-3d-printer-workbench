
from ose3dprinter.app.part import AngleFrameConnector
from ose3dprinter.app.three_dimensional_space_enums import Side

from .between_bounds import between_bounds
from .face_side_strategy import FaceSideStrategy


class YAxisFaceSideStrategy(FaceSideStrategy):

    def _get_sides(self):
        return [Side.LEFT, Side.RIGHT]

    def _is_between_lower_bounds(self, face, frame):
        return _between_left_bounds(face, frame)

    def _is_between_upper_bounds(self, face, frame):
        return _between_right_bounds(face, frame)


def _between_left_bounds(face, frame):
    value = face.Surface.Position.x

    lower_bound = frame.Shape.BoundBox.XMin

    thickness = frame.Thickness.Value
    upper_bound = lower_bound + thickness + \
        AngleFrameConnector.axis_side_mount_width

    return between_bounds(value, lower_bound, upper_bound)


def _between_right_bounds(face, frame):
    value = face.Surface.Position.x

    upper_bound = frame.Shape.BoundBox.XMax

    thickness = frame.Thickness.Value
    lower_bound = upper_bound - thickness - \
        AngleFrameConnector.axis_side_mount_width

    return between_bounds(value, lower_bound, upper_bound)
