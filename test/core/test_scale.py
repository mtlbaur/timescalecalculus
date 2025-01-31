import pytest
from timescalecalculus import core


def test_get_validity_class():
    V = core.scale.ValidityClass.valid
    E = core.scale.ValidityClass.empty
    VO = core.scale.ValidityClass.value_overlap
    NIOD = core.scale.ValidityClass.not_inc_or_dec

    assert core.scale.get_validity_class([1, 2, 3]) is V
    assert core.scale.get_validity_class([1, [2, 3]]) is V
    assert core.scale.get_validity_class([1, [2, 3], [4, 5]]) is V
    assert core.scale.get_validity_class([1, [2, 3], 3.5, [4, 5]]) is V
    assert core.scale.get_validity_class([[2, 3], [4, 5]]) is V
    assert core.scale.get_validity_class([3, 2, 1]) is V

    assert core.scale.get_validity_class([]) is E

    assert core.scale.get_validity_class([1, 2, 2, 3]) is VO
    assert core.scale.get_validity_class([[2, 3], [3, 5]]) is VO
    assert core.scale.get_validity_class([1, [2, 3], [3, 4]]) is VO
    assert core.scale.get_validity_class([1, [2, 3], 2]) is VO

    assert core.scale.get_validity_class([1, 2, 1.5]) is NIOD
    assert core.scale.get_validity_class([1, [3, 2]]) is NIOD
    assert core.scale.get_validity_class([1, [2, 3], 0]) is NIOD
    assert core.scale.get_validity_class([1, [2, 3], [0, -1]]) is NIOD


def test_is_valid():
    assert core.scale.is_valid([1, 2, 3])
    assert core.scale.is_valid([[1, 2], [3, 4]])
    assert core.scale.is_valid([[1, 2], [3, 4], 5, 7.5, [8.2, 8.4]])


def test_all_valid():
    assert core.scale.all_valid(
        [
            [1, 2, 3],
            [[1, 2], [3, 4]],
            [1, [2, 3], 3.5, [4, 5]],
        ]
    )


def test_any_valid():
    assert core.scale.any_valid(
        [
            [1, 2, 3],
            [[1, 2], [3, 4]],
            [1, [2, 3], 3.5, [4, 5]],
        ]
    )


def test_find_all():
    ts = [1, 2, 3, [4, 5], 7, 8, [9, 12], 15]

    assert core.scale.find_all(ts, [2, 3, 4.5]) == []
    assert core.scale.find_all(ts, [2, 3, 4.5, 7.7]) == [7.7]
    assert core.scale.find_all(ts, [1, 2, 3, [4, 5], 7, 8, [9, 12], 15, 4, 4.5, 5, 7.7]) == [7.7]


def test_contains_all():
    ts = [1, 2, 3, [4, 5]]

    assert core.scale.contains_all(ts, [1, 2, 3, [4, 5], 4, 4.5, 5])
    assert not core.scale.contains_all(ts, [1.2])


def test_contains():
    ts = [1, 2, 3, [4, 5]]

    assert core.scale.contains(ts, 1)
    assert core.scale.contains(ts, 4)
    assert core.scale.contains(ts, 4.5)
    assert core.scale.contains(ts, 5)
    assert not core.scale.contains(ts, 0)
    assert not core.scale.contains(ts, 6)
    assert not core.scale.contains(ts, 1.2)


def test_binary_search_f():
    ts = [1, 2, 3, [4, 5], 7, 8, [9, 12], 15]

    assert core.scale.binary_search_f(ts, 1, core.point.eq) == 0
    assert core.scale.binary_search_f(ts, 2, core.point.eq) == 1
    assert core.scale.binary_search_f(ts, 3, core.point.eq) == 2
    assert core.scale.binary_search_f(ts, 4, core.point.eq) == -1
    assert core.scale.binary_search_f(ts, 4.5, core.point.eq) == -1
    assert core.scale.binary_search_f(ts, 5, core.point.eq) == -1
    assert core.scale.binary_search_f(ts, [4, 5], core.point.eq) == -1
    assert core.scale.binary_search_f(ts, 7, core.point.eq) == 4
    assert core.scale.binary_search_f(ts, 8, core.point.eq) == 5
    assert core.scale.binary_search_f(ts, 9, core.point.eq) == -1
    assert core.scale.binary_search_f(ts, 9.5, core.point.eq) == -1
    assert core.scale.binary_search_f(ts, 12, core.point.eq) == -1
    assert core.scale.binary_search_f(ts, [9, 12], core.point.eq) == -1
    assert core.scale.binary_search_f(ts, 15, core.point.eq) == 7

    assert core.scale.binary_search_f(ts, 1, core.interval.contains) == -1
    assert core.scale.binary_search_f(ts, 2, core.interval.contains) == -1
    assert core.scale.binary_search_f(ts, 3, core.interval.contains) == -1
    assert core.scale.binary_search_f(ts, 4, core.interval.contains) == 3
    assert core.scale.binary_search_f(ts, 4.5, core.interval.contains) == 3
    assert core.scale.binary_search_f(ts, 5, core.interval.contains) == 3
    assert core.scale.binary_search_f(ts, [4, 5], core.interval.eq) == 3
    assert core.scale.binary_search_f(ts, 7, core.interval.contains) == -1
    assert core.scale.binary_search_f(ts, 8, core.interval.contains) == -1
    assert core.scale.binary_search_f(ts, 9, core.interval.contains) == 6
    assert core.scale.binary_search_f(ts, 9.5, core.interval.contains) == 6
    assert core.scale.binary_search_f(ts, 12, core.interval.contains) == 6
    assert core.scale.binary_search_f(ts, [9, 12], core.interval.eq) == 6
    assert core.scale.binary_search_f(ts, 15, core.interval.contains) == -1

    assert core.scale.binary_search_f(ts, 1, core.time.eq) == 0
    assert core.scale.binary_search_f(ts, 2, core.time.eq) == 1
    assert core.scale.binary_search_f(ts, 3, core.time.eq) == 2
    assert core.scale.binary_search_f(ts, 4, core.time.contains) == 3
    assert core.scale.binary_search_f(ts, 4.5, core.time.contains) == 3
    assert core.scale.binary_search_f(ts, 5, core.time.contains) == 3
    assert core.scale.binary_search_f(ts, [4, 5], core.time.eq) == 3
    assert core.scale.binary_search_f(ts, 7, core.time.eq) == 4
    assert core.scale.binary_search_f(ts, 8, core.time.eq) == 5
    assert core.scale.binary_search_f(ts, 9, core.time.contains) == 6
    assert core.scale.binary_search_f(ts, 9.5, core.time.contains) == 6
    assert core.scale.binary_search_f(ts, 12, core.time.contains) == 6
    assert core.scale.binary_search_f(ts, [9, 12], core.time.eq) == 6
    assert core.scale.binary_search_f(ts, 15, core.time.eq) == 7


def test_find_point():
    ts = [1, 2, 3, [4, 5], 7, 8, [9, 12], 15]

    assert core.scale.find_point(ts, 2) == 1
    assert core.scale.find_point(ts, 4) == -1
    assert core.scale.find_point(ts, 4.5) == -1
    assert core.scale.find_point(ts, [4, 5]) == -1


def test_find_interval():
    ts = [1, 2, 3, [4, 5], 7, 8, [9, 12], 15]

    assert core.scale.find_interval(ts, [4, 5]) == 3
    assert core.scale.find_interval(ts, 4) == 3
    assert core.scale.find_interval(ts, 4.5) == 3
    assert core.scale.find_interval(ts, 5) == 3
    assert core.scale.find_interval(ts, [3, 4]) == -1
    assert core.scale.find_interval(ts, 3) == -1


def test_find_time():
    ts = [1, 2, 3, [4, 5], 7, 8, [9, 12], 15]

    assert core.scale.find_time(ts, [4, 5]) == 3
    assert core.scale.find_time(ts, 4.5) == 3
    assert core.scale.find_time(ts, 3) == 2
    assert core.scale.find_time(ts, [3, 4]) == -1
    assert core.scale.find_time(ts, [3, 7]) == -1
    assert core.scale.find_time(ts, 16) == -1


def test_has_point():
    ts = [1, 2, 3, [4, 5], 7, 8, [9, 12], 15]

    assert core.scale.has_point(ts, 2)
    assert not core.scale.has_point(ts, 4)
    assert not core.scale.has_point(ts, 4.5)
    assert not core.scale.has_point(ts, [4, 5])


def test_has_interval():
    ts = [1, 2, 3, [4, 5], 7, 8, [9, 12], 15]

    assert core.scale.has_interval(ts, [4, 5])
    assert core.scale.has_interval(ts, 4)
    assert core.scale.has_interval(ts, 4.5)
    assert core.scale.has_interval(ts, 5)
    assert not core.scale.has_interval(ts, [3, 4])
    assert not core.scale.has_interval(ts, 3)


def test_has_time():
    ts = [1, 2, 3, [4, 5], 7, 8, [9, 12], 15]

    assert core.scale.has_time(ts, [4, 5])
    assert core.scale.has_time(ts, 4.5)
    assert core.scale.has_time(ts, 3)
    assert not core.scale.has_time(ts, [3, 4])
    assert not core.scale.has_time(ts, [3, 7])
    assert not core.scale.has_time(ts, 16)


def test_conv_interval_to_even_seq():
    r = core.scale.conv_interval_to_even_seq([1, 3, [4, 5], 8, [9.8, 10.4], 15], stepsize=0.2)
    assert all(x == pytest.approx(y) for x, y in zip(r, [1, 3, 4, 4.2, 4.4, 4.6, 4.8, 5, 8, 9.8, 10, 10.2, 10.4, 15]))


def test_min_():
    for ts in [
        [1, 2, 3, 7],
        [[1, 2], 4, [6, 7]],
        [1, 2, [4, 7]],
        [[1, 2], 4, 7],
    ]:
        assert core.scale.min_(ts) == 1


def test_max_():
    for ts in [
        [1, 2, 3, 7],
        [[1, 2], 4, [6, 7]],
        [1, 2, [4, 7]],
        [[1, 2], 4, 7],
    ]:
        assert core.scale.max_(ts) == 7


def test_min_max():
    for ts in [
        [1, 2, 3, 7],
        [[1, 2], 4, [6, 7]],
        [1, 2, [4, 7]],
        [[1, 2], 4, 7],
    ]:
        r = core.scale.min_max(ts)
        assert r == (1, 7)
        assert len(r) == 2


def test_solve_step_i_f():
    f = core.scale.solve_step_i_f
    spf = lambda ts, i, l, r: abs(r - l) * 2
    sif = lambda ts, i, l, r: abs(r - l)

    ts = [1, 2, [3, 4], 5, [6, 7], [8, 9]]

    assert f(ts, 0, spf, sif) == 2
    assert f(ts, 1, spf, sif) == 2
    assert f(ts, 2, spf, sif) == 3
    assert f(ts, 2, spf, sif, start_time=3.5) == 2.5
    assert f(ts, 2, spf, sif, start_time=3.5, stop_time=3.8) == pytest.approx(0.3)
    assert f(ts, 2, spf, sif, stop_time=3.8) == pytest.approx(0.8)
    assert f(ts, 4, spf, sif, start_time=6.5) == 0.5 + 2
    assert f(ts, 4, spf, sif, start_time=6.5, stop_time=7) == 0.5
    assert f(ts, 4, spf, sif, stop_time=7) == 1


def test_solve_i_f():
    f = core.scale.solve_i_f
    spf = lambda ts, i, l, r: abs(r - l) * 2
    sif = lambda ts, i, l, r: abs(r - l)

    ts = [1, 2, [3, 4], 5, [6, 7], [8, 9]]
    last = len(ts) - 1

    assert f(ts, spf, sif) == 13
    assert f(ts, spf, sif, start_index=0, stop_index=last) == 13
    assert f(ts, spf, sif, start_time=1, stop_time=9) == 13

    assert f(ts, spf, sif, start_index=1, stop_index=last - 1) == 8
    assert f(ts, spf, sif, start_time=2, stop_time=7) == 8

    assert f(ts, spf, sif, start_index=1, stop_time=7) == 8
    assert f(ts, spf, sif, start_time=2, stop_index=last - 1) == 8

    assert f(ts, spf, sif, start_time=2, stop_index=last - 1) == 8
    assert f(ts, spf, sif, start_index=1, stop_time=7) == 8

    assert f(ts, spf, sif, start_index=2, stop_index=2, start_time=3.1, stop_time=3.2) == pytest.approx(0.1)
    assert f(ts, spf, sif, start_time=3.1, stop_time=3.2) == pytest.approx(0.1)

    assert f(ts, spf, sif, start_index=2, stop_index=2) == 1
    assert f(ts, spf, sif, start_index=1, stop_index=1) == 0

    assert f(ts, spf, sif, start_index=2, stop_index=last) == 9
    assert f(ts, spf, sif, start_time=3, stop_time=5) == 3
    assert f(ts, spf, sif, start_index=2, stop_time=5) == 3
    assert f(ts, spf, sif, start_index=2, stop_index=last - 2) == 3
    assert f(ts, spf, sif, start_index=2, stop_time=8.5) == 8.5
    assert f(ts, spf, sif, start_time=3.5, stop_index=last - 2) == 2.5
    assert f(ts, spf, sif, start_time=3.5, stop_time=3.5) == 0
    assert f(ts, spf, sif, start_time=3.5, stop_time=3.75) == 0.25


def test_solve_f():
    f = core.scale.solve_f
    spf = lambda l, r: abs(r - l) * 2
    sif = lambda l, r: abs(r - l)

    ts = [1, 2, [3, 4], 5, [6, 7], [8, 9]]
    last = len(ts) - 1

    assert f(ts, spf, sif) == 13
    assert f(ts, spf, sif, start_index=0, stop_index=last) == 13
    assert f(ts, spf, sif, start_time=1, stop_time=9) == 13

    assert f(ts, spf, sif, start_index=1, stop_index=last - 1) == 8
    assert f(ts, spf, sif, start_time=2, stop_time=7) == 8

    assert f(ts, spf, sif, start_index=1, stop_time=7) == 8
    assert f(ts, spf, sif, start_time=2, stop_index=last - 1) == 8

    assert f(ts, spf, sif, start_time=2, stop_index=last - 1) == 8
    assert f(ts, spf, sif, start_index=1, stop_time=7) == 8

    assert f(ts, spf, sif, start_index=2, stop_index=2, start_time=3.1, stop_time=3.2) == pytest.approx(0.1)
    assert f(ts, spf, sif, start_time=3.1, stop_time=3.2) == pytest.approx(0.1)

    assert f(ts, spf, sif, start_index=2, stop_index=2) == 1
    assert f(ts, spf, sif, start_index=1, stop_index=1) == 0

    assert f(ts, spf, sif, start_index=2, stop_index=last) == 9
    assert f(ts, spf, sif, start_time=3, stop_time=5) == 3
    assert f(ts, spf, sif, start_index=2, stop_time=5) == 3
    assert f(ts, spf, sif, start_index=2, stop_index=last - 2) == 3
    assert f(ts, spf, sif, start_index=2, stop_time=8.5) == 8.5
    assert f(ts, spf, sif, start_time=3.5, stop_index=last - 2) == 2.5
    assert f(ts, spf, sif, start_time=3.5, stop_time=3.5) == 0
    assert f(ts, spf, sif, start_time=3.5, stop_time=3.75) == 0.25
