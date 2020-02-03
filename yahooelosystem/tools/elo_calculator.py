import pandas as pd
import numpy as np
import logging

WEEK = 1
FULL_ROWS = ['fgpct', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'true_score',
             'week']

t = {
    '395.l.12682.t.1': {
        'teamid': 0, 'week': 14, 'leagueid': 0, 'score': 6, 'fgm': 235, 'fga': 501, 'fgpct': 0.469061876247505, 'ftm': 107, 'fta': 144, 'ftpct': 0.7430555555555556, 'threes': '87', 'points': '664', 'rebounds': '230', 'assists': '135', 'steals': '52', 'blocks': '31', 'turnovers': '63', 'opponent': 8
    },
    '395.l.12682.t.7': {
        'teamid': 8, 'week': 14, 'leagueid': 0, 'score': 3, 'fgm': 222, 'fga': 431, 'fgpct': 0.5150812064965197, 'ftm': 74, 'fta': 101, 'ftpct': 0.7326732673267327, 'threes': '67', 'points': '585', 'rebounds': '255', 'assists': '110', 'steals': '28', 'blocks': '40', 'turnovers': '69', 'opponent': 0
    },
    '395.l.12682.t.2': {
        'teamid': 1, 'week': 14, 'leagueid': 0, 'score': 6, 'fgm': 324, 'fga': 644, 'fgpct': 0.5031055900621118, 'ftm': 137, 'fta': 178, 'ftpct': 0.7696629213483146, 'threes': '100', 'points': '885', 'rebounds': '304', 'assists': '197', 'steals': '46', 'blocks': '21', 'turnovers': '114', 'opponent': 11
    },
    '395.l.12682.t.12': {
        'teamid': 11, 'week': 14, 'leagueid': 0, 'score': 3, 'fgm': 197, 'fga': 439, 'fgpct': 0.44874715261959, 'ftm': 103, 'fta': 132, 'ftpct': 0.7803030303030303, 'threes': '56', 'points': '553', 'rebounds': '271', 'assists': '104', 'steals': '29', 'blocks': '23', 'turnovers': '71', 'opponent': 1
    },
    '395.l.12682.t.3': {
        'teamid': 6, 'week': 14, 'leagueid': 0, 'score': 6, 'fgm': 265, 'fga': 576, 'fgpct': 0.4600694444444444, 'ftm': 159, 'fta': 212, 'ftpct': 0.75, 'threes': '69', 'points': '758', 'rebounds': '287', 'assists': '201', 'steals': '50', 'blocks': '35', 'turnovers': '98', 'opponent': 10
    },
    '395.l.12682.t.11': {
        'teamid': 10, 'week': 14, 'leagueid': 0, 'score': 3, 'fgm': 264, 'fga': 532, 'fgpct': 0.49624060150375937, 'ftm': 138, 'fta': 161, 'ftpct': 0.8571428571428571, 'threes': '59', 'points': '725', 'rebounds': '228', 'assists': '139', 'steals': '38', 'blocks': '22', 'turnovers': '84', 'opponent': 6
    },
    '395.l.12682.t.4': {
        'teamid': 7, 'week': 14, 'leagueid': 0, 'score': 7, 'fgm': 297, 'fga': 650, 'fgpct': 0.45692307692307693, 'ftm': 141, 'fta': 160, 'ftpct': 0.88125, 'threes': '80', 'points': '815', 'rebounds': '248', 'assists': '153', 'steals': '53', 'blocks': '31', 'turnovers': '99', 'opponent': 2
    },
    '395.l.12682.t.5': {
        'teamid': 2, 'week': 14, 'leagueid': 0, 'score': 2, 'fgm': 283, 'fga': 637, 'fgpct': 0.44427001569858715, 'ftm': 137, 'fta': 189, 'ftpct': 0.7248677248677249, 'threes': '60', 'points': '763', 'rebounds': '282', 'assists': '194', 'steals': '47', 'blocks': '26', 'turnovers': '108', 'opponent': 7
    },
    '395.l.12682.t.6': {
        'teamid': 3, 'week': 14, 'leagueid': 0, 'score': 8, 'fgm': 250, 'fga': 490, 'fgpct': 0.5102040816326531, 'ftm': 168, 'fta': 194, 'ftpct': 0.865979381443299, 'threes': '63', 'points': '731', 'rebounds': '263', 'assists': '139', 'steals': '37', 'blocks': '22', 'turnovers': '61', 'opponent': 4
    },
    '395.l.12682.t.10': {
        'teamid': 4, 'week': 14, 'leagueid': 0, 'score': 1, 'fgm': 175, 'fga': 416, 'fgpct': 0.4206730769230769, 'ftm': 79, 'fta': 104, 'ftpct': 0.7596153846153846, 'threes': '55', 'points': '484', 'rebounds': '228', 'assists': '86', 'steals': '36', 'blocks': '19', 'turnovers': '47', 'opponent': 3
    },
    '395.l.12682.t.8': {
        'teamid': 9, 'week': 14, 'leagueid': 0, 'score': 3, 'fgm': 205, 'fga': 461, 'fgpct': 0.44468546637744033, 'ftm': 72, 'fta': 94, 'ftpct': 0.7659574468085106, 'threes': '52', 'points': '534', 'rebounds': '195', 'assists': '148', 'steals': '45', 'blocks': '24', 'turnovers': '69', 'opponent': 5
    },
    '395.l.12682.t.9': {
        'teamid': 5, 'week': 14, 'leagueid': 0, 'score': 5, 'fgm': 230, 'fga': 492, 'fgpct': 0.46747967479674796, 'ftm': 91, 'fta': 124, 'ftpct': 0.7338709677419355, 'threes': '63', 'points': '614', 'rebounds': '214', 'assists': '132', 'steals': '43', 'blocks': '42', 'turnovers': '69', 'opponent': 9
    }
}

_logger = logging.getLogger(__name__)


def elo_calc(player_1, player_2, k=60):
    share_a = np.power(10, player_1[0]/400)
    share_b = np.power(10, player_2[0]/400)
    total = share_a + share_b

    expected_a = share_a/total
    expected_b = share_b/total

    return [player_1[0] + k * (player_1[1] - expected_a), player_2[0] + k * (player_2[1] - expected_b)]


class EloCalc:

    weekly_frame = None

    def __init__(self, league_info):
        _logger.info('Elo calculator started')
        self.league_info = league_info
        self.team_map = league_info['team_map']

    def _generate(self):
        _logger.info('Generating week 0 frame')
        self.weekly_frame = pd.DataFrame({'week_0': [1500] * len(self.team_map)}, index=self.team_map.values())

    def _calc(self, frame, week):
        _logger.info('Starting win/loss only calculation')
        _logger.info('Creating blank new week')
        new_week = [0] * frame.shape[0]
        players = frame.index
        calced = set()
        vals = frame['true_score']
        playoff = False
        for player_1 in self.weekly_frame.index:
            if player_1 not in calced:
                calced.add(player_1)
                player_2 = frame['opponent'][player_1]
                # figure out playoff methods later
                # try:
                #     p2_id = player_row_dict[player_2_name]
                # except KeyError:
                #     _logger.info("It's the playoffs, and there's no opponent")
                #     new_week[p1_id] = self.weekly_frame.iloc[p1_id, week - 1] * 1.0
                #     playoff = True
                if not playoff:
                    _logger.info('Calculating for %s vs. %s', player_1, player_2)
                    player_1_data = [self.weekly_frame.iloc[p1_id, week - 1] * 1.0, vals[player_1_name]]
                    player_2_data = [self.weekly_frame.iloc[p2_id, week - 1] * 1.0, vals[player_2_name]]
                    scores = elo_calc(player_1_data, player_2_data, k=40)
                    _logger.info('Adding scores to new week')
                    new_week[p1_id] = scores[0]
                    new_week[p2_id] = scores[1]
                playoff = False
        _logger.info('Writing to frame')
        self.weekly_frame['week_{}'.format(week)] = new_week

    def run(self, week_data, frame=None, week=0):
        if week:
            if frame:
                self.weekly_frame = frame
            else:
                self._generate()
            self._calc(week_data, week)
        else:
            self._generate()


if __name__ == "__main__":
    pass
