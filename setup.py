from setuptools import setup

setup(
    name='ose-3d-printer-workbench',
    version='0.1.0',
    packages=[
        'freecad',
        'freecad.ose3dprinter',
        'ose3dprinter'
    ],
    author='G Roques',
    url='https://github.com/gbroques/ose-3d-printer-workbench',
    description=('A FreeCAD workbench for designing 3D printers '
                 'by Open Source Ecology (OSE) for Distributive Enterprise'),
    install_requires=[
        'ose-workbench-core==0.1.0a4'  # Also in environment.yml
    ],
    include_package_data=True,
    classifiers=[
        # Full List: https://pypi.org/pypi?%3Aaction=list_classifiers
        ('License :: '
         'OSI Approved :: '
         'GNU Lesser General Public License v2 or later (LGPLv2+)'),
        'Programming Language :: Python :: 3 :: Only'
    ]
)
