from FreeCAD import Console, Vector


def get_face_orientation(face):
    if is_face_parallel_to_xy_plane(face):
        return 'x'
    if is_face_parallel_to_yz_plane(face):
        return 'y'
    if is_face_parallel_to_xz_plane(face):
        return 'z'
    Console.PrintWarning('Face not parallel to YZ, XZ, or XY plane.\n')
    return None


def get_is_face_parallel_to_plane_predicate(orientation):
    return {
        'x': is_face_parallel_to_xy_plane,
        'y': is_face_parallel_to_yz_plane,
        'z': is_face_parallel_to_xz_plane
    }[orientation]


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
