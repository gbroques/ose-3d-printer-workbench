# TODO: Remove try / except import for zip
#       when we no longer need to support Python 2.7
try:
    from itertools import izip as zip
except ImportError:
    pass

from itertools import tee

import Part
from osecore.app.future.freecad import LineSegment


def make_face_from_vectors(*vectors_list):
    """Make a Face from a variable number of vector lists.

    See Part::TopoShapeFacePy Class Reference:
        https://www.freecadweb.org/api/d9/d35/classPart_1_1TopoShapeFacePy.html

    :raises ValueError: When there's less than three vectors in a list.
    :raises ValueError: When vectors don't form a closed wire.
    :return: A face
    :rtype: Part.Face
    """
    wires = []
    for vectors in vectors_list:
        if len(vectors) < 3:
            raise ValueError('Must have at least 3 vectors to make a face.')
        vertices = vectors + [vectors[0]]
        edges = []
        for pair in _pair_wise(vertices):
            edge = LineSegment(*pair)
            edges.append(edge)

        shape = Part.Shape(edges)
        wire = Part.Wire(shape.Edges)
        wires.append(wire)
        if not wire.isClosed():
            raise ValueError('Vectors must form closed face.')
    return Part.Face(wires)


def _pair_wise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
