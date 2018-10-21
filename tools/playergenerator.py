from selenium import webdriver
import logging
import pickle

URL = "https://basketball.fantasysports.yahoo.com/nba/{league}/matchup?week=1&module=matchup&mid1="
LEAGUE = '5726'
XPATH = '//section[@id="matchup-wall-header"]/table/tbody/tr'
PLAYER_PICKLE_PATH = './players.pkl'


class PlayerGenerator:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.getLevelName('INFO'))
    logger.info('Starting Job')
    player_nums = {0: '-/-'}

    def __init__(self, league):
        self.url = URL.format(league=league)

    def _connect(self):
        self.driver = webdriver.Firefox()

    def _scrape(self):
        for i in range(0, 11):
            url = self.url + str(i)
            self.driver.get(url)
            elem = self.driver.find_elements_by_xpath(XPATH)
            team = elem[0].text.split('\n')
            print(team)
            self.player_nums[i] = team[0]

    def _write(self):
        with open(PLAYER_PICKLE_PATH, 'wb') as file:
            pickle.dump(self.player_nums, file)

    def run(self):
        self._connect()
        self._scrape()
        self._write()

if __name__ == '__main__':
    pg = PlayerGenerator(LEAGUE)
    pg.run()