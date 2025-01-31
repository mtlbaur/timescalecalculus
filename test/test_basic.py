import numpy
import mpmath
import pytest
from copy import deepcopy
from timescalecalculus import basic
from timescalecalculus import legacytimescalecalculus as ltsc


def test_sigma():
    a = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    b = ltsc.timescale(deepcopy(a))

    assert basic.sigma(a, 0) == 1
    assert basic.sigma(a, 1) == 2
    assert basic.sigma(a, 4) == 5
    assert basic.sigma(a, 5.5) == 5.5
    assert basic.sigma(a, 10) == 11
    assert basic.sigma(a, 34) == 35
    assert basic.sigma(a, 35) == 35

    vals = [0, 1, 3, 5, 5.5, 10, 12, 35]

    for x in vals:
        assert basic.sigma(a, x) == b.sigma(x)


def test_rho():
    ts = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]

    assert basic.rho(ts, 0) == 0
    assert basic.rho(ts, 4) == 3
    assert basic.rho(ts, 5) == 4
    assert basic.rho(ts, 5.5) == 5.5
    assert basic.rho(ts, 10) == 10
    assert basic.rho(ts, 11) == 10
    assert basic.rho(ts, 35) == 34

    a = [0, 1, 2, 3, 4]
    b = ltsc.timescale(deepcopy(a))

    for x in a:
        assert basic.rho(a, x) == b.rho(x)


def test_mu():
    a = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    b = ltsc.timescale(deepcopy(a))

    assert basic.mu(a, 0) == 1
    assert basic.mu(a, 3) == 1
    assert basic.mu(a, 4) == 1
    assert basic.mu(a, 5) == 0
    assert basic.mu(a, 5.5) == 0
    assert basic.mu(a, 10) == 1
    assert basic.mu(a, 11) == 1
    assert basic.mu(a, 34) == 1
    assert basic.mu(a, 35) == 0

    vals = [0, 1, 4, 5, 5.5, 10, 11, 34, 35]

    for x in vals:
        assert basic.mu(a, x) == b.mu(x)


def test_nu():
    ts = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]

    assert basic.nu(ts, 0) == 0
    assert basic.nu(ts, 4) == 1
    assert basic.nu(ts, 5) == 1
    assert basic.nu(ts, 5.5) == 0
    assert basic.nu(ts, 10) == 0
    assert basic.nu(ts, 11) == 1
    assert basic.nu(ts, 34) == 1
    assert basic.nu(ts, 35) == 1


def test_dderivative():
    a = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    b = ltsc.timescale(deepcopy(a))

    vals = [0, 1, 3, 4, 5, 5.5, 10, 11, 34, 35]
    fs = [lambda x: mpmath.sin(x), lambda x: mpmath.cos(x), lambda x: mpmath.cos(mpmath.cos(x)) ** x]

    for v in vals:
        for f in fs:
            assert basic.dderivative(a, f, v) == pytest.approx(b.dderivative(f, v), 1e-9)


# CHECK: add interval support?
def test_nderivative():
    a = [1, 2, 3, 5, 8, 10]
    b = ltsc.timescale(deepcopy(a))

    fs = [lambda x: mpmath.sin(x), lambda x: mpmath.cos(x), lambda x: mpmath.cos(mpmath.cos(x)) ** x]

    # `a[1:]` because the backwards derivative of the leftmost value causes a division by zero due to`nu(leftmost_value) == 0`
    for t in a[1:]:
        for f in fs:
            assert basic.nderivative(a, f, t) == b.nderivative(f, t)


def test_cyl():
    a = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    b = ltsc.timescale(deepcopy(a))

    for t in [0, 1, 3, 4, 5, 5.5, 10, 11, 34, 35]:
        for z in numpy.linspace(0, 10, 1000):
            assert basic.cyl(a, t, z) == b.cyl(t, z)


def test_dexp_p():
    ts = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    lts = ltsc.timescale(deepcopy(ts))

    def f(x):
        return x * 2j

    for t in [0, 1, 3, 4, 5, 5.5, 10, 11, 34, 35]:
        assert basic.dexp_p(ts, f, 0, t) == pytest.approx(lts.dexp_p(f, t, 0))


def test_mucircleminus():
    a = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    b = ltsc.timescale(deepcopy(a))

    fs = [lambda x: mpmath.sin(x), lambda x: mpmath.cos(x), lambda x: mpmath.cos(mpmath.cos(x)) ** x]

    for f in fs:
        for t in [0, 1, 3, 4, 5, 5.5, 10, 11, 34, 35]:
            assert basic.mucircleminus(a, f, t) == b.mucircleminus(f, t)


def test_dcos_p():
    ts = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    lts = ltsc.timescale(deepcopy(ts))

    def f(x):
        return x * 2j

    for t in [0, 1, 3, 4, 5, 5.5, 10, 11, 34, 35]:
        assert basic.dcos_p(ts, f, 0, t) == pytest.approx(lts.dcos_p(f, t, 0))


def test_dsin_p():
    ts = [0, 1, 2, 3, 4, [5, 10], 11, 12, 13, 14, 15, [16, 20], 21, 22, 23, 24, 25, [26, 30], 31, 32, 33, 34, 35]
    lts = ltsc.timescale(deepcopy(ts))

    def f(x):
        return x * 2j

    for t in [0, 1, 3, 4, 5, 5.5, 10, 11, 34, 35]:
        assert basic.dsin_p(ts, f, 0, t) == pytest.approx(lts.dsin_p(f, t, 0))


# FIX: missing intervals because the old library calls standard `max` on the timescale which doesn't work for number <-> list comparisons
def test_laplace_transform():
    ts = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 25, 26, 30, 31, 32, 33, 34, 35]
    lts = ltsc.timescale(deepcopy(ts))

    def f(x):
        return x * 2j

    def z(x):
        return x * -1j

    for s in [0, 1, 3, 4, 5, 10, 11, 34, 35]:
        assert basic.laplace_transform(ts, f, z, s) == lts.laplace_transform(f, z, s)
