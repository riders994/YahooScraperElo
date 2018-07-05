import pandas as pd
import numpy as np
import pickle

PLAYER_PICKLE_PATH = './players.pkl'
WEEK = 1
FRAME = pd.read_csv('./weekly_stats/week_{}.csv'.format(WEEK), index_col=0)
FULL_ROWS = ['fgpct', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'true_score',
             'week']


def elo_calc(player_1, player_2, K = 60):
    share_a = np.power(10, player_1[0]/400)
    share_b = np.power(10, player_2[0]/400)
    total = share_a + share_b

    expected_a = share_a/total
    expected_b = share_b/total

    return [player_1[0] + K * (player_1[1] - expected_a), player_2[0] + K * (player_2[1] - expected_b)]


class EloCalc:
    def __init__(self, week, stats=False):
        self.stats = stats
        if week:
            self.week = week
            self._load()
            if not self._verify():
                raise ValueError
        else:
            self._generate()

    def _generate(self):
        with open(PLAYER_PICKLE_PATH, "rb") as pkl:
            players = pickle.load(pkl)
            print(players)
        players = players[1:]
        if self.stats == 'full':
            self.weekly_frame = pd.DataFrame({player: [1500] * len(players) for player in players}, index=FULL_ROWS)
            self.weekly_frame['week'] = 0
        else:
            self.weekly_frame = pd.DataFrame({'week_0': [1500] * len(players)}, index=players)

    def _load(self):
        if self.stats:
            if self.stats == 'full':
                try:
                    self.weekly_frame = pd.read_csv('./elo/weekly_elo_full_week_{}.csv'.format(self.week - 1))
                except FileNotFoundError:
                    self._generate()
                except Exception as e:
                    raise e
            else:
                try:
                    self.weekly_frame = pd.read_csv('./elo/weekly_elo.csv')
                except FileNotFoundError:
                    self._generate()
                except Exception as e:
                    raise e
        else:
            try:
                self.weekly_frame = pd.read_csv('./elo/weekly_elo.csv', index_col=0)
            except FileNotFoundError:
                self._generate()
            except Exception as e:
                raise e

    def _verify(self):
        if self.stats == 'full':
            return self.weekly_frame.week[0] == (self.week - 1)
        else:
            return 'week_{}'.format(self.week - 1) in self.weekly_frame.columns

    def _full_load(self):
        pass

    def _full_calc(self, frame):
        self._full_load()

    def _calc(self, frame):
        if self.stats == 'full':
            pass
        elif self.stats:
            pass
        else:
            new_week = [0] * frame.shape[0]
            player_row_dict = {player: i for i, player in enumerate(self.weekly_frame.index)}
            calced = set()
            vals = frame['true_score']
            for player_1_name in self.weekly_frame.index:
                if player_1_name not in calced:
                    calced.add(player_1_name)
                    p1_id = player_row_dict[player_1_name]
                    player_2_name = frame['opponent'][player_1_name]
                    calced.add(player_2_name)
                    p2_id = player_row_dict[player_2_name]
                    player_1 = [self.weekly_frame.iloc[p1_id, self.week - 1] * 1.0, vals[player_1_name]]
                    player_2 = [self.weekly_frame.iloc[p2_id, self.week - 1] * 1.0, vals[player_2_name]]
                    scores = elo_calc(player_1, player_2)
                    new_week[p1_id] = scores[0]
                    new_week[p2_id] = scores[1]
            self.weekly_frame['week_{}'.format(self.week)] = new_week

    def _write(self):
        if self.stats == 'full':
            if self.week:
                self.weekly_frame.to_csv('./elo/weekly_elo_full_week_{}.csv'.format(self.week))
            else:
                self.weekly_frame.to_csv('./elo/weekly_elo_full_week')
        else:
            self.weekly_frame.to_csv('./elo/weekly_elo.csv')

    def run(self, frame):
        if self.week:
            self._calc(frame)
        self._write()


if __name__ == "__main__":
    calc = EloCalc(WEEK)
    calc.run(FRAME)
