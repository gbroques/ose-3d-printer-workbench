def get_outer_faces_of_cnc_cut_frame(cnc_cut_frame):
    """Get outer faces of a frame constructed by
    cutting six sheets with a CNC machine.

    Assumes the 6 largest faces are the outer faces of the frame.
    """
    faces = cnc_cut_frame.Shape.Faces
    sorted_faces = sorted(faces, key=lambda f: f.Area, reverse=True)
    return sorted_faces[:6]
