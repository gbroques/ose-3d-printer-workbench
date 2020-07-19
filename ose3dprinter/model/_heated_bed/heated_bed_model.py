from typing import Union

from FreeCAD import Placement, Vector
from osecore.app.model import Model

from ose3dprinter.part import HeatedBed


class HeatedBedModel(Model):
    """
    Encapsulates the data (i.e. topography and shape) for a Heated Bed,
    and is separate from the "view" or GUI representation.
    """

    Type = 'OSEHeatedBed'

    def __init__(self,
                 obj,
                 placement=Placement(),
                 origin_translation_offset=Vector()):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        super(HeatedBedModel, self).__init__(obj)
        self.placement = placement
        self.origin_translation_offset = origin_translation_offset

        # Size property
        size_tooltip = 'Size or dimension of heated bed.'
        obj.addProperty('App::PropertyLength', 'Size', 'Base', size_tooltip)
        obj.Size = 203.2  # 8 inches

    def execute(self, obj):
        """Execute on document recompute."""
        size = obj.Size.Value
        obj.Shape = HeatedBed.make(
            size, self.placement, self.origin_translation_offset)

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
