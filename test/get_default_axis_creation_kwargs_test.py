import unittest

from FreeCAD import Placement, Rotation, Vector
from ose3dprinter.core.get_default_axis_creation_kwargs import \
    get_default_axis_creation_kwargs

from .freecad_test_case import FreeCADTestCase


class GetDefaultAxisCreationKwargsTest(FreeCADTestCase):

    def test_get_default_axis_creation_kwargs_for_x_axis(self):
        result = get_default_axis_creation_kwargs('x')

        expected = {
            'origin_translation_offset': Vector(),
            'placement': Placement()
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_default_axis_creation_kwargs_for_y_axis(self):
        result = get_default_axis_creation_kwargs('y')

        expected = {
            'origin_translation_offset': Vector(-1, -1, 0),
            'placement': Placement(Vector(), Rotation(-90, 0, 90), Vector())
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def test_get_default_axis_creation_kwargs_for_z_axis(self):
        result = get_default_axis_creation_kwargs('z')

        expected = {
            'origin_translation_offset': Vector(0, -1, -1),
            'placement': Placement(Vector(), Rotation(0, 90, 90), Vector())
        }

        self.assert_result_and_expected_are_equal(result, expected)

    def assert_result_and_expected_are_equal(self, result, expected):
        self.assertEqual(result['origin_translation_offset'],
                         expected['origin_translation_offset'])
        self.assertPlacementEqual(result['placement'], expected['placement'])


if __name__ == '__main__':
    unittest.main()
