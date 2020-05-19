from functools import reduce

import Part
from FreeCAD import Vector


class CNCCutFrame:

    @staticmethod
    def make(side, width, sheet_thickness):
        """Make a frame from flat sheets cut by a CNC machine,
        then welded or epoxied together.

        This approach works best with welding.

        See Also:
            https://wiki.opensourceecology.org/wiki/D3D_Frame

        :param side: Dimension of one side of a cubic sheet.
        :type side: float
        :param width: Width of outer sheet,
                    after an inner sheet is cut out of the center.
        :type width: float
        :param sheet_thickness: Thickness of each sheet.
        :type sheet_thickness: float
        :return: A frame "welded" together from eight CNC cut sheets.
        :rtype: Part.Shape
        """
        bottom_frame = make_sheet(side, width, sheet_thickness)

        top_frame = bottom_frame.copy()
        top_frame.translate(Vector(0, 0, side - sheet_thickness))

        left_wall = bottom_frame.copy()
        left_wall.rotate(Vector(0, 0, 0), Vector(0, -1, 0), 90)
        left_wall.translate(Vector(sheet_thickness, 0, 0))

        right_wall = left_wall.copy()
        right_wall.translate(Vector(side - sheet_thickness, 0, 0))

        front_wall = bottom_frame.copy()
        front_wall.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 90)
        front_wall.translate(Vector(0, sheet_thickness, 0))

        rear_wall = front_wall.copy()
        rear_wall.translate(Vector(0, side - sheet_thickness, 0))

        parts = [
            bottom_frame,
            left_wall,
            right_wall,
            front_wall,
            rear_wall,
            top_frame
        ]

        frame = reduce(lambda union, part: union.fuse(part), parts)

        # removeSplitter() refines shape
        return frame.removeSplitter()


def make_sheet(side, width, thickness):
    """Make one side of the frame or "sheet".

    See the following 2-dimensional ASCII rendering of a sheet below.
    ______________
    | __________ |
    | |        | |
    | |        | |
    | |________| |
    |____________|

    A sheet is a cubic plane of metal with dimensions specified by `side`,
    thickness specified by `thickness`, and inner sheet cut out of the center,
    leaving the outer width with a dimension specified by `width`.

    :param side: Dimension of one side of the cubic sheet.
    :type side: float
    :param width: Width of outer sheet,
                  after an inner sheet is cut out of the center.
    :type width: float
    :param thickness: Thickness of the sheet.
    :type thickness: float
    :return: A sheet, or one side of a frame.
    :rtype: Part.Shape
    """
    sheet = Part.makeBox(side, side, thickness)

    inner_side = side - (width * 2)
    inner_sheet = Part.makeBox(inner_side, inner_side, thickness)
    inner_sheet.translate(Vector(width, width, 0))

    return sheet.cut(inner_sheet)
