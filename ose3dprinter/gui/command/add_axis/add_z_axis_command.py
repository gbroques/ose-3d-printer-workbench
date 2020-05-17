from ose3dprinter.app.enums import Axis
from ose3dprinter.gui.icon import get_icon_path

from .handle_add_axis_command_activation import \
    handle_add_axis_command_activation


class AddZAxisCommand:
    """
    Command to add Z Axis object.
    """

    NAME = 'AddZAxis'

    def Activated(self):
        handle_add_axis_command_activation(Axis.Z)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('ZAxis.svg'),
            'MenuText': 'Add Z Axis',
            'ToolTip': 'Add Z Axis'
        }
