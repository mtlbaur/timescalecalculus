import pytest
from timescalecalculus import core


def test_is_valid():
    assert core.time.is_valid(1)
    assert core.time.is_valid(1.5)
    assert core.time.is_valid([1, 2.5])
    assert not core.time.is_valid([1, 2, 3])
    assert not core.time.is_valid("invalid")
    assert not core.time.is_valid([1, "invalid"])


def test_all_valid():
    assert core.time.all_valid([1, 1.5, [1, 2.5]])
    assert not core.time.all_valid([1, 2, [3, 4, 5], [6, 7]])


def test_any_valid():
    assert core.time.any_valid([1, 2])
    assert core.time.any_valid([1, [2, 3]])
    assert core.time.any_valid([[1, 2], [3, 4]])
    assert not core.time.any_valid([[3, 4, 5], "invalid"])


def test_get_type():
    assert core.time.get_type(1) is core.time.Type.point
    assert core.time.get_type([1, 2]) is core.time.Type.interval


def test_get_point_class():
    LS = core.time.PointClass.left_scattered
    RS = core.time.PointClass.right_scattered
    LD = core.time.PointClass.left_dense
    RD = core.time.PointClass.right_dense

    assert core.time.get_point_class(1) == (LS, RS)
    assert core.time.get_point_class(1, 1) == (LS, RS)
    assert core.time.get_point_class([1, 2], 1) == (LS, RD)
    assert core.time.get_point_class([1, 2], 1.5) == (LD, RD)
    assert core.time.get_point_class([1, 2], 2) == (LD, RS)


def test_is_left_dense():
    assert not core.time.is_left_dense([1, 2], 1)
    assert core.time.is_left_dense([1, 2], 1.5)
    assert core.time.is_left_dense([1, 2], 2)


def test_is_right_dense():
    assert core.time.is_right_dense([1, 2], 1)
    assert core.time.is_right_dense([1, 2], 1.5)
    assert not core.time.is_right_dense([1, 2], 2)


def test_is_left_scattered():
    assert core.time.is_left_scattered(1)
    assert core.time.is_left_scattered(1, 1)
    assert core.time.is_left_scattered([1, 2], 1)
    assert not core.time.is_left_scattered([1, 2], 1.5)
    assert not core.time.is_left_scattered([1, 2], 2)


def test_is_right_scattered():
    assert core.time.is_right_scattered(1)
    assert core.time.is_right_scattered(1, 1)
    assert not core.time.is_right_scattered([1, 2], 1)
    assert not core.time.is_right_scattered([1, 2], 1.5)
    assert core.time.is_right_scattered([1, 2], 2)


def test_overlaps():
    assert core.time.overlaps(1, 1)
    assert core.time.overlaps(1, [1, 2])
    assert core.time.overlaps([1, 2], 1)
    assert core.time.overlaps(2, [1, 2])
    assert core.time.overlaps([1, 2], 2)
    assert core.time.overlaps(1.5, [1, 2])
    assert core.time.overlaps([1, 2], 1.5)
    assert core.time.overlaps([1, 2], [1, 2])
    assert core.time.overlaps([0, 1], [1, 2])
    assert core.time.overlaps([1, 2], [0, 1])
    assert core.time.overlaps([2, 3], [1, 2])
    assert core.time.overlaps([1, 2], [2, 3])
    assert core.time.overlaps([0, 1.5], [1, 2])
    assert core.time.overlaps([1, 2], [1, 1.5])
    assert core.time.overlaps([0, 3], [1, 2])
    assert core.time.overlaps([1, 2], [0, 3])
    assert not core.time.overlaps(1, 2)
    assert not core.time.overlaps(1, [2, 3])
    assert not core.time.overlaps([0, 1], [2, 3])


def test_lt():
    assert core.time.lt(1, 2)
    assert core.time.lt(2, [3, 4])
    assert core.time.lt([1, 2], [3, 4])
    assert not core.time.lt(2, 2)
    assert not core.time.lt(2, 1)
    assert not core.time.lt(3, [3, 4])
    assert not core.time.lt([1, 3], [3, 4])


def test_le():
    assert core.time.le(1, 2)
    assert core.time.le(2, 2)
    assert core.time.le(2, [3, 4])
    assert core.time.le([1, 2], [3, 4])
    assert core.time.le([3, 4], [3, 4])
    assert not core.time.le(3, 2)
    assert not core.time.le([2, 3], 2)
    assert not core.time.le([2, 3], 1)
    assert not core.time.le([2, 4], [3, 4])


def test_eq():
    assert core.time.eq(2, 2)
    assert core.time.eq([3, 4], [3, 4])
    assert not core.time.eq(2, 3)
    assert not core.time.eq(3, [3, 4])
    assert not core.time.eq([3, 4], 3)
    assert not core.time.eq([3, 4], [3, 5])
    assert not core.time.eq([3, 4], [4, 3])


def test_ge():
    assert core.time.ge(2, 1)
    assert core.time.ge(2, 2)
    assert core.time.ge([3, 4], 2)
    assert core.time.ge([3, 4], [1, 2])
    assert core.time.ge([3, 4], [3, 4])
    assert not core.time.ge(2, 3)
    assert not core.time.ge(2, [2, 3])
    assert not core.time.ge(1, [2, 3])
    assert not core.time.ge([3, 4], [2, 3])
    assert not core.time.ge([3, 4], [5, 6])


def test_gt():
    assert core.time.gt(3, 2)
    assert core.time.gt([4, 5], 3)
    assert core.time.gt([5, 6], [3, 4])
    assert not core.time.gt(3, 3)
    assert not core.time.gt(3, 4)
    assert not core.time.gt([4, 5], 4)
    assert not core.time.gt([5, 6], [3, 5])
    assert not core.time.gt([5, 6], [7, 8])


def test_contains():
    assert core.time.contains(1, 1)
    assert core.time.contains([1, 2], 1)
    assert core.time.contains([1, 2], 1.5)
    assert core.time.contains([1, 2], 2)
    assert core.time.contains([1, 2], [1, 2])
    assert core.time.contains([1, 2], [1, 1.5])
    assert core.time.contains([1, 2], [1.5, 2])
    assert core.time.contains([1, 2], [1.25, 1.75])
    assert not core.time.contains(1, 0)
    assert not core.time.contains([1, 2], 0)
    assert not core.time.contains([1, 2], 4)
    assert not core.time.contains([1, 2], [3, 4])
    assert not core.time.contains([1, 2], [2, 4])
    assert not core.time.contains([1, 2], [0, 1])


def test_min_():
    for ts in [
        [1, 2, 3, 7],
        [[1, 2], 4, [6, 7]],
        [1, 2, [4, 7]],
        [[1, 2], 4, 7],
    ]:
        assert core.time.min_(ts[0], ts[-1]) == 1


def test_max_():
    for ts in [
        [1, 2, 3, 7],
        [[1, 2], 4, [6, 7]],
        [1, 2, [4, 7]],
        [[1, 2], 4, 7],
    ]:
        assert core.time.max_(ts[0], ts[-1]) == 7


def test_min_max():
    for ts in [
        [1, 2, 3, 7],
        [[1, 2], 4, [6, 7]],
        [1, 2, [4, 7]],
        [[1, 2], 4, 7],
    ]:
        r = core.time.min_max(ts[0], ts[-1])
        assert r == (1, 7)
        assert len(r) == 2


def test_solve_step_f():
    spf = lambda cur, nxt: abs(nxt - cur) * 2
    sif = lambda begin, end: abs(end - begin)

    assert core.time.solve_step_f(1, 2, spf, sif) == 2
    assert core.time.solve_step_f(2, [3, 4], spf, sif) == 2
    assert core.time.solve_step_f([3, 4], 5, spf, sif) == 1 + 2
    assert core.time.solve_step_f([3, 4], 5, spf, sif, start_time=3.5) == 0.5 + 2
    assert core.time.solve_step_f([3, 4], None, spf, sif, start_time=3.5, stop_time=3.8) == pytest.approx(0.3)
    assert core.time.solve_step_f([3, 4], None, spf, sif, stop_time=3.8) == pytest.approx(0.8)
    assert core.time.solve_step_f([6, 7], [8, 9], spf, sif, start_time=6.5) == 0.5 + 2
    assert core.time.solve_step_f([6, 7], None, spf, sif, start_time=6.5, stop_time=7) == 0.5
    assert core.time.solve_step_f([6, 7], None, spf, sif, stop_time=7) == 1
