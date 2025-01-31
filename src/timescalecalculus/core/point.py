"""Definitions for timescale points. Points are regular Python numbers."""

from numbers import Number


def is_valid(point):
    return isinstance(point, Number)


def all_valid(points):
    return all(is_valid(p) for p in points)


def any_valid(points):
    return any(is_valid(p) for p in points)


def eq(point, value):
    """`point` == `value`"""
    return is_valid(point) and is_valid(value) and point == value
