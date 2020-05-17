from math import degrees

import Part
from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.app.three_dimensional_space_enums import Axis, Side
from ose3dprinter.app.model.base_model import BaseModel
from ose3dprinter.app.shape.edge import is_edge_parallel_to_z_axis


class AxisModel(BaseModel):
    """
    Encapsulates the data (i.e. topography and shape) for a Axis,
    and is separate from the "view" or GUI representation.
    """

    Type = 'OSEAxis'

    motor_box_width = 59.5

    carriage_box_width = 52

    idler_box_width = 26
    idler_box_length = 66

    # Motor side, idler side, and carriage boxes share same height
    box_height = 24

    hole_radius = 3.39

    # y_distance_between_holes
    distance_between_holes = 22.44
    x_distance_between_holes = 23.36
    distance_between_hole_and_inner_motor_side = hole_radius + 9.2

    def __init__(self,
                 obj,
                 length=304.80,
                 carriage_position=50,
                 orientation=Axis.X,
                 side=Side.TOP,
                 placement=Placement(),
                 origin_translation_offset=Vector()):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        init_args = (obj, placement, origin_translation_offset)
        super(AxisModel, self).__init__(*init_args)

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

        # Carriage Position property
        carriage_position_tooltip = 'Position of carriage relative to available rod.'
        obj.addProperty('App::PropertyPercent', 'CarriagePosition',
                        'Base', carriage_position_tooltip)
        obj.CarriagePosition = carriage_position

        # Orientation property
        orientation_tooltip = 'Orientation of axis: X, Y, or Z.'
        hidden = 4
        obj.addProperty('App::PropertyString', 'Orientation',
                        'Base', orientation_tooltip, hidden)
        obj.Orientation = orientation

        # Side property
        side_tooltip = 'Which side the bottom of the axis faces.'
        obj.addProperty('App::PropertyString', 'Side',
                        'Base', side_tooltip, hidden)
        obj.Side = side

    def execute(self, obj):
        """
        Called on document recompute
        """
        # Get rod dimensions
        rod_length = obj.Length.Value
        rod_radius = obj.RodDiameter.Value / 2

        # Define dimensions of motor side box
        motor_box_length = 66
        motor_side_box_dimensions = (
            self.motor_box_width, motor_box_length, self.box_height)

        # Make motor side box
        motor_side_box = Part.makeBox(*motor_side_box_dimensions)
        motor_side_box_with_holes = self.cut_holes_in_motor_side_box(
            motor_side_box, self.box_height, motor_box_length)

        # Motor
        motor_side = 37.8
        motor_height = 39.878
        motor_dimensions = (motor_side, motor_side, motor_height)

        # Make Motor
        motor = Part.makeBox(*motor_dimensions)
        half_motor_box_width = self.motor_box_width / 2
        half_motor_box_length = motor_box_length / 2
        half_motor_side = motor_side / 2
        motor.translate(Vector(
            half_motor_box_width - half_motor_side,
            half_motor_box_length - half_motor_side,
            self.box_height
        ))
        motor.rotate(Vector(half_motor_box_width,
                            half_motor_box_length, 0), Vector(0, 0, 1), 45)
        vertical_edges = list(
            filter(is_edge_parallel_to_z_axis, motor.Edges))
        chamfered_motor = motor.makeChamfer(5, vertical_edges)

        # Define dimensions of carriage box
        carriage_box_length = 74
        carriage_box_dimensions = (
            self.carriage_box_width, carriage_box_length, self.box_height)

        # Make carriage
        carriage_box = Part.makeBox(*carriage_box_dimensions)
        carriage_box_x = self.calculate_carriage_box_x()

        carriage_box_y = -(carriage_box_length - motor_box_length) / 2
        carriage_box.translate(Vector(carriage_box_x, carriage_box_y, 0))

        # Define dimensions of idler side box
        self.idler_box_length = 66
        idler_side_box_dimensions = (
            self.idler_box_width, self.idler_box_length, self.box_height)

        distance_between_hole_and_idler_side = (
            self.idler_box_length - (self.distance_between_holes + (self.hole_radius * 2))) / 2
        front_cylinder = Part.makeCylinder(self.hole_radius, self.box_height)
        rear_cylinder = front_cylinder.copy()
        front_cylinder.translate(Vector(
            self.idler_box_width / 2,
            distance_between_hole_and_idler_side,
            0
        ))
        rear_cylinder.translate(Vector(
            self.idler_box_width / 2,
            self.idler_box_length - distance_between_hole_and_idler_side,
            0
        ))

        # Make idler
        idler_side_box = Part.makeBox(*idler_side_box_dimensions)

        idler_side_box_with_front_hole = idler_side_box.cut(front_cylinder)
        idler_side_box_with_holes = idler_side_box_with_front_hole.cut(
            rear_cylinder)

        idler_side_box_with_holes.translate(
            Vector(rod_length - self.idler_box_width, 0, 0))

        space_between_rod_and_box_edge = 10
        half_box_height = self.box_height / 2

        rod1_y_position = self.idler_box_length - space_between_rod_and_box_edge

        rod1 = Part.makeCylinder(rod_radius, rod_length)
        rod1.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 90)
        rod1.translate(Vector(0, rod1_y_position, half_box_height))

        rod2_y_position = space_between_rod_and_box_edge
        rod2 = Part.makeCylinder(rod_radius, rod_length)
        rod2.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 90)
        rod2.translate(Vector(0, rod2_y_position, half_box_height))

        parts = [
            motor_side_box_with_holes,
            chamfered_motor,
            carriage_box,
            idler_side_box_with_holes,
            rod1,
            rod2
        ]

        placement_strategy = get_placement_strategy(obj.Orientation,
                                                    obj.Side,
                                                    self.box_height,
                                                    rod_length,
                                                    motor_box_length)
        rotation = placement_strategy['rotation']
        translation = placement_strategy['translation']
        for part in parts:
            part.rotate(Vector(), rotation.Axis, degrees(rotation.Angle))
            part.translate(translation)

        reference_dimensions = (rod_length, motor_box_length, self.box_height)
        self.move_parts(parts, reference_dimensions, rotation)

        compound = Part.makeCompound(parts)
        obj.Shape = compound

    def cut_holes_in_motor_side_box(self,
                                    motor_side_box,
                                    box_height,
                                    motor_box_length):
        front_right_cylinder = Part.makeCylinder(self.hole_radius, box_height)
        rear_right_cylinder = front_right_cylinder.copy()
        front_left_cylinder = front_right_cylinder.copy()
        rear_left_cylinder = front_right_cylinder.copy()

        right_cylinder_x = self.motor_box_width - \
            self.distance_between_hole_and_inner_motor_side
        distance_from_hole_to_side = (
            motor_box_length - (self.distance_between_holes + (self.hole_radius * 2))) / 2
        front_right_cylinder.translate(Vector(
            right_cylinder_x,
            distance_from_hole_to_side,
            0
        ))
        rear_right_cylinder.translate(Vector(
            right_cylinder_x,
            motor_box_length - distance_from_hole_to_side,
            0
        ))

        left_cylinder_x = right_cylinder_x - \
            (self.x_distance_between_holes + (self.hole_radius * 2))
        front_left_cylinder.translate(Vector(
            left_cylinder_x,
            distance_from_hole_to_side,
            0
        ))
        rear_left_cylinder.translate(Vector(
            left_cylinder_x,
            motor_box_length - distance_from_hole_to_side,
            0
        ))

        motor_side_box = motor_side_box.cut(front_right_cylinder)
        motor_side_box = motor_side_box.cut(rear_right_cylinder)
        motor_side_box = motor_side_box.cut(front_left_cylinder)
        motor_side_box_with_holes = motor_side_box.cut(rear_left_cylinder)
        return motor_side_box_with_holes

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state

    @classmethod
    def distance_between_inner_motor_side_holes_and_outer_edge(cls):
        return (
            cls.motor_box_width -
            cls.distance_between_hole_and_inner_motor_side
        )

    @classmethod
    def distance_between_idler_side_holes_and_outer_edge(cls):
        return cls.idler_box_width / 2

    def calculate_carriage_box_x(self):
        obj = self.Object
        rod_length = obj.Length.Value
        carriage_position = obj.CarriagePosition

        available_rod_length = (
            rod_length -
            self.motor_box_width -
            self.idler_box_width)
        scale_factor = carriage_position / 100.0
        return (
            self.motor_box_width +
            (
                (available_rod_length - self.carriage_box_width) *
                scale_factor
            )
        )

    def is_x(self):
        """Return whether or not this axis is a X axis.

        This assumes the axis is parallel to the XY, YZ, or XZ planes,
        and not rotated in a weird diagonal or skewed way.

        :return: Whether this axis is a X axis.
        :rtype: bool
        """
        axis = self.Object
        return _is_oriented_in(axis, Axis.X)

    def is_y(self):
        """Return whether or not this axis is a Y axis.

        This assumes the axis is parallel to the XY, YZ, or XZ planes,
        and not rotated in a weird diagonal or skewed way.

        :return: Whether this axis is a Y axis.
        :rtype: bool
        """
        axis = self.Object
        return _is_oriented_in(axis, Axis.Y)

    def is_z(self):
        """Return whether or not this axis is a Z axis.

        This assumes the axis is parallel to the XY, YZ, or XZ planes,
        and not rotated in a weird diagonal or skewed way.

        :return: Whether this axis is a Z axis.
        :rtype: bool
        """
        axis = self.Object
        return _is_oriented_in(axis, Axis.Z)

    def calculate_top_of_carriage_box_for_z_axis(self):
        return (
            self.Object.Shape.BoundBox.ZMin +
            (
                self.Object.Length.Value -
                self.calculate_carriage_box_x()
            )
        )


def _is_oriented_in(axis, axis_orientation):
    bound_box = axis.Shape.BoundBox
    lengths = [
        bound_box.XLength,
        bound_box.YLength,
        bound_box.ZLength
    ]
    max_length = max(lengths)
    length_property = _get_length_property(axis_orientation)
    return max_length == getattr(bound_box, length_property)


def _get_length_property(axis_orientation):
    return {
        Axis.X: 'XLength',
        Axis.Y: 'YLength',
        Axis.Z: 'ZLength',
    }[axis_orientation]


def get_placement_strategy(orientation,
                           side,
                           box_height,
                           length,
                           motor_box_length):
    try:
        return {
            Axis.X: {
                Side.TOP: {
                    'rotation': Rotation(),
                    'translation': Vector()
                }
            },
            Axis.Y: {
                Side.LEFT: {
                    'rotation': Rotation(-90, 0, 90),
                    'translation': Vector(box_height, length, 0)
                },
                Side.RIGHT: {
                    'rotation': Rotation(-90, 0, -90),
                    'translation': Vector(0, length, motor_box_length)
                }
            },
            Axis.Z: {
                Side.FRONT: {
                    'rotation': Rotation(0, 90, 90),
                    'translation': Vector(0, box_height, length)
                },
                Side.REAR: {
                    'rotation': Rotation(0, 90, -90),
                    'translation': Vector(motor_box_length, 0, length)
                }
            }
        }[orientation][side]
    except KeyError:
        message = 'Invalid combination of orientation "{}" and side "{}" passed.'
        raise ValueError(message.format(orientation, side))
