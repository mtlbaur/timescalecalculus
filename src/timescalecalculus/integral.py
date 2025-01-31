import mpmath
from timescalecalculus import core, basic


def solve_point(f, cur, nxt):
    """Integrate a function `f` from timescale point `cur` to `nxt`. `nxt` must immediately follow `cur`."""
    return 0 if cur == nxt else (nxt - cur) * f(cur)


def solve_interval(f, begin, end, **kwargs):
    """
    Integrate a function `f` over a timescale interval `[s, t]`; accepts complex-valued functions.

    - `f`: a function of the form `f(x) = y` where `(x, y)` are numbers.
    - `begin`: starting integral bound.
    - `end`: ending integral bound.
    - `kwargs`: `mpmath.quad()` keyword-args.

    If the imaginary part is zero, only the real component is returned.
    """

    if begin == end:
        return 0

    real = float(mpmath.quad(lambda t: f(t).real, [begin, end], **kwargs))
    imag = float(mpmath.quad(lambda t: f(t).imag, [begin, end], **kwargs))

    return real if imag == 0 else real + 1j * imag


def solve_delta_point_ts_i(ts, i, f, point):
    return basic.mu_i(ts, i, point) * f(point)


def solve_delta_ts(ts, f, start_time, stop_time):
    """Delta integral over the timescale."""

    def spf(ts, i, l, r):
        return solve_delta_point_ts_i(ts, i, f, l)

    def sif(ts, i, l, r):
        return solve_interval(f, l, r)

    return core.scale.solve_i_f(ts, spf, sif, start_time=start_time, stop_time=stop_time)


def solve_gen_ts_nsum(gen_ts_f, f, start_bound, stop_bound):
    """Integrate potentially infinite timescale sections of points and intervals."""

    def spf(l, r):
        return solve_point(f, l, r)

    def sif(l, r):
        return solve_interval(f, l, r)

    return core.genscale.solve_nsum_f(gen_ts_f, spf, sif, start_bound, stop_bound)


def solve_gen_ts_for_t(gen_ts_f, f, start_bound, stop_bound, start_time, stop_time, unsorted=True):
    def spf(l, r):
        return solve_point(f, l, r)

    def sif(l, r):
        return solve_interval(f, l, r)

    return core.genscale.solve_for_t_f(gen_ts_f, spf, sif, start_bound, stop_bound, start_time, stop_time, unsorted)


# CHECK: possibly remove when the newer version works as intended
def solve_gen_ts_for_t_old(
    gen_ts_f, f, start_bound, stop_bound, start_time, stop_time, signif_num=10, signif_thresh=0.0000001, signif_inc=True
):
    if start_time == stop_time:
        return 0

    cur = 0
    nxt = gen_ts_f(start_bound)
    i = start_bound + 1

    while i < stop_bound:
        cur = nxt
        nxt = gen_ts_f(i)

        if core.time.is_valid(cur) and core.time.contains(cur, start_time):
            break

        i += 1

    if core.interval.is_valid(cur) and core.interval.contains_point(cur, stop_time):
        return solve_interval(f, start_time, stop_time)

    result = 0
    prior_results = [0 for i in range(signif_num)]

    if core.time.gt(stop_time, cur):  # FIX: inc/dec
        result += core.time.solve_step_f(
            cur,
            nxt,
            lambda l, r: solve_point(f, l, r),
            lambda l, r: solve_interval(f, l, r),
            start_time=start_time,
        )

    prior_results[i % signif_num] = result

    i += 1

    while i < stop_bound:
        cur = nxt
        nxt = gen_ts_f(i)

        if core.interval.is_valid(cur) and core.interval.contains_point(cur, stop_time):
            return result + solve_interval(f, cur[0], stop_time)

        if core.point.is_valid(cur) and core.point.eq(cur, stop_time):
            return result

        result += core.time.solve_step_f(
            cur,
            nxt,
            lambda l, r: solve_point(f, l, r),
            lambda l, r: solve_interval(f, l, r),
        )

        prior_results[i % signif_num] = result

        if i >= signif_num:
            insignificant = True
            last_result = abs(prior_results[i % signif_num])

            for j in range(i, i + signif_num):
                older_result = abs(prior_results[(i + j) % signif_num])

                if older_result > signif_thresh:
                    insignificant = False

                if signif_inc is True and last_result > older_result:
                    insignificant = False

            if insignificant:
                break

        i += 1

    print(
        "timescalecalculus.compute.integral.inf_for_t():\n",
        "WARNING:\n",
        "- Could not find `stop_time` because the last "
        + str(signif_num)
        + " prior results were all below the significance threshold of "
        + str(signif_thresh)
        + ".\n",
        "- Increasing values are significant: " + str(signif_inc) + ".\n",
        "- Prior results, from oldest to most recent, are as follows:\n",
    )

    for j in range(i, i - signif_num, -1):
        index = (i + j) % signif_num
        print("#" + str(index) + ":", prior_results[index])

    return result


# CHECK: remove when the newer version works as intended
def solve_inf_ts_for_t(gen_ts_f, f, t_0, t_target, l, r, signif_num=10, signif_thresh=0.0000001, signif_inc=True):
    """
    Integrate a generated timescale section of points and intervals for t.

    ### Parameters

    - `f`: The function with which to solve the timescale for a particular target value = t.

    - `t_0`: The timescale value from which to begin solving.

    - `t_target`: The timescale value for which to solve.

    - `gen_ts_f`
        - The function that, when it is fed values where, for any value n, l <= n <= r is True AND (n_(m + 1) - n_m) = 1.
        - In other words: the difference between two consecutive n-values is always 1.

    - `signif_num`: How many previously calcuated values (that are obtained from solving integrals or discrete points) to check the "significance" of -- see "signif_thresh" for more information.

    - `signif_thresh`:
        - The value that a particular calculated value (from solving an integral or discrete point) must be below to be considered "insignificant".
        - If m=signif_num previously calculated values are all below this signif_thresh, then the for_t() function will
                        return the current result sum with a warning message.

    - `signif_inc`: If this boolean is True: when insignificant_prior_results() detects that result values seem to be increasing (when they were decreasing before), it will not consider them to be insignificant even if all are below the signif_thresh.
    """

    if t_0 == t_target:
        return 0  # integral from 0 to 0 is 0
    elif t_0 > t_target:  # FIX: inc/dec
        raise Exception("`t_0` cannot be greater than `t_target`.")

    result = 0
    prior_results = [0 for i in range(signif_num)]

    cur = 0
    nxt = gen_ts_f(l)

    # `l + 1` because this is the value of `nxt`, not `cur`
    i = l + 1

    # generate timescale values until we find `t_0`
    while i < r:
        cur = nxt
        nxt = gen_ts_f(i)

        if core.time.is_valid(cur) and core.time.contains(cur, t_0):
            break

        i += 1

    # if `cur`` is an interval that contains `t_target``, we can immediately compute and return the result
    if core.interval.is_valid(cur) and core.interval.contains_point(cur, t_target):
        return solve_interval(f, t_0, t_target)

    # begin computing the result w.r.t. `t_0` (a partial starting interval is possible e.g. { [t_0, cur[1]] | cur[0] < t_0 })
    if core.time.gt(t_target, cur):  # FIX: inc/dec
        result += core.time.solve_step_f(
            cur,
            nxt,
            lambda l, r: solve_point(f, l, r),
            lambda l, r: solve_interval(f, l, r),
            start_time=t_0,
        )

    prior_results[i % signif_num] = result

    i += 1

    while i < r:
        cur = nxt
        nxt = gen_ts_f(i)

        if core.interval.is_valid(cur) and core.interval.contains_point(cur, t_target):
            return result + solve_interval(f, cur[0], t_target)

        if core.point.is_valid(cur) and core.point.eq(cur, t_target):
            return result

        result += core.time.solve_step_f(
            cur,
            nxt,
            lambda l, r: solve_point(f, l, r),
            lambda l, r: solve_interval(f, l, r),
        )

        prior_results[i % signif_num] = result

        if i >= signif_num:
            insignificant = True
            last_result = abs(prior_results[i % signif_num])

            for j in range(i, i + signif_num):
                older_result = abs(prior_results[(i + j) % signif_num])

                if older_result > signif_thresh:
                    insignificant = False

                if signif_inc is True and last_result > older_result:
                    insignificant = False

            if insignificant:
                break

        i += 1

    print(
        "timescalecalculus.compute.integral.inf_for_t():\n",
        "WARNING:\n",
        "- Could not find `t_target` because the last "
        + str(signif_num)
        + " prior results were all below the significance threshold of "
        + str(signif_thresh)
        + ".\n",
        "- Increasing values are significant: " + str(signif_inc) + ".\n",
        "- Prior results, from oldest to most recent, are as follows:\n",
    )

    for j in range(i, i - signif_num, -1):
        index = (i + j) % signif_num
        print("#" + str(index) + ":", prior_results[index])

    return result
