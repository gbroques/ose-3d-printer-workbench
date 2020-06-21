import FreeCAD as App
import FreeCADGui as Gui

from .icon import get_icon_path
from .OSE_3D_Printer import register_commands


class ThreeDimensionalPrinterWorkbench(Gui.Workbench):
    """
    3D Printer Workbench
    """
    MenuText = 'OSE 3D Printer'
    ToolTip = \
        'A workbench for designing 3D printers by Open Source Ecology (OSE)'
    Icon = get_icon_path('Frame.svg')

    def Initialize(self):
        """
        Executed when FreeCAD starts
        """

        main_toolbar, main_menu = register_commands()

        self.appendToolbar('OSE 3D Printer', main_toolbar)
        self.appendMenu('OSE 3D Printer', main_menu)

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
