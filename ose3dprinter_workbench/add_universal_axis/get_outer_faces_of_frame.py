def get_outer_faces_of_frame(frame):
    """Get outer faces of the frame.

    Assumes the 6 largest faces are the outer faces.
    """
    faces = frame.Shape.Faces
    sorted_faces = sorted(faces, key=lambda f: f.Area, reverse=True)
    return sorted_faces[:6]
