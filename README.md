# OSE 3D Printer Workbench
[![Build Status](https://travis-ci.org/gbroques/ose-3d-printer-workbench.svg?branch=master)](https://travis-ci.org/gbroques/ose-3d-printer-workbench)
[![Documentation Status](https://readthedocs.org/projects/ose-3d-printer-workbench/badge/?version=latest)](https://ose-3d-printer-workbench.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/gbroques/ose-3d-printer-workbench/badge.svg)](https://coveralls.io/github/gbroques/ose-3d-printer-workbench) [![FreeCAD Addon Manager Status](https://img.shields.io/badge/FreeCAD%20Addon%20manager-available-brightgreen)](https://github.com/FreeCAD/FreeCAD-addons)

A FreeCAD workbench for designing 3D printers by [Open Source Ecology](https://www.opensourceecology.org/) for [Distributive Enterprise](https://wiki.opensourceecology.org/wiki/Distributive_Enterprise).

* [Main Toolbar](#main-toolbar)
* [Main Menu](#main-menu)
* [Installation](#installation)
* [Documentation](#documentation)
* [Contributing](#contributing)
* [License](#license)
* [Limitations](#limitations)
* [Supported FreeCAD Versions](#supported-freecad-versions)

## Main Toolbar
* [<img alt="Add Frame" src="freecad/ose3dprinter/icon/Frame.svg" width="32" height="32" /> Add Frame](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/add_frame.html)
* [<img alt="Add X Axis" src="freecad/ose3dprinter/icon/XAxis.svg" width="32" height="32" /> Add X Axis](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/add_axis.html)
* [<img alt="Add Y Axis" src="freecad/ose3dprinter/icon/YAxis.svg" width="32" height="32" /> Add Y Axis](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/add_axis.html)
* [<img alt="Add Z Axis" src="freecad/ose3dprinter/icon/ZAxis.svg" width="32" height="32" /> Add Z Axis](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/add_axis.html)
* [<img alt="Add Heated Bed" src="freecad/ose3dprinter/icon/HeatedBed.svg" width="32" height="32" /> Add Heated Bed](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/add_heated_bed.html)
* [<img alt="Add Extruder" src="freecad/ose3dprinter/icon/Extruder.svg" width="32" height="32" /> Add Extruder](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/add_extruder.html)

## Main Menu
* [<img alt="Copy Rod Cut List to Clipboard" src="freecad/ose3dprinter/icon/edit-copy.svg" width="32" height="32" /> Copy Rod Cut List to Clipboard](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/generate_cut_list.html)
* [<img alt="Save Rod Cut List as CSV" src="freecad/ose3dprinter/icon/document-save-as.svg" width="32" height="32" /> Save Rod Cut List as CSV](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/generate_cut_list.html)
* [<img alt="Make Angle Frame Connector" src="freecad/ose3dprinter/icon/Std_CoordinateSystem.svg" width="32" height="32" /> Make Angle Frame Connector](https://ose-3d-printer-workbench.readthedocs.io/en/latest/pages/make_angle_frame_connector.html)

## Installation
1. Identify where you need to manually download and install the workbench.
    * Common locations for various operating systems can be found on "[Installing more workbenches](https://wiki.freecadweb.org/Installing_more_workbenches)" in the FreeCAD wiki.
    * You can also execute `FreeCAD.getUserAppDataDir()` within the **Python console** in FreeCAD for this location. Workbenches will always go into the `Mod` directory in the user's application data directory.
2. Download the workbench as a **ZIP** archive and extract, or use command-line `git` to `clone` the repository into the correct location (e.g. `~/.FreeCAD/Mod/ose-3d-printer-workbench`)

Additionally, there are installation walk-through videos on YouTube featuring instructions with and without the command-line:
* [Command Line Installation Video](https://youtu.be/PtBoIBTPNv4)
* [Installation for Beginners Video](https://youtu.be/C3W3fNzsydo)

## Documentation
Documentation is hosted at the following URL:

https://ose-3d-printer-workbench.readthedocs.io/en/latest/

## Contributing
See [Contributing Guidelines](./CONTRIBUTING.md).

## License
Licensed under the [GNU Lesser General Public License, version 2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html) or LGPL v2.1. See [LICENSE](./LICENSE) for details.

This is the same license as [FreeCAD](https://wiki.freecadweb.org/Licence) to ensure this code could potentially be incorporated into future FreeCAD modules or FreeCAD source itself.

## Limitations
* Attaching axes to rotated frame is not supported.

## Supported FreeCAD Versions
This workbench supports FreeCAD 19.
