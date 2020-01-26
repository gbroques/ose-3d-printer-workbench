from .universal_axis_model import UniversalAxisModel


def create_universal_axis(document, name):
    """
    Creates a universal axis object with the given name,
    and adds it to the document.
    """
    obj = document.addObject('Part::FeaturePython', name)
    UniversalAxisModel(obj)
    obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
