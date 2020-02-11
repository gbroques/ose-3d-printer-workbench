import unittest

import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.core.get_axis_frame_attachment_kwargs import \
    get_axis_frame_attachment_kwargs
from ose3dprinter.workbench.part import create_frame


class FreeCADTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        document = App.newDocument()
        cls.frame = create_frame(document, 'Frame')
        document.recompute()

    def test_get_axis_frame_attachment_kwargs_for_top_face(self):
        top_face = self.frame.Shape.Faces[34]

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
        left_face = self.frame.Shape.Faces[30]

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
        right_face = self.frame.Shape.Faces[35]

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
        front_face = self.frame.Shape.Faces[31]

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
        rear_face = self.frame.Shape.Faces[33]

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

    def assert_result_and_expected_are_equal(self, result, expected):
        self.assertEqual(result['origin_translation_offset'],
                         expected['origin_translation_offset'])
        self.assertEqual(result['length'].Value, self.frame.Size)
        self.assertEqual(result['placement'].Base, expected['placement'].Base)
        self.assertEqual(result['placement'].Rotation.Angle,
                         expected['placement'].Rotation.Angle)
        self.assertEqual(result['placement'].Rotation.Axis,
                         expected['placement'].Rotation.Axis)


if __name__ == '__main__':
    unittest.main()
