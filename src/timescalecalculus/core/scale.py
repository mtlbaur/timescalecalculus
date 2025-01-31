"""Definitions for timescales as lists of points and/or intervals."""

from enum import Enum
from timescalecalculus import core


class ValidityClass(Enum):
    """A class for describing a timescale's invalidity."""

    valid = 0
    empty = 1
    invalid_value = 2
    value_overlap = 3
    not_inc_or_dec = 4


# CHECK: could add optional parameters for controlling which conditions to check
def get_validity_class(ts):
    """
    This function returns `ValidityClass.valid` if `ts`:

    - Does not contain duplicate values; a point that is both in an interval and separate counts as duplicate.
    - Is strictly increasing or decreasing.

    Otherwise one of:

    - `ValidityClass.empty`
    - `ValidityClass.invalid_value`
    - `ValidityClass.value_overlap`
    - `ValidityClass.not_inc_or_dec`

    is returned.
    """

    if not ts:
        return ValidityClass.empty

    if len(ts) == 1:
        if core.time.is_valid(ts[0]):
            return ValidityClass.valid

        return ValidityClass.invalid_value

    comparator = None

    if core.time.is_valid(ts[0]) and core.time.is_valid(ts[1]):
        if core.time.lt(ts[0], ts[1]):
            comparator = core.time.gt
        elif core.time.gt(ts[0], ts[1]):
            comparator = core.time.lt
        else:
            return ValidityClass.value_overlap
    else:
        return ValidityClass.invalid_value

    def check_time_validity(t):
        if core.interval.is_valid(t):
            if comparator(t[0], t[1]):
                return ValidityClass.not_inc_or_dec
        elif not core.point.is_valid(t):
            return ValidityClass.invalid_value

    for i in range(len(ts) - 1):
        j = i + 1

        vc = check_time_validity(ts[i])

        if vc:
            return vc

        if core.time.overlaps(ts[i], ts[j]):
            return ValidityClass.value_overlap

        if comparator(ts[i], ts[j]):
            return ValidityClass.not_inc_or_dec

    vc = check_time_validity(ts[-1])

    if vc:
        return vc

    return ValidityClass.valid


def is_valid(ts):
    return get_validity_class(ts) == ValidityClass.valid


def all_valid(scales):
    return all(is_valid(s) for s in scales)


def any_valid(scales):
    return any(is_valid(s) for s in scales)


def find_all(ts, times):
    """Searches for the values of `times` in `ts`. When a match is found, it removes the time (and any duplicates) from `times`; a search that finds all values listed in `times` will return an empty list."""

    targets = times.copy()

    for time in ts:
        found_times = []

        for target in targets:
            if core.time.contains(time, target):
                found_times.append(target)

        for found in found_times:
            targets.remove(found)

        if not targets:
            return targets

    return targets


def contains_all(ts, times):
    return len(find_all(ts, times)) == 0


def contains(ts, time):
    return contains_all(ts, [time])


def linear_search_f(ts, target, f):
    """Linear search `ts` feeding each `ts[i]` along with `target` to argument function `f`. If `f` returns true, return the index of the current `ts[i]`. If `f` never returns true, return -1."""

    for i in range(len(ts)):
        if f(ts[i], target):
            return i

    return -1


def binary_search_f(ts, target, f):
    """Binary search `ts` feeding each `ts[i]` along with `target` to argument function `f`. If `f` returns true, return the index of the current `ts[i]`. If `f` never returns true, return -1. Assumes `ts` is sorted."""

    return core.utility.binary_search_template(target, 0, len(ts) - 1, lambda m: ts[m], f, *get_left_right_of_f(ts))


def find_point(ts, point):
    """Returns the index of `point` in `ts` or -1 if not found."""
    return binary_search_f(ts, point, core.point.eq)


def find_interval(ts, interval):
    """Returns the index of `interval` in `ts` or -1 if not found."""
    return binary_search_f(ts, interval, core.interval.contains)


def find_time(ts, time):
    """
    Returns the index of `time` in `ts` or -1 if not found.

    `time` can be:

    1. a discrete point
    2. an interval
    3. a point in an interval
    """
    return binary_search_f(ts, time, core.time.contains)


def has_point(ts, point):
    return find_point(ts, point) != -1


def has_interval(ts, interval):
    return find_interval(ts, interval) != -1


def has_time(ts, time):
    return find_time(ts, time) != -1


def conv_interval_to_even_seq(ts, **kwargs):
    """Scan `ts` for intervals and convert them into evenly-spaced sequences of numbers via `core.util.gen_even_seq(interval[0], interval[1], **kwargs)`. The result is returned as a new list."""

    points = []

    for time in ts:
        if core.point.is_valid(time):
            points.append(time)

        elif core.interval.is_valid(time):
            for point in core.utility.gen_even_seq(time[0], time[1], **kwargs):
                points.append(point)

        else:
            raise Exception(time)

    return points


def min_(ts):
    return core.time.min_(ts[0], ts[-1])


def max_(ts):
    return core.time.max_(ts[0], ts[-1])


def min_max(ts):
    return core.time.min_max(ts[0], ts[-1])


def inc_i(ts, i):
    i += 1
    return i if valid_index(ts, i) else -1


def dec_i(ts, i):
    i -= 1
    return i if valid_index(ts, i) else -1


def is_inc(ts):
    return core.time.le(ts[0], ts[-1])


def is_dec(ts):
    return core.time.ge(ts[0], ts[-1])


def get_left_i(ts, i):
    i = dec_i(ts, i)
    return i if valid_index(ts, i) else -1


def get_right_i(ts, i):
    i = inc_i(ts, i)
    return i if valid_index(ts, i) else -1


def get_left(ts, i):
    i = dec_i(ts, i)
    return ts[i] if valid_index(ts, i) else None


def get_right(ts, i):
    i = inc_i(ts, i)
    return ts[i] if valid_index(ts, i) else None


def get_left_closest(ts, i):
    l = get_left(ts, i)
    return l[1] if l and core.interval.is_valid(l) else l


def get_right_closest(ts, i):
    r = get_right(ts, i)
    return r[0] if r and core.interval.is_valid(r) else r


def left_of(ts, a, b):
    if is_inc(ts):
        return core.time.lt(a, b)
    return core.time.gt(a, b)


def right_of(ts, a, b):
    if is_inc(ts):
        return core.time.gt(a, b)
    return core.time.lt(a, b)


def get_left_of_f(ts):
    if is_inc(ts):
        return core.time.lt
    if is_dec(ts):
        return core.time.gt

    raise Exception()


def get_right_of_f(ts):
    if is_inc(ts):
        return core.time.gt
    if is_dec(ts):
        return core.time.lt

    raise Exception()


def get_left_right_of_f(ts):
    if is_inc(ts):
        return (core.time.lt, core.time.gt)
    if is_dec(ts):
        return (core.time.gt, core.time.lt)

    raise Exception()


def valid_index(ts, i):
    return i >= 0 and i < len(ts)


def init_index_time(ts, index, time, side):
    if time is None:
        if index is None:
            index = 0 if side == 0 else len(ts) - 1

        if core.point.is_valid(ts[index]):
            time = ts[index]
        elif core.interval.is_valid(ts[index]):
            time = ts[index][side]
        else:
            raise Exception()

    if index is None:
        index = core.scale.find_time(ts, time)

        if index == -1:
            raise Exception()

    return (index, time)


def solve_step_i_f(ts, i, spf, sif, start_time=None, stop_time=None):
    """
    A generalization that will solve from one point/interval to the next point/interval.

    `spf` is the point-solving function; `sif` is the interval-solving function.

    Both `spf` and `sif` require the following signature:

    ```py
    def sf(ts, i, l, r): ...
    ```

    where:

    - `ts` is the timescale
    - `i` is the index of the current timescale value from which to solve
    - `l` is the left point or interval bound
    - `r` is the right point or interval bound

    How `spf` and `sif` evaluate their arguments is up to the user. The values returned from these functions are summed and returned.

    The keyword arguments `start_time` and `stop_time` allow a sub-interval of `cur` to be solved. This means that if either `start_time` or `stop_time` are defined, `cur` must be an interval and `nxt` is unused.
    """

    cur = ts[i]
    nxt = get_right(ts, i)
    nxt_closest = nxt[0] if core.interval.is_valid(nxt) else nxt

    if core.point.is_valid(cur):
        if start_time is not None and not core.point.eq(cur, start_time):
            raise Exception()
        if stop_time is not None and not core.point.eq(cur, stop_time):
            raise Exception()

        return spf(ts, i, cur, nxt_closest) if nxt_closest and not stop_time else 0

    elif core.interval.is_valid(cur):
        l, r = cur

        if start_time is not None:
            if core.interval.contains_point(cur, start_time):
                l = start_time
            else:
                raise Exception()

        if stop_time is not None:
            if core.interval.contains_point(cur, stop_time):
                r = stop_time
            else:
                raise Exception()

        return sif(ts, i, l, r) + (spf(ts, i, r, nxt_closest) if nxt_closest and not stop_time else 0)

    raise Exception()


def solve_i_f(ts, spf, sif, start_index=None, stop_index=None, start_time=None, stop_time=None):
    start_index, start_time = init_index_time(ts, start_index, start_time, 0)
    stop_index, stop_time = init_index_time(ts, stop_index, stop_time, 1)

    if start_index > stop_index:
        raise Exception()

    if start_time == stop_time:
        return 0

    if start_index == stop_index:
        return solve_step_i_f(ts, start_index, spf, sif, start_time=start_time, stop_time=stop_time)

    r = solve_step_i_f(ts, start_index, spf, sif, start_time=start_time)

    for i in range(start_index + 1, stop_index):
        r += solve_step_i_f(ts, i, spf, sif)

    return r + solve_step_i_f(ts, stop_index, spf, sif, stop_time=stop_time)


def solve_f(ts, spf, sif, start_index=None, stop_index=None, start_time=None, stop_time=None):
    start_index, start_time = init_index_time(ts, start_index, start_time, 0)
    stop_index, stop_time = init_index_time(ts, stop_index, stop_time, 1)

    if start_index > stop_index:
        raise Exception()

    if start_time == stop_time:
        return 0

    if start_index == stop_index:
        return core.time.solve_step_f(ts[start_index], None, spf, sif, start_time=start_time, stop_time=stop_time)

    r = core.time.solve_step_f(ts[start_index], get_right(ts, start_index), spf, sif, start_time=start_time)

    for i in range(start_index + 1, stop_index):
        r += core.time.solve_step_f(ts[i], get_right(ts, i), spf, sif)

    return r + core.time.solve_step_f(ts[stop_index], None, spf, sif, stop_time=stop_time)
