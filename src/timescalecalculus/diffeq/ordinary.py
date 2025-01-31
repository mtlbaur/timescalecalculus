import numpy
import scipy
from timescalecalculus import core, basic
from .utility import validate_args


# CHECK: these need more work


def solve_for_t(ts, y_0, t_0, t_target, y_prime):
    """
    Ordinary Differential Equation (ODE) solver for equations of the form

        `y'(t) = p(t)*y(t)`

    where `t_0` is the starting value in the timescale and

        `y_0 = y(t_0)`

    is the initial value provided by the user.

    ### Parameters

    - `y_0`: Is the initial value assigned to y(t_0) that is used as a starting point to evaluate the ODE.

    - `t_0`: the initial value that is considered the starting point in the timescale from which to solve subsequent points. In other words, t_0 is the value that is plugged into y to determine y_0 via: y_0 = y(t_0).

    - `t_target`: the timescale value for which y should be evaluated and returned.

    - `y_prime`: the function y'(t) of the ODE y'(t) = p(t)*y(t).

    - NOTE: `y_prime` MUST be defined such that the arguments ("t" and "y") appear in this order: y_prime(t, y).

    ### Other Variables

    - `cur` is the current value of t. t must be a value in the timescale.

    - `y_cur` holds the value obtained from y(cur).

    ### Notes

    - `y(t_0) == y_0`

    - The function will solve for the next t value until the value of y(t_target) is obtained.
    y(t_target) is then returned.

    - Currently, t_target > t_0 is a requirement -- solving for a t_target < t_0 is not supported. FIX: inc/dec
    """

    validate_args(ts, t_0, t_target)

    if t_0 == t_target:
        return y_0

    cur = t_0
    y_cur = y_0

    ode = scipy.integrate.ode(y_prime)

    for i in range(core.scale.find_time(ts, t_0), len(ts)):
        if core.time.is_right_scattered(ts[i], cur):
            y_sigma_of_t_current = y_cur + y_prime(cur, y_cur) * basic.mu(ts, cur)
            t_next = basic.sigma(ts, cur)

            if t_target == t_next:
                return y_sigma_of_t_current

            cur = t_next
            y_cur = y_sigma_of_t_current

        elif core.time.is_right_dense(ts[i], cur):
            ode.set_initial_value(y_cur, cur)
            interval = ts[i]

            if t_target > interval[1]:  # FIX: inc/dec
                cur = interval[1]
                y_cur = ode.integrate(interval[1])

            elif core.interval.contains(interval, t_target):
                return ode.integrate(t_target)

            else:
                raise Exception()

            if not ode.successful():
                raise Exception()
        else:
            raise Exception()


def solve_for_t_with_odeint(ts, y_0, t_0, t_target, y_prime, stepsize=0.0001):
    """
    This function is another version of the solve_for_t() function.
    It uses scipy.integrate.odeint to integrate over intervals rather than the scipy.integrate.ode method used by the solve_for_t() function.
    In general, it seems to be less accurate than solve_for_t().
    The additional stepsize argument (default value = 0.0001) can be used to somewhat mitigate this inaccuracy.
    However, even with extremely small step sizes (like stepsize = 0.0000001), solve_for_t() seems to be better.

    NOTE: The scipy.integrate.odeint function requires that its supplied y_prime is of the form: y_prime(y, t) -- this is the opposite of what scipy.integrate.ode wants.

    ### Notes

    - `y(t_0) == y_0`
    """

    validate_args(ts, t_0, t_target)

    if t_0 == t_target:
        return y_0

    cur = t_0
    y_cur = y_0

    for i in range(core.scale.find_time(ts, t_0), len(ts)):
        if core.time.is_right_scattered(ts[i], cur):
            y_sigma_of_t_current = y_cur + y_prime(y_cur, cur) * basic.mu(ts, cur)
            t_next = basic.sigma(ts, cur)

            if t_target == t_next:
                return y_sigma_of_t_current

            cur = t_next
            y_cur = y_sigma_of_t_current

        elif core.time.is_right_dense(ts[i], cur):
            interval = ts[i]

            if t_target > interval[1]:  # FIX: inc/dec
                # CHECK: this should be replacable with:
                # interval = core.utility.gen_even_seq(cur, interval[1], stepsize=stepsize)
                interval = numpy.arange(cur, interval[1] + stepsize, stepsize)

                cur = interval[1]
                y_cur = scipy.integrate.odeint(y_prime, y_cur, interval)[-1]

            elif core.interval.contains(interval, t_target):
                # CHECK: this should be replacable with:
                # interval = core.utility.gen_even_seq(cur, t_target, stepsize=stepsize)
                interval = numpy.arange(cur, t_target + stepsize, stepsize)

                return scipy.integrate.odeint(y_prime, y_cur, interval)[-1]

            else:
                raise Exception()

        else:
            raise Exception()


def solve_system_for_t(ts, y_0, t_0, t_target, y_prime, stepsize=0.0001):
    """
    Ordinary Differential Equation System Solver

    ### Parameters

    - "y_0" is a list of the initial values assigned to y(t_0). These are used as a starting point from which to evaluate the system.

    - "t_0" is the initial value that is considered the starting point in the timescale from which to solve subsequent points. Initially, t_0 is the value that is fed to y to determine y_0 via: y_0 = y(t_0).

    - "t_target" is the timescale value for which y should be evaluated and returned.
    Since this function solves a system of equations, the result will be a list of values that constitute the results for each of the equations in the system for t_target.

    - "y_prime" is the system of equations where each individual equation is of the form y'(t) = p(t)*y(t).

    NOTE: Since this solver uses the scipy.integrate.odeint function to obtain its result, y_prime MUST be defined with a specific format. As an example, for a system of two equations, y_prime would have to defined in the following manner:
        ```
        # Argument order is required by the scipy.integrate.odeint class -- "y_prime_vector(y, vector)" will result in incorrect results
        def y_prime_vector(vector, t):
            x, y = vector # Extract and store the first item from "vector" into x and the second item into y

            dt_vector = [x*t, y*t*t] # Define the system of equations

            return dt_vector # Return the system
        ```

    NOTE: If the number of items in y_0 is not the same as the number of equations in y_prime, then this solver will fail.

    ### Notes

    - `y(t_0) == y_0`
    """

    validate_args(ts, t_0, t_target)

    if t_0 == t_target:
        return y_0

    cur = t_0
    y_cur = y_0

    for i in range(core.scale.find_time(ts, t_0), len(ts)):
        if core.time.is_right_scattered(ts[i], cur):
            temp1 = list(map(lambda x: x * basic.mu(ts, cur), y_prime(y_cur, cur)))
            temp2 = list(map(lambda x, y: x + y, y_cur, temp1))
            y_sigma_of_t_current = temp2
            t_next = basic.sigma(ts, cur)

            if t_target == t_next:
                return y_sigma_of_t_current

            cur = t_next
            y_cur = y_sigma_of_t_current
        elif core.time.is_right_dense(ts[i], cur):
            interval = ts[i]

            if t_target > interval[1]:  # FIX: inc/dec
                # CHECK: this should be replacable with:
                # interval = core.utility.gen_even_seq(cur, interval[1], stepsize=stepsize)
                interval = numpy.arange(cur, interval[1] + stepsize, stepsize)

                cur = interval[1]
                y_cur = scipy.integrate.odeint(y_prime, y_cur, interval)[-1]

            elif core.interval.contains(interval, t_target):
                # CHECK: this should be replacable with:
                # interval = core.utility.gen_even_seq(cur, t_target, stepsize=stepsize)
                interval = numpy.arange(cur, t_target + stepsize, stepsize)

                return scipy.integrate.odeint(y_prime, y_cur, interval)[-1]

            else:
                raise Exception()
        else:
            raise Exception()
