class Model:
    """
    Base class for models that encapsulate the data (i.e. topography and shape)
    for a part, and is separate from the "view" or GUI representation.
    """

    def __init__(self, obj):
        """
        Constructor

        Arguments
        ---------
        - obj: Created with document.addObject('Part::FeaturePython', '{name}')
        """
        self.Object = obj

        obj.Proxy = self

    def onDocumentRestored(self, fp):
        """Executed after a document is restored,
        or a FeaturePython object is copied or duplicated.

        :param fp: Custom feature python object
        :type fp: Part::FeaturePython
        """
        self.Object = fp
