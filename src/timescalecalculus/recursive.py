from timescalecalculus import basic, integral


def g_k(ts, k, s, t, cache={}):
    """
    Generalized g_k polynomial from page 38 with memoization.

    NOTE: `cache` must initially be an empty dictionary. However, it can be reused as long as `ts` doesn't change. When `ts` changes you must provide a corresponding empty dictionary so as to avoid retrieving a mismatched cached value belonging to the previous `ts`.
    """

    def dfs(k, s, t):
        if k > 0:
            key = f"{k}:{t}:{s}"

            if key in cache:
                return cache[key]

            def g(x):
                return dfs(k - 1, s, basic.sigma(ts, x))

            result = integral.solve_delta_ts(ts, g, s, t)
            cache[key] = result

            return result

        if k == 0:
            return 1

        raise Exception("`k` ==", k, "cannot be less than 0.")

    return dfs(k, s, t)


def h_k(ts, k, s, t, cache={}):
    """
    Generalized h_k polynomial from page 38 with memoization.

    NOTE: `cache` must initially be an empty dictionary. However, it can be reused as long as `ts` doesn't change. When `ts` changes you must provide a corresponding empty dictionary so as to avoid retrieving a mismatched cached value belonging to the previous `ts`.
    """

    def dfs(k, s, t):
        if k > 0:
            key = f"{k}:{t}:{s}"

            if key in cache:
                return cache[key]

            def h(x):
                return dfs(k - 1, s, x)

            result = integral.solve_delta_ts(ts, h, s, t)
            cache[key] = result

            return result

        if k == 0:
            return 1

        raise Exception("`k` ==", k, "cannot be less than 0.")

    return dfs(k, s, t)
