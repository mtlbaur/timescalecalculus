import numpy
import mpmath
from timescalecalculus import core, integral


def jump_i(ts, i, t, right: bool):
    """
    Jump left or right by index if valid and return the value.

    - `ts`: the timescale.

    - `i`: the index of the value of the timescale from which to jump.

    - `t`: the value of the timescale from which to jump. NOTE: the reason why `t` must be passed has to do with intervals: if `t[i]` is an interval, then we have to know if we are at the leftmost or rightmost position in that interval; if we aren't, we can't jump. `t` tells us the actual value in that interval from which we want to jump.

    - `right`: jump right if `True`, left otherwise
    """

    if not core.point.is_valid(t):
        raise Exception()

    if not core.scale.valid_index(ts, i):
        raise Exception()

    if right:
        if i == len(ts) - 1:
            return ts[i]
    else:
        if i == 0:
            return ts[i]

    cur = ts[i]
    nxt = ts[i + 1 if right else i - 1]

    # we can't jump within an interval
    if core.interval.is_valid(cur) and t != cur[int(right)]:
        return t

    if core.interval.is_valid(nxt):
        return nxt[int(right) ^ 1]

    return nxt


def sigma_i(ts, i, t):
    """Forward jump by index."""
    return jump_i(ts, i, t, True)


def sigma(ts, t):
    """Forward jump."""
    return sigma_i(ts, core.scale.find_time(ts, t), t)


def rho_i(ts, i, t):
    """Backwards jump by index."""
    return jump_i(ts, i, t, False)


def rho(ts, t):
    """Backwards jump."""
    return rho_i(ts, core.scale.find_time(ts, t), t)


def grain(ts, i, t, right: bool):
    """Left or right graininess if valid; this is basically just the `jump()` function with an additional difference computation."""
    r = jump_i(ts, i, t, right)

    if right:
        return r - t

    return t - r


def mu_i(ts, i, t):
    """Graininess by index."""
    return grain(ts, i, t, True)


def mu(ts, t):
    """Graininess."""
    return mu_i(ts, core.scale.find_time(ts, t), t)


def nu_i(ts, i, t):
    """Backward graininess by index."""
    return grain(ts, i, t, False)


def nu(ts, t):
    """Backward graininess."""
    return nu_i(ts, core.scale.find_time(ts, t), t)


def dderivative_i(ts, i, f, t):
    """Delta derivative by index."""

    if sigma_i(ts, i, t) == t:
        # `misc.derivative()` is getting deprecated, switched it to `mpmath.diff()` instead
        # the previous code: `misc.derivative(f, t, dx=(1.0 / 2**16))`
        return mpmath.diff(f, t)

    return (f(sigma_i(ts, i, t)) - f(t)) / mu_i(ts, i, t)


def dderivative(ts, f, t):
    """Delta derivative."""
    return dderivative_i(ts, core.scale.find_time(ts, t), f, t)


# CHECK: this isn't a complete counterpart of `dderivative()`, should it be expanded to include intervals?
def nderivative_i(ts, i, f, t):
    """Nabla derivative by index."""
    return (f(t) - f(rho_i(ts, i, t))) / nu_i(ts, i, t)


def nderivative(ts, f, t):
    """Nabla derivative."""
    return nderivative_i(ts, core.scale.find_time(ts, t), f, t)


def cyl(ts, t, z):
    """Cylinder transformation from definition 2.21."""

    if mu(ts, t) == 0:
        return z

    return 1 / mu(ts, t) * numpy.log(1 + z * mu(ts, t))


def dexp_p(ts, p, s, t):
    """Delta exponential based on definition 2.30."""
    return numpy.exp(integral.solve_delta_ts(ts, lambda t: cyl(ts, t, p(t)), s, t))


def mucircleminus(ts, f, t):
    """Forward circle minus."""
    return -f(t) / (1 + f(t) * mu(ts, t))


def dcos_p(ts, p, s, t):
    """The forward-derivative cosine trigonometric function."""

    a = dexp_p(ts, lambda x: p(x) * 1j, s, t)
    b = dexp_p(ts, lambda x: p(x) * -1j, s, t)

    return core.utility.only_real_if_no_imag((a + b) / 2)


def dsin_p(ts, p, s, t):
    """The forward-derivative sine trigonometric function."""

    a = dexp_p(ts, lambda x: p(x) * 1j, s, t)
    b = dexp_p(ts, lambda x: p(x) * -1j, s, t)

    return core.utility.only_real_if_no_imag((a - b) / 2j)


def laplace_transform(ts, f, z, s):
    """The Laplace transform function."""

    def g(t):
        return f(t) * dexp_p(ts, lambda t: mucircleminus(ts, z, t), s, sigma(ts, t))

    return integral.solve_delta_ts(ts, g, s, core.scale.max_(ts))
