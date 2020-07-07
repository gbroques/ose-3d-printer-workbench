"""Utility script to automatically create thumbnail screenshots of parts.

Run with freecad -c part_screenshot.py when ose3dprinter conda environment is activated.
"""
import importlib
import inspect
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui
import ose3dprinter.part as ose3dprinter_parts
import Part


def is_part_class(x) -> bool:
    return inspect.isclass(x) and not inspect.isbuiltin(x)


members = inspect.getmembers(ose3dprinter_parts, is_part_class)

document = App.newDocument()

# Setup Gui
Gui.showMainWindow()
main_window = Gui.getMainWindow()
main_window.hide()

screenshot_path = Path('./_static/screenshot')
screenshot_path.mkdir(parents=True, exist_ok=True)

for (name, part) in members:
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
