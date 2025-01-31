import numpy
import symengine
import jitcdde
import pytest
from copy import deepcopy
from timescalecalculus import core, basic, diffeq
from timescalecalculus import legacytimescalecalculus as ltsc


def test_solve_for_t_points_only():
    a = [x for x in range(-100, 100 + 1)]
    b = ltsc.timescale(deepcopy(a))

    def a_y_prime(t, y):
        rho_t = basic.rho(a, t)
        i = core.scale.find_time(a, rho_t)
        rho_rho_t = basic.rho_i(a, i, rho_t)
        mu_rho_t = basic.mu_i(a, i, rho_t)
        mu_rho_rho_t = basic.mu(a, rho_rho_t)

        return 3 * (1 + 3 * mu_rho_rho_t) * (1 + 3 * mu_rho_t) * y[rho_rho_t]

    def b_y_prime(t, y):
        return (
            3
            * (1 + 3 * b.mu(b.delay(b.rho(b.rho(t)))))
            * (1 + 3 * b.mu(b.delay(b.rho(t))))
            * y[b.delay(b.rho(b.rho(t)))]
        )

    # ----

    y_values = {-1: 1, 0: 2, 1: -3}
    ra = diffeq.delay.solve_for_t(a, y_values, 1, 6, a_y_prime)

    # ----

    y_values = {-1: 1, 0: 2, 1: -3}
    rb = b.solve_dde_for_t(y_values, 1, 6, b_y_prime)

    # ----

    assert ra == rb


def test_solve_for_t_with_intervals():
    a = [0, 0.1, 0.2, 0.3, 0.4, [0.5, 1], 1.1, 1.2, 1.3, 1.4, 1.5, [1.6, 2], 2.1, 2.2, 2.3, 2.4, 2.5, [2.6, 3]]
    b = ltsc.timescale(deepcopy(a))

    def y_prime(t, y):
        if t == 0:
            return t
        return t - 0.1

    # ----

    past_function = [symengine.sin(jitcdde.t)]
    y_prime_jitcdde = [jitcdde.y(0, jitcdde.t - 3 * numpy.pi / 2)]
    times_of_interest = numpy.arange(-10, 0, 0.01)
    # times_of_interest = numpy.linspace(-10, 0, 1000) # CHECK: for some reason this doesn't work

    dde = jitcdde.jitcdde(y_prime_jitcdde, max_delay=3 * numpy.pi / 2)
    dde.past_from_function(past_function, times_of_interest)
    dde.generate_lambdas()

    y_values = {0: numpy.sin(0)}

    ra = diffeq.delay.solve_for_t(a, y_values, 0, 3, y_prime, jitcdde=dde)

    # ----

    past_function = [symengine.sin(jitcdde.t)]
    y_prime_jitcdde = [jitcdde.y(0, jitcdde.t - 3 * numpy.pi / 2)]
    times_of_interest = numpy.arange(-10, 0, 0.01)
    # times_of_interest = numpy.linspace(-10, 0, 1000) # CHECK: for some reason this doesn't work

    dde = jitcdde.jitcdde(y_prime_jitcdde, max_delay=3 * numpy.pi / 2)
    dde.past_from_function(past_function, times_of_interest)
    dde.generate_lambdas()

    y_values = {0: numpy.sin(0)}

    rb = b.solve_dde_for_t(y_values, 0, 3, y_prime, JiTCDDE=dde)

    # ----

    assert ra == pytest.approx(rb, 1e-8)
