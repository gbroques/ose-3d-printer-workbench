"""
The filename where Gui.addCommand is executed,
is used to group commands together.
"""
import FreeCADGui as Gui


class CommandRegistry:

    def __init__(self, namespace):
        self.namespace = namespace
        self.command_keys = []

    def register(self, command_name, command):
        """Registers command by prepending each command name with a unique namespace.

        :param command_name: Name of command. Must be unique within scope of workbench.
        :param command: Command instance (e.g. MyCommand())
        """
        key = self.from_command_name_to_key(command_name)
        if key in self.command_keys:
            raise ValueError('{} is already registered.'.format(command_name))
        self.command_keys.append(key)
        Gui.addCommand(key, command)

    def from_command_name_to_key(self, command_name):
        return '{}_{}'.format(self.namespace, command_name)


# Singleton registry for commands.
command_namespace = 'OSE3DP'
command_registry = CommandRegistry(command_namespace)
