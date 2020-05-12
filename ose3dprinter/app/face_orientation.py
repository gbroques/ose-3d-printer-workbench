import Part
from FreeCAD import Console

from .enums import AxisOrientation, Plane, Side
from .get_outer_faces import (get_outer_faces_of_angled_bar,
                              get_outer_faces_of_cnc_cut_frame,
                              get_outer_faces_of_corner)
from .is_face_parallel_to_plane import (is_face_parallel_to_xy_plane,
                                        is_face_parallel_to_xz_plane,
                                        is_face_parallel_to_yz_plane)
from .model.frame.angle_frame_connector import AngleFrameConnector


def get_face_side(frame, face):
    attachable_axis_orientation = get_orientation_of_attachable_axis(face)
    if attachable_axis_orientation is None:
        return None
    if frame.HasCorners:
        return _get_face_side_for_frame_with_corners(frame,
                                                     face,
                                                     attachable_axis_orientation)
    else:
        return _get_face_side_for_cnc_cut_frame(frame,
                                                face,
                                                attachable_axis_orientation)


def get_orientation_of_attachable_axis(face):
    """
    Returns the orientation of which axis is attachable to the face.
    """
    d = _get_is_face_parallel_to_plane_by_axis_orientation()
    for axis_orientation, is_face_parallel_to_plane in d.items():
        if is_face_parallel_to_plane(face):
            return axis_orientation
    Console.PrintWarning('Face not parallel to XY, XZ, or YZ plane.\n')
    return None


def get_faces_by_side(cnc_cut_frame):
    """Gets a dictionary of outer faces of the frame by their Side.

    :param cnc_cut_frame: CNC Cut Frame (frame without corners)
    :type cnc_cut_frame: Document Object
    :return: Dictionary where the keys are a Side, and value is a Face
    :rtype: dict
    """
    faces_by_side = {}
    outer_faces = get_outer_faces_of_cnc_cut_frame(cnc_cut_frame)
    for outer_face in outer_faces:
        parallel_plane = _get_parallel_plane(outer_face)
        is_face_parallel_to_plane = _get_is_parallel_to_plane_predicate(
            parallel_plane)
        outer_faces_parallel_to_plane = filter(
            is_face_parallel_to_plane, outer_faces)
        perpendicular_axis_to_plane = _get_perpendicular_axis_to_plane(
            parallel_plane)
        sorted_faces_by_position = sorted(
            outer_faces_parallel_to_plane,
            key=lambda f: getattr(f.Surface.Position, perpendicular_axis_to_plane))
        side_index = 0 if sorted_faces_by_position[0].isEqual(
            outer_face) else 1
        ordered_sides_by_plane = {
            Plane.XY: [Side.BOTTOM, Side.TOP],
            Plane.YZ: [Side.LEFT, Side.RIGHT],
            Plane.XZ: [Side.FRONT, Side.REAR]
        }
        side = ordered_sides_by_plane[parallel_plane][side_index]
        faces_by_side[side] = outer_face

    return faces_by_side


def get_faces_within_bounds_of_side_for_frame_with_corners(frame_with_corners,
                                                           side):
    """TODO: Doesn't include outward faces of angle frame connector tabs

    :param frame_with_corners: Frame object with HasCorners property = True
    :type frame_with_corners: Document object
    :param side: Side of frame.
    :type side: See Side enum.
    :return: List of faces within bound of side for a frame with corners.
    :rtype: List[Part.Faces]
    """
    corners = _get_corners(frame_with_corners)
    outer_corner_faces = map(get_outer_faces_of_corner, corners)
    corner_faces = _flatten(outer_corner_faces)

    angled_bars = _get_angled_bars(frame_with_corners)
    outer_angle_bar_faces = map(get_outer_faces_of_angled_bar, angled_bars)
    angle_bar_faces = _flatten(outer_angle_bar_faces)

    faces = corner_faces + angle_bar_faces

    plane = _get_plane_from_side(side)
    is_face_parallel_to_plane = _get_is_parallel_to_plane_predicate(plane)
    angle_bar_faces_parallel_to_side = filter(
        is_face_parallel_to_plane, faces)

    faces_within_bound_of_side = filter(
        lambda f: _is_face_within_bounds_of_side(f, frame_with_corners, side),
        angle_bar_faces_parallel_to_side)
    return list(faces_within_bound_of_side)


def _get_face_side_for_frame_with_corners(frame_with_corners,
                                          face,
                                          attachable_axis_orientation):
    if not _is_face_planar_and_within_y_bounds(face, frame_with_corners):
        Console.PrintWarning(
            'Face is not planar or within Y bounds of frame.\n')
        return None
    plane = _get_plane_from_axis_orientation(attachable_axis_orientation)
    if plane == Plane.XY:
        if _between_top_bounds(face, frame_with_corners):
            return Side.TOP
    elif plane == Plane.YZ:
        if _between_left_bounds(face, frame_with_corners):
            return Side.LEFT
        if _between_right_bounds(face, frame_with_corners):
            return Side.RIGHT
    elif plane == Plane.XZ:
        if _between_front_bounds(face, frame_with_corners):
            return Side.FRONT
        if _between_rear_bounds(face, frame_with_corners):
            return Side.REAR
    else:
        Console.PrintWarning('{} is not a valid plane.\n'.format(plane))
        return None


def _is_face_within_bounds_of_side(face,
                                   frame_with_corners,
                                   side):
    if not _is_face_planar_and_within_y_bounds(face, frame_with_corners):
        return False

    plane = _get_plane_from_side(side)
    if plane == Plane.XY:
        if side == Side.TOP and _between_top_bounds(face, frame_with_corners):
            return True
    elif plane == Plane.YZ:
        if side == Side.LEFT and _between_left_bounds(face, frame_with_corners):
            return True
        if side == Side.RIGHT and _between_right_bounds(face, frame_with_corners):
            return True
    elif plane == Plane.XZ:
        if side == Side.FRONT and _between_front_bounds(face, frame_with_corners):
            return True
        if side == Side.REAR and _between_rear_bounds(face, frame_with_corners):
            return True
    else:
        return False


def _is_face_planar_and_within_y_bounds(face, frame_with_corners):
    # Exclude cylindrical surfaces and holes
    if not isinstance(face.Surface, Part.Plane):
        return False
    elif _isclose(face.BoundBox.YMax, frame_with_corners.Proxy.YMax):
        return True
    # Filter out back or inwards faces of angle frame connector tabs
    elif face.BoundBox.YMax > frame_with_corners.Proxy.YMax:
        return False
    # Filter out back or inwards faces of angle frame connector tabs
    elif face.BoundBox.YMin < frame_with_corners.Proxy.YMin:
        return False
    else:
        return True


def _between_top_bounds(face, frame_with_corners):
    value = face.Surface.Position.z

    upper_bound = frame_with_corners.Proxy.ZMax
    thickness = frame_with_corners.Thickness.Value

    lower_bound = upper_bound - thickness

    return _between_bounds(value, lower_bound, upper_bound)


def _between_left_bounds(face, frame_with_corners):
    value = face.Surface.Position.x

    lower_bound = frame_with_corners.Shape.BoundBox.XMin

    thickness = frame_with_corners.Thickness.Value
    upper_bound = lower_bound + thickness + \
        AngleFrameConnector.axis_side_mount_width

    return _between_bounds(value, lower_bound, upper_bound)


def _between_right_bounds(face, frame_with_corners):
    value = face.Surface.Position.x

    upper_bound = frame_with_corners.Shape.BoundBox.XMax

    thickness = frame_with_corners.Thickness.Value
    lower_bound = upper_bound - thickness - \
        AngleFrameConnector.axis_side_mount_width

    return _between_bounds(value, lower_bound, upper_bound)


def _between_front_bounds(face, frame_with_corners):
    value = face.Surface.Position.y

    lower_bound = frame_with_corners.Proxy.YMin

    thickness = frame_with_corners.Thickness.Value
    upper_bound = lower_bound + thickness

    return _between_bounds(value, lower_bound, upper_bound)


def _between_rear_bounds(face, frame_with_corners):
    value = face.Surface.Position.y
    upper_bound = frame_with_corners.Proxy.YMax

    thickness = frame_with_corners.Thickness.Value
    lower_bound = upper_bound - thickness
    return _between_bounds(value, lower_bound, upper_bound)


def _flatten(list_of_lists):
    return [val for sublist in list_of_lists for val in sublist]


def _get_corners(frame_with_corners):
    return filter(
        lambda s: _is_solid_corner(s, frame_with_corners),
        frame_with_corners.Shape.Solids)


def _get_angled_bars(frame_with_corners):
    return filter(
        lambda s: _is_solid_angled_bar(s, frame_with_corners),
        frame_with_corners.Shape.Solids)


def _is_solid_corner(solid, frame):
    return not _is_solid_angled_bar(solid, frame)


def _is_solid_angled_bar(solid, frame):
    return (
        _is_solid_top_or_bottom_angled_bar(solid, frame) or
        _is_solid_upright_angled_bar(solid, frame)
    )


def _is_solid_upright_angled_bar(solid, frame):
    bracket_length = AngleFrameConnector.calculate_bracket_length(
        frame.Width, frame.Thickness)
    lower_bound = frame.Shape.BoundBox.ZMin + bracket_length.Value
    upper_bound = frame.Shape.BoundBox.ZMax - bracket_length.Value

    return (
        _isclose(lower_bound, solid.BoundBox.ZMin) and
        _isclose(upper_bound, solid.BoundBox.ZMax)
    )


def _is_solid_top_or_bottom_angled_bar(solid, frame):
    frame_center = frame.Shape.BoundBox.Center
    solid_center = solid.CenterOfMass
    return (
        _isclose(frame_center.x, solid_center.x) or
        _isclose(frame_center.y, solid_center.y)
    )


def _get_plane_from_side(side):
    return {
        Side.BOTTOM: Plane.XY,
        Side.TOP: Plane.XY,
        Side.LEFT: Plane.YZ,
        Side.RIGHT: Plane.YZ,
        Side.FRONT: Plane.XZ,
        Side.REAR: Plane.XZ
    }[side]


def _get_is_parallel_to_plane_predicate(plane):
    return {
        Plane.XY: is_face_parallel_to_xy_plane,
        Plane.YZ: is_face_parallel_to_yz_plane,
        Plane.XZ: is_face_parallel_to_xz_plane
    }[plane]


def _get_is_face_parallel_to_plane_by_axis_orientation():
    return {
        AxisOrientation.X: is_face_parallel_to_xy_plane,
        AxisOrientation.Y: is_face_parallel_to_yz_plane,
        AxisOrientation.Z: is_face_parallel_to_xz_plane
    }


def _get_plane_from_axis_orientation(axis_orientation):
    return {
        AxisOrientation.X: Plane.XY,
        AxisOrientation.Y: Plane.YZ,
        AxisOrientation.Z: Plane.XZ
    }[axis_orientation]


def _get_sides_by_axis_orientation():
    return {
        AxisOrientation.X: (Side.BOTTOM, Side.TOP),
        AxisOrientation.Y: (Side.LEFT, Side.RIGHT),
        AxisOrientation.Z: (Side.FRONT, Side.REAR)
    }


def _get_face_side_for_cnc_cut_frame(cnc_cut_frame,
                                     face,
                                     attachable_axis_orientation):
    attachable_axis_orientation = get_orientation_of_attachable_axis(face)
    if attachable_axis_orientation is None:
        return None
    sides_by_axis_orientation = _get_sides_by_axis_orientation()
    lower_side, upper_side = sides_by_axis_orientation[attachable_axis_orientation]
    face_closest_to_origin = _get_face_closest_to_origin(
        cnc_cut_frame, attachable_axis_orientation)
    if face.isEqual(face_closest_to_origin):
        return lower_side
    else:
        return upper_side


def _get_is_face_parallel_to_plane(axis_orientation):
    d = _get_is_face_parallel_to_plane_by_axis_orientation()
    return d[axis_orientation]


def _get_face_closest_to_origin(cnc_cut_frame, axis_orientation):
    """
    Get the face closest to the origin based on axis orientation.

    For example, if the axis orientation is x,
    then the face closest to the origin is the bottom face.
    """
    is_face_parallel_to_plane = _get_is_face_parallel_to_plane(
        axis_orientation)

    outer_faces = get_outer_faces_of_cnc_cut_frame(cnc_cut_frame)

    outer_faces_parallel_to_plane = filter(
        is_face_parallel_to_plane, outer_faces)
    sorted_faces_by_position = _sort_faces_by_surface_position(
        outer_faces_parallel_to_plane, axis_orientation)
    return sorted_faces_by_position[0]


def _sort_faces_by_surface_position(faces, axis_orientation):
    """
    If orientation of axis is x, then sort faces by z
    If orientation of axis is y, then sort faces by x
    If orientation of axis is z, then sort faces by y
    """
    axis_orientation_index = [
        AxisOrientation.X,
        AxisOrientation.Y,
        AxisOrientation.Z
    ].index(axis_orientation)
    position_index = ((axis_orientation_index - 1) + 3) % 3
    return sorted(faces, key=lambda f: f.Surface.Position[position_index])


def _between_bounds(value, lower_bound, upper_bound):
    is_between_bounds = lower_bound < value < upper_bound
    return (
        _isclose(value, lower_bound) or
        is_between_bounds or
        _isclose(value, upper_bound)
    )


def _isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """
    TODO: Replace with math.isclose in python 3.5
    Sources:
        https://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
        https://docs.python.org/3/whatsnew/3.5.html#pep-485-a-function-for-testing-approximate-equality
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def _get_parallel_plane(face):
    """
    Returns which plane the face is parallel to
    """
    if is_face_parallel_to_xy_plane(face):
        return Plane.XY
    elif is_face_parallel_to_yz_plane(face):
        return Plane.YZ
    elif is_face_parallel_to_xz_plane(face):
        return Plane.XZ
    else:
        raise ValueError('Face must be parallel to XY, YZ, or XZ plane.')


def _get_perpendicular_axis_to_plane(plane):
    return {
        Plane.XY: 'z',
        Plane.YZ: 'x',
        Plane.XZ: 'y'
    }[plane]
