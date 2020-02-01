from FreeCAD import Placement, Vector

from .universal_axis_model import UniversalAxisModel


def create_universal_axis(document,
                          name,
                          length=304.80,
                          placement=Placement(),
                          translation_reference_point=Vector()):
    """
    Creates a universal axis object with the given name,
    and adds it to the document.
    """
    obj = document.addObject('Part::FeaturePython', name)
    UniversalAxisModel(obj, length, placement, translation_reference_point)
    obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
