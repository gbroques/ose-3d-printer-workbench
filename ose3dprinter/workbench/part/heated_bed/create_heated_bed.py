from FreeCAD import Placement, Vector
from ose3dprinter.core.model import HeatedBedModel


def create_heated_bed(document,
                      name,
                      placement=Placement(),
                      origin_translation_offset=Vector()):
    """
    Creates a heated bed object with the given name,
    and adds it to the document.
    """
    obj = document.addObject('Part::FeaturePython', name)
    HeatedBedModel(obj, placement, origin_translation_offset)
    if obj.ViewObject is not None:
        obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
