from ose3dprinter.app.model import FrameModel


def create_frame(document, name):
    """
    Creates a frame object with the given name,
    and adds it to the document.
    """
    obj = document.addObject('Part::FeaturePython', name)
    FrameModel(obj)
    obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded
    return obj
