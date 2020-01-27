from importlib import import_module

package = 'ose3dprinter_workbench.registry'
ose_3d_printer = import_module('.OSE-3D-Printer', package=package)
registry = ose_3d_printer.registry


class CommandCollection:
    """
    Collection of commands for toolbars, menus, and context menu.
    """

    def __init__(self, collection_name):
        """
        :param collection_name: Name of toolbar, menu, sub-menu, or context menu.
        """
        self.name = collection_name
        self.command_names = []

    def add(self, name):
        if name in self.command_names:
            raise ValueError('{} already added to {}.'.format(name, self.name))
        if not registry.has(name):
            raise ValueError('{} must be registered first.'.format(name))
        self.command_names.append(name)

    @property
    def commands(self):
        names = self.command_names
        prepend_namespace = registry.prepend_namespace
        return list(map(prepend_namespace, names))
