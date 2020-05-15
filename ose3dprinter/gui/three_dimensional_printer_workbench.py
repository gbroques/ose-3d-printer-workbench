
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
        from importlib import import_module
        ose_3d_printer = import_module(
            '.OSE-3D-Printer', package='ose3dprinter.gui')

        main_toolbar, main_menu = ose_3d_printer.register_commands()

        self.appendToolbar(main_toolbar.name, main_toolbar.command_keys)
        self.appendMenu(main_menu.name, main_menu.command_keys)

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
