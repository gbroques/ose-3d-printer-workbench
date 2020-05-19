import Part
from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.app.shape import move_parts, place_shapes
from ose3dprinter.app.shape.edge import is_edge_parallel_to_z_axis
from ose3dprinter.app.three_dimensional_space_enums import CoordinateAxis, Side

class Axis:
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

    @classmethod
    def make(cls,
             rod_length,
             rod_radius,
             carriage_position,
             orientation,
             side,
             initial_placement,
             origin_translation_offset):
        # Define dimensions of motor side box
        motor_box_length = 66
        motor_side_box_dimensions = (
            cls.motor_box_width, motor_box_length, cls.box_height)

        # Make motor side box
        motor_side_box = Part.makeBox(*motor_side_box_dimensions)
        motor_side_box_with_holes = cls.cut_holes_in_motor_side_box(
            motor_side_box, cls.box_height, motor_box_length)

        # Motor
        motor_side = 37.8
        motor_height = 39.878
        motor_dimensions = (motor_side, motor_side, motor_height)

        # Make Motor
        motor = Part.makeBox(*motor_dimensions)
        half_motor_box_width = cls.motor_box_width / 2
        half_motor_box_length = motor_box_length / 2
        half_motor_side = motor_side / 2
        motor.translate(Vector(
            half_motor_box_width - half_motor_side,
            half_motor_box_length - half_motor_side,
            cls.box_height
        ))
        motor.rotate(Vector(half_motor_box_width,
                            half_motor_box_length, 0), Vector(0, 0, 1), 45)
        vertical_edges = list(
            filter(is_edge_parallel_to_z_axis, motor.Edges))
        chamfered_motor = motor.makeChamfer(5, vertical_edges)

        # Define dimensions of carriage box
        carriage_box_length = 74
        carriage_box_dimensions = (
            cls.carriage_box_width, carriage_box_length, cls.box_height)

        # Make carriage
        carriage_box = Part.makeBox(*carriage_box_dimensions)
        carriage_box_x = cls.calculate_carriage_box_x(
            rod_length, carriage_position)

        carriage_box_y = -(carriage_box_length - motor_box_length) / 2
        carriage_box.translate(Vector(carriage_box_x, carriage_box_y, 0))

        # Define dimensions of idler side box
        idler_side_box_dimensions = (
            cls.idler_box_width, cls.idler_box_length, cls.box_height)

        distance_between_hole_and_idler_side = (
            cls.idler_box_length - (cls.distance_between_holes + (cls.hole_radius * 2))) / 2
        front_cylinder = Part.makeCylinder(cls.hole_radius, cls.box_height)
        rear_cylinder = front_cylinder.copy()
        front_cylinder.translate(Vector(
            cls.idler_box_width / 2,
            distance_between_hole_and_idler_side,
            0
        ))
        rear_cylinder.translate(Vector(
            cls.idler_box_width / 2,
            cls.idler_box_length - distance_between_hole_and_idler_side,
            0
        ))

        # Make idler
        idler_side_box = Part.makeBox(*idler_side_box_dimensions)

        idler_side_box_with_front_hole = idler_side_box.cut(front_cylinder)
        idler_side_box_with_holes = idler_side_box_with_front_hole.cut(
            rear_cylinder)

        idler_side_box_with_holes.translate(
            Vector(rod_length - cls.idler_box_width, 0, 0))

        space_between_rod_and_box_edge = 10
        half_box_height = cls.box_height / 2

        rod1_y_position = cls.idler_box_length - space_between_rod_and_box_edge

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

        placement = get_placement(orientation,
                                  side,
                                  cls.box_height,
                                  rod_length,
                                  motor_box_length)
        place_shapes(parts, placement)

        reference_dimensions = (rod_length, motor_box_length, cls.box_height)
        move_parts(parts,
                   initial_placement,
                   origin_translation_offset,
                   reference_dimensions,
                   placement.Rotation)

        return Part.makeCompound(parts)

    @classmethod
    def cut_holes_in_motor_side_box(cls,
                                    motor_side_box,
                                    box_height,
                                    motor_box_length):
        front_right_cylinder = Part.makeCylinder(cls.hole_radius, box_height)
        rear_right_cylinder = front_right_cylinder.copy()
        front_left_cylinder = front_right_cylinder.copy()
        rear_left_cylinder = front_right_cylinder.copy()

        right_cylinder_x = cls.motor_box_width - \
            cls.distance_between_hole_and_inner_motor_side
        distance_from_hole_to_side = (
            motor_box_length - (cls.distance_between_holes + (cls.hole_radius * 2))) / 2
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
            (cls.x_distance_between_holes + (cls.hole_radius * 2))
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

    @classmethod
    def distance_between_inner_motor_side_holes_and_outer_edge(cls):
        return (
            cls.motor_box_width -
            cls.distance_between_hole_and_inner_motor_side
        )

    @classmethod
    def distance_between_idler_side_holes_and_outer_edge(cls):
        return cls.idler_box_width / 2

    @classmethod
    def calculate_carriage_box_x(cls, rod_length, carriage_position):
        available_rod_length = (
            rod_length -
            cls.motor_box_width -
            cls.idler_box_width)
        scale_factor = carriage_position / 100.0
        return (
            cls.motor_box_width +
            (
                (available_rod_length - cls.carriage_box_width) *
                scale_factor
            )
        )


def get_placement(orientation,
                  side,
                  box_height,
                  length,
                  motor_box_length):
    try:
        return {
            CoordinateAxis.X: {
                Side.TOP: Placement()
            },
            CoordinateAxis.Y: {
                Side.LEFT: Placement(
                    Vector(box_height, length, 0),
                    Rotation(-90, 0, 90)
                ),
                Side.RIGHT: Placement(
                    Vector(0, length, motor_box_length),
                    Rotation(-90, 0, -90)
                )
            },
            CoordinateAxis.Z: {
                Side.FRONT: Placement(
                    Vector(0, box_height, length),
                    Rotation(0, 90, 90)
                ),
                Side.REAR: Placement(
                    Vector(motor_box_length, 0, length),
                    Rotation(0, 90, -90)
                )
            }
        }[orientation][side]
    except KeyError:
        message = 'Invalid combination of orientation "{}" and side "{}" passed.'
        raise ValueError(message.format(orientation, side))
