"""Parts for 3D Printer."""
from ._axis import Axis
from ._extruder import Extruder
from ._frame import AngledBarFrame, AngleFrameConnector, CNCCutFrame
from ._heated_bed import HeatedBed

__all__ = [
    'AngleFrameConnector',
    'AngledBarFrame',
    'Axis',
    'CNCCutFrame',
    'Extruder',
    'HeatedBed'
]
