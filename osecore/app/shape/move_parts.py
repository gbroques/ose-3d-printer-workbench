from math import degrees

import Part
from FreeCAD import Console, Rotation, Vector
from osecore.app.shape.edge import (find_edges_connected_to_vertex,
                                    is_edge_parallel_to_x_axis,
                                    is_edge_parallel_to_y_axis,
                                    is_edge_parallel_to_z_axis)


def move_parts(parts,
               placement,
               origin_translation_offset,
               reference_dimensions,
               rotation=Rotation()):
    translation_offset = _get_translation_offset(
        reference_dimensions, rotation, origin_translation_offset)
    for part in parts:
        part.translate(translation_offset)
        placement_rotation = placement.Rotation
        part.rotate(translation_offset, placement_rotation.Axis,
                    degrees(placement_rotation.Angle))
        part.translate(placement.Base)


def _get_translation_offset(reference_dimensions,
                            rotation,
                            origin_translation_offset):
    reference_box = Part.makeBox(*reference_dimensions)
    reference_box.rotate(Vector(0, 0, 0), rotation.Axis,
                         degrees(rotation.Angle))
    first_vertex = reference_box.Vertexes[0]
    first_vertex_edges = find_edges_connected_to_vertex(
        first_vertex, reference_box.Edges)
    num_edges = len(first_vertex_edges)
    if num_edges != 3:
        message = 'Found {} edges'.format(num_edges)
        message += ' connected to cube vertex instead of 3.\n'
        Console.PrintWarning(message)
    x = y = z = 1.0
    for e in first_vertex_edges:
        if is_edge_parallel_to_x_axis(e):
            x = e.Length
        elif is_edge_parallel_to_y_axis(e):
            y = e.Length
        elif is_edge_parallel_to_z_axis(e):
            z = e.Length
        else:
            def round_vec(v):
                return Vector(round(v.x), round(v.y), round(v.z))
            Console.PrintWarning(
                'Edge: {} not parallel to x, y, or z axes\n'.format(
                    [round_vec(v.Point) for v in e.Vertexes]))

    return Vector(
        x * origin_translation_offset.x,
        y * origin_translation_offset.y,
        z * origin_translation_offset.z
    )
