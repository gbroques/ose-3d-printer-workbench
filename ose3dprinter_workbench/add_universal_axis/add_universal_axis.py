import FreeCAD as App
from ose3dprinter_workbench.resources import get_resource_path
from ose3dprinter_workbench.universal_axis import create_universal_axis

from .attach_universal_axis_to_frame import attach_universal_axis_to_frame


class AddUniversalAxis:
    """
    Command to add Universal Axis object.
    """

    NAME = 'AddUniversalAxis'

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        kwargs = attach_universal_axis_to_frame()
        create_universal_axis(document, 'UniversalAxis', **kwargs)
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('UniversalAxis.svg'),
            'MenuText': 'Add Universal Axis',
            'ToolTip': 'Add Universal Axis'
        }
