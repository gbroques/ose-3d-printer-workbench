from FreeCAD import Placement, Vector
from ose3dprinter.app.three_dimensional_space_enums import Axis, Side
from ose3dprinter.app.model import AxisModel


def create_axis(document,
                name,
                length=304.80,
                carriage_position=50,
                orientation=Axis.X,
                side=Side.TOP,
                placement=Placement(),
                origin_translation_offset=Vector()):
    """
    Creates a axis object with the given name,
    and adds it to the document.
    """
    obj = document.addObject('Part::FeaturePython', name)
    AxisModel(obj,
              length,
              carriage_position,
              orientation,
              side,
              placement,
              origin_translation_offset)
    obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
