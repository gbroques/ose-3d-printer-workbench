# Contributing Guidelines
The following sections are meant as contributing *guidelines*, or **best-practices**. We encourage you to follow them, but your contribution may still be accepted without following them strictly.

Are you a potential first-time contributor? Look for issues tagged with <a href="https://github.com/gbroques/ose-3d-printer-workbench/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22" style="height: 20px; padding: .15em 4px; font-weight: 600; line-height: 15px; border-radius: 2px; box-shadow: inset 0 -1px 0 rgba(27,31,35,.12); font-size: 12px;background-color: #7057ff; color: white">good first issue</a>.

## Pre-Requisites
Install [OSE Workbench Platform](https://github.com/gbroques/ose-workbench-platform).

    pip install ose-workbench-platform==0.1.0a17

## Code Style Guide
Code should follow the official [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

## Tests
Unit tests are encouraged for complex non-trivial logic (e.g. attaching axes to the frame), and can be found in the `tests/` directory within the root of this repository.

It's expected that you fix any changes you make that break existing tests.

Pull requests will not be merged if tests are failing.

To execute all unit tests, run:

    osewb test

## Documentation
Improving the docstring on packages, modules, classes, functions, and other symbols throughout the codebase is encouraged.

We use the [Sphinx docstring format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html) which is the standard docstring format used with [Sphinx](https://www.sphinx-doc.org/en/master/).

To build the docs, run:

    osewb docs

## Philosophy
We generally subscribe to the philosophy provided by [The Zen of Python](https://www.python.org/dev/peps/pep-0020/).

```
>>> import this;
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

## Upgrading OSE Workbench Platform
There's three references to the version of `ose-workbench-platform` that this workbench depends on.

When updating this version, ensure you update **ALL** references.

1. Inside `.travis.yml`:

> https://github.com/gbroques/ose-workbench-platform.git#<version>:osewb

2. Inside `docs/requirements.txt`:

>     ose-workbench-platform==<version>

3. Under [Pre-Requisites](#pre-requisites) in this document:

>     pip install ose-workbench-platform==<version>
