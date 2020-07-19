from typing import Union

from FreeCAD import Placement, Vector
from osecore.app.model import Model

from ose3dprinter.part import Extruder


class ExtruderModel(Model):
    """
    Encapsulates the data (i.e. topography and shape) for a Extruder,
    and is separate from the "view" or GUI representation.

    Based on:
        https://wiki.opensourceecology.org/wiki/File:Simpleextruderassy.fcstd

    See:
        https://wiki.opensourceecology.org/wiki/File:Finalextruder.png
    """

    Type = 'OSEExtruder'

    def __init__(self,
                 obj,
                 placement=Placement(),
                 origin_translation_offset=Vector()):
        super(ExtruderModel, self).__init__(obj)
        self.placement = placement
        self.origin_translation_offset = origin_translation_offset

    def execute(self, obj):
        """Execute on document recompute."""
        obj.Shape = Extruder.make(
            self.placement, self.origin_translation_offset)

    def __getstate__(self) -> Union[str, tuple]:
        """Execute when serializing and persisting the object.

        See Also:
            https://docs.python.org/3/library/pickle.html#object.__getstate__

        :return: state
        """
        return self.Type

    def __setstate__(self, state: str) -> None:
        """Execute when deserializing the object.

        See Also:
            https://docs.python.org/3/library/pickle.html#object.__setstate__

        :param state: state, in this case type of object.
        """
        if state:
            self.Type = state
