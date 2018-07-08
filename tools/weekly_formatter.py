import pandas as pd
import logging
import pickle


PLAYER_PICKLE_PATH = './player_stats.pkl'
INIT_COLS = ['fgmfga', 'fgpct', 'ftmfta', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks',
             'turnovers', 'score', 'opponent']
KEEP_COLS = ['fgm', 'fga', 'fgpct', 'ftm', 'fta', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks'
             , 'turnovers', 'true_score', 'opponent', 'week']
INT_COLS = ['fgm', 'fga', 'ftm', 'fta', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers',
            'week']
FLT_COLS = ['fgpct', 'ftpct', 'score']
WEEK = 1


def _purge_stars(column):
    return column.str.replace('*', '', regex=False)


class WeeklyFormatter:
    def __init__(self, week):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.getLevelName('INFO'))
        self.logger.info('Formatter started')
        self.week = week
        self.score_dict = dict()

    def _fix_scores(self, frame):
        self.logger.info('Fixing scores')
        frame['true_score'] = 0.0
        scored = set()
        for team in frame.index:
            if team not in scored:
                home = frame.loc[team]
                away = home.opponent
                self.logger.info('Fixing scores for {home} and {away} for week {week}'.format(home=team, away=away, week=self.week))
                home_score = home.score * 1.0
                try:
                    away_score = frame.loc[away].score * 1.0
                except KeyError:
                    away_score = 0
                except Exception as e:
                    raise e
                diff = (9 - home_score - away_score)/2
                home_score += diff
                away_score += diff
                home_score /= 9
                away_score /= 9
                self.logger.info('boop')
                frame['true_score'][team] = home_score
                self.logger.info('boop')
                frame['true_score'][away] = away_score
                self.logger.info('boop')
                scored.add(team)
                scored.add(away)
                self.logger.info('Fixed scores for {home} and {away} for week {week}'.format(home=team, away=away, week=self.week))
        return frame[KEEP_COLS]

    def _format(self, player_dict):
        frame = pd.DataFrame.from_dict(player_dict, orient='index', columns=INIT_COLS)
        self.logger.info('Loaded frame')
        for col in ['-/-', '0']:
            try:
                frame.drop(index=col, inplace=True)
            except KeyError:
                pass
            except Exception as e:
                raise e
        fg = frame.fgmfga.str.split('/')
        ft = frame.ftmfta.str.split('/')
        self.logger.info('Splitting field goals and free throws')
        frame[['fgm', 'fga']] = pd.DataFrame(fg.tolist(), index=frame.index)
        frame[['ftm', 'fta']] = pd.DataFrame(ft.tolist(), index=frame.index)
        frame['week'] = self.week
        for col in INT_COLS:
            frame[col] = frame[col].astype(int)
            self.logger.info(col)
        for col in FLT_COLS:
            try:
                frame[col] = frame[col].astype(float)
            except ValueError:
                column = _purge_stars(frame[col])
                frame[col] = column.astype(float)
            except Exception as e:
                raise e

        self.frame = self._fix_scores(frame)
        self.logger.info('Scores fixed')

    def _write(self):
        self.frame.to_csv('./weekly_stats/week_{}.csv'.format(self.week))

    def run(self, player_dict):
        self.logger.info('Loading testing dictionary.')
        self._format(player_dict)
        self._write()


if __name__ == '__main__':
    with open('player_stats.pkl', 'rb') as file:
        stats_dict = pickle.load(file)

    frm = WeeklyFormatter(WEEK)
    frm.run(stats_dict)
