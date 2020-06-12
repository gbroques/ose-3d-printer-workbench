:fcicon:`Add X Axis Command (md) <XAxis.svg>` Add Axis
======================================================
There a three tools in the main toolbar to add a Axis, or :osewikipage:`Universal Axis` object in different orientations to the **active** document:

1. :fcicon:`X Axis Icon (md) <XAxis.svg>` Add X Axis
2. :fcicon:`Y Axis Icon (md) <YAxis.svg>` Add Y Axis
3. :fcicon:`Z Axis Icon (md) <ZAxis.svg>` Add Z Axis

Custom Properties
-----------------
.. fc-custom-property-table:: ose3dprinter.model.axis.axis_model.AxisModel

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
