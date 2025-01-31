from timescalecalculus import core


def test_is_valid():
    assert core.point.is_valid(1)
    assert not core.point.is_valid([1, 2])


def test_all_valid():
    assert core.point.all_valid([1, 2, 3])
    assert not core.point.all_valid([1, 2, [4, 5]])


def test_any_valid():
    assert core.point.any_valid([1, [1, 2]])
    assert not core.point.any_valid([[1, 2], [3, 4]])


def test_eq():
    assert core.point.eq(1, 1)
    assert not core.point.eq(1, 2)
    assert not core.point.eq(1, [3, 4])
    assert not core.point.eq([1, 2], [3, 4])
    assert not core.point.eq([1, 2], [1, 2])
