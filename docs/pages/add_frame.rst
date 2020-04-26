|Frame Icon| Add Frame
======================

.. |Frame Icon| image:: /../ose3dprinter/gui/resources/Frame.svg
   :height: 32px
   :width: 32px
   :alt: Add Frame Command

The **Add Frame** tool adds a Frame to the **active** document.

You can use this to begin to design a :osewikipage:`D3D Pro` printer of any size or axis configuration.

Custom Properties
-----------------
.. csv-table::
   :file: FrameModelPropertyTable.csv
   :header-rows: 1

Attaching Axes to the Frame
---------------------------
You may attach axes to the frame by selecting one of it's outer faces, and then clicking a button in the main toolbar to add a universal axis.

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

See also:

* :osewikipage:`Universal Axis`
* :osewikipage:`D3D Frame`