import numpy as np


def elo_ratio(r1, r2):
    return np.power(10, r1 / 400), np.power(10, r2 / 400)


def week_formatter(week):
    s = week.split(':')
    if len(s) - 1:
        try:
            return range(int(s[0]), int(s[-1]) + 1), True
        except ValueError:
            return
    else:
        return int(week), False


def score_elo_calc(player_1, player_2, k=60, proba=False):
    share_a = np.power(10, player_1[0]/400)
    share_b = np.power(10, player_2[0]/400)
    total = share_a + share_b

    expected_a = share_a/total
    expected_b = share_b/total

    if proba:
        return (player_1[0] + k * (player_1[1] - expected_a), player_2[0] + k * (player_2[1] - expected_b)),\
               (expected_a, expected_b)
    return [player_1[0] + k * (player_1[1] - expected_a), player_2[0] + k * (player_2[1] - expected_b)]


def bin_elo_calc(player_1, player_2, k=60, proba=False):
    r1 = player_1[0]
    r2 = player_2[0]
    score1 = player_1[1]
    score2 = player_2[1]
    share_a, share_b = elo_ratio(r1, r2)
    total = share_a + share_b

    if score1 == 0.5:
        score1 = 0
    if score2 == 0.5:
        score2 = 0
    score1 = round(score1)
    score2 = round(score2)

    expected_a = share_a/total
    expected_b = share_b/total

    if proba:
        return (r1 + k * (score1 - expected_a), r2 + k * (score2 - expected_b)),\
               (expected_a, expected_b)
    return [r1 + k * (score1 - expected_a), r2 + k * (score2 - expected_b)]


def trin_elo_calc(player_1, player_2, k=60, proba=False):
    r1 = player_1[0]
    r2 = player_2[0]
    score1 = player_1[1]
    score2 = player_2[1]
    share_a, share_b = elo_ratio(r1, r2)
    total = share_a + share_b

    if score1 != .5:
        score1 = round(score1)
        score2 = round(score2)

    expected_a = share_a/total
    expected_b = share_b/total

    if proba:
        return (r1 + k * (score1 - expected_a), r2 + k * (score2 - expected_b)),\
               (expected_a, expected_b)
    return [r1 + k * (score1 - expected_a), r2 + k * (score2 - expected_b)]

