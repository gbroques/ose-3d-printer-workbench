import unittest


class FreeCADTestCase(unittest.TestCase):
    """
    Base test case containing FreeCAD specific assertions and utility methods.
    """

    def assertPlacementEqual(self, a, b):
        self.assertEqual(a.Base, b.Base)
        self.assertEqual(a.Rotation.Angle, b.Rotation.Angle)
        self.assertEqual(a.Rotation.Axis, b.Rotation.Axis)
