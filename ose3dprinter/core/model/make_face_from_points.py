# TODO: Remove when we no longer need to support Python 2.7
try:
    from itertools import izip as zip
except ImportError:
    pass

from itertools import tee

import FreeCAD
import Part


def make_face_from_points(*points_list):
    wires = []
    for points in points_list:
        if len(points) < 3:
            raise ValueError('Must have at least 3 points to make a face.')
        vertices = points + [points[0]]
        edges = []
        for pair in pair_wise(vertices):
            edge = LineSegment(*pair)
            edges.append(edge)

        shape = Part.Shape(edges)
        wire = Part.Wire(shape.Edges)
        wires.append(wire)
        if not wire.isClosed():
            raise ValueError('Points must form closed face.')
    return Part.Face(wires)


def pair_wise(iterable):
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

    :return: FreeCAD minor version (e.g. 16, 17, 18)
    :rtype: int
    """
    return int(FreeCAD.Version()[1])
