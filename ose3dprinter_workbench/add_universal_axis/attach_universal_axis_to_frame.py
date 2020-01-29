import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console, Placement, Rotation, Vector
from Part import Face


def attach_universal_axis_to_frame():
    selection = Gui.Selection.getSelectionEx()
    frame, face = validate_potential_frame_face_selection(selection)
    if frame is None and face is None:
        return {}
    if is_frame_rotated(frame):
        Console.PrintWarning('Attaching axis to rotated frame is not supported.\n')
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
            'Selected object doesn\'t have one sub object. Skipping attachment.\n')
        return none_tuple
    first_sub_object = first_selection.SubObjects[0]
    if not isinstance(first_sub_object, Face):
        Console.PrintMessage(
            'Selected element is not a face. Skipping attachment.\n')
        return none_tuple
    if first_selection.Object.Proxy.Type != 'OSEFrame':
        Console.PrintMessage('Must select face on frame. Skipping attachment.\n')
        return none_tuple
    return first_selection.Object, first_sub_object


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


def get_kwargs(frame, face):
    orientation = get_face_orientation(face)
    if orientation is None:
        return {}
    face_closest_to_origin = get_face_closest_to_origin(frame, orientation)
    lower, upper = get_placement_strategy(orientation)
    placement_kwargs = None
    if face.isEqual(face_closest_to_origin):
        placement_kwargs = lower(frame, face)
    else:
        placement_kwargs = upper(frame, face)
    return dict(length=frame.Size, **placement_kwargs)


def get_placement_strategy(orientation):
    return {
        'x': (get_placement_for_left_face, get_placement_for_right_face),
        'y': (get_placement_for_front_face, get_placement_for_rear_face),
        'z': (get_placement_for_bottom_face, get_placement_for_top_face),
    }[orientation]


def get_face_closest_to_origin(frame, orientation):
    """Get the face closest to the origin based on origin.

    For example, if the orientation is Z,
    hen the face closest to the origin is the bottom face.
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


def get_placement_for_left_face(frame, face):
    x = face.Placement.Base.x
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(-90, 0, 90), Vector(0, 0, 0))
    return {
        'placement': placement,
        'reference_point': Vector(0, 0, 1)
    }


def get_placement_for_right_face(frame, face):
    x = frame.Shape.BoundBox.XMax
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(-90, 0, -90), Vector(0, 0, 0))
    return {
        'placement': placement,
        'reference_point': Vector(0, 0, 0)
    }


def get_placement_for_front_face(frame, face):
    x = face.CenterOfMass.x
    y = face.Placement.Base.y
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(0, 90, 90), Vector(0, 0, 0))
    return {
        'placement': placement,
        'reference_point': Vector(0.5, 0, 0)
    }


def get_placement_for_rear_face(frame, face):
    x = face.CenterOfMass.x
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(0, 90, -90), Vector(0, 0, 0))
    return {
        'placement': placement,
        'reference_point': Vector(-0.5, 0, 0)
    }


def get_placement_for_bottom_face(frame, face):
    Console.PrintMessage('Attaching axis to bottom face is not supported.\n')
    return {}


def get_placement_for_top_face(frame, face):
    x = face.Placement.Base.x
    y = face.CenterOfMass.y
    z = frame.Shape.BoundBox.ZMax
    placement = App.Placement(
                Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    return {
        'placement': placement,
        'reference_point': Vector(0, 0.5, 0)
    }


def is_frame_rotated(frame):
    rotation = frame.Placement.Rotation
    return rotation.Axis != Vector(0, 0, 1) or rotation.Angle != 0
