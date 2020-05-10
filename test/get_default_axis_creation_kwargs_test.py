import unittest

from ose3dprinter.app.enums import AxisOrientation, Side
from ose3dprinter.app.get_default_axis_creation_kwargs import \
    get_default_axis_creation_kwargs

from .freecad_test_case import FreeCADTestCase


class GetDefaultAxisCreationKwargsTest(FreeCADTestCase):

    def test_get_default_axis_creation_kwargs_for_x_axis(self):
        result = get_default_axis_creation_kwargs('x')

        expected = {
            'orientation': AxisOrientation.X,
            'side': Side.TOP
        }

        self.assertEqual(result, expected)

    def test_get_default_axis_creation_kwargs_for_y_axis(self):
        result = get_default_axis_creation_kwargs('y')

        expected = {
            'orientation': AxisOrientation.Y,
            'side': Side.LEFT
        }

        self.assertEqual(result, expected)

    def test_get_default_axis_creation_kwargs_for_z_axis(self):
        result = get_default_axis_creation_kwargs('z')

        expected = {
            'orientation': AxisOrientation.Z,
            'side': Side.FRONT
        }

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
