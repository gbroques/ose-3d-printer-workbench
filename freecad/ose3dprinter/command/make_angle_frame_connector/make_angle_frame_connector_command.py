import FreeCADGui as Gui
from freecad.ose3dprinter.icon import get_icon_path

from .make_angle_frame_connector_task_panel import AngleFrameConnectorTaskPanel


class MakeAngleFrameConnectorCommand:
    """
    Command to make an Angle Frame Connector.
    """

    NAME = 'MakeAngleFrameConnector'

    def Activated(self):
        show_make_angle_frame_connector_task_panel()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('Std_CoordinateSystem.svg'),
            'MenuText': 'Make Angle Frame Connector',
            'ToolTip': 'Make Angle Frame Connector'
        }


def show_make_angle_frame_connector_task_panel():
    Gui.Control.closeDialog()
    task_panel = AngleFrameConnectorTaskPanel()
    Gui.Control.showDialog(task_panel)
