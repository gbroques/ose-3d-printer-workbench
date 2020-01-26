import Part
from FreeCAD import Base


class UniversalAxisModel:
    """
    Encapsulates the data (i.e. topography and shape) for a Universal Axis,
    and is separate from the "view" or GUI representation.
    """

    def __init__(self, obj):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        self.Type = 'OSEUniversalAxis'

        obj.Proxy = self

        # Length property
        length_tooltip = 'Length of axis corresponds to rod length.'
        obj.addProperty('App::PropertyLength', 'Length', 'Base', length_tooltip)
        obj.Length = 304.80

        # Rod Diameter property
        rod_diameter_tooltip = 'Diameter of rod.'
        read_only = 1
        obj.addProperty('App::PropertyLength', 'RodDiameter', 'Base', rod_diameter_tooltip, read_only)
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
        motor_side_box_dimensions = (motor_box_width, motor_box_length, box_height)

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
        motor.translate(Base.Vector(
            half_motor_box_width - half_motor_side,
            half_motor_box_length - half_motor_side,
            box_height
        ))
        motor.rotate(Base.Vector(half_motor_box_width, half_motor_box_length, 0), Base.Vector(0, 0, 1), 45)
        vertical_edges = list(filter(is_cube_edge_oriented_in_z_plane, motor.Edges))
        chamfered_motor = motor.makeChamfer(5, vertical_edges)

        # Define dimensions of idler side box
        idler_box_width = 55
        idler_box_length = 66
        idler_side_box_dimensions = (idler_box_width, idler_box_length, box_height)

        # Make idler
        idler_side_box = Part.makeBox(*idler_side_box_dimensions)
        idler_side_box.translate(Base.Vector(rod_length - idler_box_width, 0, 0))

        space_between_rod_and_box_edge = 10
        half_box_height = box_height / 2

        rod1_y_position = idler_box_length - space_between_rod_and_box_edge

        rod1 = Part.makeCylinder(rod_radius, rod_length)
        rod1.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
        rod1.translate(Base.Vector(0, rod1_y_position, half_box_height))

        rod2_y_position = space_between_rod_and_box_edge
        rod2 = Part.makeCylinder(rod_radius, rod_length)
        rod2.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
        rod2.translate(Base.Vector(0, rod2_y_position, half_box_height))

        obj.Shape = Part.makeCompound([
            motor_side_box,
            chamfered_motor,
            idler_side_box,
            rod1,
            rod2
        ])

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state


def is_cube_edge_oriented_in_z_plane(edge):
    first_point = edge.valueAt(edge.FirstParameter)
    x1 = first_point.x
    y1 = first_point.y

    last_point = edge.valueAt(edge.LastParameter)
    x2 = last_point.x
    y2 = last_point.y

    return x1 == x2 and y1 == y2
