import FreeCAD as App
from FreeCAD import Console
from ose3dprinter.app.attachment import (
    AttachmentError, get_heated_bed_frame_axis_attachment_kwargs)
from ose3dprinter.app.model import AxisModel, FrameModel
from ose3dprinter.gui.icon import get_icon_path
from ose3dprinter.gui.part import create_heated_bed
from ose3dprinter.gui.selection_object import find_selection_object_by_type


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
            'Pixmap': get_icon_path('HeatedBed.svg'),
            'MenuText': 'Add Heated Bed',
            'ToolTip': 'Add Heated Bed'
        }


def get_heated_bed_creation_kwargs():
    try:
        frame, axis = find_frame_and_axis_in_selection()
        return get_heated_bed_frame_axis_attachment_kwargs(frame, axis)
    except AttachmentError as reason:
        log_message_template = '{}. Placing heated bed in default position.\n'
        Console.PrintMessage(log_message_template.format(reason))
        return {}


def find_frame_and_axis_in_selection():
    frame_selection_object = find_selection_object_by_type(FrameModel.Type)
    axis_selection_object = find_selection_object_by_type(AxisModel.Type)
    if frame_selection_object is None or axis_selection_object is None:
        raise AttachmentError('Must select Frame and Axis')
    return frame_selection_object.Object, axis_selection_object.Object
