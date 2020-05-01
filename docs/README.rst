Documentation
=============

We automatically generate our documentation with a tool called `Sphinx <http://www.sphinx-doc.org/en/master/>`_.

A Sphinx extension, called `sphinx-apidoc <http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html>`_,
automatically generates Sphinx sources as reStructuredText or ``.rst`` files from the ``ose3dprinter`` package.

For a primer on reStructuredText see Sphinx's `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_.

Sphinx creates the HTML and other necessary files in ``docs/_build``.

We host our documentation using a free service called `Read the Docs <https://readthedocs.org/>`_.

How to Update the Docs
----------------------

1. Make your desired changes.

2. Run ``make html`` from ``./docs``.

3. Verify your changes by opening ``docs/_build/html/index.html`` in your favorite web browser.

4. Commit, and push your changes. Read the Docs will update the documentation site upon pushing.
