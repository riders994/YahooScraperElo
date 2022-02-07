import pandas as pd
import numpy as np
import logging
from .funkydo import elo_calc

WEEK = 2
FULL_ROWS = ['fgpct', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'true_score',
             'week']

_logger = logging.getLogger(__name__)


class SeasonalFrameCalculator:

    dename = dict()
    lake_names = None
    lake_players = None
    team_elo_frame = None
    stat_elo_frame = None
    roto_frame = None

    def __init__(self, data_lake=dict()):
        self.data_lake = data_lake

    def fill_lake(self, data=None):
        if data:
            self.data_lake = data
        self.lake_names = self.data_lake.get('names')
        self.dename.update({v: k for k, v in self.lake_names.items()})
        self.lake_players = self.data_lake.get('players')

    def freeze_lake(self):
        self.data_lake.update({
            'players': self.lake_players,
            'names': self.lake_names
        })

    def drain_lake(self):
        return self.data_lake

    def _generate(self, schema):
        if isinstance(schema, list):
            for s in schema:
                self._generate(s)
        else:
            if schema == 'team_elo':
                self.team_elo_frame = pd.DataFrame(
                    {'week_0': [1500] * len(self.lake_players)}, index=self.lake_players.keys()
                )

    def _team_elo(self, board, week=0):
        last_week = 'week_{}'.format(week - 1)
        new_week = {k: v for k, v in self.team_elo_frame[last_week].iteritems()}
        calced = set()
        vals = board['true_score']
        for player_1_id in board.index:
            if player_1_id not in calced:
                player_2_id = board['opponent'][player_1_id]

                #                 _logger.info('Calculating for %s vs. %s', player_1, player_2)
                player_1_data = [
                    self.team_elo_frame.loc[player_1_id, 'week_{}'.format(week - 1)] * 1.0, vals[player_1_id]
                ]
                player_2_data = [
                    self.team_elo_frame.loc[player_2_id, 'week_{}'.format(week - 1)] * 1.0, vals[player_2_id]
                ]
                scores = elo_calc(player_1_data, player_2_data, k=60)
                #                 _logger.info('Adding scores to new week')
                new_week.update({player_1_id: scores[0]})
                new_week.update({player_2_id: scores[1]})
                calced.add(player_1_id)
                calced.add(player_2_id)
        #         _logger.info('Writing to frame')
        self.team_elo_frame['week_{}'.format(week)] = pd.Series(new_week)

    def run(self, week=0, scoreboard=None, team_elo=None, stat_elo=None, roto=None):
        if week:
            if team_elo is not None:
                if not isinstance(team_elo, bool):
                    self.team_elo_frame = team_elo.rename(index=self.dename)
                self._team_elo(scoreboard, week)
        else:
            schema = list()
            if team_elo:
                schema.append('team_elo')
            if stat_elo:
                schema.append('stat_elo')
            if roto:
                schema.append('roto')
            if len(schema) == 1:
                schema = schema[0]
            elif len(schema) == 0:
                schema = ['team_elo']
            self._generate(schema)


if __name__ == "__main__":
    pass
