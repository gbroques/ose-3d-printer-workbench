
from ose3dprinter.app.enums import AxisOrientation

from .add_axis_base import AddAxisBase


class AddZAxis:
    """
    Command to add Z Axis object.
    """

    NAME = 'AddZAxis'

    def __init__(self):
        self.base = AddAxisBase(AxisOrientation.Z)

    def Activated(self):
        self.base.Activated()

    def IsActive(self):
        return self.base.IsActive()

    def GetResources(self):
        return self.base.GetResources()
