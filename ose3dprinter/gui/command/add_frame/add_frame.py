import FreeCAD as App
from ose3dprinter.gui.icon import get_icon_path
from ose3dprinter.gui.part import create_frame


class AddFrame:
    """
    Command to add Frame object.
    """

    NAME = 'AddFrame'

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        create_frame(document, 'Frame')
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('Frame.svg'),
            'MenuText': 'Add Frame',
            'ToolTip': 'Add Frame'
        }
