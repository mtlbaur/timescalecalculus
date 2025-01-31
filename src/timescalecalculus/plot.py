import matplotlib.colors
from matplotlib import pyplot, patches
from itertools import cycle
from timescalecalculus import core


def apply_separate_f(ts, f, gen_even_seq_kwargs):
    """
    Applies the function `f` on all values of `ts` and returns the result in tuple containing:

        `(in_points, in_intervals, out_points, out_intervals)`

    where:

    - `in_points` contains point input values
    - `in_intervals` contains lists of interval input values
    - `out_points` contains point output values
    - `out_intervals` contains lists of interval output values
    - `gen_even_seq_kwargs` determines interval point generation.
    """

    in_points = []
    in_intervals = []
    out_points = []
    out_intervals = []

    for a in ts:
        if core.point.is_valid(a):
            in_points.append(a)
            out_points.append(f(a))
        elif core.interval.is_valid(a):
            in_ = []
            out = []

            for b in core.utility.gen_even_seq(a[0], a[1], **gen_even_seq_kwargs):
                in_.append(b)
                out.append(f(b))

            in_intervals.append(in_)
            out_intervals.append(out)
        else:
            raise Exception("`a` was neither a point nor an interval.")

    return (in_points, in_intervals, out_points, out_intervals)


def functions(
    ts,
    functions: list | dict,
    colors=matplotlib.colors.TABLEAU_COLORS,
    point_style=".",
    interval_style="-",
    gen_even_seq_kwargs={"stepsize": 0.001},
    pyplot_kwargs={},
):
    """
    Plots the results of executing functions on timescale values. Each function gets its own plotted curve with a cycled color from `colors`. Points and intervals and be drawn with different styles.

    NOTE: remember to call `matplotlib.pyplot.show()` at some point after this function to display the actual figures.

    - `ts`: the timescale.

    - `functions`: either a `list` or a `dict` of functions to apply on the timescale. If a `dict` is used, the form should be `{ f1: "label1", f2: "label2", ... fN: "labelN" }` where `f` is the function and `label` is a the name of the function that will be displayed in the plot's legend.

    - `colors`: a collection of matplotlib.colors; you can supply your own color list in `RGB` form, e.g.: `[[0, 0, 1], [1, 1, 0]]` would be `[blue, yellow]`. Colors are cycled through while plotting functions; if the colors run out before all functions are plotted, we simply loop back to the first color.

    - `point_style`: the matplotlib style used for points; default value `.` indicates a point.

    - `interval_style`: the matplotlib style used for intervals; default value `-` indicates interval points should be drawn as one line. If `.` is used instead, then intervals will be drawn as points rather than a line through points.

    - `gen_even_seq_kwargs`: configuration options for how the plot points of an interval should be generated. The default value specifies a maximum stepsize between generated interval points and includes the starting and ending interval bounds. To fully understand these options, please refer to the description of `timescalecalculus.core.utility.gen_even_seq()` function.

    - `pyplot_kwargs`: keyword arguments for the `matplotlib.pyplot.plot()` function calls.

    A full example can be found in: `./ex/plot.py`
    """

    cycled_colors = cycle(colors)

    for f, c in zip(functions, cycled_colors):
        ip, ii, op, oi = apply_separate_f(ts, f, gen_even_seq_kwargs)

        pyplot.plot(ip, op, point_style, c=c, **pyplot_kwargs)

        for i, o in zip(ii, oi):
            pyplot.plot(i, o, interval_style, c=c, **pyplot_kwargs)

    if isinstance(functions, dict):
        pyplot.legend(handles=[patches.Patch(label=functions[f], color=c) for f, c in zip(functions, cycle(colors))])
