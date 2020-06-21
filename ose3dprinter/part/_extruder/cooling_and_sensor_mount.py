from functools import reduce

import Part
from FreeCAD import Vector
from osecore.app.shape.face import make_face_from_vectors


class CoolingAndSensorMount:
    """Cooling and Sensor mount for extruder, and sensor itself.

    Based on:
        https://wiki.opensourceecology.org/wiki/File:ExtruderActiveCoolingAndSensor.FCStd

    See:
        https://wiki.opensourceecology.org/images/thumb/d/dd/Secondxtruderpart.png/120px-Secondxtruderpart.png

    Sensor:
        https://wiki.opensourceecology.org/images/thumb/9/9e/8mmsensor.jpg/120px-8mmsensor.jpg
    """

    vent_box_width = 5

    @classmethod
    def make(cls,
             slanted_side_width,
             main_part_length,
             main_part_bottom_base_overhang_width):
        slanted_side = make_cooling_and_sensor_slanted_side(
            slanted_side_width, main_part_length)
        slanted_side.translate(
            Vector(-slanted_side_width, 0, 0))

        sensor_holder_width = 25
        sensor_holder_height = 9
        sensor, sensor_holder = make_sensor_and_sensor_holder(
            sensor_holder_width, sensor_holder_height)

        blower_vent_width = 22
        blower_vent = Part.makeCylinder(
            sensor_holder_width,
            blower_vent_width,
            Vector(
                -blower_vent_width,
                0,
                0
            ),
            Vector(1, 0, 0),
            90
        )

        blower_vent_box = Part.makeBox(
            blower_vent_width, cls.vent_box_width, sensor_holder_width)
        blower_vent_box.translate(Vector(-blower_vent_width, 0, 0))

        lower_blower_vent_height = 18
        lower_blower_vent_center = Vector(
            -blower_vent_width, 0, -sensor_holder_height)
        lower_blower_vent = Part.makeCylinder(
            lower_blower_vent_height,
            sensor_holder_width,
            lower_blower_vent_center,
            Vector(0, -1, 0),
            90
        )
        lower_blower_vent.rotate(
            lower_blower_vent_center, Vector(0, 1, 0), 90)
        lower_blower_vent.translate(
            Vector(blower_vent_width - slanted_side_width, 0, 0))

        lower_blower_vent_box = Part.makeBox(
            slanted_side_width, sensor_holder_width, lower_blower_vent_height)
        lower_blower_vent_box.translate(Vector(
            -slanted_side_width,
            -sensor_holder_width,
            -lower_blower_vent_height - sensor_holder_height))

        parts = [
            slanted_side,
            sensor,
            sensor_holder,
            blower_vent,
            blower_vent_box,
            lower_blower_vent,
            lower_blower_vent_box
        ]

        return reduce(lambda union, part: union.fuse(part), parts)


def make_cooling_and_sensor_slanted_side(thickness, length):
    """
          20
       ---------
       |        \
       |         \
       |          \
    55 |           \
       |            \  19
       |             -------
       |                   | 7
       ---------------------
             87
    """
    top = 20
    middle = 19
    bottom = length
    left = 55
    right = 7

    bottom_left = Vector(0, 0, 0)
    bottom_right = Vector(0, bottom, 0)

    mid_right = Vector(0, bottom, right)
    mid_left = Vector(0, bottom - middle, right)

    top_right = Vector(0, top, left)
    top_left = Vector(0, 0, left)

    vectors = [
        bottom_left,
        bottom_right,
        mid_right,
        mid_left,
        top_right,
        top_left
    ]

    face = make_face_from_vectors(vectors)

    return face.extrude(Vector(thickness, 0, 0))


def make_sensor_and_sensor_holder(sensor_holder_box_width,
                                  sensor_holder_box_height):
    """
    /-------
    | O    |
    \-------
    """
    sensor_holder_cylinder_radius = sensor_holder_box_width / 2
    sensor_holder_thickness = 2
    sensor_holder_box_length = 34
    offset = 0.5

    sensor_center_x = -sensor_holder_box_length + offset

    # Sensor
    # ------
    sensor = Part.makeCylinder(
        sensor_holder_cylinder_radius - sensor_holder_thickness,
        69.5,
        Vector(
            sensor_center_x,
            sensor_holder_cylinder_radius + offset - sensor_holder_box_width,
            -15 - sensor_holder_box_height)
    )

    # Sensor Holder
    # -------------
    sensor_holder_box = Part.makeBox(
        sensor_holder_box_length,
        sensor_holder_box_width,
        sensor_holder_box_height)
    sensor_holder_box.translate(Vector(
        -sensor_holder_box_length,
        -sensor_holder_box_width,
        -sensor_holder_box_height))

    sensor_cylinder_center = Vector(
        sensor_center_x,
        sensor_holder_cylinder_radius + offset,
        0)
    sensor_holder_cylinder = Part.makeCylinder(
        sensor_holder_cylinder_radius + offset - sensor_holder_thickness,
        sensor_holder_box_height,
        sensor_cylinder_center)
    sensor_holder_cylinder.translate(
        Vector(0, -sensor_holder_box_width, -sensor_holder_box_height))

    hollow_sensor_holder_cylinder = sensor_holder_cylinder.makeThickness(
        [   # Top and bottom faces of cylinder
            sensor_holder_cylinder.Faces[1],
            sensor_holder_cylinder.Faces[2]
        ], sensor_holder_thickness, 0)

    sensor_holder_box_with_cylinder_cutout = sensor_holder_box.cut(
        sensor_holder_cylinder)

    sensor_holder = hollow_sensor_holder_cylinder.fuse(
        sensor_holder_box_with_cylinder_cutout)

    return sensor, sensor_holder
