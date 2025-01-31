from timescalecalculus import core


def validate_args(ts, t_0, t_target):
    if t_0 > t_target:  # FIX: inc/dec
        raise Exception("`t_0` cannot be greater than `t_target`.")

    t_0_in_ts = False
    t_target_in_ts = False

    for x in ts:
        if core.point.is_valid(x):
            if t_0 == x:
                t_0_in_ts = True

            if t_target == x:
                t_target_in_ts = True
        elif core.interval.is_valid(x):
            if t_target >= x[0] and t_target <= x[1]:  # FIX: use new functions
                t_target_in_ts = True

            if t_0 >= x[0] and t_0 < x[1]:
                t_0_in_ts = True

            if t_0 == x[1]:
                t_0_in_ts = True

        if t_0_in_ts and t_target_in_ts:
            break

    if not t_0_in_ts and not t_target_in_ts:
        raise Exception("`t_0` and `t_target` are not values in the timescale.")
    if not t_0_in_ts and t_target_in_ts:
        raise Exception("`t_0` is not a value in the timescale.")
    if t_0_in_ts and not t_target_in_ts:
        raise Exception("`t_target` is not a value in the timescale.")
