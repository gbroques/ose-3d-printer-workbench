
from ose3dprinter.app.enums import AxisOrientation

from .add_axis_base import AddAxisBase


class AddYAxis:
    """
    Command to add Y Axis object.
    """

    NAME = 'AddYAxis'

    def __init__(self):
        self.base = AddAxisBase(AxisOrientation.Y)

    def Activated(self):
        self.base.Activated()

    def IsActive(self):
        return self.base.IsActive()

    def GetResources(self):
        return self.base.GetResources()
