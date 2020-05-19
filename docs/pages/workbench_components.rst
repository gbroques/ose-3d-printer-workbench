Workbench Components
====================

Repository and Base Package
---------------------------
Every OSE workbench has the same structure and components to make working between various workbenches easier, and increase collaboriation.

First, all code for a particular workbench is located within it's own repository that contains a single top-level base package.

Repositories are named ``ose-{machine}-workbench``, and the base is named ``ose{{machine}}``.

For example, the OSE workbench for designing 3d printers has a repository named ``ose-3d-printer-workbench`` and base ``ose3dprinter`` package.

The one exception is the ``InitGui.py`` file located within the root of the repository which will be discussed later after the main components and structure of the workbench are discussed.

Base Package Structure: App & Gui
---------------------------------
The base package is separated into two main sub-packages: ``app`` and ``gui``.

At a high-level, the ``app`` package contains code related to the geometry of parts, and how those parts relate to each other.

While the ``gui`` package contains code related to the graphical user interface of FreeCAD such as what happens when buttons are clicked, or various components the user will interact with like dialogs and panels.

Code in the ``gui`` package may call code in the ``app`` package, while **the reverse is not true**.

The main goal of this rule is to decouple machine-specific knowledge, such as the geometry of parts, from it's graphical representation.

In doing so, other frontends besides FreeCAD's GUI can be used to display and interact with OSE's machines. For example, imagine other desktop, web, or mobile applications.

Reasons for this structure are discussed further in `App Gui Architecture <app_gui_architecture.html>`_ .

Gui Package
-----------

Workbench Class
^^^^^^^^^^^^^^^
Every workbench will have a class within the ``gui`` package that extends ``Gui.Workbench``.

For example, the **workbench class** for OSE's Tractor Workbench will be located within the ``osetractor.gui`` package and inside the ``tractor_workbench.py`` module:

.. code-block:: python

    import FreeCADGui as Gui


    class TractorWorkbench(Gui.Workbench):
        ...


App Package
-----------

Model Classes
^^^^^^^^^^^^^
