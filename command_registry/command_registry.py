from collections import OrderedDict
from importlib import import_module

ose_3d_printer = import_module('.OSE-3D-Printer', package='command_registry')
base_registry = ose_3d_printer.base_registry


class CommandRegistry:

    def __init__(self):
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
