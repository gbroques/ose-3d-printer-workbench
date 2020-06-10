import unittest

import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.attachment import get_axis_frame_attachment_kwargs
from ose3dprinter.model import FrameModel
from ose3dprinter.part import AngleFrameConnector
from osecore.app.attachment import AttachmentError
from osecore.app.three_dimensional_space_enums import CoordinateAxis, Side

from .freecad_test_case import FreeCADTestCase


class GetAxisFrameAttachmentKwargsForFrameWithCornersTest(FreeCADTestCase):

    @classmethod
    def setUpClass(cls):
        document = App.newDocument()
        cls.frame = document.addObject('Part::FeaturePython', 'Frame')
        FrameModel(cls.frame, has_corners=True)
        document.recompute()

    def test_get_axis_frame_attachment_kwargs_for_top_face(self):
        top_faces = self.frame.Proxy.get_faces_for_side(Side.TOP)
        for top_face in top_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, top_face, CoordinateAxis.X)

            expected = {
                'origin_translation_offset': Vector(0.0, -0.5, 0.0),
                'placement': Placement(
                    Vector(0, self.frame.Size / 2, self.frame.Size),
                    Rotation()
                ),
                'length_value': self.frame.Size.Value,
                'orientation': CoordinateAxis.X,
                'side': Side.TOP
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_left_face(self):
        left_faces = self.frame.Proxy.get_faces_for_side(Side.LEFT)
        for left_face in left_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, left_face, CoordinateAxis.Y)
            three_inches = 76.2  # in millimeters (mm)
            length = self.frame.Size.Value + three_inches
            expected = {
                'origin_translation_offset': Vector(-1.0, 0.0, -1.0),
                'placement': Placement(
                    Vector(
                        -AngleFrameConnector.axis_side_mount_width,
                        -21.14446,  # TODO: Replace magic number with something meaningful
                        305.2  # TODO: Replace magic number with something meaningful
                    ),
                    Rotation(),
                    Vector()
                ),
                'length_value': length,
                'orientation': CoordinateAxis.Y,
                'side': Side.LEFT
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_right_face(self):
        right_faces = self.frame.Proxy.get_faces_for_side(Side.RIGHT)
        for right_face in right_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, right_face, CoordinateAxis.Y)

            frame_size = self.frame.Size.Value
            three_inches = 76.2  # in millimeters (mm)
            length = frame_size + three_inches
            expected = {
                'origin_translation_offset': Vector(0.0, 0.0, -1.0),
                'placement': Placement(
                    Vector(
                        frame_size + AngleFrameConnector.axis_side_mount_width,
                        -21.14446,  # TODO: Replace magic number with something meaningful
                        305.2  # TODO: Replace magic number with something meaningful
                    ),
                    Rotation(),
                    Vector()
                ),
                'length_value': length,
                'orientation': CoordinateAxis.Y,
                'side': Side.RIGHT
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_front_face(self):
        front_faces = self.frame.Proxy.get_faces_for_side(Side.FRONT)
        for front_face in front_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, front_face, CoordinateAxis.Z)

            expected = {
                'origin_translation_offset': Vector(-0.5, -1.0, 0.0),
                'placement': Placement(
                    Vector(self.frame.Size / 2, 0, 0),
                    Rotation(),
                    Vector()
                ),
                'length_value': self.frame.Size.Value,
                'orientation': CoordinateAxis.Z,
                'side': Side.FRONT
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_rear_face(self):
        rear_faces = self.frame.Proxy.get_faces_for_side(Side.REAR)
        for rear_face in rear_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, rear_face, 'z')

            expected = {
                'origin_translation_offset': Vector(-0.5, 0, 0),
                'placement': Placement(
                    Vector(self.frame.Size / 2, self.frame.Size, 0),
                    Rotation(),
                    Vector()
                ),
                'length_value': self.frame.Size.Value,
                'orientation': CoordinateAxis.Z,
                'side': Side.REAR
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_bottom_face(self):
        bottom_faces = self.frame.Proxy.get_faces_for_side(Side.BOTTOM)
        for bottom_face in bottom_faces:
            with self.assertRaises(AttachmentError):
                get_axis_frame_attachment_kwargs(self.frame, bottom_face, 'x')

    def assert_result_and_expected_are_equal(self, result, expected):
        self.assertEqual(result['origin_translation_offset'],
                         expected['origin_translation_offset'])
        self.assertPlacementEqual(result['placement'], expected['placement'])
        self.assertAlmostEqual(
            result['length'].Value, expected['length_value'], places=2)
        self.assertEqual(result['orientation'], expected['orientation'])
        self.assertEqual(result['side'], expected['side'])


if __name__ == '__main__':
    unittest.main()
