from yahoo_tools.yahoo_table_scraper import YahooTableScraper
from yahoo_tools.weekly_formatter import WeeklyFormatter
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

    def __init__(self, league, week, players):
        self.scraper = YahooTableScraper(league, week, players)
        self.formatter = WeeklyFormatter()
        pass

    def _scrape(self):
        self.scraper.run()

    def _format(self, scraper):
        self.formatter.run(scraper)

    def run(self):
        self._scrape()
        self._format(self.scraper)
        self._elo()

        pass


if __name__ == "__main__":
    scraper = YahooTableScraper(LEAGUE, WEEK, PLAYERS)