def sort_faces_by_area_descending(faces):
    return sorted(faces, key=lambda f: f.Area, reverse=True)
