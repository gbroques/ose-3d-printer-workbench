"""Exposes functions for the following topological data types or "shapes":
    * Compound - A group of any type of topological object.
    * Compsolid - A composite solid is a set of solids,
                  connected by their faces.
                  It expands the notions of WIRE and SHELL to solids.
    * Solid - A part of space limited by shells. It is three dimensional.
    * Shell - A set of faces connected by their edges.
              A shell can be open or closed.
    * Face - In 2D it is part of a plane; in 3D it is part of a surface.
             Its geometry is constrained (trimmed) by contours.
             It is two dimensional.
    * Wire - A set of edges connected by their vertices.
             It can be an open or closed contour,
             depending on whether the edges are linked or not.
    * Edge - A topological element corresponding to a restrained curve.
             An edge is generally limited by vertices.
             It has one dimension.
    * Vertex - A topological element corresponding to a point.
               It has zero dimension.

Shape is  generic term covering all of the above.

See Also:
    https://wiki.freecadweb.org/Topological_data_scripting
"""
from .place_shape import place_shape, place_shapes
from .move_parts import move_parts
