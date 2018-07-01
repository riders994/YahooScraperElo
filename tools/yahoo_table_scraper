from selenium import webdriver
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
        print('Starting Job')
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
                print('Fetching game at url: ' + url)
                self.driver.get(url)
                print('connecting')
                elem = self.driver.find_elements_by_xpath(XPATH)
                print('Connected')
                for el in elem:
                    print('Grab Player')
                    stats = el.text.split('\n')
                    player_id = stats[0]
                    self.player_stats[player_id] = stats[1:]
                    crawled.add(player_id)
                    print('Done Grabbing')




    def run(self):
        self._connect()
        self._crawl()


if __name__ == "__main__":
    s = YahooTableScraper(LEAGUE, 1, PLAYERS)
    print('boop')
    s.run()
    print('boop')
    for p, i in s.player_stats.items():
        print(p)
        print(i)

    print('boop')
