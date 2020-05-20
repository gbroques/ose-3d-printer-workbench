from ose3dprinter.app.future.python import isclose


def between_bounds(value, lower_bound, upper_bound):
    is_between_bounds = lower_bound < value < upper_bound
    return (
        isclose(value, lower_bound) or
        is_between_bounds or
        isclose(value, upper_bound)
    )
