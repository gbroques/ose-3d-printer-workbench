from FreeCAD import Console

from .face_side_strategy_factory import FaceSideStrategyFactory
from .get_orientation_of_attachable_axis import \
    get_orientation_of_attachable_axis


def get_face_side(frame, face, axis_orientation):
    face_side_strategy = FaceSideStrategyFactory.create(axis_orientation)
    return face_side_strategy.get_face_side(frame, face)
