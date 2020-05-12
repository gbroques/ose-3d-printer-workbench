

import abc

import Part
from FreeCAD import Console
from ose3dprinter.app.future import ABC
from ose3dprinter.app.get_outer_faces import get_outer_faces_of_cnc_cut_frame


class FaceSideStrategy(ABC):
    """TODO: Break up strategy for frame with and without corners
    """

    def get_face_side(self, frame, face):
        if frame.HasCorners:
            return self._get_face_side_for_frame_with_corners(frame,
                                                              face)
        else:
            return self._get_face_side_for_cnc_cut_frame(frame,
                                                         face)

    def _get_face_side_for_frame_with_corners(self,
                                              frame_with_corners,
                                              face):
        # Exclude cylindrical surfaces and holes
        if not isinstance(face.Surface, Part.Plane):
            Console.PrintWarning('Face is not planar.\n')
            return None
        lower_side, upper_side = self._get_sides()
        if self._is_between_lower_bounds(face, frame_with_corners):
            return lower_side
        elif self._is_between_upper_bounds(face, frame_with_corners):
            return upper_side
        else:
            Console.PrintWarning(
                'Face is not between upper or lower bounds.\n')
            return None

    def _get_face_side_for_cnc_cut_frame(self,
                                         cnc_cut_frame,
                                         face):
        lower_side, upper_side = self._get_sides()
        face_closest_to_origin = self._get_face_closest_to_origin(
            cnc_cut_frame)
        if face.isEqual(face_closest_to_origin):
            return lower_side
        else:
            return upper_side

    @abc.abstractmethod
    def _get_sides(self):
        pass

    @abc.abstractmethod
    def _is_between_lower_bounds(self, face, frame_with_corners):
        pass

    @abc.abstractmethod
    def _is_between_upper_bounds(self, face, frame_with_corners):
        pass

    def _get_face_closest_to_origin(self, cnc_cut_frame):
        outer_faces = get_outer_faces_of_cnc_cut_frame(cnc_cut_frame)

        outer_faces_parallel_to_plane = filter(
            self._is_face_parallel_to_plane, outer_faces)
        sorted_faces_by_position = self._sort_faces_by_surface_position(
            outer_faces_parallel_to_plane)
        return sorted_faces_by_position[0]

    @abc.abstractmethod
    def _is_face_parallel_to_plane(self, face):
        pass

    @abc.abstractmethod
    def _get_axis_orientation_index(self):
        pass

    def _sort_faces_by_surface_position(self, faces):
        """
        If orientation of axis is x, then sort faces by z
        If orientation of axis is y, then sort faces by x
        If orientation of axis is z, then sort faces by y
        """
        axis_orientation_index = self._get_axis_orientation_index()
        position_index = ((axis_orientation_index - 1) + 3) % 3
        return sorted(faces, key=lambda f: f.Surface.Position[position_index])
