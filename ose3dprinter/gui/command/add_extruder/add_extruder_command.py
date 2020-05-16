import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console
from ose3dprinter.app.attachment import (AttachmentError,
                                         get_extruder_axis_attachment_kwargs)
from ose3dprinter.app.model import AxisModel
from ose3dprinter.gui.icon import get_icon_path
from ose3dprinter.gui.part import create_extruder
from ose3dprinter.gui.selection_object import (find_face_in_selection_object,
                                               find_selection_object_by_type)


class AddExtruderCommand:
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
            'Pixmap': get_icon_path('Extruder.svg'),
            'MenuText': 'Add Extruder',
            'ToolTip': 'Add Extruder'
        }


def get_extruder_creation_kwargs():
    selection_objects = Gui.Selection.getSelectionEx()
    try:
        axis, face = find_axis_and_face_in_selection(selection_objects)
        return get_extruder_axis_attachment_kwargs(axis, face)
    except AttachmentError as reason:
        log_message_template = '{}. Placing extruder in default position.\n'
        Console.PrintMessage(log_message_template.format(reason))
        return {}


def find_axis_and_face_in_selection(selection_objects):
    axis_selection_object = find_selection_object_by_type(
        selection_objects, AxisModel.Type)
    if axis_selection_object is None:
        raise AttachmentError('Must select Axis')
    axis_face = find_face_in_selection_object(axis_selection_object)
    if axis_face is None:
        raise AttachmentError('Must select a face of the Axis')
    return axis_selection_object.Object, axis_face
