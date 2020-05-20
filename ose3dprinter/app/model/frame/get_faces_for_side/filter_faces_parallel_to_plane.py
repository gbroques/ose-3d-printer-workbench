from osecore.app.shape.face import (is_face_parallel_to_xy_plane,
                                    is_face_parallel_to_xz_plane,
                                    is_face_parallel_to_yz_plane)
from osecore.app.three_dimensional_space_enums import Plane


def filter_faces_parallel_to_plane(faces, plane):
    is_face_parallel_to_plane = _get_is_parallel_to_plane_predicate(
        plane)
    return filter(is_face_parallel_to_plane, faces)


def _get_is_parallel_to_plane_predicate(plane):
    return {
        Plane.XY: is_face_parallel_to_xy_plane,
        Plane.YZ: is_face_parallel_to_yz_plane,
        Plane.XZ: is_face_parallel_to_xz_plane
    }[plane]
