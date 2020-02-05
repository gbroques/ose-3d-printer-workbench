from FreeCAD import Vector
from Part import Face

from .get_outer_faces_of_frame import get_outer_faces_of_frame
from .face_orientation import get_face_orientation, get_face_orientation_name


def validate_frame_face_selection(selection, axis_orientation):
    """Validates a potential selection is a face of a frame.

    Returns whether the selection is valid and reason if not valid.
    """
    num_selected = len(selection)
    if num_selected != 1:
        reason = 'Selected {} instead of 1 element'.format(num_selected)
        return False, reason
    first_selection = selection[0]
    num_sub_objects = len(first_selection.SubObjects)
    if num_sub_objects != 1:
        reason = 'Selected object has {} sub objects instead of 1'.format(
            num_sub_objects)
        return False, reason
    potential_face = first_selection.SubObjects[0]
    if not isinstance(potential_face, Face):
        reason = 'Selected element is not a face'
        return False, reason
    face = potential_face
    potential_frame = first_selection.Object
    if potential_frame.Proxy.Type != 'OSEFrame':
        reason = 'Must select frame'
        return False, reason
    frame = potential_frame
    if is_frame_rotated(frame):
        reason = 'Frame is rotated'
        return False, reason
    if not is_outer_face_of_frame(face, frame):
        reason = 'Must select outer face of frame'
        return False, reason
    face_orientation_name = get_face_orientation_name(frame, face)
    if face_orientation_name == 'bottom':
        reason = 'Cannot attach axis to bottom side of frame'
        return False, reason
    face_orientation = get_face_orientation(face)
    if face_orientation != axis_orientation:
        reason = 'Cannot attach {} axis to {} side of frame'.format(
            axis_orientation.upper(), face_orientation_name)
        return False, reason
    return True, ''


def get_frame_and_face_from_selection(selection, axis_orientation):
    """
    Assumes first selected element is frame, and first sub-object is face.
    """
    is_valid, _ = validate_frame_face_selection(selection, axis_orientation)
    if not is_valid:
        return None, None
    else:
        first_selection = selection[0]
        frame = first_selection.Object
        face = first_selection.SubObjects[0]
        return frame, face


def is_frame_rotated(frame):
    rotation = frame.Placement.Rotation
    return rotation.Axis != Vector(0, 0, 1) or rotation.Angle != 0


def is_outer_face_of_frame(face, frame):
    outer_faces = get_outer_faces_of_frame(frame)
    return any(map(lambda f: f.isEqual(face), outer_faces))
