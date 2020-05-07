from math import degrees

import Part
from FreeCAD import Console, Vector, Rotation
from ose3dprinter.app.is_edge_parallel_to_axis import (
    is_edge_parallel_to_x_axis, is_edge_parallel_to_y_axis,
    is_edge_parallel_to_z_axis)


class BaseModel(object):
    """
    Base class for models that encapsulate the data (i.e. topography and shape)
    for a part, and is separate from the "view" or GUI representation.
    """

    def __init__(self, obj, placement, origin_translation_offset):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        obj.Proxy = self

        self.Object = obj
        self.placement = placement
        self.origin_translation_offset = origin_translation_offset

    def onDocumentRestored(self, fp):
        """Executed after a document is restored,
        or a FeaturePython object is copied or duplicated.

        :param fp: Custom feature python object
        :type fp: Part::FeaturePython
        """
        self.Object = fp

    def move_parts(self, parts, reference_dimensions, rotation=Rotation()):
        translation_offset = get_translation_offset(
            reference_dimensions, rotation, self.origin_translation_offset)
        for part in parts:
            part.translate(translation_offset)
            placement_rotation = self.placement.Rotation
            part.rotate(translation_offset, placement_rotation.Axis,
                        degrees(placement_rotation.Angle))
            part.translate(self.placement.Base)


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


def get_edges_connected_to_vertex(vertex, edges):
    vertex_edges = []
    for e in edges:
        for v in e.Vertexes:
            if v.isSame(vertex):
                vertex_edges.append(e)
    return vertex_edges
