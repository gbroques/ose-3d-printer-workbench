from FreeCAD import Console
from ose3dprinter.app.enums import Side
from ose3dprinter.app.is_face_parallel_to_plane import \
    is_face_parallel_to_xy_plane

from .between_bounds import between_bounds
from .face_side_strategy import FaceSideStrategy


class XAxisFaceSideStrategy(FaceSideStrategy):

    def _get_sides(self):
        return [Side.BOTTOM, Side.TOP]

    def _is_between_lower_bounds(self, face, frame_with_corners):
        Console.PrintWarning('Bottom side bounds checking not supported.\n')
        pass

    def _is_between_upper_bounds(self, face, frame_with_corners):
        return _between_top_bounds(face, frame_with_corners)

    def _is_face_parallel_to_plane(self, face):
        return is_face_parallel_to_xy_plane(face)

    def _get_axis_orientation_index(self):
        return 0


def _between_top_bounds(face, frame_with_corners):
    value = face.Surface.Position.z

    upper_bound = frame_with_corners.Proxy.ZMax
    thickness = frame_with_corners.Thickness.Value

    lower_bound = upper_bound - thickness

    return between_bounds(value, lower_bound, upper_bound)
