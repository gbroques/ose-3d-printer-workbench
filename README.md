# OSE 3D Printer Workbench
[![Build Status](https://travis-ci.org/gbroques/ose-3d-printer-workbench.svg?branch=master)](https://travis-ci.org/gbroques/ose-3d-printer-workbench) [![Coverage Status](https://coveralls.io/repos/github/gbroques/ose-3d-printer-workbench/badge.svg)](https://coveralls.io/github/gbroques/ose-3d-printer-workbench)

A workbench for designing 3D printers by [Open Source Ecology](https://www.opensourceecology.org/).

## Tools
* <img alt="Add Frame" src="ose3dprinter/workbench/resources/Frame.svg" width="32" height="32" /> Add Frame
* <img alt="Add Universal X Axis" src="ose3dprinter/workbench/resources/UniversalXAxis.svg" width="32" height="32" /> Add Universal X Axis
* <img alt="Add Universal Y Axis" src="ose3dprinter/workbench/resources/UniversalYAxis.svg" width="32" height="32" /> Add Universal Y Axis
* <img alt="Add Universal Z Axis" src="ose3dprinter/workbench/resources/UniversalZAxis.svg" width="32" height="32" /> Add Universal Z Axis
* <img alt="Add Heated Bed" src="ose3dprinter/workbench/resources/HeatedBed.svg" width="32" height="32" /> Add Heated Bed
* <img alt="Add Extruder" src="ose3dprinter/workbench/resources/Extruder.svg" width="32" height="32" /> Add Extruder

## Documentation
Documentation is located within the `/docs` directory of this reposiotry.

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
