Command Registry and Collection Pattern
=======================================
Background
----------
A FreeCAD Command is executed every time a user clicks a toolbar button or selects a menu option.

When you register custom commands for an external workbench via ``FreeCADGui.addCommand(commandName, commandObject)``, FreeCAD adds the command to it's global command registry.

Avoiding Name Collisions & Ensuring Uniqueness
----------------------------------------------
To avoid name collisions and ensure uniqueness, a command name is typically prefixed with the name of the module and underscore. For example, "Part_Cylinder" or "OSE3DP_AddFrame".

The Command Registry pattern handles prefixing a unique namespace to the name of your command for you.

In this way, if in the future we need to change the name of our command namespace (e.g. "OSE3DP") because it collides with another external workbench, then the change is easy.

Grouping Commands Together by a Consistent Category
---------------------------------------------------
Additionally, FreeCAD derives a "Category" to organize commands from the name of the Python module in which ``FreeCADGui.addCommand`` is called.

Since all commands in the workbench are ultimately registered with ``FreeCADGui.addCommand`` in a Python module called ``OSE_3D_Printer.py`` via the Command Registry abstraction, the derived "Category" for grouping these commands is "OSE_3D_Printer".

.. image:: /_static/commands.png


Command Collection Pattern
--------------------------
When you need to add a collection of commands to a toolbar, file menu, or context menu in ``Gui.Workbench`` via ``self.appendToolbar``, ``self.appendMenu``, or ``self.appendContextMenu`` the Command Collection abstraction has knowledge of the unique command namespace and can retrieve those command keys for you via the ``command_keys`` property.
