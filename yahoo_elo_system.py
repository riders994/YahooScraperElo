from tools.yahoo_table_scraper import YahooTableScraper
from tools.weekly_formatter import WeeklyFormatter
from tools.elo_calculator import EloCalc
import argparse

parser = argparse.ArgumentParser()

LEAGUE = '10560'
WEEK = '1'
PLAYER_PICKLE_PATH = './players.pkl'
PLAYERS = dict()

with open(PLAYER_PICKLE_PATH, "rb") as pkl:
    players = pickle.load(pkl)
for i, p in enumerate(players):
    PLAYERS[i] = p


class YahooEloSystem:

    def __init__(self, league, week, players, stats=False):
        self.scraper = YahooTableScraper(league, week, players)
        self.formatter = WeeklyFormatter()
        self.elo_calc = EloCalc(WEEK, stats)
        pass

    def _scrape(self):
        self.scraper.run()

    def _format(self, scraper):
        self.formatter.run(scraper)

    def _elo(self):

    def run(self):
        self._scrape()
        self._format(self.scraper)
        self._elo()

        pass


if __name__ == "__main__":
    sys = YahooTableScraper(LEAGUE, WEEK, PLAYERS)
    sys.run()