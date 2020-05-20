from abc import abstractmethod

import Part
from FreeCAD import Console
from osecore.app.future.python import ABC


class FaceSideStrategy(ABC):

    def get_face_side(self, frame, face):
        # Exclude cylindrical surfaces and holes
        if not isinstance(face.Surface, Part.Plane):
            Console.PrintWarning('Face is not planar.\n')
            return None
        lower_side, upper_side = self._get_sides()
        if self._is_between_lower_bounds(face, frame):
            return lower_side
        elif self._is_between_upper_bounds(face, frame):
            return upper_side
        else:
            warning_message = 'Face is not between upper or lower bounds.\n'
            Console.PrintWarning(warning_message)
            return None

    @abstractmethod
    def _get_sides(self):
        """Get a list of sides ordered by distance to the origin ascending.

        For example,
            the "front" side is closer to the origin than the "rear" side.
        """
        pass

    @abstractmethod
    def _is_between_lower_bounds(self, face, frame):
        """Determine whether the face is between the bounds of the "lower side"
        closest to the origin.

        :param face: Face to check whether it's between lower bounds.
        :type face: Part.Face
        :param frame: Frame object
        :type frame: App::DocumentObject
        """
        pass

    @abstractmethod
    def _is_between_upper_bounds(self, face, frame):
        """Determine whether the face is between the bounds of the "upper side"
        farthest from the origin.

        :param face: Face to check whether it's between upper bounds.
        :type face: Part.Face
        :param frame: Frame object
        :type frame: App::DocumentObject
        """
        pass
