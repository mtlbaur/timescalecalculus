from copy import deepcopy
from timescalecalculus import recursive
from timescalecalculus import legacytimescalecalculus as ltsc


def test_g_k_and_h_k():
    ts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    lts = ltsc.timescale(deepcopy(ts))
    cache = {}

    assert recursive.g_k(ts, 3, 1, 9, cache) == 120
    assert recursive.g_k(ts, 3, 1, 9, cache) == 120
    assert recursive.g_k(ts, 5, 1, 9, cache) == 792
    assert recursive.g_k(ts, 5, 1, 9, cache) == 792
    assert recursive.g_k(ts, 3, 1, 9, cache) == lts.g_k(3, 9, 1)

    cache.clear()

    assert recursive.h_k(ts, 3, 1, 9, cache) == 56
    assert recursive.h_k(ts, 3, 1, 9, cache) == 56
    assert recursive.h_k(ts, 5, 1, 9, cache) == 56
    assert recursive.h_k(ts, 5, 1, 9, cache) == 56
    assert recursive.h_k(ts, 3, 1, 9, cache) == lts.h_k(3, 9, 1)

    # commented out due to slow computing time

    # ts = [[0.5, 0.8], 1, 2, [3, 4], [5, 6], 7, 8, 9, [11, 12], [15, 19], 21, 22]
    # lts = ltsc.timescale(deepcopy(ts))
    # cache.clear()

    # assert recursive.g_k(ts, 3, 3, 3.01, cache) == 1.66666666666656e-07
    # assert recursive.g_k(ts, 3, 3, 3.01, cache) == 1.66666666666656e-07
    # assert recursive.g_k(ts, 3, 3, 3.01, cache) == lts.g_k(3, 3.01, 3)

    # cache.clear()

    # assert recursive.h_k(ts, 3, 3, 3.01, cache) == 1.66666666666656e-07
    # assert recursive.h_k(ts, 3, 3, 3.01, cache) == 1.66666666666656e-07
    # assert recursive.h_k(ts, 3, 3, 3.01, cache) == lts.h_k(3, 3.01, 3)
