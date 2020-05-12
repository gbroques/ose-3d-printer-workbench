from ose3dprinter.app.enums import Side
from ose3dprinter.app.is_face_parallel_to_plane import \
    is_face_parallel_to_xz_plane

from .between_bounds import between_bounds
from .face_side_strategy import FaceSideStrategy


class ZAxisFaceSideStrategy(FaceSideStrategy):

    def _get_sides(self):
        return [Side.FRONT, Side.REAR]

    def _is_between_lower_bounds(self, face, frame_with_corners):
        return _between_front_bounds(face, frame_with_corners)

    def _is_between_upper_bounds(self, face, frame_with_corners):
        return _between_rear_bounds(face, frame_with_corners)

    def _is_face_parallel_to_plane(self, face):
        return is_face_parallel_to_xz_plane(face)

    def _get_axis_orientation_index(self):
        return 2


def _between_front_bounds(face, frame_with_corners):
    value = face.Surface.Position.y

    lower_bound = frame_with_corners.Proxy.YMin

    thickness = frame_with_corners.Thickness.Value
    upper_bound = lower_bound + thickness

    return between_bounds(value, lower_bound, upper_bound)


def _between_rear_bounds(face, frame_with_corners):
    value = face.Surface.Position.y
    upper_bound = frame_with_corners.Proxy.YMax

    thickness = frame_with_corners.Thickness.Value
    lower_bound = upper_bound - thickness
    return between_bounds(value, lower_bound, upper_bound)
