
from ose3dprinter.app.enums import AxisOrientation

from .add_axis_base import AddAxisBase


class AddXAxis:
    """
    Command to add X Axis object.
    """

    NAME = 'AddXAxis'

    def __init__(self):
        self.base = AddAxisBase(AxisOrientation.X)

    def Activated(self):
        self.base.Activated()

    def IsActive(self):
        return self.base.IsActive()

    def GetResources(self):
        return self.base.GetResources()
