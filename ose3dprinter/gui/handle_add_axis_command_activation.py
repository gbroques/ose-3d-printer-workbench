import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console
from ose3dprinter.app.attachment import (AttachmentError,
                                         get_axis_frame_attachment_kwargs,
                                         get_default_axis_creation_kwargs)
from ose3dprinter.gui.get_first_selected_object_and_sub_object import \
    get_first_selected_object_and_sub_object
from ose3dprinter.gui.part import create_axis


def handle_add_axis_command_activation(axis_orientation):
    document = App.ActiveDocument
    if not document:
        document = App.newDocument()
    name = '{}Axis'.format(axis_orientation.upper())
    kwargs = _get_axis_creation_kwargs(axis_orientation)
    create_axis(document, name, **kwargs)
    document.recompute()


def _get_axis_creation_kwargs(axis_orientation):
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
