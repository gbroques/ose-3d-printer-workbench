from FreeCAD import Placement, Vector

from ose3dprinter.app.model import UniversalAxisModel
from ose3dprinter.app.enums import AxisOrientation, Side


def create_universal_axis(document,
                          name,
                          length=304.80,
                          carriage_position=50,
                          orientation=AxisOrientation.X,
                          side=Side.TOP,
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
                       orientation,
                       side,
                       placement,
                       origin_translation_offset)
    obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
