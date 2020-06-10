from freecad.ose3dprinter.icon import get_icon_path
from osecore.app.three_dimensional_space_enums import CoordinateAxis

from .handle_add_axis_command_activation import \
    handle_add_axis_command_activation


class AddXAxisCommand:
    """
    Command to add X Axis object.
    """

    NAME = 'AddXAxis'

    def Activated(self):
        handle_add_axis_command_activation(CoordinateAxis.X)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('XAxis.svg'),
            'MenuText': 'Add X Axis',
            'ToolTip': 'Add X Axis'
        }
