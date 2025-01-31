from copy import deepcopy
from timescalecalculus import diffeq
from timescalecalculus import legacytimescalecalculus as ltsc


def test_solve_for_t():
    a = [0, 1, 2, 3, 4, [5, 6]]
    b = ltsc.timescale(deepcopy(a))

    def y_prime(t, y):
        return t * t * y

    assert diffeq.ordinary.solve_for_t(a, 1, 0, 5.1, y_prime) == b.solve_ode_for_t(1, 0, 5.1, y_prime)


def test_solve_for_t_with_odient():
    a = [0, 1, 2, 3, 4, [5, 6]]
    b = ltsc.timescale(deepcopy(a))

    # NOTE: opposite parameter order compared to the y_prime in solve_for_t()
    def y_prime(y, t):
        return t * t * y

    for x, y in zip(
        diffeq.ordinary.solve_for_t_with_odeint(a, 1, 0, 5.1, y_prime),
        b.solve_ode_for_t_with_odeint(1, 0, 5.1, y_prime),
        strict=True,
    ):
        assert x == y


def test_solve_system_for_t():
    a = [0, 1, 2, 3, 4, [5, 6]]
    b = ltsc.timescale(deepcopy(a))

    def y_prime_vector(vector, t):
        a, b = vector

        dt_vector = [5 * a - 3 * b, -6 * a + 2 * b]

        return dt_vector

    for x, y in zip(
        diffeq.ordinary.solve_system_for_t(a, [1, 1], 0, 5.4, y_prime_vector),
        b.solve_ode_system_for_t([1, 1], 0, 5.4, y_prime_vector),
        strict=True,
    ):
        assert x == y
