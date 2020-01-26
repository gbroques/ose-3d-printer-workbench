import FreeCADGui as Gui
import FreeCAD as App


class ThreeDimensionalPrinterWorkbench(Gui.Workbench):
    """
    3D Printer Workbench
    """

    def __init__(self):
        import os
        from InitWorkbench import ICON_PATH

        self.__class__.MenuText = 'OSE 3D Printer'
        self.__class__.ToolTip = \
            'A workbench for designing 3D printers by Open Source Ecology'
        self.__class__.Icon = os.path.join(ICON_PATH, 'Frame.svg')

    def Initialize(self):
        """
        Executed when FreeCAD starts
        """
        pass

    def Activated(self):
        """
        Executed when workbench is activated.
        """
        if not(App.ActiveDocument):
            App.newDocument()

    def Deactivated(self):
        """
        Executed when workbench is deactivated.
        """
        pass

    def GetClassName(self):
        return 'Gui::PythonWorkbench'


Gui.addWorkbench(ThreeDimensionalPrinterWorkbench())
