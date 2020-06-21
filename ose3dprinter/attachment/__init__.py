"""Attachment functions to make 3D Printer parts appear attached to each other.
"""
from ._get_axis_frame_attachment_kwargs import (
    get_axis_frame_attachment_kwargs, get_default_axis_creation_kwargs)
from ._get_extruder_axis_attachment_kwargs import \
    get_extruder_axis_attachment_kwargs
from ._get_heated_bed_frame_axis_attachment_kwargs import \
    get_heated_bed_frame_axis_attachment_kwargs

__all__ = [
    'get_axis_frame_attachment_kwargs',
    'get_default_axis_creation_kwargs',
    'get_extruder_axis_attachment_kwargs',
    'get_heated_bed_frame_axis_attachment_kwargs'
]
