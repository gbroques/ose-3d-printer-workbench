def get_outer_faces_of_cnc_cut_frame(cnc_cut_frame):
    """Get outer faces of a frame constructed by
    cutting six sheets with a CNC machine.

    Assumes the 6 largest faces are the outer faces of the frame.
    """
    faces = cnc_cut_frame.Shape.Faces
    sorted_faces = sort_faces_by_area_descending(faces)
    return sorted_faces[:6]


def get_outer_faces_of_angled_bar(angled_bar_solid):
    """Get outer faces of angled bar.

    Assumes the 2 largest faces are the outer faces of the angled bar.
    """
    faces = angled_bar_solid.Faces
    sorted_faces = sort_faces_by_area_descending(faces)
    return sorted_faces[:2]


def get_outer_faces_of_corner(corner_solid):
    """Get outer faces of frame corner (angle frame connector).

    Assumes the 3 largest faces are the outer faces of the corner.
    """
    faces = corner_solid.Faces
    sorted_faces = sort_faces_by_area_descending(faces)
    return sorted_faces[:3]


def sort_faces_by_area_descending(faces):
    return sorted(faces, key=lambda f: f.Area, reverse=True)
