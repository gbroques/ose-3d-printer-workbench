
from ose3dprinter.core.enums import AxisOrientation

from .add_universal_axis_base import AddUniversalAxisBase


class AddUniversalZAxis:
    """
    Command to add Universal Z Axis object.
    """

    NAME = 'AddUniversalZAxis'

    def __init__(self):
        self.base = AddUniversalAxisBase(AxisOrientation.Z)

    def Activated(self):
        self.base.Activated()

    def IsActive(self):
        return self.base.IsActive()

    def GetResources(self):
        return self.base.GetResources()
