Generate Rod Cut List
=====================

There are two options in the main menu to generate a rod cut list:

1. |Copy Icon| Copy Rod Cut List to Clipboard
2. |Save Icon| Save Rod Cut List to CSV


.. |Copy Icon| image:: /../ose3dprinter/gui/resources/edit-copy.svg
   :height: 32px
   :width: 32px
   :alt: Copy Rod Cut List to Clipboard Command

.. |Save Icon| image:: /../ose3dprinter/gui/resources/document-save-as.svg
   :height: 32px
   :width: 32px
   :alt: Save Rod Cut List to CSV

How it Works
------------
Both options query the **active** document for Universal Axis objects and the Frame object in order to determine the rods for the cut list.

Determining Rod Quantity
^^^^^^^^^^^^^^^^^^^^^^^^
* **2** X Axis Rods are added for every X Axis object
* **2** Y Axis Rods are added or every Y Axis object
* **2** Z Axis Rods are added for every Z Axis object
* **2** Spool Holder Rods & **3** Heated Bed Rods are added for every Frame object

Determining Rod Length
^^^^^^^^^^^^^^^^^^^^^^
* X Axis Rod Length is adjusted by **adding 4 inches**
* Y Axis Rod Length corresponds with ``Length`` of the axis in the document
* Z Axis Rod Length is adjusted by **subtracting 1 inch**
* Length of **2** Heated Bed Rods and **1** Spool Holder Rod are equal to the length of the Frame
* Length of **2** Spool Holder Rods are equal to the length of the Frame **minus 1 inch** (similar to Z axis rods)
