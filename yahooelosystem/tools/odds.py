from .basics.class_bases import SystemBase
from .basics.funkydo import elo_ratio
import pandas as pd


class OddsCalculator(SystemBase):
    vig = .1
    pvig = .15
    formatter = None
    odds_frame = pd.DataFrame

    def __init__(self,data_lake=dict()):
        super().__init__(data_lake=data_lake)

    @staticmethod
    def _scrape_curr(league, week):
        matchups = league.matchups(week)
        return matchups['fantasy_content']['league'][1]['scoreboard']['0']['matchups']

    def _make_frame(self, prev_elo, matchups, week):
        self.formatter.ingest(matchups, week, True)
        pairs = self.formatter.odds[str(week)]
        rows = list()
        for pair in pairs.values():
            home_guid = pair[0]
            home_elo = prev_elo[home_guid]
            e2 = prev_elo[pair[1]]
            if e2 > home_elo:
                away_elo = home_elo
                home_elo = e2
                away_guid = home_guid
                home_guid = pair[1]
            else:
                away_guid = pair[1]
                away_elo = e2
            p, q = elo_ratio(home_elo, away_elo)
            t = p + q
            p /= t
            q /= t
            rows.append({
                'home': home_guid,
                'away': away_guid,
                'home_elo': home_elo,
                'away_elo': away_elo,
                'p': p,
                'q': q
            })
        return pd.DataFrame(rows)

    def _amer(self, week_frame, p):
        if p:
            v = self.pvig
        else:
            v = self.vig
        week_frame['home_american'] = 10000 * week_frame['p'] * (1 + v)/(week_frame['p'] * 100 - 100)
        week_frame['away_american'] = (100 - 100 * week_frame['q']) * (1 - v)/week_frame['q']
        return week_frame

    def _spread(self, week_frame, p):
        if p:
            v = self.pvig
        else:
            v = self.vig
        week_frame['spread'] = round((1 - v) * (week_frame['p'] - .5) * 18)/2
        return week_frame

    def _set_vig(self, new, vig='r'):
        if vig != 'p':
            self.vig = new
        self.pvig = new

    def set_formatter(self, formatter):
        self.formatter = formatter

    def run(self, week, league, elo_frame, playoff=False):
        if week:
            prev_elo = elo_frame['week_{}'.format(week)]
            week += 1
            matchups = self._scrape_curr(league, week)
            frame = self._make_frame(prev_elo, matchups, week)
            frame = frame.replace({'home': self.lake_names})
            frame = frame.replace({'away': self.lake_names})
            frame = self._amer(frame, playoff)
            frame = self._spread(frame, playoff)
            self.odds_frame = frame
            return self.odds_frame
