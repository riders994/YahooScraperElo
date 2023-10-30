import os
import json
import pandas as pd
import numpy as np
from collections import defaultdict

K_GRID = {20, 40, 60}
OSA_GRID = {0, 20, 40, 60}
ELO_NAMES = {'_c_k_{}_osa_{}'.format(k, osa) for k in K_GRID for osa in OSA_GRID}
ELO_NAMES.update({name + '_trin' for name in ELO_NAMES})
FILE_BASE = './resources/'
CONTROLS = {'historic_wins_share', 'season_wins_share', 'blind'}
with open(os.path.join(os.getcwd(), 'data', 'names.json'), 'r') as f:
    NAMES = json.load(f)


def load_elos(year):
    dename = {v: k for k, v in NAMES.items()}
    file_name = FILE_BASE + 'weekly_elos_'
    frames = {elo: pd.read_csv(file_name + str(year) + elo + '.csv', index_col=0).rename(index=dename) for elo in
              ELO_NAMES}
    frames.update({'default': pd.read_csv(file_name + str(year) + '.csv', index_col=0).rename(index=dename)})
    return frames


def load_matchups(year):
    return pd.read_csv(FILE_BASE + 'matchups_' + str(year) + '.csv', index_col=0)


def proba_calc(player_1, player_2):
    share_a = np.power(10, player_1 / 400)
    share_b = np.power(10, player_2 / 400)
    total = share_a + share_b

    return share_a / total


def get_probas(matchup, season_frames, week):
    home_guid = matchup['home_guid']
    away_guid = matchup['away_guid']
    res = {
        'historic_wins_share': .5,
        'season_wins_share': .5,
        'blind': .5,
        'week': matchup['week'],
        'season': matchup['season'],
        'home_guid': home_guid,
        'away_guid': away_guid,
        'playoffs': matchup['playoffs'],
        'true_score': matchup['home_score'],
        'winner_guid': matchup['winner_guid'],
        'loser_guid': matchup['loser_guid']

    }

    for win in ['historic_wins', 'season_wins']:
        total = matchup['home_' + win] + matchup['away_' + win]
        if total > 0:
            res.update({win + '_share': matchup['home_' + win] / total})

    for name, frame in season_frames.items():
        col = 'week_' + str(week)
        elos = frame[col]
        res.update({name + '_proba': proba_calc(elos[home_guid], elos[away_guid])})
    return res


def process_matchup(year, week, matchup, season_frames, historic_wins, season_wins):
    matchup_row = {
        'home_historic_wins': historic_wins[matchup.home_guid],
        'home_season_wins': season_wins[matchup.home_guid],
        'away_historic_wins': historic_wins[matchup.away_guid],
        'away_season_wins': season_wins[matchup.away_guid],
        'home_guid': matchup.home_guid,
        'away_guid': matchup.away_guid,
        'home_score': matchup.home_score,
        'away_score': matchup.away_score,
        'week': week,
        'season': year,
        'playoffs': matchup.playoff,
        'winner_guid': matchup.winner_guid,
        'loser_guid': matchup.loser_guid
    }
    historic_wins[matchup.winner_guid] += 1
    season_wins[matchup.winner_guid] += 1

    proba_row = get_probas(matchup_row, season_frames, week)
    return matchup_row, proba_row


def process_week(year, week, matchup_frame, season_frames, historic_wins, season_wins):
    matchup_rows = dict()
    proba_rows = dict()
    tranche = matchup_frame[matchup_frame.week == week + 1]
    for i, row in tranche.iterrows():
        name = ''.join([str(el) for el in [year, week, i]])
        m, p = process_matchup(year, week, row, season_frames, historic_wins, season_wins)
        matchup_rows.update({name: m})
        proba_rows.update({name: p})
    return matchup_rows, proba_rows


def process_season(year, historical_wins, matchup_rows, proba_rows):
    season_wins = defaultdict(int)
    season_frames = load_elos(year)
    weeks = season_frames['default'].shape[1]
    matchup_frame = load_matchups(year)
    for week in range(0, weeks):
        m, p = process_week(year, week, matchup_frame, season_frames, historical_wins, season_wins)
        matchup_rows.update(m)
        proba_rows.update(p)
    return matchup_rows, proba_rows


def process_data():
    historic_wins = defaultdict(int)
    matchup_rows = dict()
    proba_rows = dict()
    for year in range(2014, 2022):
        m, p = process_season(year, historic_wins, matchup_rows, proba_rows)
    return m, p


def rmse_calc(proba, error):
    # Here we only get the squared error, rmse is actually calculated in the RMSE analysis in order to apply different
    # aggregations
    for elo in ELO_NAMES:
        if elo in CONTROLS:
            error[elo + '_error'] = (proba['true_score'] - proba[elo]) ** 2
        else:
            error[elo + '_error'] = (proba['true_score'] - proba[elo + '_proba']) ** 2
    return error


def process_error(frame, error='RMSE'):
    # maybe there's some other error i could look at in the future, but so far analysis kinda fits my conclusions
    error_frame = frame['season,week,home_guid,away_guid,playoffs,winner_guid,true_score'.split(',')].copy()
    if error == 'RMSE':
        rmse_calc(frame, error_frame)
    return error_frame


def run():
    m, p = process_data()
    prob_frame = pd.DataFrame.from_dict(p, orient='index')
    matchup_frame = pd.DataFrame.from_dict(m, orient='index')
    matchup_frame.to_csv('./data/matchup_summary_frame.csv')
    prob_frame.to_csv('./data/proba_summary_frame.csv')
    ELO_NAMES.update({'default'})
    ELO_NAMES.update(CONTROLS)
    error_frame = process_error(prob_frame)
    error_frame.to_csv('./data/error_frame.csv')
    return error_frame


if __name__ == "__main__":
    t = run()
    print('done')
