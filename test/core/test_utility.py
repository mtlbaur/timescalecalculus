import pytest
from timescalecalculus import core


def test_only_real_if_no_imag():
    assert core.utility.only_real_if_no_imag(1 + 1j) == 1 + 1j
    assert core.utility.only_real_if_no_imag(1 + 0j) == 1


def test_gen_even_seq():
    r = core.utility.gen_even_seq(1, 3, count=6)
    assert all(x == y for x, y in zip(r, [1.0, 1.4, 1.8, 2.2, 2.6, 3.0]))

    r = core.utility.gen_even_seq(1, 3, count=6, excl_start=True, excl_end=True)
    assert all(x == y for x, y in zip(r, [1.4, 1.8, 2.2, 2.6]))

    r = core.utility.gen_even_seq(1, 3, count=6, excl_start=True)
    assert all(x == pytest.approx(y) for x, y in zip(r, [1.4, 1.8, 2.2, 2.6, 3.0]))

    r = core.utility.gen_even_seq(1, 3, count=6, excl_end=True)
    assert all(x == y for x, y in zip(r, [1.0, 1.4, 1.8, 2.2, 2.6]))

    r = core.utility.gen_even_seq(3, 1, count=6)
    assert all(x == pytest.approx(y) for x, y in zip(r, [3.0, 2.6, 2.2, 1.8, 1.4, 1.0]))

    r = core.utility.gen_even_seq(3, 1, count=6, excl_start=True, excl_end=True)
    assert all(x == pytest.approx(y) for x, y in zip(r, [2.6, 2.2, 1.8, 1.4]))

    r = core.utility.gen_even_seq(3, 1, count=6, excl_start=True)
    assert all(x == y for x, y in zip(r, [2.6, 2.2, 1.8, 1.4, 1.0]))

    r = core.utility.gen_even_seq(3, 1, count=6, excl_end=True)
    assert all(x == pytest.approx(y) for x, y in zip(r, [3.0, 2.6, 2.2, 1.8, 1.4]))

    r = core.utility.gen_even_seq(1, 1, count=6)
    assert all(x == y for x, y in zip(r, [1, 1, 1, 1, 1, 1]))

    r = core.utility.gen_even_seq(1, 1, count=6, excl_start=True)
    assert all(x == y for x, y in zip(r, [1, 1, 1, 1, 1]))

    r = core.utility.gen_even_seq(1, 1, count=2, excl_start=True)
    assert all(x == y for x, y in zip(r, [1, 1]))

    r = core.utility.gen_even_seq(1, 3, stepsize=0.4)
    assert all(x == y for x, y in zip(r, [1.0, 1.4, 1.8, 2.2, 2.6, 3.0]))

    r = core.utility.gen_even_seq(3, 1, stepsize=0.4)
    assert all(x == pytest.approx(y) for x, y in zip(r, [3.0, 2.6, 2.2, 1.8, 1.4, 1.0]))

    r = core.utility.gen_even_seq(0, 4, stepsize=0.4)
    assert all(x == pytest.approx(y) for x, y in zip(r, [0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]))
