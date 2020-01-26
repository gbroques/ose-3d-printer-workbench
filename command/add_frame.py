import FreeCAD as App
from init_workbench import get_resource_path
from frame import create_frame


class AddFrame:
    """
    Command to add Frame object.
    """

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('Frame.svg'),
            'MenuText': 'Add Frame',
            'ToolTip': 'Add Frame'
        }

    def Activated(self):
        document = App.ActiveDocument
        if not(document):
            document = App.newDocument()

        frame = create_frame(document, 'Frame')
        document.recompute()

    def IsActive(self):
        """
        Define if command must be active or not (greyed) if certain conditions
        are met or not.
        """
        return True
