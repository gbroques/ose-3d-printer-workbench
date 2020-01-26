import FreeCAD as App
from init_workbench import get_resource_path
from universal_axis import create_universal_axis


class AddUniversalAxis:
    """
    Command to add Universal Axis object.
    """

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('UniversalAxis.svg'),
            'MenuText': 'Add Universal Axis',
            'ToolTip': 'Add Universal Axis'
        }

    def Activated(self):
        document = App.ActiveDocument
        if not(document):
            document = App.newDocument()

        universal_axis = create_universal_axis(document, 'UniversalAxis')
        document.recompute()

    def IsActive(self):
        """
        Define if command must be active or not (greyed) if certain conditions
        are met or not.
        """
        return True
