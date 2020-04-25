import Part
from ose3dprinter.app.model.base_model import BaseModel


class HeatedBedModel(BaseModel):
    """
    Encapsulates the data (i.e. topography and shape) for a Heated Bed,
    and is separate from the "view" or GUI representation.
    """

    Type = 'OSEHeatedBed'

    def __init__(self, obj, placement, origin_translation_offset):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        init_args = (placement, origin_translation_offset)
        super(HeatedBedModel, self).__init__(*init_args)

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
        dimensions = (size, size, 50.8)  # 50.8 mm = 2 inches
        bed = Part.makeBox(*dimensions)

        parts = [bed]
        self.move_parts(parts, dimensions)

        # TODO: Why does this need to be a compound to visually center heated bed?
        obj.Shape = Part.makeCompound(parts)

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
