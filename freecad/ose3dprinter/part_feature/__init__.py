"""Exposes functions to create Part::FeaturePython objects.

Minimally, these objects are custom, parameteric,
and have a Shape for viewing in three dimensions.

See Also:
    https://wiki.freecadweb.org/FeaturePython_Objects
    https://wiki.freecadweb.org/Creating_a_FeaturePython_Box,_Part_II
    https://wiki.freecadweb.org/Scripted_objects

Additionally, they may have a ViewProvider class
for providing additional customization to their 3d representation,
and how they respond to certain graphical interactions such as selection.

See Also:
    https://wiki.freecadweb.org/Viewprovider
"""
from ._axis import create_axis
from ._extruder import create_extruder
from ._frame import create_frame
from ._heated_bed import create_heated_bed

__all__ = [
    'create_axis',
    'create_extruder',
    'create_frame',
    'create_heated_bed'
]
