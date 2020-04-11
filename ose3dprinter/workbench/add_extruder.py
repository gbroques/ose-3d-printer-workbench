import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console
from ose3dprinter.core.exceptions import AttachmentError
from ose3dprinter.core.get_extruder_x_axis_carriage_attachment_kwargs import \
    get_extruder_x_axis_carriage_attachment_kwargs
from ose3dprinter.workbench.get_first_selected_object_and_sub_object import \
    get_first_selected_object_and_sub_object
from ose3dprinter.workbench.part import create_extruder
from ose3dprinter.workbench.resources import get_resource_path


class AddExtruder:
    """
    Command to add extruder object.
    """

    NAME = 'AddExtruder'

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        kwargs = get_extruder_creation_kwargs()
        create_extruder(document, 'Extruder', **kwargs)
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('Extruder.svg'),
            'MenuText': 'Add Extruder',
            'ToolTip': 'Add Extruder'
        }


def get_extruder_creation_kwargs():
    selection = Gui.Selection.getSelectionEx()
    try:
        axis, face = get_first_selected_object_and_sub_object(selection)
        return get_extruder_x_axis_carriage_attachment_kwargs(axis, face)
    except AttachmentError as reason:
        log_message_template = '{}. Placing extruder in default position.\n'
        Console.PrintMessage(log_message_template.format(reason))
        return {}
