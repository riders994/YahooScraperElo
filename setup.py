from setuptools import setup, find_packages

setup(
    name="YahooScraperElo",
    version='2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'objectpath', 'pytz', 'yahoo_oauth', 'docopt', 'yahoo_fantasy_api', 'YahooScrapingTools'
    ],
    dependency_links=[
      'git+https://github.com/riders994/YahooScrapingTools.git#egg=YahooScrapingTools-v1'
    ],
    python_requires='>=3',
)
