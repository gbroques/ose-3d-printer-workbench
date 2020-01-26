from collections import OrderedDict
from importlib import import_module

package = 'ose3dprinter_workbench.command_registry'
ose_3d_printer = import_module('.OSE-3D-Printer', package=package)
base_registry = ose_3d_printer.base_registry


class CommandRegistry:
    """
    Registry of commands for toolbars, menus, and context menu.
    """

    def __init__(self, registry_name):
        """
        :param registry_name: Name of toolbar, menu, sub-menu, or context menu.
        """
        self.name = registry_name
        self.command_by_name = OrderedDict()

    def register(self, name, command):
        self.command_by_name[name] = command
        if not base_registry.has_name(name):
            base_registry.register(name, command)

    @property
    def keys(self):
        names = self.command_by_name.keys()
        prepend_namespace = base_registry.prepend_namespace
        return list(map(prepend_namespace, names))
