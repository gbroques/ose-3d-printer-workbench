from osecore.app.three_dimensional_space_enums import Side

from .between_bounds import between_bounds
from .face_side_strategy import FaceSideStrategy


class ZAxisFaceSideStrategy(FaceSideStrategy):

    def _get_sides(self):
        return [Side.FRONT, Side.REAR]

    def _is_between_lower_bounds(self, face, frame):
        return _between_front_bounds(face, frame)

    def _is_between_upper_bounds(self, face, frame):
        return _between_rear_bounds(face, frame)


def _between_front_bounds(face, frame):
    value = face.Surface.Position.y

    lower_bound = frame.Proxy.YMin

    thickness = frame.Thickness.Value
    upper_bound = lower_bound + thickness

    return between_bounds(value, lower_bound, upper_bound)


def _between_rear_bounds(face, frame):
    value = face.Surface.Position.y
    upper_bound = frame.Proxy.YMax

    thickness = frame.Thickness.Value
    lower_bound = upper_bound - thickness
    return between_bounds(value, lower_bound, upper_bound)
