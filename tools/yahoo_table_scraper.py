from selenium import webdriver
import logging
import pickle

URL_PART_1 = "https://basketball.fantasysports.yahoo.com/nba/{league}/matchup?week="
URL_PART_2 = "{week}&module=matchup&mid1="
LEAGUE = '5726'
XPATH = '//section[@id="matchup-wall-header"]/table/tbody/tr'
PLAYER_PICKLE_PATH = './players.pkl'
PLAYERS = dict()
WEEK = '1'

with open(PLAYER_PICKLE_PATH, "rb") as file:
    players = pickle.load(file)
for i, p in enumerate(players):
    PLAYERS[i] = p


class YahooTableScraper:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.getLevelName('INFO'))
    logger.info('Starting Job')
    player_stats = dict()

    def __init__(self, league, players):
        self.url = URL_PART_1.format(league=league)
        self.players = players

        pass

    def _connect(self):
        self.driver = webdriver.Firefox()

    def _crawl(self, week):
        crawled = set()
        url_piece = self.url + URL_PART_2.format(week=week)
        for i in range(0,11):
            if self.players[i] not in crawled:
                url = url_piece + str(i)
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




    def run(self, week):
        self._connect()
        self._crawl(week)


if __name__ == "__main__":
    log = logging.getLogger('Test')
    s = YahooTableScraper(LEAGUE, PLAYERS)
    log.info('boop')
    s.run(WEEK)
    log.info('boop')
    for p, i in s.player_stats.items():
        log.info(p)
        log.info(i)
    with open('player_stats.pkl', "wb") as file:
        pickle.dump(s.player_stats, file)
    log.info('boop')
