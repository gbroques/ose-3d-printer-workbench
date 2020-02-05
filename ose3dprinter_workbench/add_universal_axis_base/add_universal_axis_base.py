import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console, Placement, Rotation, Vector
from ose3dprinter_workbench.part import create_universal_axis
from ose3dprinter_workbench.resources import get_resource_path

from .enums import AxisOrientation
from .get_axis_frame_attachment_kwargs import get_axis_frame_attachment_kwargs
from .get_placement_strategy import (get_rotation_for_front_face,
                                     get_rotation_for_left_face)
from .validate_frame_face_selection import validate_frame_face_selection


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
        selection = Gui.Selection.getSelectionEx()
        is_valid, reason = validate_frame_face_selection(
            selection, self.axis_orientation)
        kwargs = get_creation_kwargs(
            is_valid, reason, selection, self.axis_orientation)
        name = 'Universal{}Axis'.format(self.axis_orientation.upper())
        axis = create_universal_axis(document, name, **kwargs)
        document.recompute()
        if not is_valid:
            translation = get_post_creation_translation_vector(
                axis, self.axis_orientation)
            placement = Placement()
            placement.move(translation)
            axis.Placement = placement
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


def get_creation_kwargs(is_valid, reason, selection, axis_orientation):
    if is_valid:
        return get_axis_frame_attachment_kwargs(selection, axis_orientation)
    else:
        log_invalid_selection_reason(reason)
        placement, translation_reference_point = get_placement_and_translation_reference_point(
            axis_orientation)
        return {
            'placement': placement,
            'translation_reference_point': translation_reference_point
        }


def log_invalid_selection_reason(reason):
    log_message_template = '{}. Skipping attachment of axis to frame.\n'
    Console.PrintMessage(log_message_template.format(reason))


def get_placement_and_translation_reference_point(axis_orientation):
    rotation = get_rotation(axis_orientation)
    translation_reference_point = get_translation_reference_point(
        axis_orientation)
    return Placement(Vector(), rotation, Vector()), translation_reference_point


def get_rotation(axis_orientation):
    return {
        AxisOrientation.X: Rotation(),
        AxisOrientation.Y: get_rotation_for_left_face(),
        AxisOrientation.Z: get_rotation_for_front_face()
    }[axis_orientation]


def get_translation_reference_point(axis_orientation):
    return {
        AxisOrientation.X: Vector(),
        AxisOrientation.Y: Vector(-1, 0, 0),
        AxisOrientation.Z: Vector(0, -1, 0)
    }[axis_orientation]


def get_post_creation_translation_vector(axis, axis_orientation):
    if axis_orientation == AxisOrientation.X:
        return Vector()
    if axis_orientation == AxisOrientation.Y:
        return Vector(0, axis.Length, 0)
    if axis_orientation == AxisOrientation.Z:
        return Vector(0, 0, axis.Length)
