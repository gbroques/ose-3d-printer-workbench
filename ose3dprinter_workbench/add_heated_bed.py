import FreeCAD as App

from .resources import get_resource_path
from .heated_bed import create_heated_bed


class AddHeatedBed:
    """
    Command to add Heated Bed object.
    """

    NAME = 'AddHeatedBed'

    def Activated(self):
        document = App.ActiveDocument
        create_heated_bed(document, 'HeatedBed')
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('HeatedBed.svg'),
            'MenuText': 'Add Heated Bed',
            'ToolTip': 'Add Heated Bed'
        }
