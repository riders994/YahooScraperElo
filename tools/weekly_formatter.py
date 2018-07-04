import pandas as pd
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

class WeeklyFormatter:
    def __init__(self, week):
        print('Formatter started')
        self.week = int(week)
        self.score_dict = dict()

    def _fix_scores(self, frame):
        print('Fixing scores')
        frame['true_score'] = 0.0
        scored = set()
        for team in frame.index:
            if team not in scored:
                home = frame.loc[team]
                away = home.opponent
                print('Fixing scores for {home} and {away} for week {week}'.format(home=team, away=away, week=self.week))
                home_score = home.score
                away_score = frame.loc[away].score
                diff = (9 - home_score - away_score)/2
                home_score += diff
                away_score += diff
                print('boop')
                frame['true_score'][team] = home_score
                print('boop')
                frame['true_score'][away] = away_score
                print('boop')
                scored.add(team)
                scored.add(away)
                print('Fixed scores for {home} and {away} for week {week}'.format(home=team, away=away, week=self.week))
        return(frame[KEEP_COLS])

    def _format(self, player_dict):
        frame = pd.DataFrame.from_dict(player_dict, orient='index', columns=INIT_COLS)
        print('Loaded frame')
        frame.drop(index=['-/-', '0'], inplace=True)
        fg = frame.fgmfga.str.split('/')
        ft = frame.ftmfta.str.split('/')
        print('Splitting field goals and free throws')
        frame[['fgm', 'fga']] = pd.DataFrame(fg.tolist(), index=frame.index)
        frame[['ftm', 'fta']] = pd.DataFrame(ft.tolist(), index=frame.index)
        frame['week'] = self.week
        for col in INT_COLS:
            frame[col] = frame[col].astype(int)
            print(col)
        for col in FLT_COLS:
            frame[col] = frame[col].astype(float)
        self.frame = self._fix_scores(frame)
        print('Scores fixed')

    def _write(self):
        self.frame.to_csv('./weekly_stats/week_{}.csv'.format(self.week))

    def run(self, player_dict):
        print('Loading testing dictionary.')
        self._format(player_dict)
        self._write()


if __name__ == '__main__':
    with open('player_stats.pkl', 'rb') as file:
        stats_dict = pickle.load(file)

    frm = WeeklyFormatter(WEEK)
    frm.run(stats_dict)
