|X Axis Icon| Add Axis
==========================================

There a three tools in the main toolbar to add a Axis, or :osewikipage:`Universal Axis` object in different orientations to the **active** document:

1. |X Axis Icon| Add X Axis
2. |Y Axis Icon| Add Y Axis
3. |Z Axis Icon| Add Z Axis

.. |X Axis Icon| image:: /../ose3dprinter/gui/icon/XAxis.svg
   :height: 32px
   :width: 32px
   :alt: Add X Axis Icon

.. |Y Axis Icon| image:: /../ose3dprinter/gui/icon/YAxis.svg
   :height: 32px
   :width: 32px
   :alt: Add Y Axis Icon

.. |Z Axis Icon| image:: /../ose3dprinter/gui/icon/ZAxis.svg
   :height: 32px
   :width: 32px
   :alt: Add Z Axis Icon

Custom Properties
-----------------
.. csv-table::
   :file: ../property_table/AxisModelPropertyTable.csv
   :header-rows: 1

Attaching Axes to the Frame
---------------------------
You may attach axes to the frame by selecting one of it's outer faces, and then clicking a button in the main toolbar to add a axis.

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

The axis-frame attachment logic assumes the frame is **not** rotated, and determines whether the user is attaching the axis to the appropriate side of the frame based on whether the selected face is parallel to the XY, YZ, or XZ plane.

.. Tip:: See the **Report View** for attachment troubleshooting.
