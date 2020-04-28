import unittest

import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.app.enums import Plane, Side
from ose3dprinter.app.exceptions import AttachmentError
from ose3dprinter.app.get_axis_frame_attachment_kwargs import \
    get_axis_frame_attachment_kwargs
from ose3dprinter.app.get_outer_faces_of_cnc_cut_frame import \
    get_outer_faces_of_cnc_cut_frame
from ose3dprinter.app.is_face_parallel_to_plane import (
    is_face_parallel_to_xy_plane, is_face_parallel_to_xz_plane,
    is_face_parallel_to_yz_plane)
from ose3dprinter.app.model import FrameModel

from .freecad_test_case import FreeCADTestCase


class GetAxisFrameAttachmentKwargsForCNCCutFrameTest(FreeCADTestCase):

    @classmethod
    def setUpClass(cls):
        document = App.newDocument()
        cls.frame = document.addObject('Part::FeaturePython', 'Frame')
        FrameModel(cls.frame)
        document.recompute()
        cls.faces_by_side = get_faces_by_side(cls.frame)

    def test_get_axis_frame_attachment_kwargs_for_top_face(self):
        top_face = self.faces_by_side[Side.TOP]

        result = get_axis_frame_attachment_kwargs(self.frame, top_face, 'x')

        expected = {
            'origin_translation_offset': Vector(0.0, 0.5, 0.0),
            'placement': Placement(
                Vector(0, self.frame.Size / 2, self.frame.Size),
                Rotation()
            )
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_left_face(self):
        left_face = self.faces_by_side[Side.LEFT]

        result = get_axis_frame_attachment_kwargs(self.frame, left_face, 'y')

        expected = {
            'origin_translation_offset': Vector(0, 0, 1),
            'placement': Placement(
                Vector(0, self.frame.Size, self.frame.Size),
                Rotation(-90, 0, 90),
                Vector()
            )
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_right_face(self):
        right_face = self.faces_by_side[Side.RIGHT]

        result = get_axis_frame_attachment_kwargs(self.frame, right_face, 'y')

        expected = {
            'origin_translation_offset': Vector(0, 0, 0),
            'placement': Placement(
                Vector(self.frame.Size, self.frame.Size, self.frame.Size),
                Rotation(-90, 0, -90),
                Vector()
            )
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_front_face(self):
        front_face = self.faces_by_side[Side.FRONT]

        result = get_axis_frame_attachment_kwargs(self.frame, front_face, 'z')

        expected = {
            'origin_translation_offset': Vector(0.5, 0, 0),
            'placement': Placement(
                Vector(self.frame.Size / 2, 0, self.frame.Size),
                Rotation(0, 90, 90),
                Vector()
            )
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_rear_face(self):
        rear_face = self.faces_by_side[Side.REAR]

        result = get_axis_frame_attachment_kwargs(self.frame, rear_face, 'z')

        expected = {
            'origin_translation_offset': Vector(-0.5, 0, 0),
            'placement': Placement(
                Vector(self.frame.Size / 2, self.frame.Size, self.frame.Size),
                Rotation(0, 90, -90),
                Vector()
            )
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_bottom_face(self):
        bottom_face = self.faces_by_side[Side.BOTTOM]

        with self.assertRaises(AttachmentError):
            get_axis_frame_attachment_kwargs(self.frame, bottom_face, 'x')

    def assert_result_and_expected_are_equal(self, result, expected):
        self.assertEqual(result['origin_translation_offset'],
                         expected['origin_translation_offset'])
        self.assertEqual(result['length'].Value, self.frame.Size)
        self.assertPlacementEqual(result['placement'], expected['placement'])


def get_faces_by_side(cnc_cut_frame):
    """Gets a dictionary of outer faces of the frame by their Side.

    TODO: Should this be in ose3dprinter.app package instead of a test?

    :param cnc_cut_frame: CNC Cut Frame (frame without corners)
    :type cnc_cut_frame: Document Object
    :return: Dictionary where the keys are a Side, and value is a Face
    :rtype: dict
    """
    faces_by_side = {}
    outer_faces = get_outer_faces_of_cnc_cut_frame(cnc_cut_frame)
    for outer_face in outer_faces:
        parallel_plane = get_parallel_plane(outer_face)
        is_face_parallel_to_plane = get_is_parallel_to_plane_predicate(
            parallel_plane)
        outer_faces_parallel_to_plane = filter(
            is_face_parallel_to_plane, outer_faces)
        perpendicular_axis_to_plane = get_perpendicular_axis_to_plane(
            parallel_plane)
        sorted_faces_by_position = sorted(
            outer_faces_parallel_to_plane,
            key=lambda f: getattr(f.Surface.Position, perpendicular_axis_to_plane))
        side_index = 0 if sorted_faces_by_position[0].isEqual(
            outer_face) else 1
        ordered_sides_by_plane = {
            Plane.XY: [Side.BOTTOM, Side.TOP],
            Plane.YZ: [Side.LEFT, Side.RIGHT],
            Plane.XZ: [Side.FRONT, Side.REAR]
        }
        side = ordered_sides_by_plane[parallel_plane][side_index]
        faces_by_side[side] = outer_face

    return faces_by_side


def get_is_parallel_to_plane_predicate(plane):
    return {
        Plane.XY: is_face_parallel_to_xy_plane,
        Plane.YZ: is_face_parallel_to_yz_plane,
        Plane.XZ: is_face_parallel_to_xz_plane
    }[plane]


def get_parallel_plane(face):
    """
    Returns which plane the face is parallel to
    """
    if is_face_parallel_to_xy_plane(face):
        return Plane.XY
    elif is_face_parallel_to_yz_plane(face):
        return Plane.YZ
    elif is_face_parallel_to_xz_plane(face):
        return Plane.XZ
    else:
        raise ValueError('Face must be parallel to XY, YZ, or XZ plane.')


def get_perpendicular_axis_to_plane(plane):
    return {
        Plane.XY: 'z',
        Plane.YZ: 'x',
        Plane.XZ: 'y'
    }[plane]


if __name__ == '__main__':
    unittest.main()
