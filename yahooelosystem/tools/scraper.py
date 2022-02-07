import json
import os
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa

PARAMS = {
    'access_token': os.environ.get('ACCESS_TOKEN'),
    'consumer_key': os.environ.get('CONSUMER_KEY'),
    'consumer_secret': os.environ.get('CONSUMER_SECRET'),
    'guid': os.environ.get('GUID'),
    'token_time': float(os.environ.get('TOKEN_TIME')),
    'token_type': os.environ.get('TOKEN_TYPE'),
    'refresh_token': os.environ.get('REFRESH_TOKEN')
}

SPORTS = {'nba', 'nfl'}


class YahooScraper:

    sc = None
    league = None
    lake_sports = None
    lake_leagues = None
    lake_players = None
    last_league = None
    last_sport = 'nba'

    def __init__(self, creds, data_lake=dict()):
        self.data_lake = data_lake
        if creds:
            try:
                self.params = self._load_creds(creds)
            except ValueError:
                raise
        else:
            self.params = PARAMS

    @staticmethod
    def _load_creds(creds):
        if isinstance(creds, str):
            try:
                with open(os.path.join(os.getcwd(), creds), 'rb') as file:
                    dcreds = json.load(file)
            except FileNotFoundError:
                dcreds = json.loads(creds)
        elif isinstance(creds, dict):
            dcreds = creds
        else:
            raise ValueError
        return dcreds

    def _get_session(self):
        return OAuth2(**self.params)

    def _set_league(self, lid):
        self.last_league = lid

    def _set_sport(self, spid):
        self.lake_sports = spid

    def pick_sport(self, spid):
        self._set_sport(spid)

    def login(self):
        self.sc = self._get_session()

    def fill_lake(self, data=None):
        if data:
            self.data_lake = data
        self.lake_sports = self.data_lake.get('sports')
        self.lake_leagues = self.data_lake.get('leagues')
        self.lake_players = self.data_lake.get('players')

    def freeze_lake(self):
        self.data_lake.update({
            'sports': self.lake_sports,
            'leagues': self.lake_leagues,
            'players': self.lake_players
        })

    def drain_lake(self):
        return self.data_lake

    def scan_sports(self):
        for sport in SPORTS:
            game = yfa.Game(self.sc, sport)
            league_ids = list(game.league_ids())
            if self.lake_sports:
                s = self.lake_sports.get(sport)
                if s:
                    s.append(league_ids)
                else:
                    self.lake_sports.update({sport: league_ids})
            else:
                self.lake_sports = dict()
                self.lake_sports.update({sport: league_ids})

    def scan_years(self):
        pass

    def show_sports(self):
        pass

    def pick_league(self, choice=-1, sport=None):
        if sport is None:
            sport = self.last_sport
        if isinstance(choice, str):
            print('not yet')
        if isinstance(choice, int):
            self._set_league(self.lake_sports[sport][choice])

    def scan_league(self, league_id=None):
        if league_id:
            lid = league_id
            self._set_league(lid)
        else:
            lid = self.last_league
        self.league = yfa.League(self.sc, lid)
        if self.lake_leagues:
            league_data = self.lake_leagues
        else:
            league_data = dict()
        teams = self.league.teams()
        league_data.update(
            {
                lid: {
                    'year': self.league.settings()['season'],
                    'guids': [team['managers'][0]['manager']['guid'] for _, team in teams.items()]
                }
            }
        )
        self.lake_leagues = league_data

        if self.lake_players:
            player_data = self.lake_players
        else:
            player_data = dict()
        for _, team in teams.items():
            guid = team['managers'][0]['manager']['guid']
            team_info = player_data.get(guid)
            if team_info:
                if lid not in team_info['lids']:
                    team_info['lids'].append(lid)
                if team['name'] not in team_info['names']:
                    team_info['names'].append(team['name'])
            else:
                team_info = {
                    'lids': [lid],
                    'names': [team['name']]
                }
            player_data.update({guid: team_info})
        self.lake_players = player_data

        return league_data, player_data

    def get_scoreboards(self, league=None, week=None):
        if league:
            if league != self.last_league:
                self._set_league(league)
                self.league = yfa.League(self.sc, league)

        if not self.league:
            if not league:
                league = self.last_league
            self.league = yfa.League(self.sc, league)

        matchups = self.league.matchups(week)
        return matchups['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
