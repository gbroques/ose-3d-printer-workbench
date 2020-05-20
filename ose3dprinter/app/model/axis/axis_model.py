from FreeCAD import Placement, Vector
from ose3dprinter.app.part import Axis
from osecore.app.model import Model
from osecore.app.three_dimensional_space_enums import CoordinateAxis, Side


class AxisModel(Model):
    """
    Encapsulates the data (i.e. topography and shape) for a Axis,
    and is separate from the "view" or GUI representation.
    """

    Type = 'OSEAxis'

    def __init__(self,
                 obj,
                 length=304.80,
                 carriage_position=50,
                 orientation=CoordinateAxis.X,
                 side=Side.TOP,
                 placement=Placement(),
                 origin_translation_offset=Vector()):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        super(AxisModel, self).__init__(obj)
        self.placement = placement
        self.origin_translation_offset = origin_translation_offset

        # Length property
        length_tooltip = 'Length of axis corresponds to rod length.'
        obj.addProperty('App::PropertyLength', 'Length',
                        'Base', length_tooltip)
        obj.Length = length

        # Rod Diameter property
        rod_diameter_tooltip = 'Diameter of rod.'
        read_only = 1
        obj.addProperty('App::PropertyLength', 'RodDiameter',
                        'Base', rod_diameter_tooltip, read_only)
        obj.RodDiameter = 8

        # Carriage Position property
        carriage_position_tooltip = 'Position of carriage relative to available rod.'
        obj.addProperty('App::PropertyPercent', 'CarriagePosition',
                        'Base', carriage_position_tooltip)
        obj.CarriagePosition = carriage_position

        # Orientation property
        orientation_tooltip = 'Orientation of axis: X, Y, or Z.'
        hidden = 4
        obj.addProperty('App::PropertyString', 'Orientation',
                        'Base', orientation_tooltip, hidden)
        obj.Orientation = orientation

        # Side property
        side_tooltip = 'Which side the bottom of the axis faces.'
        obj.addProperty('App::PropertyString', 'Side',
                        'Base', side_tooltip, hidden)
        obj.Side = side

    def execute(self, obj):
        """
        Called on document recompute
        """
        # Get rod dimensions
        rod_length = obj.Length.Value
        rod_radius = obj.RodDiameter.Value / 2

        obj.Shape = Axis.make(rod_length,
                              rod_radius,
                              obj.CarriagePosition,
                              obj.Orientation,
                              obj.Side,
                              self.placement,
                              self.origin_translation_offset)

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state

    def calculate_carriage_box_x(self):
        obj = self.Object
        rod_length = obj.Length.Value
        carriage_position = obj.CarriagePosition
        return Axis.calculate_carriage_box_x(
            rod_length, carriage_position)

    def calculate_top_of_carriage_box_for_z_axis(self):
        return (
            self.Object.Shape.BoundBox.ZMin +
            (
                self.Object.Length.Value -
                self.calculate_carriage_box_x()
            )
        )

    def is_x(self):
        """Return whether or not this axis is a X axis.

        This assumes the axis is parallel to the XY, YZ, or XZ planes,
        and not rotated in a weird diagonal or skewed way.

        :return: Whether this axis is a X axis.
        :rtype: bool
        """
        axis = self.Object
        return _is_oriented_in(axis, CoordinateAxis.X)

    def is_y(self):
        """Return whether or not this axis is a Y axis.

        This assumes the axis is parallel to the XY, YZ, or XZ planes,
        and not rotated in a weird diagonal or skewed way.

        :return: Whether this axis is a Y axis.
        :rtype: bool
        """
        axis = self.Object
        return _is_oriented_in(axis, CoordinateAxis.Y)

    def is_z(self):
        """Return whether or not this axis is a Z axis.

        This assumes the axis is parallel to the XY, YZ, or XZ planes,
        and not rotated in a weird diagonal or skewed way.

        :return: Whether this axis is a Z axis.
        :rtype: bool
        """
        axis = self.Object
        return _is_oriented_in(axis, CoordinateAxis.Z)


def _is_oriented_in(axis, axis_orientation):
    bound_box = axis.Shape.BoundBox
    lengths = [
        bound_box.XLength,
        bound_box.YLength,
        bound_box.ZLength
    ]
    max_length = max(lengths)
    length_property = _get_length_property(axis_orientation)
    return max_length == getattr(bound_box, length_property)


def _get_length_property(axis_orientation):
    return {
        CoordinateAxis.X: 'XLength',
        CoordinateAxis.Y: 'YLength',
        CoordinateAxis.Z: 'ZLength',
    }[axis_orientation]
