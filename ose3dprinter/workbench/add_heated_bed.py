import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console
from ose3dprinter.core.exceptions import AttachmentError
from ose3dprinter.core.get_heated_bed_frame_attachment_kwargs import \
    get_heated_bed_frame_attachment_kwargs
from ose3dprinter.core.model import FrameModel, UniversalAxisModel
from ose3dprinter.workbench.part import create_heated_bed
from ose3dprinter.workbench.resources import get_resource_path


class AddHeatedBed:
    """
    Command to add Heated Bed object.
    """

    NAME = 'AddHeatedBed'

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        kwargs = get_heated_bed_creation_kwargs()
        create_heated_bed(document, 'HeatedBed', **kwargs)
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_resource_path('HeatedBed.svg'),
            'MenuText': 'Add Heated Bed',
            'ToolTip': 'Add Heated Bed'
        }


def get_heated_bed_creation_kwargs():
    selection_objects = Gui.Selection.getSelectionEx()
    try:
        frame, axis = get_frame_and_axis(selection_objects)
        return get_heated_bed_frame_attachment_kwargs(frame, axis)
    except AttachmentError as reason:
        log_message_template = '{}. Placing heated bed in default position.\n'
        Console.PrintMessage(log_message_template.format(reason))
        return {}


def get_frame_and_axis(selection_objects):
    if is_frame_and_axis_selected(selection_objects):
        frame = find_object_by_type_in_selection_objects(
            selection_objects, FrameModel.Type)
        axis = find_object_by_type_in_selection_objects(
            selection_objects, UniversalAxisModel.Type)
        return frame, axis
    else:
        raise AttachmentError('Must select Frame and Axis')


def is_frame_and_axis_selected(selection_objects):
    return (
        is_frame_selected(selection_objects) and
        is_axis_selected(selection_objects)
    )


def is_frame_selected(selection_objects):
    return _do_selection_objects_contain_type(
        selection_objects, FrameModel.Type)


def is_axis_selected(selection_objects):
    return _do_selection_objects_contain_type(
        selection_objects, UniversalAxisModel.Type)


def find_object_by_type_in_selection_objects(selection_objects,
                                             object_type):
    potential_objects = list(filter(
        lambda x: _is_selection_object_type_of(x, object_type),
        selection_objects))
    if len(potential_objects) == 0:
        raise AttachmentError(
            'No object with type {} selected'.format(object_type))
    return potential_objects[0].Object


def _do_selection_objects_contain_type(selection_objects, object_type):
    is_type_of_flags = map(
        lambda x: _is_selection_object_type_of(x, object_type),
        selection_objects)
    return any(is_type_of_flags)


def _is_selection_object_type_of(selection_object, object_type):
    return selection_object.Object.Proxy.Type == object_type
