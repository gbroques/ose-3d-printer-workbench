from ose3dprinter.app.three_dimensional_space_enums import Axis
from ose3dprinter.gui.icon import get_icon_path

from .handle_add_axis_command_activation import \
    handle_add_axis_command_activation


class AddYAxisCommand:
    """
    Command to add Y Axis object.
    """

    NAME = 'AddYAxis'

    def Activated(self):
        handle_add_axis_command_activation(Axis.Y)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('YAxis.svg'),
            'MenuText': 'Add Y Axis',
            'ToolTip': 'Add Y Axis'
        }
