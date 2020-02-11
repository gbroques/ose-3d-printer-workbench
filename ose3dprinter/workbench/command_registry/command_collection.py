from importlib import import_module

command_registry = import_module(
    '.OSE-3D-Printer',
    package='ose3dprinter.workbench.command_registry'
).command_registry


class CommandCollection:
    """
    Collection of commands for toolbars, menus, and context menu.
    """

    def __init__(self, collection_name):
        """
        :param collection_name: Name of toolbar, menu, or context menu.
        """
        self.name = collection_name
        self.command_names = []

    def add(self, name):
        if name in self.command_names:
            raise ValueError('{} already added to {}.'.format(name, self.name))
        self.command_names.append(name)

    @property
    def command_keys(self):
        names = self.command_names
        to_key = command_registry.from_command_name_to_key
        return list(map(to_key, names))
