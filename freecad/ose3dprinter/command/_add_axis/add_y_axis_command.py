from osecore.app.three_dimensional_space_enums import CoordinateAxis

from freecad.ose3dprinter.icon import get_icon_path

from .handle_add_axis_command_activation import \
    handle_add_axis_command_activation


class AddYAxisCommand:
    """
    Command to add Y Axis object.
    """

    NAME = 'AddYAxis'

    def Activated(self):
        handle_add_axis_command_activation(CoordinateAxis.Y)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('YAxis.svg'),
            'MenuText': 'Add Y Axis',
            'ToolTip': 'Add Y Axis'
        }
