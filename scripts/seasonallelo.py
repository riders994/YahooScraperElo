import json
import os
import pandas as pd
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
    elo_sys = YahooEloSystem(scraper)
    elo_sys.load(data_lake=scraper.drain_lake(), force_load=True)
    for i in range(2014, 2022):
        year = str(i)
        weeks = WEEKS.get(year)
        elo_sys.run('0', True, year)
        elo_sys.run(weeks, True, year)
        elo_sys.dump(True)


def col_finder(cols, num=None):
    nums = [int(col.split('_')[1]) for col in cols]
    if num:
        return max(nums)
    return 'week_{}'.format(max(nums))


def off_season_adjustment(last_season, lake, year, adj=.4):
    dename = {v: k for k, v in lake['names'].items()}
    week = col_finder(last_season.columns)
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
    final_elos[both] = (final_elos[both] * scale - 1500) * adj + 1500
    adjusted_elos = final_elos.loc[both]
    return adjusted_elos.append(pd.Series(newbies))


def run_full_elo(lake):
    elo_sys = YahooEloSystem()
    new = None
    for i in range(2014, 2022):
        if i > 2014:
            elo_sys.load(data_model={'weekly_elos': pd.DataFrame(new, columns=['week_0'])}, force_load=True)
        week = WEEKS.get(str(i), '0:21')
        elo_sys.run(week, True, str(i))
        elo_sys.dump(True, '_c')
        new = off_season_adjustment(elo_sys.data_model['weekly_elos'], lake, str(i + 1))


def stitch():
    last_week = None
    core_df = None
    for i in range(2014, 2022):
        name = 'weekly_elos_{}.csv'.format(i)
        df = pd.read_csv(os.path.join(os.getcwd(), 'resources', name), index_col=0)
        if last_week:
            old_cols = df.columns
            end = col_finder(old_cols, True)
            df.columns = ['week_{}'.format(j) for j in range(last_week + 1, last_week + end + 2)]
            last_week = col_finder(df.columns, True)
            core_df = core_df.merge(df, how='outer', left_index=True, right_index=True)
        else:
            last_week = col_finder(df.columns, True)
            core_df = df
    core_df.to_csv(os.path.join(os.getcwd(), 'resources', 'seasonal_elo.csv'))


def run():
    lake = fill_lake()
    scraper = run_scraper(lake)
    run_annual_elo(scraper)
    run_full_elo(lake)
    stitch()


if __name__ == "__main__":
    run()
