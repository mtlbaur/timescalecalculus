from timescalecalculus import core


def test_is_valid():
    assert core.interval.is_valid([1, 2])
    assert not core.interval.is_valid(1)


def test_all_valid():
    assert core.interval.all_valid([[1, 2], [3, 4]])
    assert not core.interval.all_valid([1, 2, [3, 4]])


def test_any_valid():
    assert core.interval.any_valid([1, [2, 3], 4])
    assert not core.interval.any_valid([1, 3, 4])


def test_eq():
    assert core.interval.eq([1, 2], [1, 2])
    assert not core.interval.eq([1, 2], [1, 3])
    assert not core.interval.eq([1, 2], [0, 2])
    assert not core.interval.eq([1, 2], [2, 1])
    assert not core.interval.eq([1, 2], [1, 2.1])
    assert not core.interval.eq([1, 2], [0.9, 2])
    assert not core.interval.eq([1, 2], [1.1, 2])
    assert not core.interval.eq([1, 2], [1, 1.9])
    assert not core.interval.eq([1, 2], [1.1, 1.9])


def test_contains_point():
    assert core.interval.contains_point([1, 2], 1)
    assert core.interval.contains_point([1, 2], 2)
    assert core.interval.contains_point([1, 2], 1.1)
    assert core.interval.contains_point([1, 2], 1.9)
    assert not core.interval.contains_point([1, 2], 0.9)
    assert not core.interval.contains_point([1, 2], 2.1)


def test_contains_interval():
    assert core.interval.contains_interval([1, 2], [1, 2])
    assert core.interval.contains_interval([1, 2], [1.1, 2])
    assert core.interval.contains_interval([1, 2], [1.1, 1.9])
    assert core.interval.contains_interval([1, 2], [1, 1.9])
    assert core.interval.contains_interval([1, 2], [1.1, 1.9])
    assert not core.interval.contains_interval([1, 2], [0.9, 2])
    assert not core.interval.contains_interval([1, 2], [1, 2.1])
    assert not core.interval.contains_interval([1, 2], [0.9, 2.1])


def test_contains():
    assert core.interval.contains([1, 2], 1)
    assert core.interval.contains([1, 2], 1.5)
    assert core.interval.contains([1, 2], 2)
    assert core.interval.contains([1, 2], [1, 2])
    assert core.interval.contains([1, 2], [1.2, 1.8])
    assert core.interval.contains([1, 2], [1.2, 2])
    assert core.interval.contains([1, 2], [1, 1.8])
    assert not core.interval.contains([1, 2], 0)
    assert not core.interval.contains([1, 2], [0, 1])
    assert not core.interval.contains([1, 2], [2, 3])
    assert not core.interval.contains([1, 2], [1, 2.1])
    assert not core.interval.contains([1, 2], [0.9, 2])
    assert not core.interval.contains([1, 2], [0.9, 2.1])


def test_overlaps():
    assert core.interval.overlaps([1, 2], [1, 2])
    assert core.interval.overlaps([1, 2], [1, 3])
    assert core.interval.overlaps([1, 2], [0, 1])
    assert core.interval.overlaps([1, 2], [0, 1.5])
    assert core.interval.overlaps([1, 2], [1.5, 3])
    assert core.interval.overlaps([1, 2], [2, 3])
    assert core.interval.overlaps([1, 2], [0, 3])
    assert not core.interval.overlaps([1, 2], [0, 0.5])
    assert not core.interval.overlaps([1, 2], [2.5, 3])
