from collections import OrderedDict

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
        self.commandByKey = OrderedDict()

    def register(self, name, command):
        """Register a command prepending each name with a "OSE3DP" namespace.

        :param name: Name of command. Must be unique.
        :param command: Command instance (e.g. MyCommand())
        """
        namespace = 'OSE3DP'
        key = '{}_{}'.format(namespace, name)
        self.commandByKey[key] = command
        Gui.addCommand(key, command)

    @property
    def keys(self):
        return self.commandByKey.keys()


command_registry = register()
