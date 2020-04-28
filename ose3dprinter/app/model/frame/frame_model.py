import Part
from FreeCAD import Placement, Vector
from ose3dprinter.app.model.base_model import BaseModel

from .angle_frame_connector import AngleFrameConnector
from .angled_bar_frame import AngledBarFrame
from .cnc_cut_frame import CNCCutFrame


class FrameModel(BaseModel):
    """
    Encapsulates the data (i.e. topography and shape) for a Frame,
    and is separate from the "view" or GUI representation.

    See D3D Frame on the Open Source Ecology Wiki:
    https://wiki.opensourceecology.org/wiki/D3D_Frame
    """

    Type = 'OSEFrame'

    def __init__(self,
                 obj,
                 placement=Placement(),
                 origin_translation_offset=Vector()):
        init_args = (obj, placement, origin_translation_offset)
        super(FrameModel, self).__init__(*init_args)

        # Size property
        size_tooltip = 'Size or dimension of cubic frame.'
        obj.addProperty('App::PropertyLength', 'Size', 'Base', size_tooltip)
        obj.Size = 304.8  # 12 inches

        # Width property
        width_tooltip = 'Width of frame.'
        obj.addProperty('App::PropertyLength', 'Width', 'Base', width_tooltip)
        obj.Width = 38.1  # 1.5 inches

        # Thickness property
        thickness_tooltip = 'Thickness of frame.'
        obj.addProperty('App::PropertyLength', 'Thickness',
                        'Base', thickness_tooltip)
        obj.Thickness = 3.175  # 1/8 inch

        # HasCorners property
        has_corners = 'Whether the frame has 3d printed corners or not.'
        obj.addProperty('App::PropertyBool', 'HasCorners', 'Base', has_corners)
        obj.HasCorners = False

    def execute(self, obj):
        """
        Called on document recompute
        """
        side = obj.Size.Value
        # Width of 12" (304.8 mm) frame is 1" (25.4 mm)
        width = obj.Width.Value
        sheet_thickness = obj.Thickness.Value

        Frame = AngledBarFrame if obj.HasCorners else CNCCutFrame

        obj.Shape = Frame.make(side, width, sheet_thickness)

    @property
    def distance_between_axis_side_mount_holes(self):
        d = AngleFrameConnector.distance_between_axis_side_mount_holes_and_frame()
        return self.Object.Size.Value + (d * 2)

    @property
    def XMin(self):
        x_min = self.Object.Shape.BoundBox.XMin
        if self.Object.HasCorners:
            return x_min + AngleFrameConnector.axis_side_mount_width
        else:
            return x_min

    @property
    def XMax(self):
        x_min = self.Object.Shape.BoundBox.XMax
        if self.Object.HasCorners:
            return x_min - AngleFrameConnector.axis_side_mount_width
        else:
            return x_min

    @property
    def YMin(self):
        y_min = self.Object.Shape.BoundBox.YMin
        if self.Object.HasCorners:
            return y_min + \
                AngleFrameConnector.calculate_y_axis_overhang_distance()
        else:
            return y_min

    @property
    def YMax(self):
        y_max = self.Object.Shape.BoundBox.YMax
        if self.Object.HasCorners:
            return y_max - \
                AngleFrameConnector.calculate_y_axis_overhang_distance()
        else:
            return y_max

    @property
    def ZMin(self):
        return self.Object.Shape.BoundBox.ZMin

    @property
    def ZMax(self):
        return self.Object.Shape.BoundBox.ZMax

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
