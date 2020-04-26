App Gui Architecture
====================
FreeCAD is made from the beginning to work as a command-line application without its user interface.
Therefore, almost everything is separated between a "geometry" component and a "visual" component.
When you execute FreeCAD in command-line mode, the geometry part is present, but the visual part is absent.

For more information see `"Python scripting tutorial - App and Gui", on the FreeCAD Wiki <https://wiki.freecadweb.org/Python_scripting_tutorial#App_and_Gui>`_.

The OSE 3D Printer Workbench mirrors this in it's top-level package structure for the following reasons:

* Provide the ability to run the ``app`` package from a command-line context, similar to FreeCAD
* Encapsulate logic in the ``app`` package, and keep the ``gui`` package "dumb" 
* Make the ``app`` package easy to write unit tests for
