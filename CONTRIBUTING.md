# Contributing Guidelines
The following sections are meant as contributing *guidelines*, or **best-practices**. We encourage you to follow them, but your contribution may still be accepted without following them strictly.

## Code Style Guide
Code should follow the official [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

## Tests
Unit tests are encouraged for complex non-trivial logic (e.g. attaching axes to the frame), and can be found in the `test/` directory within the root of this repository.

It's expected that you fix any changes you make that break existing tests.

Pull requests will not be merged if tests are failing.

We currently don't have end-to-end or integration tests, but are interested in exploring these in the future.

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
