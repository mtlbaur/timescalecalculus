"""Definitions for timescale points and intervals."""

import operator
from enum import Enum
from timescalecalculus import core


class Type(Enum):
    """Classification of timescale values as either points or intervals."""

    invalid = 0
    point = 1
    interval = 2


class PointClass(Enum):
    """Classification of timescale points based on Table/Figure 1.1. These values are either discrete or values within intervals."""

    invalid = 0
    left_dense = 1
    right_dense = 2
    left_scattered = 3
    right_scattered = 4


def is_valid(time):
    return core.point.is_valid(time) or core.interval.is_valid(time)


def all_valid(times):
    return all(is_valid(t) for t in times)


def any_valid(times):
    return any(is_valid(t) for t in times)


def get_type(time):
    if core.point.is_valid(time):
        return Type.point

    if core.interval.is_valid(time):
        return Type.interval

    return Type.invalid


def get_point_class(time, point=None):
    if core.point.is_valid(time):
        if point is None or time == point:
            return (PointClass.left_scattered, PointClass.right_scattered)

        return PointClass.invalid

    if core.interval.is_valid(time):
        if core.interval.contains(time, point):
            if point > time[0] and point < time[1]:
                return (PointClass.left_dense, PointClass.right_dense)

            if point == time[0]:
                return (PointClass.left_scattered, PointClass.right_dense)

            if point == time[1]:
                return (PointClass.left_dense, PointClass.right_scattered)

    return PointClass.invalid


def is_left_dense(time, point):
    return get_point_class(time, point)[0] is PointClass.left_dense


def is_right_dense(time, point):
    return get_point_class(time, point)[1] is PointClass.right_dense


def is_left_scattered(time, point=None):
    return get_point_class(time, point)[0] is PointClass.left_scattered


def is_right_scattered(time, point=None):
    return get_point_class(time, point)[1] is PointClass.right_scattered


def eval_pair_f(a, b, ppf, pif, ipf, iif):
    """
    Returns the result of one of `(ppf, pif, ipf, iif)` based on the types of parameters `a` and `b` as follows:

    ```txt
    | a_type   | b_type   | returns |
    |----------|----------|---------|
    | point    | point    | ppf()   |
    | point    | interval | pif()   |
    | interval | point    | ipf()   |
    | interval | interval | iif()   |
    ```
    """

    a_type = get_type(a)
    b_type = get_type(b)

    if a_type is Type.point:
        if b_type is Type.point:
            return ppf()

        if b_type is Type.interval:
            return pif()

        raise Exception(a_type, b_type)

    if a_type is Type.interval:
        if b_type is Type.point:
            return ipf()

        if b_type is Type.interval:
            return iif()

    raise Exception(a_type, b_type)


def overlaps(a, b):
    return eval_pair_f(
        a,
        b,
        lambda: core.point.eq(a, b),
        lambda: core.interval.contains(b, a),
        lambda: core.interval.contains(a, b),
        lambda: core.interval.overlaps(a, b),
    )


def compare(op, a, b):
    return eval_pair_f(
        a,
        b,
        lambda: op(a, b),
        lambda: op(a, b[0]) and op(a, b[1]),
        lambda: op(a[0], b) and op(a[1], b),
        lambda: op(a[0], b[0]) and op(a[0], b[1]) and op(a[1], b[0]) and op(a[1], b[1]),
    )


def lt(a, b):
    """`a` < `b`"""
    return compare(operator.lt, a, b)


def le(a, b):
    """`a` <= `b`"""
    return lt(a, b) or eq(a, b)


def eq(a, b):
    """`a` == `b`; assumes: `[0, 1] != [1, 0]`"""
    return eval_pair_f(
        a,
        b,
        lambda: core.point.eq(a, b),
        lambda: a == b[0] and a == b[1],
        lambda: a[0] == b and a[1] == b,
        lambda: a == b,
    )


def ge(a, b):
    """`a` >= `b`"""
    return gt(a, b) or eq(a, b)


def gt(a, b):
    """`a` > `b`"""
    return compare(operator.gt, a, b)


def contains(a, b):
    return eq(a, b) or core.interval.is_valid(a) and core.interval.contains(a, b)


def min_or_max(a, b, f):
    return eval_pair_f(
        a,
        b,
        lambda: f(a, b),
        lambda: f(f(a, b[0]), f(a, b[1])),
        lambda: f(f(a[0], b), f(a[1], b)),
        lambda: f(f(a[0], b[0]), f(a[0], b[1]), f(a[1], b[0]), f(a[1], b[1])),
    )


def min_(a, b):
    return min_or_max(a, b, min)


def max_(a, b):
    return min_or_max(a, b, max)


def min_max(a, b):
    return eval_pair_f(
        a,
        b,
        lambda: (
            min(a, b),
            max(a, b),
        ),
        lambda: (
            min(min(a, b[0]), min(a, b[1])),
            max(max(a, b[0]), max(a, b[1])),
        ),
        lambda: (
            min(min(a[0], b), min(a[1], b)),
            max(max(a[0], b), max(a[1], b)),
        ),
        lambda: (
            min(min(a[0], b[0]), min(a[0], b[1]), min(a[1], b[0]), min(a[1], b[1])),
            max(max(a[0], b[0]), max(a[0], b[1]), max(a[1], b[0]), max(a[1], b[1])),
        ),
    )


def solve_step_f(cur, nxt=None, spf=None, sif=None, start_time=None, stop_time=None):
    """
    A generalization that will solve from one point/interval to the next point/interval.

    `spf` is the point-solving function; `sif` is the interval-solving function.

    Both `spf` and `sif` require the following signature:

    ```py
    def sf(l, r): ...
    ```

    where:

    - `l` is the left point or interval bound
    - `r` is the right point or interval bound

    How `spf` and `sif` evaluate their arguments is up to the user. The values returned from these functions are summed and returned.

    The keyword arguments `start_time` and `stop_time` allow a sub-interval of `cur` to be solved. This means that if either `start_time` or `stop_time` are defined, `cur` must be an interval and `nxt` is unused.

    An example of allowed behavior is as follows:

    ```txt
    p = spf = lambda l, r: abs(r - l) * 2
    i = sif = lambda l, r: abs(r - l)

    ts = [1, 2, [3, 4], 5, [6, 7], [8, 9]]

    |cur   |nxt   |start_time|stop_time|result                     |
    |--------------------------------------------------------------|
    |1     |2     |None      |None     |p(1, 2)               = 2  |
    |2     |[3, 4]|None      |None     |p(2, 3)               = 2  |
    |[3, 4]|5     |None      |None     |i(3, 4)     + p(4, 5) = 3  |
    |[3, 4]|5     |3.5       |None     |i(3.5, 4)   + p(4, 5) = 2.5|
    |[3, 4]|None  |3.5       |3.8      |i(3.5, 3.8)           = 0.3|
    |[3, 4]|None  |None      |3.8      |i(3, 3.8)             = 0.8|
    |[6, 7]|[8, 9]|6.5       |None     |i(6.5, 7)   + p(7, 8) = 2.5|
    ```
    """

    if not spf or not sif:
        raise Exception()

    nxt_closest = nxt[0] if core.interval.is_valid(nxt) else nxt

    if core.point.is_valid(cur):
        if start_time is not None and not core.point.eq(cur, start_time):
            raise Exception()
        if stop_time is not None and not core.point.eq(cur, stop_time):
            raise Exception()

        return spf(cur, nxt_closest) if nxt_closest and not stop_time else 0

    elif core.interval.is_valid(cur):
        l, r = cur

        if start_time is not None:
            if core.interval.contains_point(cur, start_time):
                l = start_time
            else:
                raise Exception()

        if stop_time is not None:
            if core.interval.contains_point(cur, stop_time):
                r = stop_time
            else:
                raise Exception()

        return sif(l, r) + (spf(r, nxt_closest) if nxt_closest and not stop_time else 0)

    raise Exception()
