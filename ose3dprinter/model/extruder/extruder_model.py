from FreeCAD import Placement, Vector
from ose3dprinter.part import Extruder
from osecore.app.model import Model


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
        """
        Called on document recompute
        """
        obj.Shape = Extruder.make(
            self.placement, self.origin_translation_offset)

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
