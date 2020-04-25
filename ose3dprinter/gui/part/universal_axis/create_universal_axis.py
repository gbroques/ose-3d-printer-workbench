from FreeCAD import Placement, Vector

from ose3dprinter.app.model import UniversalAxisModel


def create_universal_axis(document,
                          name,
                          length=304.80,
                          carriage_position=50,
                          placement=Placement(),
                          origin_translation_offset=Vector()):
    """
    Creates a universal axis object with the given name,
    and adds it to the document.
    """
    obj = document.addObject('Part::FeaturePython', name)
    UniversalAxisModel(obj,
                       length,
                       carriage_position,
                       placement,
                       origin_translation_offset)
    if obj.ViewObject is not None:
        obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
