import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console, Placement, Rotation, Vector
from ose3dprinter_workbench.part import create_universal_axis
from ose3dprinter_workbench.resources import get_resource_path

from .enums import AxisOrientation
from .get_axis_frame_attachment_kwargs import (
    AxisFrameAttachmentError, get_axis_frame_attachment_kwargs)
from .get_placement_strategy import (get_rotation_for_front_face,
                                     get_rotation_for_left_face)


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
        return get_axis_frame_attachment_kwargs(selection, axis_orientation)
    except AxisFrameAttachmentError as reason:
        log_message_template = '{}. Placing axis in default position.\n'
        Console.PrintMessage(log_message_template.format(reason))
        return {}
    else:
        return get_default_axis_creation_kwargs(axis_orientation)


def get_default_axis_creation_kwargs(axis_orientation):
    rotation = get_rotation(axis_orientation)
    placement = Placement(Vector(), rotation, Vector())
    origin_translation_offset = get_origin_translation_offset(
        axis_orientation)
    return {
        'placement': placement,
        'origin_translation_offset': origin_translation_offset
    }


def get_rotation(axis_orientation):
    return {
        AxisOrientation.X: Rotation(),
        AxisOrientation.Y: get_rotation_for_left_face(),
        AxisOrientation.Z: get_rotation_for_front_face()
    }[axis_orientation]


def get_origin_translation_offset(axis_orientation):
    return {
        AxisOrientation.X: Vector(),
        AxisOrientation.Y: Vector(-1, -1, 0),
        AxisOrientation.Z: Vector(0, -1, -1)
    }[axis_orientation]
