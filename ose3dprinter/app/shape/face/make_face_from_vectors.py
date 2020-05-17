# TODO: Remove try / except import for zip
#       when we no longer need to support Python 2.7
try:
    from itertools import izip as zip
except ImportError:
    pass

from itertools import tee

import FreeCAD
import Part


def make_face_from_vectors(*vectors_list):
    """Make a Face from a variable number of vector lists.

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


def LineSegment(*args):
    """Call Part.Line or Part.LineSegment with args
    depending upon version of FreeCAD.

    In FreeCAD 0.16 Part.Line is used,
    for FreeCAD 0.17 Part.LineSegment has to be used.

    TODO: Should this be moved to a freecad_future module?

    .. seealso::
        https://www.freecadweb.org/wiki/Topological_data_scripting#Line

    :return: Part.Line or Part.LineSegment
    :rtype: Part.Line or Part.LineSegment
    """
    freecad_version = get_freecad_version()
    if freecad_version <= 16:
        return Part.Line(*args)
    else:
        return Part.LineSegment(*args)


def get_freecad_version():
    """Get FreeCAD Version as an integer.

    TODO: Should this be moved to a freecad_future module?

    :return: FreeCAD minor version (e.g. 16, 17, 18)
    :rtype: int
    """
    return int(FreeCAD.Version()[1])
