from math import degrees

import Part
from FreeCAD import Console, Vector
from ose3dprinter.app.is_edge_parallel_to_axis import (
    is_edge_parallel_to_x_axis, is_edge_parallel_to_y_axis,
    is_edge_parallel_to_z_axis)


class BaseModel(object):
    """
    Base class for models that encapsulate the data (i.e. topography and shape)
    for a part, and is separate from the "view" or GUI representation.
    """

    def __init__(self, placement, origin_translation_offset):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        self.placement = placement
        self.origin_translation_offset = origin_translation_offset

    def move_parts(self, parts, reference_dimensions):
        base = self.placement.Base
        rotation = self.placement.Rotation

        translation_offset = get_translation_offset(
            reference_dimensions, rotation, self.origin_translation_offset)
        origin = base - translation_offset
        for part in parts:
            part.translate(origin)
            part.rotate(origin, rotation.Axis, degrees(rotation.Angle))

    def move_part(self, part, reference_dimensions):
        base = self.placement.Base
        rotation = self.placement.Rotation

        translation_offset = get_translation_offset(
            reference_dimensions, rotation, self.origin_translation_offset)
        origin = base - translation_offset

        part.translate(origin)
        part.rotate(origin, rotation.Axis, degrees(rotation.Angle))


def get_translation_offset(reference_dimensions,
                           rotation,
                           origin_translation_offset):
    reference_box = Part.makeBox(*reference_dimensions)
    reference_box.rotate(Vector(0, 0, 0), rotation.Axis,
                         degrees(rotation.Angle))
    first_vertex = reference_box.Vertexes[0]
    first_vertex_edges = get_edges_connected_to_vertex(
        first_vertex, reference_box.Edges)
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


def get_edges_connected_to_vertex(vertex, edges):
    vertex_edges = []
    for e in edges:
        for v in e.Vertexes:
            if v.isSame(vertex):
                vertex_edges.append(e)
    return vertex_edges
