
from .add_universal_axis_base import AddUniversalAxisBase


class AddUniversalXAxis:
    """
    Command to add Universal X Axis object.
    """

    NAME = 'AddUniversalXAxis'

    def __init__(self):
        self.base = AddUniversalAxisBase('x')

    def Activated(self):
        self.base.Activated()

    def IsActive(self):
        return self.base.IsActive()

    def GetResources(self):
        return self.base.GetResources()
