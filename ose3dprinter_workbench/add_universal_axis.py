import FreeCAD as App

from .resources import get_resource_path
from .universal_axis import create_universal_axis


class AddUniversalAxis:
    """
    Command to add Universal Axis object.
    """

    NAME = 'AddUniversalAxis'

    def Activated(self):
        document = App.ActiveDocument
        create_universal_axis(document, 'UniversalAxis')
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('UniversalAxis.svg'),
            'MenuText': 'Add Universal Axis',
            'ToolTip': 'Add Universal Axis'
        }
