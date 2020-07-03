"""Utility script to automatically create thumbnail screenshots of parts.

Run with freecad -c part_screenshot.py when ose3dprinter conda environment is activated.
"""
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui
import Part

import ose3dprinter.part as ose3dprinter_parts
from ose3dprinter.part import (AngledBarFrame, AngleFrameConnector, Axis,
                               CNCCutFrame, Extruder, HeatedBed)

parts = [
    AngleFrameConnector, AngledBarFrame, Axis,
    CNCCutFrame, Extruder, HeatedBed
]

document = App.newDocument()

# Setup Gui
Gui.showMainWindow()
main_window = Gui.getMainWindow()
main_window.hide()

screenshot_path = Path('./_static/screenshot')
screenshot_path.mkdir(parents=True, exist_ok=True)

for (name, part) in zip(ose3dprinter_parts.__all__, parts):
    made_part = part.make()
    Part.show(made_part)

    active_view = Gui.activeView()
    active_view.setCameraType('Orthographic')
    active_view.viewIsometric()
    active_view.fitAll()

    image_name = str(screenshot_path.joinpath('{}.png'.format(name)))
    print('Saving image {}'.format(image_name))
    active_view.saveImage(image_name, 150, 150, 'Transparent')

    document.removeObject('Shape')

App.closeDocument(document.Name)
exit(0)
