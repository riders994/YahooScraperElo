import json
import os
import pandas as pd
from yahooelosystem import YahooEloSystem
from yahooelosystem.tools import YahooScraper
from time import sleep

LAKE = {
    'sports', 'leagues', 'players', 'names'
}

WEEKS = {
    '2023': '1:24',
    '2022': '1:24',
    '2021': '1:24',
    '2020': '1:20',
    '2019': '1:19',
    '2018': '1:23',
    '2017': '1:23',
    '2016': '1:22',
    '2015': '1:22',
    '2014': '0:24'
}

K_GRID = {20, 40, 60}
OSA_GRID = {0, 20, 40, 60}


def fill_lake():
    res = dict()
    for puddle in LAKE:
        with open(os.path.join(os.getcwd(), 'data', puddle + '.json'), 'r') as f:
            res.update({puddle: json.load(f)})
    return res


def setup_scrape(lake):
    return YahooScraper(None, lake)


def run_scraper(lake):
    scraper = setup_scrape(lake)
    scraper.fill_lake()
    scraper.login()
    scraper.freeze_lake()
    return scraper


def run_annual_elo(scraper):
    elo_sys = YahooEloSystem(scraper, summaries=True)
    elo_sys.load(data_lake=scraper.drain_lake(), force_load=True)
    for i in range(2014, 2024):
        year = str(i)
        weeks = WEEKS.get(year)
        elo_sys.run('0', True, year)
        elo_sys.run(weeks, True, year)
        elo_sys.dump(True)


def last_week_finder(cols, num=None):
    nums = [int(col.split('_')[1]) for col in cols]
    if num:
        return max(nums)
    return 'week_{}'.format(max(nums))


def off_season_adjustment(last_season, lake, year, adj=40):
    adj /= 100
    dename = {v: k for k, v in lake['names'].items()}
    week = last_week_finder(last_season.columns)
    final_elos = last_season.rename(index=dename)[week].copy()
    for league_id, league_info in lake['leagues'].items():
        if league_info['year'] == year:
            break
    guids = league_info['guids']
    both = list()
    num, total = 0, 0
    newbies = dict()
    for guid in guids:
        if guid in final_elos.index:
            num += 1
            total += final_elos[guid]
            both.append(guid)
        else:
            newbies.update({guid: 1500})
    scale = 1500/(total/num)
    if adj > 0:
        final_elos[both] = (final_elos[both] * scale - 1500) * adj + 1500
    adjusted_elos = final_elos.loc[both]
    return pd.concat([adjusted_elos, pd.Series(newbies)])


def scoreboard_from_matchups(matchups_df, week):
    rows = {}
    for _, row in matchups_df[matchups_df['week'] == week].iterrows():
        rows[row['home_guid']] = {'true_score': row['home_score'], 'opponent': row['away_guid']}
        rows[row['away_guid']] = {'true_score': row['away_score'], 'opponent': row['home_guid']}
    return pd.DataFrame.from_dict(rows, orient='index')


def run_full_elo(lake, k, osa, calc):
    from yahooelosystem.tools.calculator import SeasonalFrameCalculator
    calc_obj = SeasonalFrameCalculator(lake, calc)
    calc_obj.fill_lake(lake)
    calc_obj._set_k(k)
    new = None
    suffix = '_c_k_{}_osa_{}'.format(k, osa) + ('_trin' if calc == 'trinary' else '')
    for i in range(2014, 2024):
        year = str(i)
        matchups_df = pd.read_csv(
            os.path.join(os.getcwd(), 'resources', 'matchups_{}.csv'.format(year)), index_col=0
        )
        if new is None:
            for league_id, league_info in lake['leagues'].items():
                if league_info['year'] == year:
                    break
            guids = league_info['guids']
            calc_obj.team_elo_frame = pd.DataFrame({'week_0': [1500.0] * len(guids)}, index=guids)
        else:
            calc_obj.team_elo_frame = pd.DataFrame(new, columns=['week_0'])
        for w in sorted(matchups_df['week'].unique()):
            board = scoreboard_from_matchups(matchups_df, w)
            calc_obj._team_elo(board, int(w))
        result_frame = calc_obj.team_elo_frame.rename(index=lake['names'])
        result_frame.to_csv(
            os.path.join(os.getcwd(), 'resources', 'weekly_elos_{}{}.csv'.format(year, suffix))
        )
        new = off_season_adjustment(result_frame, lake, str(i + 1), adj=osa)


def stitch():
    last_week = None
    core_df = None
    for i in range(2014, 2024):
        name = 'weekly_elos_{}.csv'.format(i)
        df = pd.read_csv(os.path.join(os.getcwd(), 'resources', name), index_col=0)
        if last_week:
            old_cols = df.columns
            end = last_week_finder(old_cols, True)
            df.columns = ['week_{}'.format(j) for j in range(last_week + 1, last_week + end + 2)]
            last_week = last_week_finder(df.columns, True)
            core_df = core_df.merge(df, how='outer', left_index=True, right_index=True)
        else:
            last_week = last_week_finder(df.columns, True)
            core_df = df
    core_df.to_csv(os.path.join(os.getcwd(), 'resources', 'seasonal_elo.csv'))


def run():
    lake = fill_lake()
    annual_done = all(
        os.path.exists(os.path.join(os.getcwd(), 'resources', 'matchups_{}.csv'.format(y)))
        for y in range(2014, 2024)
    )
    if not annual_done:
        scraper = run_scraper(lake)
        run_annual_elo(scraper)
    for k in K_GRID:
        for osa in OSA_GRID:
            run_full_elo(lake, k, osa, 'score')
            run_full_elo(lake, k, osa, 'trinary')
    stitch()


if __name__ == "__main__":
    run()
    print('done')
