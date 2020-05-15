from ose3dprinter.app.enums import AxisOrientation

from .handle_add_axis_command_activation import \
    handle_add_axis_command_activation
from .icon import get_icon_path


class AddXAxis:
    """
    Command to add X Axis object.
    """

    NAME = 'AddXAxis'

    def Activated(self):
        handle_add_axis_command_activation(AxisOrientation.X)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('XAxis.svg'),
            'MenuText': 'Add X Axis',
            'ToolTip': 'Add X Axis'
        }
