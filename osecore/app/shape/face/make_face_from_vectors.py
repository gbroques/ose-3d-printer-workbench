from itertools import tee

import Part


def make_face_from_vectors(vectors):
    """Make a Face from list of vectors.

    See Part::TopoShapeFacePy Class Reference:
        https://www.freecadweb.org/api/d9/d35/classPart_1_1TopoShapeFacePy.html

    :raises ValueError: When there's less than three vectors in a list.
    :raises ValueError: When vectors don't form a closed wire.
    :return: A face
    :rtype: Part.Face
    """
    if len(vectors) < 3:
        raise ValueError('Must have at least 3 vectors to make a face.')
    vertices = vectors + [vectors[0]]
    edges = []
    for pair in _pair_wise(vertices):
        edge = Part.LineSegment(*pair)
        edges.append(edge)

    shape = Part.Shape(edges)
    wire = Part.Wire(shape.Edges)
    if not wire.isClosed():
        raise ValueError('Vectors must form closed face.')
    return Part.Face(wire)


def _pair_wise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
