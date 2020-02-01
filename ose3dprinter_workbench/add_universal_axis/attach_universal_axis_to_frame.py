import FreeCADGui as Gui
from FreeCAD import Console, Vector
from Part import Face

from .get_placement_strategy import get_placement_strategy


def attach_universal_axis_to_frame():
    selection = Gui.Selection.getSelectionEx()
    frame, face = validate_potential_frame_face_selection(selection)
    if frame is None and face is None:
        return {}
    if is_frame_rotated(frame):
        Console.PrintWarning(
            'Attaching axis to rotated frame is not supported.\n')
        return {}
    return get_kwargs(frame, face)


def validate_potential_frame_face_selection(selection):
    """Validates a potential selection is a face of a frame.

    Returns frame and selected face,
    or None tuple if no face is selected.
    """
    none_tuple = None, None
    if len(selection) != 1:
        Console.PrintMessage(
            'Didn\'t select 1 element. Skipping attachment.\n')
        return none_tuple
    first_selection = selection[0]
    if len(first_selection.SubObjects) != 1:
        Console.PrintMessage(
            'Selected object doesn\'t have a single sub object. Skipping attachment.\n')
        return none_tuple
    first_sub_object = first_selection.SubObjects[0]
    if not isinstance(first_sub_object, Face):
        Console.PrintMessage(
            'Selected element is not a face. Skipping attachment.\n')
        return none_tuple
    frame = first_selection.Object
    if frame.Proxy.Type != 'OSEFrame':
        Console.PrintMessage('Must select frame. Skipping attachment.\n')
        return none_tuple
    outer_faces = get_outer_faces_of_frame(frame)
    if not any(map(lambda f: f.isEqual(first_sub_object), outer_faces)):
        Console.PrintMessage('Must select outer face of frame. Skipping attachment.\n')
        return none_tuple
    return frame, first_sub_object


def get_kwargs(frame, face):
    orientation = get_face_orientation(face)
    if orientation is None:
        return {}
    face_closest_to_origin = get_face_closest_to_origin(frame, orientation)
    lower, upper = get_placement_strategy(orientation)
    placement = translation_reference_point = None
    if face.isEqual(face_closest_to_origin):
        placement, translation_reference_point = lower(frame, face)
    else:
        placement, translation_reference_point = upper(frame, face)
    return {
        'length': frame.Size,
        'placement': placement,
        'translation_reference_point': translation_reference_point
    }


def get_face_closest_to_origin(frame, orientation):
    """Get the face closest to the origin based on orientation,
    where the origin is defined as the point (0, 0, 0).

    For example, if the orientation is z,
    then the face closest to the origin is the bottom face.
    """
    predicate_by_orientation = {
        'x': is_face_parallel_to_yz_plane,
        'y': is_face_parallel_to_xz_plane,
        'z': is_face_parallel_to_xy_plane
    }
    is_face_oriented_in_plane = predicate_by_orientation[orientation]

    outer_faces = get_outer_faces_of_frame(frame)

    outer_plane_faces = filter(is_face_oriented_in_plane, outer_faces)
    sorted_faces_by_position = sort_faces_by_surface_position(
        outer_plane_faces, orientation)
    return sorted_faces_by_position[0]


def sort_faces_by_surface_position(faces, orientation):
    position_index = ['x', 'y', 'z'].index(orientation)
    return sorted(faces, key=lambda f: f.Surface.Position[position_index])


def get_outer_faces_of_frame(frame):
    """Get outer faces of the frame.

    Assumes the 6 largest faces are the outer faces.
    """
    faces = frame.Shape.Faces
    sorted_faces = sorted(faces, key=lambda f: f.Area, reverse=True)
    outer_faces = sorted_faces[:6]
    return outer_faces


def get_face_orientation(face):
    if is_face_parallel_to_yz_plane(face):
        return 'x'
    if is_face_parallel_to_xz_plane(face):
        return 'y'
    if is_face_parallel_to_xy_plane(face):
        return 'z'
    Console.PrintWarning('Face not parallel to YZ, XZ, or XY plane.\n')
    return None


def is_frame_rotated(frame):
    rotation = frame.Placement.Rotation
    return rotation.Axis != Vector(0, 0, 1) or rotation.Angle != 0


def is_face_parallel_to_yz_plane(face):
    x_axis = Vector(1, 0, 0)
    return is_face_parallel_to_plane(face, x_axis)


def is_face_parallel_to_xz_plane(face):
    y_axis = Vector(0, 1, 0)
    return is_face_parallel_to_plane(face, y_axis)


def is_face_parallel_to_xy_plane(face):
    z_axis = Vector(0, 0, 1)
    return is_face_parallel_to_plane(face, z_axis)


def is_face_parallel_to_plane(face, axis_vector):
    return axis_vector == Vector(
        abs(round(face.Surface.Axis.x)),
        abs(round(face.Surface.Axis.y)),
        abs(round(face.Surface.Axis.z))
    )
