import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console
from ose3dprinter_workbench.part import create_universal_axis
from ose3dprinter_workbench.resources import get_resource_path

from .get_axis_creation_kwargs import get_axis_creation_kwargs
from .validate_frame_face_selection import validate_frame_face_selection


class AddUniversalXAxis:
    """
    Command to add Universal X Axis object.
    """

    NAME = 'AddUniversalXAxis'

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        kwargs = get_creation_kwargs()
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


def get_creation_kwargs():
    selection = Gui.Selection.getSelectionEx()
    is_valid, reason = validate_frame_face_selection(selection)
    if is_valid:
        return get_axis_creation_kwargs(selection)
    else:
        log_invalid_selection_reason(reason)
        return {}


def log_invalid_selection_reason(reason):
    log_message_template = '{}. Skipping attachment of axis to frame.\n'
    Console.PrintMessage(log_message_template.format(reason))
