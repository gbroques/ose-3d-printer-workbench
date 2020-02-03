import FreeCAD as App
from ose3dprinter_workbench.resources import get_resource_path
from ose3dprinter_workbench.part import create_universal_axis

from .attach_universal_axis_to_frame import attach_universal_axis_to_frame


class AddUniversalXAxis:
    """
    Command to add Universal X Axis object.
    """

    NAME = 'AddUniversalXAxis'

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        kwargs = attach_universal_axis_to_frame()
        create_universal_axis(document, 'UniversalXAxis', **kwargs)
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('UniversalXAxis.svg'),
            'MenuText': 'Add Universal X Axis',
            'ToolTip': 'Add Universal X Axis'
        }
