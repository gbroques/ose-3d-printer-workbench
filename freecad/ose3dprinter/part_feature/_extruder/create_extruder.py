from FreeCAD import Placement, Vector
from ose3dprinter.model import ExtruderModel


def create_extruder(document,
                    name,
                    placement=Placement(),
                    origin_translation_offset=Vector()):
    """
    Creates a extruder object with the given name,
    and adds it to the document.
    """
    obj = document.addObject('Part::FeaturePython', name)
    ExtruderModel(obj, placement, origin_translation_offset)
    obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
