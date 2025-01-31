import math
import numpy


def only_real_if_no_imag(complex_val):
    return complex_val if complex_val.imag else complex_val.real


def binary_search_template(t, l, r, xf, tf, lf, rf):
    """
    A generic binary search algorithm. If `tf(x, t)` returns `True` for current value `x` the index of `t` is returned. Otherwise, if a satisfactory `t` is not located, `-1` is returned. The values retrieved by `xf()` must be in sorted order.

    - `t`: target
    - `l`: left bound
    - `r`: right bound
    - `xf`: function that retrieves `x` for a given index
    - `tf`: function that compares `x` against `t`
    - `lf`: function that checks if `x` is to the left of `t`
    - `rf`: function that checks if `x` is to the right of `t`
    """

    while l <= r:
        m = l + int((r - l) / 2)
        x = xf(m)

        if lf(x, t):
            l = m + 1
        elif rf(x, t):
            r = m - 1
        elif tf(x, t):
            return m
        else:
            return -1

    return -1


def gen_even_seq(start, end, stepsize=None, count=None, excl_start=False, excl_end=False):
    """
    Generates an evenly-spaced sequence of numbers between `start` and `end` via either `stepsize` or `count`.

    - `stepsize` sets what the minimum difference should between any two numbers in the sequence. `stepsize` is used to compute the `count` of points in the sequence. If `count` does not allow `end` to be included in the sequence, then it is increased until `end` fits (in other words: higher accuracy is preferred).

    - `count` sets how many values should exist in the sequence from `start` to `end`. This means that the difference between `start` and `end` influences the resulting difference between sequence points. If this isn't desirable, use `stepsize` instead.

    - `start` and/or `end` can be excluded from the sequence. The number of excluded points is substracted from `count` to ensure that the spacing remains consistent. This means that with a `count` of `6` and both `start` and `end` excluded, the length of the resulting list would be `6 - 2 == 4`.
    """

    if stepsize and count or not stepsize and not count:
        raise Exception("either `count` or `stepsize` must be provided")

    if stepsize:
        count = abs(math.ceil((end - start) / stepsize)) + 1

    step = (end - start) / (count - 1)

    if excl_start:
        start += step
        count -= 1

    if excl_end:
        end -= step
        count -= 1

    return numpy.linspace(start, end, count, endpoint=True)
