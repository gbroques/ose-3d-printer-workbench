import Part
from FreeCAD import Base


class FrameModel:
    """
    Encapsulates the data (i.e. topography and shape) for a Frame,
    and is separate from the "view" or GUI representation.
    """

    def __init__(self, obj):
        self.Type = 'OSEFrame'

        # Size property
        size_tooltip = 'Size or dimension or cubic frame.'
        obj.addProperty('App::PropertyLength', 'Size', 'Base', size_tooltip)
        obj.Size = 406.4

        obj.Proxy = self

    def execute(self, obj):
        """
        Called on document recompute
        """
        side = obj.Size.Value
        width = 50.8
        sheet_thickness = 3

        sheet = Part.makeBox(side, side, sheet_thickness)

        inner_side = side - (width * 2)
        inner_sheet = Part.makeBox(inner_side, inner_side, sheet_thickness)
        inner_sheet.translate(Base.Vector(width, width, 0))

        bottom_frame = sheet.cut(inner_sheet)

        top_frame = bottom_frame.copy()
        top_frame.translate(Base.Vector(0, 0, side))

        left_wall = bottom_frame.copy()
        left_wall.rotate(Base.Vector(0, 0, 0), Base.Vector(0, -1, 0), 90)

        right_wall = left_wall.copy()
        right_wall.translate(Base.Vector(side, 0, 0))

        front_wall = bottom_frame.copy()
        front_wall.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 90)

        rear_wall = front_wall.copy()
        rear_wall.translate(Base.Vector(0, side, 0))

        obj.Shape = Part.makeCompound([
            bottom_frame,
            top_frame,
            left_wall,
            right_wall,
            front_wall,
            rear_wall
        ])

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
