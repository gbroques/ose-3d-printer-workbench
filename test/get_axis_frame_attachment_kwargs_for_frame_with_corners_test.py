import unittest

import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.app.enums import AxisOrientation, Side
from ose3dprinter.app.exceptions import AttachmentError
from ose3dprinter.app.face_orientation import \
    get_faces_within_bounds_of_side_for_frame_with_corners
from ose3dprinter.app.get_axis_frame_attachment_kwargs import \
    get_axis_frame_attachment_kwargs
from ose3dprinter.app.model import FrameModel
from ose3dprinter.app.model.frame.angle_frame_connector import \
    AngleFrameConnector

from .freecad_test_case import FreeCADTestCase


class GetAxisFrameAttachmentKwargsForFrameWithCornersTest(FreeCADTestCase):

    @classmethod
    def setUpClass(cls):
        document = App.newDocument()
        cls.frame = document.addObject('Part::FeaturePython', 'Frame')
        FrameModel(cls.frame, has_corners=True)
        document.recompute()

    def test_get_axis_frame_attachment_kwargs_for_top_face(self):
        top_faces = get_faces_within_bounds_of_side_for_frame_with_corners(
            self.frame, Side.TOP)
        for top_face in top_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, top_face, AxisOrientation.X)

            expected = {
                'origin_translation_offset': Vector(0.0, -0.5, 0.0),
                'placement': Placement(
                    Vector(0, self.frame.Size / 2, self.frame.Size),
                    Rotation()
                ),
                'length_value': self.frame.Size.Value,
                'orientation': AxisOrientation.X,
                'side': Side.TOP
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_left_face(self):
        left_faces = get_faces_within_bounds_of_side_for_frame_with_corners(
            self.frame, Side.LEFT)
        for left_face in left_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, left_face, AxisOrientation.Y)
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
                'orientation': AxisOrientation.Y,
                'side': Side.LEFT
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_right_face(self):
        right_faces = get_faces_within_bounds_of_side_for_frame_with_corners(
            self.frame, Side.RIGHT)
        for right_face in right_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, right_face, AxisOrientation.Y)

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
                'orientation': AxisOrientation.Y,
                'side': Side.RIGHT
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_front_face(self):
        front_faces = get_faces_within_bounds_of_side_for_frame_with_corners(
            self.frame, Side.FRONT)
        for front_face in front_faces:
            result = get_axis_frame_attachment_kwargs(
                self.frame, front_face, AxisOrientation.Z)

            expected = {
                'origin_translation_offset': Vector(-0.5, -1.0, 0.0),
                'placement': Placement(
                    Vector(self.frame.Size / 2, 0, 0),
                    Rotation(),
                    Vector()
                ),
                'length_value': self.frame.Size.Value,
                'orientation': AxisOrientation.Z,
                'side': Side.FRONT
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_rear_face(self):
        rear_faces = get_faces_within_bounds_of_side_for_frame_with_corners(
            self.frame, Side.REAR)
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
                'orientation': AxisOrientation.Z,
                'side': Side.REAR
            }

            self.assert_result_and_expected_are_equal(result, expected)

    def test_get_axis_frame_attachment_kwargs_for_bottom_face(self):
        bottom_faces = get_faces_within_bounds_of_side_for_frame_with_corners(
            self.frame, Side.BOTTOM)
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
