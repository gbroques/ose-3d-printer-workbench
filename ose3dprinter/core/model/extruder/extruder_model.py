import Part
from FreeCAD import Vector
from ose3dprinter.core.is_edge_parallel_to_axis import \
    is_edge_parallel_to_y_axis
from ose3dprinter.core.model.base_model import BaseModel

from .cooling_and_sensor_mount import CoolingAndSensorMount
from .main_extruder_part import MainExtruderPart


class ExtruderModel(BaseModel):
    """
    Encapsulates the data (i.e. topography and shape) for a Extruder,
    and is separate from the "view" or GUI representation.

    Based on:
        https://wiki.opensourceecology.org/wiki/File:Simpleextruderassy.fcstd

    See:
        https://wiki.opensourceecology.org/wiki/File:Finalextruder.png
    """

    Type = 'OSEExtruder'

    def __init__(self, obj,  placement, origin_translation_offset):
        init_args = (placement, origin_translation_offset)
        super(ExtruderModel, self).__init__(*init_args)

        obj.Proxy = self

    def execute(self, obj):
        """
        Called on document recompute
        """
        main_part_width = 50
        main_part_length = 87
        main_part_bottom_base_overhang_width = 5

        main_part = MainExtruderPart.make(
            main_part_width,
            main_part_length,
            main_part_bottom_base_overhang_width)

        cooling_and_sensor_slanted_side_width = 4
        cooling_and_sensor_mount = CoolingAndSensorMount.make(
            cooling_and_sensor_slanted_side_width,
            main_part_length,
            main_part_bottom_base_overhang_width
        )
        cooling_and_sensor_mount.translate(
            Vector(0, main_part_bottom_base_overhang_width, 0))

        blower_radius = 45 / 2
        blower_width = 15.4
        blower = Part.makeCylinder(
            blower_radius,
            blower_width)
        blower.rotate(Vector(0, 0, 0), Vector(0, -1, 0), 90)
        blower_y = 15.25 + blower_radius
        blower.translate(
            Vector(
                -cooling_and_sensor_slanted_side_width,
                blower_y,
                blower_radius))

        # TODO: Remove duplication of sensor_holder_width
        #       from extruder_model.py and cooling_and_sensor_mount.py
        #       Should blower box even use sensor_holder_width,
        #       or should the blower be independent from knowledge of
        #       cooling and sensor mount?
        sensor_holder_width = 25
        blower_box_y_offset = main_part_bottom_base_overhang_width + \
            CoolingAndSensorMount.vent_box_width
        blower_box = Part.makeBox(
            blower_width,
            blower_y - blower_box_y_offset,
            sensor_holder_width)
        blower_box.translate(
            Vector(
                -cooling_and_sensor_slanted_side_width - blower_width,
                blower_box_y_offset,
                0))

        motor = make_motor()
        motor.translate(Vector(0, 0, MainExtruderPart.base_height))

        parts = [
            main_part,
            cooling_and_sensor_mount,
            blower,
            blower_box,
            motor
        ]
        dimensions = (main_part_width, main_part_length, MainExtruderPart.base_height)
        self.move_parts(parts, dimensions)

        extruder = reduce(lambda union, part: union.fuse(part), parts)

        # removeSplitter() refines shape
        obj.Shape = extruder.removeSplitter()

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state


def make_motor():
    motor_side = 42
    motor_height = 44
    distance_from_side = 4.7
    motor = Part.makeBox(motor_side, motor_height, motor_side)
    motor.translate(Vector(distance_from_side, 0, 0))
    edges_parallel_to_y_axis = list(
        filter(is_edge_parallel_to_y_axis, motor.Edges))
    chamfered_motor = motor.makeChamfer(5, edges_parallel_to_y_axis)
    return chamfered_motor
