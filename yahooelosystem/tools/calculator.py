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
    k = 60
    lake_leagues = None
    lake_names = None
    lake_players = None
    proba_frame = None
    roto_frame = None
    stat_elo_frame = None
    team_elo_frame = None
    true_score_rows = list()

    def __init__(self, data_lake=dict()):
        self.data_lake = data_lake

    def fill_lake(self, data=None):
        if data:
            self.data_lake = data
        self.lake_leagues = self.data_lake.get('leagues')
        self.lake_names = self.data_lake.get('names')
        self.dename.update({v: k for k, v in self.lake_names.items()})
        self.lake_players = self.data_lake.get('players')

    def freeze_lake(self):
        self.data_lake.update({
            'players': self.lake_players,
            'names': self.lake_names,
            'lake': self.lake_leagues
        })

    def drain_lake(self):
        return self.data_lake

    def _set_k(self, new_k):
        if isinstance(int, new_k) or isinstance(float, new_k):
            if new_k > 0:
                self.k = new_k

    def _generate(self, schema, year):
        if isinstance(schema, list):
            for s in schema:
                self._generate(s, year)
        else:
            if schema == 'team_elo':
                for league_id, league_info in self.lake_leagues.items():
                    if league_info['year'] == year:
                        break
                guids = league_info['guids']
                self.team_elo_frame = pd.DataFrame(
                    {'week_0': [1500] * len(guids)}, index=guids
                )
            if schema == 'probs':
                for league_id, league_info in self.lake_leagues.items():
                    if league_info['year'] == year:
                        break
                guids = league_info['guids']
                self.proba_frame = pd.DataFrame(
                    {'week_0': [0.5] * len(guids)}, index=guids
                )
            if schema == 'true_score':
                for league_id, league_info in self.lake_leagues.items():
                    if league_info['year'] == year:
                        break
                guids = league_info['guids']
                self.true_score_frame = pd.DataFrame(
                    {'week_0': [0.5] * len(guids)}, index=guids
                )

    def _team_elo(self, board, week=0, summaries=False):
        last_week = 'week_{}'.format(week - 1)
        new_week = dict()
        calced = set()
        true_scores = board['true_score']
        for player_1_id in board.index:
            if player_1_id not in calced:
                player_2_id = board['opponent'][player_1_id]

#                 _logger.info('Calculating for %s vs. %s', player_1, player_2)
                player_1_data = [
                    self.team_elo_frame.loc[player_1_id, last_week] * 1.0, true_scores[player_1_id]
                ]
                player_2_data = [
                    self.team_elo_frame.loc[player_2_id, last_week] * 1.0, true_scores[player_2_id]
                ]
                if summaries:
                    scores, probas = elo_calc(player_1_data, player_2_data, self.k, summaries)
                    self.true_score_rows.append({
                        'week': week,
                        'player_1': player_1_id,
                        'player_2': player_2_id,
                        'player_1_score': true_scores[player_1_id],
                        'player_2_score': true_scores[player_2_id],
                        'player_1_proba': probas[0],
                        'player_2_proba': probas[1]
                    })
                    self._gen_matchup_summary_row()
                else:
                    scores = elo_calc(player_1_data, player_2_data, self.k)
#                 _logger.info('Adding scores to new week')
                new_week.update({player_1_id: scores[0]})
                new_week.update({player_2_id: scores[1]})
                calced.add(player_1_id)
                calced.add(player_2_id)
#         _logger.info('Writing to frame')
        for k, v in self.team_elo_frame[last_week].iteritems():
            if not new_week.get(k):
                new_week.update({k: v})
        self.team_elo_frame['week_{}'.format(week)] = pd.Series(new_week)

    def run(self, week=0, scoreboard=None, team_elo=None, stat_elo=None, roto=None, year=None, summstats=None, k=None):
        if k:
            self._set_k(k)
        if week:
            if team_elo is not None:
                if not isinstance(team_elo, bool):
                    self.team_elo_frame = team_elo.rename(index=self.dename)
                self._team_elo(scoreboard, week, summstats)
        else:
            schema = list()
            if team_elo:
                schema.append('team_elo')
            if stat_elo:
                schema.append('stat_elo')
            if roto:
                schema.append('roto')
            if summstats:
                schema.append('probs')
                schema.append('true_score')
            if len(schema) == 1:
                schema = schema[0]
            elif len(schema) == 0:
                schema = ['team_elo']
            self._generate(schema, year)


if __name__ == "__main__":
    pass
