|Universal X Axis Icon| Add Universal Axis
==========================================

There a three tools in the main toolbar to add a :osewikipage:`Universal Axis` object in different orientations to the **active** document:

1. |Universal X Axis Icon| Add Universal X Axis
2. |Universal Y Axis Icon| Add Universal Y Axis
3. |Universal Z Axis Icon| Add Universal Z Axis

.. |Universal X Axis Icon| image:: /../ose3dprinter/gui/resources/UniversalXAxis.svg
   :height: 32px
   :width: 32px
   :alt: Add Universal X Axis Icon

.. |Universal Y Axis Icon| image:: /../ose3dprinter/gui/resources/UniversalYAxis.svg
   :height: 32px
   :width: 32px
   :alt: Add Universal Y Axis Icon

.. |Universal Z Axis Icon| image:: /../ose3dprinter/gui/resources/UniversalZAxis.svg
   :height: 32px
   :width: 32px
   :alt: Add Universal Z Axis Icon

Custom Properties
-----------------
.. csv-table::
   :file: UniversalAxisModelPropertyTable.csv
   :header-rows: 1

Attaching Axes to the Frame
---------------------------
You may attach axes to the frame by selecting one of it's outer faces, and then clicking a button in the main toolbar to add a universal axis.

.. image:: /_static/attaching-axes-to-frame.gif
   :alt: Attaching X, Y, and Z axes to Top, Right, and Front faces

Only certain axes can be attached to certain faces or sides of the frame based on it's orientation.

================ ==================
Axis Orientation Attachable Side(s)
================ ==================
X                Top
Y                Left, Right
Z                Front, Rear
================ ==================

**Note:** You cannot attach an axis to the **Bottom** face or side of the frame.

The axis-frame attachment logic assumes the frame is **not** rotated, and determines the whether the user is attaching the axis to the appropriate side based on whether the selected face of the frame is parallel to the XY, YZ, or XZ planes.

.. Tip:: See the **Report View** for attachment troubleshooting.
