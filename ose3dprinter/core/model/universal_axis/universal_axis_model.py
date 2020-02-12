import Part
from FreeCAD import Vector
from ose3dprinter.core.is_edge_parallel_to_axis import \
    is_edge_parallel_to_z_axis
from ose3dprinter.core.model.base_model import BaseModel


class UniversalAxisModel(BaseModel):
    """
    Encapsulates the data (i.e. topography and shape) for a Universal Axis,
    and is separate from the "view" or GUI representation.
    """

    def __init__(self, obj, length, placement, origin_translation_offset):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        init_args = (placement, origin_translation_offset)
        super(UniversalAxisModel, self).__init__(*init_args)

        self.Type = 'OSEUniversalAxis'

        obj.Proxy = self

        # Length property
        length_tooltip = 'Length of axis corresponds to rod length.'
        obj.addProperty('App::PropertyLength', 'Length',
                        'Base', length_tooltip)
        obj.Length = length

        # Rod Diameter property
        rod_diameter_tooltip = 'Diameter of rod.'
        read_only = 1
        obj.addProperty('App::PropertyLength', 'RodDiameter',
                        'Base', rod_diameter_tooltip, read_only)
        obj.RodDiameter = 8

    def execute(self, obj):
        """
        Called on document recompute
        """
        # Get rod dimensions
        rod_length = obj.Length.Value
        rod_radius = obj.RodDiameter.Value / 2

        # Motor side, idler side, and carriage boxes share same height
        box_height = 24

        # Define dimensions of motor side box
        motor_box_width = 59.5
        motor_box_length = 66
        motor_side_box_dimensions = (
            motor_box_width, motor_box_length, box_height)

        # Make motor side box
        motor_side_box = Part.makeBox(*motor_side_box_dimensions)

        # Motor
        motor_side = 37.8
        motor_height = 39.878
        motor_dimensions = (motor_side, motor_side, motor_height)

        # Make Motor
        motor = Part.makeBox(*motor_dimensions)
        half_motor_box_width = motor_box_width / 2
        half_motor_box_length = motor_box_length / 2
        half_motor_side = motor_side / 2
        motor.translate(Vector(
            half_motor_box_width - half_motor_side,
            half_motor_box_length - half_motor_side,
            box_height
        ))
        motor.rotate(Vector(half_motor_box_width,
                            half_motor_box_length, 0), Vector(0, 0, 1), 45)
        vertical_edges = list(
            filter(is_edge_parallel_to_z_axis, motor.Edges))
        chamfered_motor = motor.makeChamfer(5, vertical_edges)

        # Define dimensions of carriage box
        carriage_box_width = 52
        carriage_box_length = 74
        carriage_box_dimensions = (
            carriage_box_width, carriage_box_length, box_height)

        # Make carriage
        carriage_box = Part.makeBox(*carriage_box_dimensions)
        carriage_box_x = (rod_length - carriage_box_width) / 2
        carriage_box_y = -(carriage_box_length - motor_box_length) / 2
        carriage_box.translate(Vector(carriage_box_x, carriage_box_y, 0))

        # Define dimensions of idler side box
        idler_box_width = 55
        idler_box_length = 66
        idler_side_box_dimensions = (
            idler_box_width, idler_box_length, box_height)

        # Make idler
        idler_side_box = Part.makeBox(*idler_side_box_dimensions)
        idler_side_box.translate(Vector(rod_length - idler_box_width, 0, 0))

        space_between_rod_and_box_edge = 10
        half_box_height = box_height / 2

        rod1_y_position = idler_box_length - space_between_rod_and_box_edge

        rod1 = Part.makeCylinder(rod_radius, rod_length)
        rod1.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 90)
        rod1.translate(Vector(0, rod1_y_position, half_box_height))

        rod2_y_position = space_between_rod_and_box_edge
        rod2 = Part.makeCylinder(rod_radius, rod_length)
        rod2.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 90)
        rod2.translate(Vector(0, rod2_y_position, half_box_height))

        parts = [
            motor_side_box,
            chamfered_motor,
            carriage_box,
            idler_side_box,
            rod1,
            rod2
        ]

        reference_dimensions = (rod_length, motor_box_length, box_height)
        self.move_parts(parts, reference_dimensions)

        compound = Part.makeCompound(parts)
        obj.Shape = compound

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
