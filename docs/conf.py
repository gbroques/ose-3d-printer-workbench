# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import inspect
import json
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys

from osewb.docs import conf

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

# Shared base configuration for OSE workbench documentation.
# https://github.com/gbroques/ose-workbench-platform/blob/master/osewb/docs/conf.py
print("============================================")
print("             SPHINX BASE CONFIG             ")
print("============================================")
print(json.dumps(conf, indent=4))
print("============================================")


def run_apidoc(app):
    """Generate API documentation"""
    from sphinx.ext import apidoc
    max_depth = '1'
    packages = ['ose3dprinter', 'freecad']
    for package in packages:
        apidoc.main([
            '../{}'.format(package),
            '-o', package,
            '-d', max_depth,
            '--templatedir=_templates/',
            '--force',
            '--no-toc',
            '--implicit-namespaces'
        ])


def process_docstring(app, what, name, obj, options, lines):
    if what == 'module':
        public_members = []
        if hasattr(obj, '__all__'):
            public_members = obj.__all__
        all_members = inspect.getmembers(obj)
        members = [
            (
                name + '.' + member[0],
                get_summary_line(inspect.getdoc(member[1]))
            )
            for member in all_members
            if not member[0].startswith('_')
            and member[0] in public_members
            and not inspect.isbuiltin(member[1])
            and (inspect.isclass(member[1]) or inspect.isfunction(member[1]))
        ]
        if len(members):
            lines.append('')
            lines.append('.. list-table::')
            lines.append('   :header-rows: 1')
            lines.append('')
            lines.append('   * - Name')
            lines.append('     - Description')
            lines.append('')
        for member, summary in members:
            lines.append('   * - :mod:`~{}`'.format(member))
            if summary:
                lines.append('     - ' + summary)
            else:
                lines.append('     - None')
            lines.append('')
        if len(members):
            lines.append('')
            lines.append('----')
            lines.append('')


def get_summary_line(docstring):
    if docstring is None:
        return None
    return docstring.splitlines()[0]


def setup(app):
    app.connect('builder-inited', run_apidoc)
    app.connect('autodoc-process-docstring', process_docstring)

# -- Project information -----------------------------------------------------


project = 'OSE 3D Printer Workbench'
copyright = '2020, G Roques'
author = 'G Roques'

# The full version, including alpha/beta/rc tags
release = '0.1.0'
version = '0.1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = conf['extensions']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# A boolean that decides whether module names are prepended to all object names
# (for object types where a “module” of some kind is defined),
# e.g. for py:function directives. Default is True.
add_module_names = conf['add_module_names']

# -- Auto-doc Options --------------------------------------------------------
autodoc_mock_imports = conf['ext']['autodoc']['autodoc_mock_imports']

# -- FreeCAD Custom Property Table Options -----------------------------------
remove_app_property_prefix_from_type = conf['ext'][
    'freecad_custom_property_table']['remove_app_property_prefix_from_type']

# -- FreeCAD Icon Extension Options ------------------------------------------
# Relative to docs source
freecad_icon_directory = '../freecad/ose3dprinter/icon'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = conf['html_theme']

html_logo = './_static/ose-sticker-logo.svg'

html_css_files =  ['theme_overrides.css'] + conf['html_css_files']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

extlinks = conf['ext']['extlinks']['extlinks']
