import Part
from FreeCAD import Vector


class AngleFrameConnector:
    """
    Encapsulates the data (i.e. topography and shape)
    for an Angle Frame Connector,
    and is separate from the "view" or GUI representation.

    An angle frame connector is made up of three brackets.
    """

    @staticmethod
    def make():
        bracket_length = 46.99
        bracket_width = 10.16
        bracket_height = 38.1
        # forms the outer-most corner of bracket
        bracket_outer_edge_thickness = 4.21
        bracket_inner_edge_thickness = 2.61647
        # forms the outer edges of bracket
        bracket_end_thickness = 3.41

        angle_connector_corner = make_angle_connector_corner(
            bracket_length, bracket_width)

        tri_bracket = make_tri_bracket(
            bracket_length,
            bracket_width,
            bracket_height,
            bracket_outer_edge_thickness,
            bracket_inner_edge_thickness,
            bracket_end_thickness)

        # Top tri-bracket
        top_bracket = tri_bracket.copy()
        top_bracket.translate(Vector(0, 0, bracket_length))

        # Right tri-bracket
        right_bracket = tri_bracket.copy()
        right_bracket.rotate(Vector(0, 0, 0), Vector(0, -1, 0), 90)
        x_translation = (bracket_length * 2) - bracket_width
        right_bracket.translate(Vector(x_translation, 0, 0))

        # Rear tri-bracket
        rear_bracket = tri_bracket.copy()
        rear_bracket.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 90)
        y_translation = (bracket_length * 2) - bracket_width
        rear_bracket.translate(Vector(0, y_translation, 0))

        parts = [
            angle_connector_corner, top_bracket, right_bracket, rear_bracket
        ]

        angle_frame_connector = reduce(
            lambda union, part: union.fuse(part), parts)

        # removeSplitter() refines shape
        return angle_frame_connector.removeSplitter()


def make_tri_bracket(length,
                     width,
                     height,
                     outer_edge_thickness,
                     inner_edge_thickness,
                     end_thickness):
    outer_most_edge = make_outer_most_edge_of_tri_bracket(
        length,
        width,
        height,
        outer_edge_thickness,
        end_thickness)
    inner_most_edge = make_inner_most_edge_of_tri_bracket(
        length,
        width,
        height,
        inner_edge_thickness,
        end_thickness)
    return outer_most_edge.fuse(inner_most_edge)


def make_outer_most_edge_of_tri_bracket(length,
                                        width,
                                        height,
                                        outer_edge_thickness,
                                        end_thickness):
    box = Part.makeBox(length, length, height)
    inner_box_dimension = length - outer_edge_thickness - end_thickness
    inner_box = Part.makeBox(
        inner_box_dimension, inner_box_dimension, height)
    inner_box.translate(Vector(
        outer_edge_thickness, outer_edge_thickness, 0))

    subtraction_box = Part.makeBox(length, length, height)
    subtraction_box.translate(Vector(width, width, 0))

    return box.cut(inner_box).cut(subtraction_box)


def make_inner_most_edge_of_tri_bracket(length,
                                        width,
                                        height,
                                        inner_edge_thickness,
                                        end_thickness):
    inner_most_edge_offset = width - inner_edge_thickness
    box_dimension = length - inner_most_edge_offset
    box = Part.makeBox(box_dimension, box_dimension, height)
    box.translate(
        Vector(inner_most_edge_offset, inner_most_edge_offset, 0))

    subtraction_box = Part.makeBox(length, length, height)
    subtraction_box.translate(Vector(width, width, 0))

    return box.cut(subtraction_box)


def make_angle_connector_corner(bracket_length, bracket_width):
    box = Part.makeBox(bracket_length, bracket_length, bracket_length)

    inner_box = box.copy()
    inner_box.translate(Vector(bracket_width, bracket_width, bracket_width))

    return box.cut(inner_box)
