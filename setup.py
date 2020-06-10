from setuptools import setup

setup(
    name='ose-3d-printer-workbench',
    version='0.1.0',
    packages=[
        'freecad',
        'freecad.ose3dprinter',
        'ose3dprinter',
        'osecore'
    ],
    author='G Roques',
    url='https://github.com/gbroques/ose-3d-printer-workbench',
    description='A FreeCAD workbench for designing 3D printers by Open Source Ecology (OSE) for Distributive Enterprise',
    install_requires=[],
    include_package_data=True
)
