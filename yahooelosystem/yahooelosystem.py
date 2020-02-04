import os
import logging
import argparse
import pandas as pd
from .tools import WeeklyFormatter
from yahooscrapingtools import YahooScrapingTools
from .tools import EloCalc

parser = argparse.ArgumentParser()

LEAGUE = {
    'yid': '395.l.12682',
    'year': 2019,
    'leagueid': 0,
    'team_map': {
        '395.l.12682.t.2': 1,
        '395.l.12682.t.12': 11,
        '395.l.12682.t.6': 3,
        '395.l.12682.t.1': 0,
        '395.l.12682.t.3': 6,
        '395.l.12682.t.4': 7,
        '395.l.12682.t.9': 5,
        '395.l.12682.t.8': 9,
        '395.l.12682.t.7': 8,
        '395.l.12682.t.5': 2,
        '395.l.12682.t.11': 10,
        '395.l.12682.t.10': 4
    }
}

WEEK = '1'

MODES = {'csv', 'sql'}
TABLES = ['weekly_elo']


def week_formatter(week):
    s = week.split(':')
    if len(s) - 1:
        try:
            return range(int(s[0]), int(s[-1]) + 1), True
        except ValueError:
            return
    else:
        return int(week), False


class YahooEloSystem:

    loaded = False
    scraper = None
    formatter = None
    calculator = None
    data_model = dict()
    _logger = logging.getLogger(__file__)

    def __init__(self, league_info, week, scraper=None, creds=None, mode='csv', path=None):
        self.mode = '.' + mode
        self.creds = creds
        self.league_info = league_info
        self.week, self.multi = week_formatter(week)
        if path:
            self.path = path
        else:
            self.path = os.getcwd()
        if scraper:
            self.scraper = scraper
        else:
            self._gen_scraper()
            self.scraper.login()

    def _set_mode(self, new_mode):
        if new_mode not in MODES:
            raise ValueError(f'Invalid mode: {new_mode}')
        else:
            self.mode = '.' + new_mode

    def _gen_scraper(self):
        self.scraper = YahooScrapingTools(self.creds)

    def _load_pd(self):
        for table in TABLES:
            if table == 'weekly_stats':
                pass
            frame = pd.read_csv(os.path.join(self.path, 'resources', table + self.mode))
            self.data_model.update({table: frame})
        self.loaded = True

    def _load_sql(self):
        for table in TABLES:
            if table == 'weekly_stats':
                pass
            frame = pd.read_csv(os.path.join(self.path, 'resources', table + self.mode))
            self.data_model.update({table: frame})
        self.loaded = True

    def _load(self):
        if self.mode == '.csv':
            self._load_pd()

    def dump(self):
        if self.mode == '.csv':
            for name, table in self.data_model.items():
                table.to_csv(os.path.join(self.path, 'resources', name + self.mode))

    def _check_week(self, week=None):
        if week:
            return 'week_' + week in self.data_model['weekly_elo'].columns
        return 'week_' + str(self.week) in self.data_model['weekly_elo'].columns

    def _set_formatter(self):
        self.formatter = WeeklyFormatter(self.league_info)

    def _set_calc(self):
        self.calculator = EloCalc(self.league_info)

    def run_multiple(self, override=False):
        self.multi = False
        if len(self.week) - 1:
            week_stored = self.week
        else:
            week_stored = range(self.week + 1)
        for i in week_stored:
            self.week = i
            self.run(override)

    def run(self, override=False):
        if not self.formatter:
            self._set_formatter()
        if not self.calculator:
            self._set_calc()
        if self.multi:
            self.run_multiple(override)
        else:
            if self.loaded:
                if not override:
                    if self._check_week():
                        return self.data_model['weekly_elo']['week_' + str(self.week)]

                if self._check_week(self.week - 1):
                    matchups = self.scraper.get_scoreboards(self.league_info['yid'], self.week)
                    self.formatter.ingest(matchups, self.week)
                    self.calculator.run(self.formatter.create_df(self.week), self.data_model['weekly_elo'], self.week)
                    self.data_model.update({'weekly_elo': self.calculator.weekly_frame})
                    return self.calculator.weekly_frame
                else:
                    return 'Sorry, missing data'
            else:
                self._load()
                self.run(override)


if __name__ == "__main__":
    sys = YahooEloSystem(LEAGUE, WEEK)
    sys.run(True)
    sys.dump()
    print('done')
