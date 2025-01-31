from numpy import sin, cos, tan
from matplotlib import pyplot
from timescalecalculus import core, plot


def functions():
    gen = core.utility.gen_even_seq

    ts = []
    ts.extend(gen(0, 4, stepsize=0.01, excl_end=True))
    ts.append([4, 8])
    ts.extend(gen(8, 12, stepsize=0.01, excl_start=True))
    ts.append([12, 16])

    def f(x):
        return sin(x)

    def g(x):
        return cos(x)

    def h(x):
        return cos(tan(x))

    unlabeled_functions = [
        f,
        g,
        h,
    ]
    labeled_functions = {
        f: "sin(x)",
        g: "cos(x)",
        h: "cos(tan(x))",
    }

    pyplot.figure(1)
    plot.functions(ts, labeled_functions)
    pyplot.title("with legend")

    pyplot.figure(2)
    plot.functions(ts, unlabeled_functions)
    pyplot.title("no legend")

    pyplot.figure(3)
    plot.functions(ts, labeled_functions, interval_style=".")
    pyplot.title("intervals drawn as points")

    pyplot.show()


functions()
