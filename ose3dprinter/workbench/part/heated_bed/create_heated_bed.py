from ose3dprinter.core.model import HeatedBedModel


def create_heated_bed(document, name):
    """
    Creates a heated bed object with the given name,
    and adds it to the document.
    """
    obj = document.addObject('Part::FeaturePython', name)
    HeatedBedModel(obj)
    obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
