import unittest

import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.app.attachment import (AttachmentError,
                                         get_axis_frame_attachment_kwargs)
from ose3dprinter.app.enums import AxisOrientation, Side
from ose3dprinter.app.model import FrameModel

from .freecad_test_case import FreeCADTestCase


class GetAxisFrameAttachmentKwargsForCNCCutFrameTest(FreeCADTestCase):

    @classmethod
    def setUpClass(cls):
        document = App.newDocument()
        cls.frame = document.addObject('Part::FeaturePython', 'Frame')
        FrameModel(cls.frame)
        document.recompute()

    def test_get_axis_frame_attachment_kwargs_for_top_face(self):
        top_face = self.frame.Proxy.get_faces_for_side(Side.TOP)[0]

        result = get_axis_frame_attachment_kwargs(
            self.frame, top_face, AxisOrientation.X)

        expected = {
            'origin_translation_offset': Vector(0.0, -0.5, 0.0),
            'placement': Placement(
                Vector(0, self.frame.Size / 2, self.frame.Size),
                Rotation()
            ),
            'orientation': AxisOrientation.X,
            'side': Side.TOP
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_left_face(self):
        left_face = self.frame.Proxy.get_faces_for_side(Side.LEFT)[0]

        result = get_axis_frame_attachment_kwargs(
            self.frame, left_face, AxisOrientation.Y)

        expected = {
            'origin_translation_offset': Vector(-1.0, 0.0, -1.0),
            'placement': Placement(
                Vector(0, 0, self.frame.Size),
                Rotation(),
                Vector()
            ),
            'orientation': AxisOrientation.Y,
            'side': Side.LEFT
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_right_face(self):
        right_face = self.frame.Proxy.get_faces_for_side(Side.RIGHT)[0]

        result = get_axis_frame_attachment_kwargs(
            self.frame, right_face, AxisOrientation.Y)

        expected = {
            'origin_translation_offset': Vector(0.0, 0.0, -1.0),
            'placement': Placement(
                Vector(self.frame.Size, 0, self.frame.Size),
                Rotation(),
                Vector()
            ),
            'orientation': AxisOrientation.Y,
            'side': Side.RIGHT
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_front_face(self):
        front_face = self.frame.Proxy.get_faces_for_side(Side.FRONT)[0]

        result = get_axis_frame_attachment_kwargs(
            self.frame, front_face, AxisOrientation.Z)

        expected = {
            'origin_translation_offset': Vector(-0.5, -1.0, 0.0),
            'placement': Placement(
                Vector(self.frame.Size / 2, 0, 0),
                Rotation(),
                Vector()
            ),
            'orientation': AxisOrientation.Z,
            'side': Side.FRONT
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_rear_face(self):
        rear_face = self.frame.Proxy.get_faces_for_side(Side.REAR)[0]

        result = get_axis_frame_attachment_kwargs(
            self.frame, rear_face, AxisOrientation.Z)

        expected = {
            'origin_translation_offset': Vector(-0.5, 0, 0),
            'placement': Placement(
                Vector(self.frame.Size / 2, self.frame.Size, 0),
                Rotation(),
                Vector()
            ),
            'orientation': AxisOrientation.Z,
            'side': Side.REAR
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_bottom_face(self):
        bottom_face = self.frame.Proxy.get_faces_for_side(Side.BOTTOM)[0]

        with self.assertRaises(AttachmentError):
            get_axis_frame_attachment_kwargs(
                self.frame, bottom_face, AxisOrientation.X)

    def assert_result_and_expected_are_equal(self, result, expected):
        self.assertEqual(result['origin_translation_offset'],
                         expected['origin_translation_offset'])
        self.assertEqual(result['length'].Value, self.frame.Size)
        self.assertPlacementEqual(result['placement'], expected['placement'])
        self.assertEqual(result['orientation'], expected['orientation'])
        self.assertEqual(result['side'], expected['side'])


if __name__ == '__main__':
    unittest.main()
