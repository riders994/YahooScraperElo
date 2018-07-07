from selenium import webdriver
import logging
import pickle

URL = "https://basketball.fantasysports.yahoo.com/nba/{league}/matchup?week={week}&module=matchup&mid1="
LEAGUE = '10560'
XPATH = '//section[@id="matchup-wall-header"]/table/tbody/tr'
PLAYER_PICKLE_PATH = './players.pkl'
PLAYERS = dict()

with open(PLAYER_PICKLE_PATH, "rb") as file:
    players = pickle.load(file)
for i, p in enumerate(players):
    PLAYERS[i] = p


class YahooTableScraper:
    def __init__(self, league, week, players):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Starting Job')
        self.player_stats = dict()
        self.url = URL.format(league=league, week=week)
        self.players = players

        pass

    def _connect(self):
        self.driver = webdriver.Firefox()

    def _crawl(self):
        crawled = set()
        for i in range(0,11):
            if self.players[i] not in crawled:
                url = self.url + str(i)
                self.logger.info('Fetching game at url: ' + url)
                self.driver.get(url)
                self.logger.info('connecting')
                elem = self.driver.find_elements_by_xpath(XPATH)
                self.logger.info('Connected')
                teams = [el.text.split('\n') for el in elem]
                for i, el in enumerate(teams):
                    self.logger.info('Grab Player')
                    opp = teams[abs(i - 1)]
                    stats = el
                    stats.append(opp[0])
                    player_id = stats[0]
                    self.player_stats[player_id] = stats[1:]
                    crawled.add(player_id)
                    self.logger.info('Done Grabbing')




    def run(self):
        self._connect()
        self._crawl()


if __name__ == "__main__":
    log = logging.getLogger('Test')
    s = YahooTableScraper(LEAGUE, 1, PLAYERS)
    log.info('boop')
    s.run()
    log.info('boop')
    for p, i in s.player_stats.items():
        log.info(p)
        log.info(i)
    with open('player_stats.pkl', "wb") as file:
        pickle.dump(s.player_stats, file)
    log.info('boop')
