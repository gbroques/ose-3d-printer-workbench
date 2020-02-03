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
        size_tooltip = 'Size or dimension of cubic frame.'
        obj.addProperty('App::PropertyLength', 'Size', 'Base', size_tooltip)
        obj.Size = 406.4

        obj.Proxy = self

    def execute(self, obj):
        """
        Called on document recompute
        """
        side = obj.Size.Value
        width = 50.8  # Width of 12" (304.8 mm) frame is 25.4 mm or 1"
        sheet_thickness = 3

        sheet = Part.makeBox(side, side, sheet_thickness)

        inner_side = side - (width * 2)
        inner_sheet = Part.makeBox(inner_side, inner_side, sheet_thickness)
        inner_sheet.translate(Base.Vector(width, width, 0))

        bottom_frame = sheet.cut(inner_sheet)

        top_frame = bottom_frame.copy()
        top_frame.translate(Base.Vector(0, 0, side - sheet_thickness))

        left_wall = bottom_frame.copy()
        left_wall.rotate(Base.Vector(0, 0, 0), Base.Vector(0, -1, 0), 90)
        left_wall.translate(Base.Vector(sheet_thickness, 0, 0))

        right_wall = left_wall.copy()
        right_wall.translate(Base.Vector(side - sheet_thickness, 0, 0))

        front_wall = bottom_frame.copy()
        front_wall.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 90)
        front_wall.translate(Base.Vector(0, sheet_thickness, 0))

        rear_wall = front_wall.copy()
        rear_wall.translate(Base.Vector(0, side - sheet_thickness, 0))

        parts = [
            bottom_frame,
            left_wall,
            right_wall,
            front_wall,
            rear_wall,
            top_frame
        ]

        frame = reduce(lambda union, part: union.fuse(part), parts)

        # removeSplitter() refines shape
        obj.Shape = frame.removeSplitter()

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
