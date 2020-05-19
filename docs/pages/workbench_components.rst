Workbench Components
====================

Repository and Base Package
---------------------------
Every OSE workbench has the same structure and components to make working between various workbenches easier, and increase collaboration.

First, all code for a particular workbench is located within it's own repository that contains a single top-level base package.

Repositories are named ``ose-{machine}-workbench``, and the base package is named ``ose{{machine}}``.

For example, the OSE workbench for designing 3d printers has a repository named ``ose-3d-printer-workbench`` and base ``ose3dprinter`` package.

The one exception is the ``InitGui.py`` file located within the root of the repository which will be discussed later after the main components and structure of the workbench are discussed.

Base Package Structure: App & Gui
---------------------------------
The base package is separated into two main sub-packages: ``app`` and ``gui``.

At a high-level, the ``app`` package contains code related to the geometry of parts, and how those parts relate to each other.

While the ``gui`` package contains code related to the graphical user interface of FreeCAD such as what happens when buttons are clicked, or various components the user may interact with like dialogs and panels.

Code in the ``gui`` package may reference code in the ``app`` package, while **the reverse is not true**.

The main goal of this rule is to decouple machine-specific knowledge, such as the geometry of parts, from it's graphical representation.

In doing so, other frontends besides FreeCAD's GUI can be used to display and interact with OSE's machines. For example, imagine other desktop, web, or mobile applications.

Reasons for this structure are discussed further in `App Gui Architecture <app_gui_architecture.html>`_ .

Gui Package
-----------

Workbench Class
^^^^^^^^^^^^^^^
Every workbench will have a **workbench class** within the ``gui`` package that extends ``Gui.Workbench``.

For example, the **workbench class** for OSE's Tractor Workbench will be located within the ``osetractor.gui`` package inside the ``tractor_workbench.py`` module:

.. code-block:: python

    import FreeCADGui as Gui


    class TractorWorkbench(Gui.Workbench):
        ...


Command Classes
^^^^^^^^^^^^^^^
`Commands in FreeCAD <https://wiki.freecadweb.org/Command>`_ are executed when users perform various actions in the workbench such as clicking a button in a toolbar or selecting an option in a menu.

App Package
-----------

Model Classes
^^^^^^^^^^^^^
Parts are often thought about as real world objects and therefore fit nicely in the paradigm of Object Oriented Programming (OOP) as **classes**.

How you structure your model class depends upon whether you want the user to be able to parametrically manipulate properties of the object after creation, or have the object be static.

While the desired use-case is often the former, the latter is simpler.

Static Geometry
"""""""""""""""

For example, you might have a ``Box`` class with a ``make`` method that encapsulates how to create the geometry of the box.

.. code-block:: python

    import Part


    class Box:

        @staticmethod
        def make():
            box = Part.makeBox(10, 10, 10)
            return box

While in this trivial example the ``Box`` class and ``make`` method doesn't provide much value, this abstraction offers a simple interface for "making" more complex and custom geometry.

For example, you may pass in the ``length`` and ``width`` into the ``make`` method as parameters for creating boxes of different sizes.

.. code-block:: python

    class Box:

        @staticmethod
        def make(length, width):
            height = 10
            box = Part.makeBox(length, width, height)
            return box

We could have defined a ``make_box`` **function** instead, but why is the ``class`` approach preferable?

Imagine the box is a **sub-part** of a more complex part, and that part needs to know about the static ``height`` of the box.

With a quick refactor, the parent part can now access the ``height`` of the ``Box`` as a static property, and that information stays close to the construction of the box geometry as opposed to being defined somewhere else in the program via constants or some other approach.

.. code-block:: python

    class Box:

        height = 10

        @classmethod
        def make(cls, length, width):
            box = Part.makeBox(length, width, cls.height)
            return box

Dynamic Geometry
""""""""""""""""
Our model class gets more complicated with parameteric properties the user can manipulate in FreeCAD's GUI within the `Property Editor <https://wiki.freecadweb.org/Property_editor>`_ after the box is created.

.. code-block:: python

    import Part


    class Box:

        def __init__(self, obj):
            self.Type = 'Box'

            obj.Proxy = self

            obj.addProperty('App::PropertyLength', 'Length',
                            'Dimensions', 'Box length').Length = 10.0
            obj.addProperty('App::PropertyLength', 'Width',
                            'Dimensions', 'Box width').Width = 10.0
            obj.addProperty('App::PropertyLength', 'Height',
                            'Dimensions', 'Box height').Height = 10.0

        def execute(self, obj):
            obj.Shape = Part.makeBox(obj.Length, obj.Width, obj.Height)

The constructor or ``__init__`` method initializes the parameteric properties, and the ``execute`` method handles the construction of the geometry.

While the dynamic model is more complicated, the principle in both is the same -- have a "model class" that encapsulates the construction of the geometry for a part.

For additional information on the dynamic example, see the FreeCAD Wiki on `FeaturePython Objects <https://wiki.freecadweb.org/FeaturePython_Objects>`_ and `Scripted Objects <https://wiki.freecadweb.org/Scripted_objects>`_.
