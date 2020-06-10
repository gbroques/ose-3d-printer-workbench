from functools import reduce

import Part
from FreeCAD import Vector
from osecore.app.shape.face import make_face_from_vectors


class MainExtruderPart:
    """Main extruder part

    Based on:
        https://wiki.opensourceecology.org/wiki/File:Mainextruderpart.fcstd

    See:
        https://wiki.opensourceecology.org/wiki/File:Mainextruderpart.png
    """

    base_height = 7

    @classmethod
    def make(cls, width, length, bottom_base_overhang_width):
        # Base
        # ----
        main_part_base = Part.makeBox(width, length, cls.base_height)

        # Slanted Side
        # ------------
        slanted_side_width = 3.30
        slanted_side_height = 50
        slanted_side = make_slanted_side(
            slanted_side_width,
            slanted_side_height)
        slanted_side.translate(
            Vector(width - slanted_side_width, 0, 0))

        # Roof
        # ----
        roof_height = 4
        roof_width = 25.25
        roof = Part.makeBox(width, roof_width, roof_height)
        roof.translate(Vector(0, 0, slanted_side_height))

        # Bottom Base Overhang
        # --------------------
        bottom_base_overhang_height = 27.5
        bottom_base_overhang = Part.makeBox(
            width,
            bottom_base_overhang_width,
            bottom_base_overhang_height)
        bottom_base_overhang.translate(
            Vector(0, 0, -bottom_base_overhang_height))

        # Parts
        # -----
        parts = [
            main_part_base,
            slanted_side,
            roof,
            bottom_base_overhang
        ]
        return reduce(lambda union, part: union.fuse(part), parts)


def make_slanted_side(width_or_thickness, height):
    """
            25.25
       --------------
       |             \
       |              \
       |               \
    50 |                \
       |                |
       |                |  28.27
       |                |
       ------------------
             51.10
    """
    top = 25.25
    right = 28.27
    bottom = 51.10
    left = height  # 50

    bottom_left = Vector(0, 0, 0)
    bottom_right = Vector(0, bottom, 0)

    mid_right = Vector(0, bottom, right)

    top_left = Vector(0, 0, left)
    top_right = Vector(0, top, left)

    vectors = [
        bottom_left,
        bottom_right,
        mid_right,
        top_right,
        top_left
    ]

    face = make_face_from_vectors(vectors)

    return face.extrude(Vector(width_or_thickness, 0, 0))
