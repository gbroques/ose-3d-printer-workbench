"""
The filename where Gui.addCommand is executed,
is used to group commands together.
"""
import FreeCADGui as Gui


class CommandRegistry:

    def __init__(self):
        self.command_keys = []

    def register(self, name, command):
        """Registers command by prepending each name with a unique namespace.

        :param name: Name of command. Must be unique within scope of workbench.
        :param command: Command instance (e.g. MyCommand())
        """
        key = self.prepend_namespace(name)
        if key in self.command_keys:
            raise ValueError('{} is already registered.'.format(name))
        self.command_keys.append(key)
        Gui.addCommand(key, command)

    def has(self, name):
        key = self.prepend_namespace(name)
        return key in self.command_keys

    @classmethod
    def prepend_namespace(cls, name):
        namespace = 'OSE3DP'
        return '{}_{}'.format(namespace, name)

    @property
    def keys(self):
        return self.command_keys


# Singleton registry for commands.
registry = CommandRegistry()
