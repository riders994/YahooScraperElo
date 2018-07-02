import pandas as pd
import numpy as np
import pickle

PLAYER_PICKLE_PATH = './players.pkl'
WEEK = 1
FULL_ROWS = ['fgpct', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'true_score',
             'week']


def elo_calc(player_1, player_2, K = 40):
    share_a = np.power(10, player_1[0])
    share_b = np.power(10, player_2[0])
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
        if self.stats == 'full':
            self.weekly_frame = pd.DataFrame(data=1500, index=FULL_ROWS, columns=players[1:])
            self.weekly_frame.week = 0
        elif self.stats:
            pass
        else:
            self.weekly_frame = pd.DataFrame(data=1500, index=players[1:], columns='week_0')

    def _load(self):
        if self.stats:
            if self.stats == 'full':
                try:
                    self.weekly_frame = pd.DataFrame.from_csv('./elo/weekly_elo_full_week_{}.csv'.format(self.week - 1))
                except FileNotFoundError:
                    self._generate(True)
                except Exception as e:
                    raise e
            else:
                try:
                    self.weekly_frame = pd.DataFrame.from_csv('./elo/weekly_elo.csv')
                except FileNotFoundError:
                    self._generate()
                except Exception as e:
                    raise e
        else:
            try:
                self.weekly_frame = pd.DataFrame.from_csv('./elo/weekly_elo.csv')
            except FileNotFoundError:
                self._generate()
            except Exception as e:
                raise e

    def _verify(self):
        return self.weekly_frame.week[0] == (self.week - 1)

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
            new_week = 'week_{}'.format(self.week)

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
        else:
            self._write()


if __name__ == "__main__":
    calc = EloCalc(WEEK)
