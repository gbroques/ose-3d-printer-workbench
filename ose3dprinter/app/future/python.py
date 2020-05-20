import abc
import sys


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """
    TODO: Replace with math.isclose in python 3.5
    Sources:
        https://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
        https://docs.python.org/3/whatsnew/3.5.html#pep-485-a-function-for-testing-approximate-equality
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta('ABC', (), {})
