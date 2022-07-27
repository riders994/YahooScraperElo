import numpy as np


def week_formatter(week):
    s = week.split(':')
    if len(s) - 1:
        try:
            return range(int(s[0]), int(s[-1]) + 1), True
        except ValueError:
            return
    else:
        return int(week), False


def elo_calc(player_1, player_2, k=60, proba=False):
    share_a = np.power(10, player_1[0]/400)
    share_b = np.power(10, player_2[0]/400)
    total = share_a + share_b

    expected_a = share_a/total
    expected_b = share_b/total

    if proba:
        return (player_1[0] + k * (player_1[1] - expected_a), player_2[0] + k * (player_2[1] - expected_b)),\
               (expected_a, expected_b)
    return [player_1[0] + k * (player_1[1] - expected_a), player_2[0] + k * (player_2[1] - expected_b)]

