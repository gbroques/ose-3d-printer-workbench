"""
The filename where Gui.addCommand is executed,
is used to group commands together.
"""

from collections import OrderedDict

import FreeCADGui as Gui


class BaseCommandRegistry:

    def __init__(self):
        self.command_by_key = OrderedDict()

    def register(self, name, command):
        """Registers command by prepending each name with a unique namespace.

        :param name: Name of command. Must be unique within scope of workbench.
        :param command: Command instance (e.g. MyCommand())
        """
        key = self.prepend_namespace(name)
        self.command_by_key[key] = command
        Gui.addCommand(key, command)

    def has_name(self, name):
        key = self.prepend_namespace(name)
        return key in self.command_by_key

    @classmethod
    def prepend_namespace(cls, name):
        namespace = 'OSE3DP'
        return '{}_{}'.format(namespace, name)

    @property
    def keys(self):
        return self.command_by_key.keys()


# Singleton base registry
base_registry = BaseCommandRegistry()
