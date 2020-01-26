import FreeCADGui as Gui

from .AddFrame import AddFrame
from .AddUniversalAxis import AddUniversalAxis


def register():
    registry = CommandRegistry()

    registry.register('AddFrame', AddFrame())
    registry.register('AddUniversalAxis', AddUniversalAxis())

    return registry


class CommandRegistry:

    def __init__(self):
        self.commandByName = {}

    def register(self, name, command):
        """Register a command.

        :param name: Name of command. Must be unique.
        :param command: Command instance (e.g. MyCommand())
        """
        self.commandByName[name] = command
        Gui.addCommand(name, command)

    def get_command_names(self):
        return self.commandByName.keys()


registry = register()
