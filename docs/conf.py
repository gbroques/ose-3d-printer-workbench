# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

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
    apidoc.main([
        '../ose3dprinter',
        '-o', 'ose3dprinter',
        '-d', max_depth,
        '--templatedir=_templates/',
        '--force',
        '--no-toc'
    ])


def process_docstring(app, what, name, obj, options, lines):
    if what == 'class' and name.endswith('Model'):
        lines.append('.. model-property-table::')


def setup(app):
    app.connect('builder-inited', run_apidoc)
    app.connect('autodoc-process-docstring', process_docstring)


# -- Project information -----------------------------------------------------

project = 'OSE 3D Printer Workbench'
copyright = '2020, G Roques'
author = 'G Roques'

# The full version, including alpha/beta/rc tags
release = '0.1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = conf['extensions'] + [
    'osewb.docs.ext.model_property_table'
]

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

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = conf['html_theme']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_context = {
    'css_files': [
        # overrides for wide tables in RTD theme
        '_static/theme_overrides.css'
    ]
}

extlinks = conf['ext']['extlinks']['extlinks']
