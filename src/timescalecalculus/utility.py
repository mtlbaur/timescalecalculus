import functools
import operator
from random import randint, uniform


def product(factors):
    """Product function from: https://stackoverflow.com/questions/595374/whats-the-python-function-like-sum-but-for-multiplication-product"""
    return functools.reduce(operator.mul, factors, 1)


def ts_gen_integers(a, b):
    """Create a timescale of integers `{x : a <= x <= b}`."""
    return [x for x in range(a, b + 1)]


def ts_gen_quantum(q, m, n):
    """Create a timescale of quantum numbers of form `{q^k : k=m, m+1, ..., n}`. Only does `q^(X)` where `X = {0, 1, 2, 3, ...}` at the moment."""
    return [q**k for k in range(m, n)]


def get_random_color(threshold=0.5):
    c = [uniform(0, 1), uniform(0, 1), uniform(0, 1)]

    if all(x < threshold for x in c):
        c[randint(0, 2)] = uniform(0.5, 1)

    return c
