|Angle Frame Connector Icon| Make Angle Frame Connector
=======================================================

.. |Angle Frame Connector Icon| image:: /../ose3dprinter/gui/resources/Std_CoordinateSystem.svg
   :height: 32px
   :width: 32px
   :alt: Make Angle Frame Connecto Command

The **Make Angle Frame Connector** tool makes a 3D-printable :osewikipage:`Angle Frame Connector` with the specified **parameters** entered from the Task Panel.

.. image:: /_static/make-angle-frame-connector.png
   :alt: Make Angle Frame Connector

Parameters
----------

:Slot Width: Width of three inner slots.
:Slot Thickness: Thickness of three inner slots.
:Orientation: One of eight possible corners of the frame.
:Add Set Screw: Whether to add a set screw mechanism.

  Useful for larger frames when worried about slips or frame mis-alignment.
  
  .. Attention:: Assumes **M6** set-screw and nut.
:Add Filleting: Whether to round edges of three inner slots.

  .. Tip:: Makes inserting angled bars later a little easier.

See Also
--------

* `FreeCAD Wiki - Export to STL or OBJ <https://wiki.freecadweb.org/Export_to_STL_or_OBJ>`_
