from .get_faces_for_side_of_cnc_cut_frame import \
    get_faces_for_side_of_cnc_cut_frame
from .get_faces_for_side_of_frame_with_corners import \
    get_faces_for_side_of_frame_with_corners


def get_faces_for_side(frame, side):
    """Gets a dictionary of outer faces of the frame by their Side.

    :param frame: Frame object
    :type frame: Document Object
    :return: Dictionary where the keys are a Side, and value is a Face
    :rtype: dict
    """
    if frame.HasCorners:
        return get_faces_for_side_of_frame_with_corners(frame, side)
    else:
        return get_faces_for_side_of_cnc_cut_frame(frame, side)
