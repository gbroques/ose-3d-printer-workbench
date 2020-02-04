import FreeCAD as App
from ose3dprinter_workbench.part import create_heated_bed
from ose3dprinter_workbench.resources import get_resource_path


class AddHeatedBed:
    """
    Command to add Heated Bed object.
    """

    NAME = 'AddHeatedBed'

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
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
