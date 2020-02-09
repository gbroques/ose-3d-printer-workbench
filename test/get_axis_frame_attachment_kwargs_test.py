import unittest

import FreeCAD as App
from ose3dprinter_workbench.add_universal_axis_base.get_axis_frame_attachment_kwargs import \
    get_axis_frame_attachment_kwargs
from ose3dprinter_workbench.add_universal_axis_base.get_placement_strategy import \
    get_placement_for_top_face
from ose3dprinter_workbench.part import create_frame


class FreeCADTest(unittest.TestCase):

    def setUp(self):
        document = App.newDocument()
        self.frame = create_frame(document, 'Frame')
        document.recompute()

    def test_get_axis_frame_attachment_kwargs_for_top_face(self):
        top_face = self.frame.Shape.Faces[34]

        result = get_axis_frame_attachment_kwargs(self.frame, top_face, 'x')

        expected = get_placement_for_top_face(self.frame, top_face)
        self.assertTrue(result <= expected)


if __name__ == '__main__':
    unittest.main()
