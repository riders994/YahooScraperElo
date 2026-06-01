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


class SystemBase:

    dename = dict()
    lake_sports = None
    lake_leagues = None
    lake_players = None
    last_league = None
    lake_names = None

    def __init__(self, data_lake=dict()):
        self.data_lake = data_lake

    def fill_lake(self, data=None):
        if data:
            self.data_lake = data
        self.lake_sports = self.data_lake.get('sports')
        self.lake_leagues = self.data_lake.get('leagues')
        self.lake_players = self.data_lake.get('players')
        self.lake_names = self.data_lake.get('names')
        self.dename.update({v: k for k, v in self.lake_names.items()})

    def freeze_lake(self):
        self.data_lake.update({
            'players': self.lake_players,
            'names': self.lake_names,
            'lake': self.lake_leagues
        })

    def drain_lake(self):
        return self.data_lake
