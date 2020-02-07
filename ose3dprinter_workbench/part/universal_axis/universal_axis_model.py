from math import degrees

import Part
from FreeCAD import Vector, Console, Matrix


class UniversalAxisModel:
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
        self.Type = 'OSEUniversalAxis'
        self.placement = placement
        self.origin_translation_offset = origin_translation_offset

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

        base = self.placement.Base
        rotation = self.placement.Rotation

        reference_dimensions = (rod_length, motor_box_length, box_height)
        translation_offset = get_translation_offset(
            reference_dimensions, rotation, self.origin_translation_offset)
        origin = base - translation_offset
        for part in parts:
            part.translate(origin)
            part.rotate(origin, rotation.Axis, degrees(rotation.Angle))
        compound = Part.makeCompound(parts)
        obj.Shape = compound

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state


def is_edge_parallel_to_x_axis(edge):
    return is_edge_parallel_to_axis(edge, 'x')


def is_edge_parallel_to_y_axis(edge):
    return is_edge_parallel_to_axis(edge, 'y')


def is_edge_parallel_to_z_axis(edge):
    return is_edge_parallel_to_axis(edge, 'z')


def is_edge_parallel_to_axis(edge, axis):
    index_by_axis = {'x': 0, 'y': 1, 'z': 2}
    opposite_orientations = filter(
        lambda item: item[0] != axis, index_by_axis.items())
    a_index, b_index = map(lambda item: item[1], opposite_orientations)
    first_point = edge.valueAt(edge.FirstParameter)
    a1 = round(first_point[a_index])
    b1 = round(first_point[b_index])

    last_point = edge.valueAt(edge.LastParameter)
    a2 = round(last_point[a_index])
    b2 = round(last_point[b_index])

    return a1 == a2 and b1 == b2


def get_vertex_edges(vertex, edges):
    vertex_edges = []
    for e in edges:
        for v in e.Vertexes:
            if v.isSame(vertex):
                vertex_edges.append(e)
    return vertex_edges


def get_translation_offset(reference_dimensions,
                           rotation,
                           origin_translation_offset):
    reference_box = Part.makeBox(*reference_dimensions)
    reference_box.rotate(Vector(0, 0, 0), rotation.Axis,
                         degrees(rotation.Angle))
    first_vertex = reference_box.Vertexes[0]
    first_vertex_edges = get_vertex_edges(first_vertex, reference_box.Edges)
    num_edges = len(first_vertex_edges)
    if num_edges != 3:
        Console.PrintWarning(
            'Found {} edges connected to cube vertex instead of 3.\n'.format(num_edges))
    x = y = z = 1.0
    for e in first_vertex_edges:
        if is_edge_parallel_to_x_axis(e):
            x = e.Length
        elif is_edge_parallel_to_y_axis(e):
            y = e.Length
        elif is_edge_parallel_to_z_axis(e):
            z = e.Length
        else:
            Console.PrintWarning(
                '{} not parallel to x, y, or z axes\n'.format(e))

    return Vector(
        x * origin_translation_offset.x,
        y * origin_translation_offset.y,
        z * origin_translation_offset.z
    )
