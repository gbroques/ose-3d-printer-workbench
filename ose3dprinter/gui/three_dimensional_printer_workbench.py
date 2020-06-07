import FreeCAD as App
import FreeCADGui as Gui


class ThreeDimensionalPrinterWorkbench(Gui.Workbench):
    """
    3D Printer Workbench
    """

    def __init__(self):
        from .icon import get_icon_path

        cls = self.__class__
        cls.MenuText = 'OSE 3D Printer'
        cls.ToolTip = \
            'A workbench for designing 3D printers by Open Source Ecology'
        cls.Icon = get_icon_path('Frame.svg')

    def Initialize(self):
        """
        Executed when FreeCAD starts
        """
        import ose3dprinter.gui.OSE_3D_Printer as registry

        main_toolbar, main_menu = registry.register_commands()

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
