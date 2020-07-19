from .get_outer_faces_of_cnc_cut_frame import get_outer_faces_of_cnc_cut_frame
from .get_outer_faces_of_frame_with_corners import \
    get_outer_faces_of_frame_with_corners


def get_outer_faces(frame):
    """Get outer faces of a frame."""
    if frame.HasCorners:
        return get_outer_faces_of_frame_with_corners(frame)
    else:
        return get_outer_faces_of_cnc_cut_frame(frame)
