# OSE 3D Printer FreeCAD Workbench
[![Build Status](https://travis-ci.org/gbroques/ose-3d-printer-workbench.svg?branch=master)](https://travis-ci.org/gbroques/ose-3d-printer-workbench) [![Documentation Status](https://readthedocs.org/projects/ose-3d-printer-workbench/badge/?version=latest)](https://ose-3d-printer-workbench.readthedocs.io/en/latest/?badge=latest)
 [![Coverage Status](https://coveralls.io/repos/github/gbroques/ose-3d-printer-workbench/badge.svg)](https://coveralls.io/github/gbroques/ose-3d-printer-workbench)

A FreeCAD workbench for designing 3D printers by [Open Source Ecology](https://www.opensourceecology.org/) for [Distributive Enterprise](https://wiki.opensourceecology.org/wiki/Distributive_Enterprise).

* [Tools](#tools)
* [Installation](#installation)
  * [FreeCAD 17+](#freecad-17+)
  * [FreeCAD 16](#freecad-16)
* [Documentation](#documentation)
* [Tests](#tests)
* [Limitations](#limitations)
* [Supported FreeCAD Versions](#supported-freecad-versions)

## Tools
* <img alt="Add Frame" src="ose3dprinter/workbench/resources/Frame.svg" width="32" height="32" /> Add Frame
* <img alt="Add Universal X Axis" src="ose3dprinter/workbench/resources/UniversalXAxis.svg" width="32" height="32" /> Add Universal X Axis
* <img alt="Add Universal Y Axis" src="ose3dprinter/workbench/resources/UniversalYAxis.svg" width="32" height="32" /> Add Universal Y Axis
* <img alt="Add Universal Z Axis" src="ose3dprinter/workbench/resources/UniversalZAxis.svg" width="32" height="32" /> Add Universal Z Axis
* <img alt="Add Heated Bed" src="ose3dprinter/workbench/resources/HeatedBed.svg" width="32" height="32" /> Add Heated Bed
* <img alt="Add Extruder" src="ose3dprinter/workbench/resources/Extruder.svg" width="32" height="32" /> Add Extruder

## Installation
### FreeCAD 17+
**WARNING:** Not yet available via the **Addon Manager**, but we plan to make it available there eventually. Until then, manually install as you would any other workbench.

1. Download via the [Addon Manager](https://wiki.freecadweb.org/Std_AddonMgr).

### FreeCAD 16
1. Identify where you need to manually download and install the workbench.
    * Common locations for various operating systems can be found on "[Installing more workbenches](https://wiki.freecadweb.org/Installing_more_workbenches)" in the FreeCAD wiki.
    * You can also execute `FreeCAD.getUserAppDataDir()` within the **Python console** in FreeCAD for this location. Workbenches will always go into the `Mod` directory in the user's application data directory.
2. Download the workbench as a **ZIP** archive and extract, or use command-line `git` to `clone` the repository into the correct location (e.g. `~/.FreeCAD/Mod/ose-3d-printer-workbench`)

Additionally, there are installation walk-through videos on YouTube featuring instructions with and without the command-line:
* [Command Line Installation Video](https://youtu.be/PtBoIBTPNv4)
* [Installation for Beginners Video](https://youtu.be/C3W3fNzsydo)

## Documentation
Documentation is located within the `/docs` directory of this repository, and hosted at the following URL with [Read the Docs](https://readthedocs.org/):

https://ose-3d-printer-workbench.readthedocs.io/en/latest/

To simplify execution, we use Docker to create a virtualized environment with the requisite dependencies for generating documentation in Python.

### Pre-Requisites
Install Docker and [Docker Compose](https://docs.docker.com/compose/install/).

### Build & Run the Docs Container
Run from root of repository:

    docker-compose up -d

The `-d` flag or "detached mode" is to run the container in the background.

### Make Documentation
Run from root of repository:

    docker exec -it ose3dprinter-docs make html

## Tests
Unit tests are located within the `/test` directory of this repository.

To simplify execution, we use Docker to create a virtualized FreeCAD 0.16 environment with the requisite dependencies for running unit tests in Python with features like [coverage reports](https://en.wikipedia.org/wiki/Code_coverage).

### Pre-Requisites
Install Docker and [Docker Compose](https://docs.docker.com/compose/install/).

### Build & Run the Test Container
Run from root of repository:

    docker-compose up -d

The `-d` flag or "detached mode" is to run the container in the background.

### Run Tests
Run from root of repository:

    docker exec -it ose3dprinter-test pytest test/

A shell script for the above command has been included for convenience:

    ./run_tests.sh

To generate coverage data in `.coverage`, run:

    docker exec -it ose3dprinter-test pytest --cov ose3dprinter_workbench/ test/

To generate a coverage report from the coverage data in `htmlcov/`, run:

    docker exec -it ose3dprinter-test coverage html

## Limitations
* Attaching axes to rotated frame is not supported.

## Supported FreeCAD Versions
This workbench supports FreeCAD 16 or greater.
