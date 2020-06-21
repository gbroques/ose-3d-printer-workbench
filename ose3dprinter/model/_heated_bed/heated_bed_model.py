from FreeCAD import Placement, Vector
from ose3dprinter.part import HeatedBed
from osecore.app.model import Model


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
        """
        Called on document recompute
        """
        size = obj.Size.Value
        obj.Shape = HeatedBed.make(
            size, self.placement, self.origin_translation_offset)

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
