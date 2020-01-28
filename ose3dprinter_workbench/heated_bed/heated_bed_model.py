import Part
from FreeCAD import Base


class HeatedBedModel:
    """
    Encapsulates the data (i.e. topography and shape) for a Heated Bed,
    and is separate from the "view" or GUI representation.
    """

    def __init__(self, obj):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        self.Type = 'OSEUniversalAxis'

        obj.Proxy = self

        # Size property
        size_tooltip = 'Size or dimension of heated bed.'
        obj.addProperty('App::PropertyLength', 'Size', 'Base', size_tooltip)
        obj.Size = 203.2  # 8 inches

    def execute(self, obj):
        """
        Called on document recompute
        """
        size = obj.Size.Value
        bed = Part.makeBox(size, size, 50.8)  # 50.8 mm = 2 inches
        bed.rotate(Base.Vector(0, 0, 0), Base.Vector(0, -1, 0), 90)
        obj.Shape = bed

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
