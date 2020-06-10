import unittest

from ose3dprinter.attachment import get_default_axis_creation_kwargs
from osecore.app.three_dimensional_space_enums import CoordinateAxis, Side

from .freecad_test_case import FreeCADTestCase


class GetDefaultAxisCreationKwargsTest(FreeCADTestCase):

    def test_get_default_axis_creation_kwargs_for_x_axis(self):
        result = get_default_axis_creation_kwargs('x')

        expected = {
            'orientation': CoordinateAxis.X,
            'side': Side.TOP
        }

        self.assertEqual(result, expected)

    def test_get_default_axis_creation_kwargs_for_y_axis(self):
        result = get_default_axis_creation_kwargs('y')

        expected = {
            'orientation': CoordinateAxis.Y,
            'side': Side.LEFT
        }

        self.assertEqual(result, expected)

    def test_get_default_axis_creation_kwargs_for_z_axis(self):
        result = get_default_axis_creation_kwargs('z')

        expected = {
            'orientation': CoordinateAxis.Z,
            'side': Side.FRONT
        }

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
