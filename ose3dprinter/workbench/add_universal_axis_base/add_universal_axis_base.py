import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console
from ose3dprinter.core.exceptions import AttachmentError
from ose3dprinter.core.get_axis_frame_attachment_kwargs import \
    get_axis_frame_attachment_kwargs
from ose3dprinter.core.get_default_axis_creation_kwargs import \
    get_default_axis_creation_kwargs
from ose3dprinter.workbench.get_first_selected_object_and_sub_object import \
    get_first_selected_object_and_sub_object
from ose3dprinter.workbench.part import create_universal_axis
from ose3dprinter.workbench.resources import get_resource_path


class AddUniversalAxisBase:
    """
    Base class for commands to add Universal Axis objects.
    """

    def __init__(self, axis_orientation):
        self.axis_orientation = axis_orientation

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        name = 'Universal{}Axis'.format(self.axis_orientation.upper())
        kwargs = get_axis_creation_kwargs(self.axis_orientation)
        create_universal_axis(document, name, **kwargs)
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        orientation = self.axis_orientation.upper()
        icon_name = 'Universal{}Axis.svg'.format(orientation)
        return {
            'Pixmap': get_resource_path(icon_name),
            'MenuText': 'Add Universal {} Axis'.format(orientation),
            'ToolTip': 'Add Universal {} Axis'.format(orientation)
        }


def get_axis_creation_kwargs(axis_orientation):
    selection = Gui.Selection.getSelectionEx()
    try:
        frame, face = get_first_selected_object_and_sub_object(selection)
        return get_axis_frame_attachment_kwargs(frame,
                                                face,
                                                axis_orientation)
    except AttachmentError as reason:
        log_message_template = '{}. Placing axis in default position.\n'
        Console.PrintMessage(log_message_template.format(reason))
        return get_default_axis_creation_kwargs(axis_orientation)
