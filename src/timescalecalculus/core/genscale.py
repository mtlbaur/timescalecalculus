"""Definitions for function-generated timescales."""

import mpmath
from timescalecalculus import core


def find_time_linear_search(gsf, target, start_bound, stop_bound):
    i = start_bound

    while i <= stop_bound:
        if core.time.contains(gsf(i), target):
            return i
        i += 1


def find_time_binary_search(gsf, target, left_bound, right_bound):
    """Only works when `gsf` generates sorted timescale values."""
    return core.utility.binary_search_template(
        target,
        left_bound,
        right_bound,
        gsf,
        core.time.contains,
        *core.scale.get_left_right_of_f([gsf(left_bound), gsf(right_bound)]),
    )


def find_time(gsf, target, start_bound, stop_bound, unsorted=True):
    if unsorted:
        return find_time_linear_search(gsf, target, start_bound, stop_bound)

    return find_time_binary_search(gsf, target, start_bound, stop_bound)


def solve_f(gsf, spf, sif, start_bound, stop_bound, start_time, stop_time):
    """
    This function expects the following to hold:

    - `gsf(start_bound)` contains `start_time`
    - `gsf(stop_bound)` contains `stop_time`
    """

    if start_bound > stop_bound:
        raise Exception()

    if start_time == stop_time:
        return 0

    cur = gsf(start_bound)

    if start_bound == stop_bound:
        return core.time.solve_step_f(cur, None, spf, sif, start_time=start_time, stop_time=stop_time)

    nxt = gsf(start_bound + 1)

    r = core.time.solve_step_f(cur, nxt, spf, sif, start_time=start_time)

    for i in range(start_bound + 1, stop_bound + 1):
        cur = nxt
        nxt = gsf(i)

        r += core.time.solve_step_f(cur, nxt, spf, sif)

    cur = gsf(stop_bound)

    return r + core.time.solve_step_f(cur, None, spf, sif, stop_time=stop_time)


def solve_nsum_f(gsf, spf, sif, start_bound, stop_bound):
    if start_bound == stop_bound:
        return 0

    cur = 0
    nxt = gsf(start_bound)

    def nsum_f(i_mpf):
        nonlocal cur, nxt

        cur = nxt
        nxt = gsf(float(i_mpf))

        return core.time.solve_step_f(cur, nxt, spf, sif)

    return mpmath.nsum(nsum_f, [start_bound + 1, stop_bound])


def solve_for_t_f(gsf, spf, sif, start_bound, stop_bound, start_time, stop_time, unsorted=True):
    if start_time == stop_time:
        return 0

    start_bound = find_time(gsf, start_time, start_bound, stop_bound, unsorted)
    stop_bound = find_time(gsf, stop_time, start_bound, stop_bound, unsorted)

    return solve_f(gsf, spf, sif, start_bound, stop_bound, start_time, stop_time)
