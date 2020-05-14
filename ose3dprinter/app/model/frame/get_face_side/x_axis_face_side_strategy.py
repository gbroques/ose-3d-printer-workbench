from FreeCAD import Console
from ose3dprinter.app.enums import Side

from .between_bounds import between_bounds
from .face_side_strategy import FaceSideStrategy


class XAxisFaceSideStrategy(FaceSideStrategy):

    def _get_sides(self):
        return [Side.BOTTOM, Side.TOP]

    def _is_between_lower_bounds(self, face, frame):
        Console.PrintWarning('Bottom side bounds checking not supported.\n')
        pass

    def _is_between_upper_bounds(self, face, frame):
        return _between_top_bounds(face, frame)


def _between_top_bounds(face, frame):
    value = face.Surface.Position.z

    upper_bound = frame.Proxy.ZMax
    thickness = frame.Thickness.Value

    lower_bound = upper_bound - thickness

    return between_bounds(value, lower_bound, upper_bound)
