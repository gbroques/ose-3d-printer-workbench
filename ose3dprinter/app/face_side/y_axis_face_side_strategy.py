
from ose3dprinter.app.enums import Side
from ose3dprinter.app.is_face_parallel_to_plane import \
    is_face_parallel_to_yz_plane
from ose3dprinter.app.model.frame.angle_frame_connector import \
    AngleFrameConnector

from .between_bounds import between_bounds
from .face_side_strategy import FaceSideStrategy


class YAxisFaceSideStrategy(FaceSideStrategy):

    def _get_sides(self):
        return [Side.LEFT, Side.RIGHT]

    def _is_between_lower_bounds(self, face, frame_with_corners):
        return _between_left_bounds(face, frame_with_corners)

    def _is_between_upper_bounds(self, face, frame_with_corners):
        return _between_right_bounds(face, frame_with_corners)

    def _is_face_parallel_to_plane(self, face):
        return is_face_parallel_to_yz_plane(face)

    def _get_axis_orientation_index(self):
        return 1


def _between_left_bounds(face, frame_with_corners):
    value = face.Surface.Position.x

    lower_bound = frame_with_corners.Shape.BoundBox.XMin

    thickness = frame_with_corners.Thickness.Value
    upper_bound = lower_bound + thickness + \
        AngleFrameConnector.axis_side_mount_width

    return between_bounds(value, lower_bound, upper_bound)


def _between_right_bounds(face, frame_with_corners):
    value = face.Surface.Position.x

    upper_bound = frame_with_corners.Shape.BoundBox.XMax

    thickness = frame_with_corners.Thickness.Value
    lower_bound = upper_bound - thickness - \
        AngleFrameConnector.axis_side_mount_width

    return between_bounds(value, lower_bound, upper_bound)
