import pandas as pd
import numpy as np
import logging

WEEK = 2
FULL_ROWS = ['fgpct', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'true_score',
             'week']

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
        new_week = [i[0] for i in self.weekly_frame.iloc[:, -1:].values.tolist()]
        calced = set()
        vals = frame['true_score']
        for player_1_id in frame.index:
            player_1 = self.weekly_frame.index[player_1_id]
            if player_1 not in calced:
                calced.add(player_1)
                player_2_id = frame['opponent'][player_1_id]
                player_2 = self.weekly_frame.index[player_2_id]

                _logger.info('Calculating for %s vs. %s', player_1, player_2)
                player_1_data = [self.weekly_frame.loc[player_1, 'week_{}'.format(week - 1)] * 1.0, vals[player_1_id]]
                player_2_data = [self.weekly_frame.loc[player_2, 'week_{}'.format(week - 1)] * 1.0, vals[player_2_id]]
                scores = elo_calc(player_1_data, player_2_data, k=60)
                _logger.info('Adding scores to new week')
                new_week[player_1_id] = scores[0]
                new_week[player_2_id] = scores[1]
        _logger.info('Writing to frame')
        self.weekly_frame['week_{}'.format(week)] = new_week

    def run(self, week_data, frame=False, week=0):
        if week:
            if isinstance(frame, bool):
                self._generate()
            else:
                self.weekly_frame = frame
            self._calc(week_data, week)
        else:
            self._generate()


if __name__ == "__main__":
    pass
