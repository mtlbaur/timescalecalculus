from typing import Callable
from timescalecalculus import core, basic
from .utility import validate_args

# CHECK: these need more work


def solve_point(ts, i, cur, y_values: dict, y_prime: Callable, results: list, past_points: list):
    y_sigma_of_t_current = y_values[cur] + y_prime(cur, y_values) * basic.mu_i(ts, i, cur)

    results.append(y_sigma_of_t_current)
    past_points.append([cur, [y_values[cur]], [y_sigma_of_t_current]])

    cur = basic.sigma_i(ts, i, cur)
    y_values[cur] = results[-1]

    return cur


def solve_interval(start, target, stepsize, y_values: dict, jitcdde, results: list, past_points: list):
    # add (time, state, derivative) past_point tuples that were computed between the last interval and this interval
    jitcdde.add_past_points(past_points)

    # now that the jitcdde object has those points, we can discard them
    past_points.clear()

    # CHECK: `results.extend(jitcdde.integrate_blindly(target))` instead of the following loop?
    for step in core.utility.gen_even_seq(start, target, stepsize=stepsize):
        results.append(jitcdde.integrate_blindly(step)[0])

    y_values[target] = results[-1]

    # this should hold barring accuracy limitations?
    if target != jitcdde.t:
        raise Exception(f"`target` == {target} is not equal to `jitcdde.t` == {jitcdde.t}")

    return target


def solve_for_t(ts, y_values, t_0, t_target, y_prime: Callable, jitcdde=None, stepsize=0.0001, all_results=False):
    """Delay Differential Equation (DDE) solver where `y_0 == y_values[t_0]`"""

    for key in y_values:
        if not core.scale.contains(ts, key):
            raise Exception(f"The initial y value, t == {key} is not in the timescale")

    validate_args(ts, t_0, t_target)

    if t_0 == t_target:
        return y_values[t_0]

    cur = t_0
    results = []
    past_points = []

    for i in range(core.scale.find_time(ts, t_0), len(ts)):
        if core.time.is_right_scattered(ts[i], cur):
            cur = solve_point(ts, i, cur, y_values, y_prime, results, past_points)

        elif core.time.is_right_dense(ts[i], cur):
            interval = ts[i]

            if t_target > interval[1]:  # FIX: inc/dec
                cur = solve_interval(cur, interval[1], stepsize, y_values, jitcdde, results, past_points)
                cur = solve_point(ts, i, cur, y_values, y_prime, results, past_points)

            elif core.interval.contains(interval, t_target):
                cur = solve_interval(cur, t_target, stepsize, y_values, jitcdde, results, past_points)

            else:
                raise Exception()

        else:
            raise Exception()

        if cur == t_target:
            return results if all_results else results[-1]

    raise Exception("This should never happen.")
