"""Definitions for timescale intervals. Intervals are standard Python lists of two numbers of the form `[start, end]`."""

from timescalecalculus import core


def is_valid(interval):
    return (
        isinstance(interval, list)
        and len(interval) == 2
        and core.point.all_valid(interval)
        and interval[0] != interval[1]
    )


def all_valid(intervals):
    return all(is_valid(i) for i in intervals)


def any_valid(intervals):
    return any(is_valid(i) for i in intervals)


def eq(interval, value):
    """`point` == `value`; assumes: `[0, 1] != [1, 0]`"""
    return is_valid(interval) and is_valid(value) and interval == value


def contains_point(interval, point):
    return (
        is_valid(interval)
        and core.point.is_valid(point)
        and (point >= interval[0] and point <= interval[1] or point >= interval[1] and point <= interval[0])
    )


def contains_interval(a, b):
    return (
        is_valid(a)
        and is_valid(b)
        and ((a[0] < a[1] and a[0] <= b[0] and b[1] <= a[1]) or (a[1] < a[0] and a[1] <= b[1] and b[0] <= a[0]))
    )


def contains(interval, value):
    return contains_point(interval, value) or contains_interval(interval, value)


def overlaps(a, b):
    return contains(a, b[0]) or contains(a, b[1]) or contains(b, a[0]) or contains(b, a[1])
