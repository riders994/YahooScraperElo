import os
import json
import pandas as pd
import datetime as dt
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from collections import defaultdict
from yahooelosystem import YahooEloSystem
from yahooelosystem.tools import YahooScraper

LAKE = {
    'sports', 'leagues', 'players', 'names'
}

WEEKS = {
    '2021': '1:17',
    '2020': '1:20',
    '2019': '1:19',
    '2018': '1:23',
    '2017': '1:23',
    '2016': '1:22',
    '2015': '1:22',
    '2014': '0:24'
}

SINGLES = {
    'po', 'winner'
}

DOUBLES = {
    'manager', 'true_score'
}

K_GRID = [
    20, 40, 60
]

OSA_GRID = [
    0, 20, 40, 60
]

DEFAULT_ELO = {
    'seasonal': 1500.0
}

for k in K_GRID:
    for osa in OSA_GRID:
        DEFAULT_ELO.update({'_'.join(['k', str(k), 'osa', osa, 'elo']): 1500.0})


def fill_lake():
    res = dict()
    for puddle in LAKE:
        with open(os.path.join(os.getcwd(), 'data', puddle + '.json'), 'r') as f:
            res.update({puddle: json.load(f)})
    return res


def get_leagues(context):
    game = yfa.Game(context, 'nba')
    nba_leagues = set(game.league_ids())
    return {leeg: yfa.League(context, leeg) for leeg in nba_leagues if leeg[0] != '1'}


def get_player_dict(lake):
    names = lake['names']
    players = lake['players']
    res = dict()
    for p_id, player_info in players.items():
        for team_name in player_info['names']:
            res.update({team_name: names[p_id]})
    return res


def get_matchups(p_dict):
    res = dict()
    sc = OAuth2(None, None, from_file='./secrets.json')
    leagues = get_leagues(sc)
    historic_wins = defaultdict(int)
    for l_id, lg in leagues.items():
        season_dict = dict()
        end = lg.settings()['end_week']
        season = lg.settings()['season']
        season_wins = defaultdict(int)
        for i in range(int(end) + 1):
            weekly_dict = dict()
            if i:
                scoreboard = lg.matchups(i)
                extracted_scoreboard = scoreboard['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
                for j in range(0, len(extracted_scoreboard) - 1):
                    matchup = extracted_scoreboard[str(j)]['matchup']
                    po = bool(int(matchup['is_playoff']))
                    champion = False
                    date = dt.datetime.strptime(matchup['week_end'], '%Y-%M-%d')
                    home = matchup['0']['teams']['0']['team']
                    away = matchup['0']['teams']['1']['team']
                    home_list = home[0]
                    for el in home_list:
                        if isinstance(el, dict):
                            if el.get('team_key'):
                                home_id = el.get('team_key')
                            if el.get('name'):
                                home_name = el.get('name')
                    home_score = float(home[1]['team_points']['total'])
                    away_list = away[0]
                    for el in away_list:
                        if isinstance(el, dict):
                            if el.get('team_key'):
                                away_id = el.get('team_key')
                            if el.get('name'):
                                away_name = el.get('name')
                    away_score = float(away[1]['team_points']['total'])
                    total_score = away_score + home_score

                    if str(i) == end and po != bool(int(matchup['is_consolation'])):
                        champion = matchup['winner_team_key']
                    weekly_dict.update({
                        str(j): {
                            'home': {
                                'id': home_id,
                                'name': home_name,
                                'manager': p_dict[home_name],
                                'historic_wins': historic_wins[home_name],
                                'season_wins': season_wins[home_name],
                                'score': home_score,
                                'true_score': home_score/total_score,
                                'date': date,
                                'playoff': po,
                                'champion': champion == home_id,
                                'winner': home_score/total_score > .5,
                            }
                            , 'away': {
                                'id': away_id,
                                'name': away_name,
                                'manager': p_dict[away_name],
                                'historic_wins': historic_wins[away_name],
                                'season_wins': season_wins[away_name],
                                'score': away_score,
                                'true_score': away_score/total_score,
                                'date': date,
                                'playoff': po,
                                'champion': champion == away_id,
                                'winner': away_score/total_score > .5,
                            }
                        }
                    })
                    if home_score/total_score > .5:
                        historic_wins[p_dict[home_name]] += 1
                        season_wins[p_dict[home_name]] += 1
                    if away_score / total_score > .5:
                        historic_wins[p_dict[away_name]] += 1
                        season_wins[p_dict[away_name]] += 1
                else:
                    scoreboard = lg.matchups('1')
                    extracted_scoreboard = scoreboard['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
                    for j in range(0, len(extracted_scoreboard) - 1):
                        teams = extracted_scoreboard[str(j)]['matchup']['0']['teams']
                        for team in teams:
                            team_list = team['team']
                            for el in team_list:
                                if isinstance(el, dict):
                                    name = el.get('name')
                                    if name:
                                        weekly_dict.update({p_dict[name]: historic_wins[p_dict[name]]})

            season_dict.update({str(i): weekly_dict})
        res.update({season: season_dict})
    return res


def matchups_to_rows(matchups, year):
    res = list()
    for week, weekly_dict in matchups.items():
        if int(week):
            for num, vs in weekly_dict.items():
                contest = dict()
                contest.update({
                    'year': year,
                    'week': week,
                    'contest': num,
                })
                for team in ['home', 'away']:
                    t = vs[team]
                    for k, v in t.items():
                        if k in SINGLES:
                            if k == 'winner':
                                if v:
                                    contest.update({k: team})
                            elif v:
                                contest.update({k: v})
                        elif k in DOUBLES:
                            contest.update({'_'.join([team, k]): v})
                res.append(contest)
    return res


def get_proba_row(matchup_data):
    return matchup_data


def get_elo_rows(matchup_data):
    return home_row, away_row


def process_matchup(matchup_data):
    pass


def evaluate_matchups(matchups):
    years = matchups.keys()
    n_years = [int(y) for y in years]
    n_years.sort()
    matchup_rows = list()
    player_elos = dict()
    proba_rows = list()
    off_season = False
    for y in n_years:
        season_data = matchups[str(y)]
        matchup_rows += matchups_to_rows(season_data, y)

        for i in range(len(season_data) + 1):
            weekly_data = season_data[str(i)]
            if i:
                pass
            else:
                off_season_elos = dict()
                for player, wins in weekly_data.items():
                    if wins:
                        pass
                    else:
                        off_season_elos.update({player: DEFAULT_ELO.copy()})
                        


    matchup_frame = pd.DataFrame(matchup_rows)
    player_frame, proba_frame = 1, 1
    return matchup_frame, player_frame, proba_frame


def run():
    lake = fill_lake()
    player_dict = get_player_dict(lake)
    matchup_data = get_matchups(player_dict)
    dfs = evaluate_matchups(matchup_data)


if __name__ == "__main__":
    run()
