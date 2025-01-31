import math
import mpmath
import pytest
from copy import deepcopy
from timescalecalculus import integral
from timescalecalculus import legacytimescalecalculus as ltsc


def test_solve_delta_ts():
    a = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    b = ltsc.timescale(deepcopy(a))

    def f(t):
        return mpmath.sin(t) + t * 1j

    ar = integral.solve_delta_ts(a, f, 0, 35)
    br = b.dintegral(f, 35, 0)

    assert ar.real == pytest.approx(br.real)
    assert ar.imag == br.imag


def solve_gen_ts_nsum():
    ts = ltsc.timescale([])

    def x(t):
        return 100 / (10**t)

    def gen_ts_f(t):
        if t % 2 == 0:
            return t
        return [t, t + 0.5]

    af = integral.solve_gen_ts_nsum
    bf = ts.compute_potentially_infinite_timescale

    ar = af(gen_ts_f, x, 0, math.inf)
    br = bf(x, gen_ts_f, [0, math.inf])

    assert ar == br


def test_solve_gen_ts_for_t():
    ts = ltsc.timescale([])

    def x(t):
        return 100 / (10**t)

    def gen_ts_f(t):
        if t % 2 == 0:
            return t
        return [t, t + 0.5]

    af = integral.solve_gen_ts_for_t
    bf = ts.compute_potentially_infinite_timescale_for_t

    ar = af(gen_ts_f, x, 1, math.inf, 3.24, 17.3)
    br = bf(x, 17.3, 3.24, gen_ts_f, [0, math.inf])

    assert ar == pytest.approx(br)


def test_solve_gen_ts_for_t_old():
    ts = ltsc.timescale([])

    def x(t):
        return 100 / (10**t)

    def gen_ts_f(t):
        if t % 2 == 0:
            return t
        return [t, t + 0.5]

    af = integral.solve_gen_ts_for_t_old
    bf = ts.compute_potentially_infinite_timescale_for_t

    ar = af(gen_ts_f, x, 1, math.inf, 3.24, 17.3)
    br = bf(x, 17.3, 3.24, gen_ts_f, [0, math.inf])

    assert ar == pytest.approx(br)
