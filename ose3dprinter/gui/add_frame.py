import FreeCAD as App

from .part import create_frame
from .resources import get_resource_path


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
            'Pixmap': get_resource_path('Frame.svg'),
            'MenuText': 'Add Frame',
            'ToolTip': 'Add Frame'
        }
