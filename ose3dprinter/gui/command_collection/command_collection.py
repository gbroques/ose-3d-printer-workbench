class CommandCollection:
    """
    Collection of commands for toolbars, menus, sub-menus, and context menu.
    """

    def __init__(self, collection_name):
        """
        :param collection_name: Name of toolbar, menu, sub-menu, or context menu.
        """
        self.name = collection_name
        self.command_keys = []

    def add(self, command_key):
        if command_key in self.command_keys:
            message = '"{}" command already added to "{}" collection.'
            raise ValueError(message.format(command_key, self.name))
        self.command_keys.append(command_key)
