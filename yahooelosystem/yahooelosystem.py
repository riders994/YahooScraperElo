import os
import logging
import argparse
import pandas as pd
from tools import WeeklyFormatter, SeasonalFrameCalculator, YahooScraper, week_formatter
import json

parser = argparse.ArgumentParser()


LAKE = {
    'sports': {
        'nfl': ['380.l.436197', '390.l.470721', '399.l.684980', '406.l.200662'],
        'nba': [
            '112.l.71520',
            '131.l.196878',
            '342.l.15082',
            '353.l.37110',
            '364.l.32235',
            '375.l.10560',
            '385.l.5726',
            '395.l.12682',
            '402.l.8048',
            '410.l.11456'
        ]
    },
    'leagues': {
        '410.l.11456': {
            'year': '2021',
            'guids': [
                'YWVPE4432SD4KI54TYIBYSUY4E',
                'LNRT67BZLFW4H3EUP2TDHOG74M',
                'VWB4LBHYWJRAQ2E66SHEWFTCRI',
                'VOKZZSOK4ZQXCRZS4X3C6A2UKM',
                'QOSB6TNJH6AZSUXHZXGSCF6KGY',
                'PMEMCDE2SSHJ5YKGBVJZ4PI62E',
                'NIHSTHKSFAGS6M5GEP36QG4T64',
                'NZ2X6OUUEORPJ3ZFHCL4EBEU6J',
                '5RADOHUTBULBXBWUKY4J275JZE',
                'VFTMFPVMSCHKRTIILW7BM5UIGA',
                'NVAFN332AJMUVGCGC3CVBDWNQQ',
                'CCYS62GDCHMWDZZZQDTB35DTRE'
            ]
        }
    },
    'players': {
        'YWVPE4432SD4KI54TYIBYSUY4E': {
            'lids': ['410.l.11456'],
            'names': ["CJ M'Gollum"]
        },
        'LNRT67BZLFW4H3EUP2TDHOG74M': {
            'lids': ['410.l.11456'],
            'names': ['The Jive Turkeys']
        },
        'VWB4LBHYWJRAQ2E66SHEWFTCRI': {
            'lids': ['410.l.11456'],
            'names': ['Spicy T']
        },
        'VOKZZSOK4ZQXCRZS4X3C6A2UKM': {
            'lids': ['410.l.11456'],
            'names': ['The Young Bane Rises']
        },
        'QOSB6TNJH6AZSUXHZXGSCF6KGY': {
            'lids': ['410.l.11456'],
            'names': ['Ball Drogo']
        },
        'PMEMCDE2SSHJ5YKGBVJZ4PI62E': {
            'lids': ['410.l.11456'],
            'names': ['Every “DeRozan” Has Its Thorn']
        },
        'NIHSTHKSFAGS6M5GEP36QG4T64': {
            'lids': ['410.l.11456'],
            'names': ['Bing Bong']
        },
        'NZ2X6OUUEORPJ3ZFHCL4EBEU6J': {
            'lids': ['410.l.11456'],
            'names': ['The Bealtles']
        },
        '5RADOHUTBULBXBWUKY4J275JZE': {
            'lids': ['410.l.11456'],
            'names': ['SexLand']
        },
        'VFTMFPVMSCHKRTIILW7BM5UIGA': {
            'lids': ['410.l.11456'],
            'names': ['Kennard-ly Wait']
        },
        'NVAFN332AJMUVGCGC3CVBDWNQQ': {
            'lids': ['410.l.11456'],
            'names': ['Lebran Grains']
        },
        'CCYS62GDCHMWDZZZQDTB35DTRE': {
            'lids': ['410.l.11456'],
            'names': ['Globo Gym Purple Cobras']
        }
    },
    'names': {
        'YWVPE4432SD4KI54TYIBYSUY4E': 'Neil',
        'LNRT67BZLFW4H3EUP2TDHOG74M': 'John',
        'VWB4LBHYWJRAQ2E66SHEWFTCRI': 'Ravi',
        'VOKZZSOK4ZQXCRZS4X3C6A2UKM': 'Chris',
        'QOSB6TNJH6AZSUXHZXGSCF6KGY': 'Rohan',
        'PMEMCDE2SSHJ5YKGBVJZ4PI62E': 'James C',
        'NIHSTHKSFAGS6M5GEP36QG4T64': 'Alison',
        'NZ2X6OUUEORPJ3ZFHCL4EBEU6J': 'Aaron',
        '5RADOHUTBULBXBWUKY4J275JZE': 'Alex W',
        'VFTMFPVMSCHKRTIILW7BM5UIGA': 'Sahil',
        'NVAFN332AJMUVGCGC3CVBDWNQQ': 'Alex K',
        'CCYS62GDCHMWDZZZQDTB35DTRE': 'James W'
    }
}

WEEK = '0:16'

MODES = {'.csv', '.sql'}
TABLES = ['weekly_elos']
PUDDLES = LAKE.keys()
YEAR = '2021'


class YahooEloSystem:

    calculator = None
    data_lake = dict()
    data_model = dict()
    formatter = None
    last_year = None
    loaded = False
    multi = False
    scraper = None
    week = '0'

    _logger = logging.getLogger(__file__)

    def __init__(self, scraper=None, creds=None, mode='.csv', path=None):
        self.mode = mode
        self.creds = creds
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
            raise ValueError('Invalid mode: {}'.format(new_mode))
        else:
            self.mode = new_mode

    def _gen_scraper(self):
        self.scraper = YahooScraper(self.creds)

    def _load_pd(self):
        for table in TABLES:
            if table == 'weekly_stats':
                pass
            try:
                frame = pd.read_csv(os.path.join(self.path, 'resources', table + self.mode), index_col=0)
                self.data_model.update({table: frame})
            except FileNotFoundError:
                pass
        self.loaded = True

    def _load_json(self):
        for son in PUDDLES:
            with open(os.path.join(self.path, 'data', son + '.json'), 'r') as f:
                self.data_lake.update({son: json.load(f)})

    def _load_sql(self):
        for table in TABLES:
            if table == 'weekly_stats':
                pass
            frame = pd.read_csv(os.path.join(self.path, 'resources', table + self.mode), index_col=0)
            self.data_model.update({table: frame})
        self.loaded = True

    def load(self, payload=None):
        if isinstance(payload, dict):
            self.data_model.update(payload)
        elif self.mode == '.csv':
            self._load_json()
            self._load_pd()

    def dump(self, publish=False, pub_sig=''):
        if self.mode == '.csv':
            for name, pond in self.data_lake.items():
                with open(os.path.join(self.path, 'data', name + '.json'), 'w') as f:
                    json.dump(pond, f)
            for name, table in self.data_model.items():
                table.to_csv(os.path.join(
                    self.path, 'resources', name +
                                            publish * '_{}'.format(self.last_year) + publish * pub_sig + self.mode
                ))

    def ingest(self, choice=-1):
        self.scraper.fill_lake(self.data_lake)
        self.scraper.pick_league(choice)
        leagues, players = self.scraper.scan_league()
        self.data_lake.update({
            'leagues': leagues,
            'players': players
        })

    def _set_week(self, week):
        self.week, self.multi = week_formatter(str(week))

    def _set_formatter(self):
        if not self.formatter:
            self.formatter = WeeklyFormatter()

    def _set_calc(self):
        if not self.calculator:
            self.calculator = SeasonalFrameCalculator(self.data_lake)

    def run_multiple(self, override=False, year=YEAR):
        self.multi = False
        if len(self.week) - 1:
            week_stored = self.week
        else:
            week_stored = range(self.week + 1)
        for i in week_stored:
            self.week = i
            self.run(self.week, override, year)

    def run(self, week=WEEK, override=False, year=YEAR):
        self._set_week(week)
        self.last_year = year
        self._set_formatter()
        self._set_calc()
        if self.multi:
            self.run_multiple(override, year)
        else:
            if self.loaded:
                self.calculator.fill_lake(self.data_lake)
                if self.week == 0:
                    self.calculator.run(self.week)
                    self.data_model.update(
                        {'weekly_elos': self.calculator.team_elo_frame.rename(index=self.data_lake['names'])}
                    )
                else:
                    w = week or self.week
                    if 'week_' + str(w) in self.data_model['weekly_elos'].columns:
                        if not override:
                            if 'week_' + str(w) in self.data_model['weekly_elos'].columns:
                                return
                        for league_id, league_info in self.data_lake['leagues'].items():
                            league = league_id
                            if league_info['year'] == year:
                                break
                        matchups = self.scraper.get_scoreboards(league, self.week)
                        self.formatter.ingest(matchups, self.week)
                        df = self.formatter.create_df(self.week)
                        self.calculator.run(self.week, df, self.data_model['weekly_elos'])
                        self.data_model.update(
                            {'weekly_elos': self.calculator.team_elo_frame.rename(index=self.data_lake['names'])}
                        )
                        self.loaded = True
            else:
                self.load()
                self.run(str(self.week), override, year)


if __name__ == "__main__":
    elo_sys = YahooEloSystem()
    elo_sys.run(WEEK, True, '2021')
    elo_sys.dump(False)
    print('done')
