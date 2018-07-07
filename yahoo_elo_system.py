from tools.yahoo_table_scraper import YahooTableScraper
from tools.weekly_formatter import WeeklyFormatter
from tools.elo_calculator import EloCalc
import argparse
import pickle

parser = argparse.ArgumentParser()

LEAGUE = '10560'
WEEK = '1'
PLAYER_PICKLE_PATH = './players.pkl'
PLAYERS = dict()

with open(PLAYER_PICKLE_PATH, "rb") as pkl:
    players = pickle.load(pkl)
for i, p in enumerate(players):
    PLAYERS[i] = p

def week_formatter(week):
    s = week.split(':')
    if len(s) - 1:
        return range(int(s[0], int(s[-1]))), True
    else:
        return week, False


class YahooEloSystem:

    def __init__(self, league, week, players, stats=False):
        self.league = league
        self.players = players
        self.week, self.multi= week_formatter(week)
        self.stats = stats
        self.formatter = WeeklyFormatter()


    def _scrape(self):
        self.scraper = YahooTableScraper(self.league, self.week, self.players)
        self.scraper.run()

    def _format(self, scraper):
        self.formatter.run(scraper)

    def _elo(self):
<<<<<<< HEAD
        self.elo_calc.run(self.formatter.frame)

    def run(self):
        self._scrape()
        self._format(self.scraper)
        self._elo()
        pass
=======
        self.elo_calc = EloCalc(WEEK, self.stats)
        self.elo_calc.run(self.formatter.frame)

    def run_multiple(self):


    def run(self):
        if self.multi:
            self.run_multiple()
        else:
            self._scrape()
            self._format(self.scraper)
            self._elo()
>>>>>>> tools-elo


if __name__ == "__main__":
    sys = YahooTableScraper(LEAGUE, WEEK, PLAYERS)
    sys.run()
