import json
import os
import pandas as pd
from yahooelosystem import YahooEloSystem
from yahooelosystem.tools import YahooScraper

LAKE = {
    'sports', 'leagues', 'players', 'names'
}

WEEKS = {
    '2021': '0:17',
    '2020': '0:17',
    '2019': '0:20',
    '2016': '0:19',
    '2015': '0:20',
    '2014': '0:22'
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
    for i in range(-1, -9, -1):
        scraper.pick_league(i)
        scraper.scan_league()
    return scraper


def run_annual_elo(scraper):
    elo_sys = YahooEloSystem(scraper)
    for i in range(2014, 2022):
        year = str(i)
        weeks = WEEKS.get(year) or '0:21'
        elo_sys.run(weeks, True, year)
        elo_sys.dump(True)


def off_season_adjustment(last_season, lake, year):
    dename = {v: k for k, v in lake['names'].items()}
    final_elos = last_season.rename(index=dename)['week_0'].copy()
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
    scale = (total/num)/1500
    final_elos[both] = (final_elos[both] * scale - 1500) * .4 + 1500
    final_elos.append(pd.Series(newbies))
    return final_elos


def run_full_elo(lake):
    elo_sys = YahooEloSystem()
    new = None
    for i in range(2014, 2022):
        if i > 2014:
            elo_sys.load({'weekly_elos': new})
        week = WEEKS.get(str(i), '0:21')
        elo_sys.run(week, True, str(i))
        elo_sys.dump(True, '_c')
        new = off_season_adjustment(elo_sys.data_model['weekly_elos'], lake, str(i + 1))


def run():
    lake = fill_lake()
    scraper = run_scraper(lake)
    run_annual_elo(scraper)
    run_full_elo(lake)


if __name__ == "__main__":
    run()
