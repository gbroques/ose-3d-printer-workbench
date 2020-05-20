import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console
from ose3dprinter.app.attachment import (AttachmentError,
                                         get_axis_frame_attachment_kwargs,
                                         get_default_axis_creation_kwargs)
from ose3dprinter.app.model import FrameModel
from ose3dprinter.gui.create_part_feature import create_axis
from ose3dprinter.gui.selection_object import (find_face_in_selection_object,
                                               find_selection_object_by_type)


def handle_add_axis_command_activation(axis_orientation):
    document = App.ActiveDocument
    if not document:
        document = App.newDocument()
    name = '{}Axis'.format(axis_orientation.upper())
    kwargs = _get_axis_creation_kwargs(axis_orientation)
    create_axis(document, name, **kwargs)
    document.recompute()


def _get_axis_creation_kwargs(axis_orientation):
    selection_objects = Gui.Selection.getSelectionEx()
    try:
        frame, face = find_frame_and_face_in_selection(selection_objects)
        return get_axis_frame_attachment_kwargs(frame,
                                                face,
                                                axis_orientation)
    except AttachmentError as reason:
        log_message_template = '{}. Placing axis in default position.\n'
        Console.PrintMessage(log_message_template.format(reason))
        return get_default_axis_creation_kwargs(axis_orientation)


def find_frame_and_face_in_selection(selection_objects):
    frame_selection_object = find_selection_object_by_type(
        selection_objects, FrameModel.Type)
    if frame_selection_object is None:
        raise AttachmentError('Must select Frame')
    frame_face = find_face_in_selection_object(frame_selection_object)
    if frame_face is None:
        raise AttachmentError('Must select a face of the Frame')
    return frame_selection_object.Object, frame_face
