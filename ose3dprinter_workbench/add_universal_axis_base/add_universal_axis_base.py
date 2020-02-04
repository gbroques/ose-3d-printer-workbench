import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console
from ose3dprinter_workbench.part import create_universal_axis
from ose3dprinter_workbench.resources import get_resource_path

from .get_axis_creation_kwargs import get_axis_creation_kwargs
from .validate_frame_face_selection import validate_frame_face_selection


class AddUniversalAxisBase:
    """
    Base class for commands to add Universal Axis objects.
    """

    def __init__(self, orientation):
        self.orientation = orientation

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        kwargs = get_creation_kwargs(self.orientation)
        name = 'Universal{}Axis'.format(self.orientation.upper())
        create_universal_axis(document, name, **kwargs)
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        orientation = self.orientation.upper()
        icon_name = 'Universal{}Axis.svg'.format(orientation)
        return {
            'Pixmap': get_resource_path(icon_name),
            'MenuText': 'Add Universal {} Axis'.format(orientation),
            'ToolTip': 'Add Universal {} Axis'.format(orientation)
        }


def get_creation_kwargs(orientation):
    selection = Gui.Selection.getSelectionEx()
    is_valid, reason = validate_frame_face_selection(selection, orientation)
    if is_valid:
        return get_axis_creation_kwargs(selection, orientation)
    else:
        log_invalid_selection_reason(reason)
        return {}


def log_invalid_selection_reason(reason):
    log_message_template = '{}. Skipping attachment of axis to frame.\n'
    Console.PrintMessage(log_message_template.format(reason))
