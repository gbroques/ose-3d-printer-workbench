import FreeCAD as App
import FreeCADGui as Gui
from ose3dprinter.core.get_heated_bed_frame_centered_kwargs import \
    get_heated_bed_frame_centered_kwargs
from ose3dprinter.core.model import FrameModel
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
    if is_frame_selected(selection_objects):
        frame = selection_objects[0].Object
        return get_heated_bed_frame_centered_kwargs(frame)
    else:
        return {}


def is_frame_selected(selection_objects):
    return _is_object_selected(selection_objects, FrameModel.Type)


def _is_object_selected(selection_objects, objectType):
    return (len(selection_objects) > 0 and
            selection_objects[0].Object.Proxy.Type == objectType)
