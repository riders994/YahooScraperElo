from setuptools import setup, find_packages

setup(
    name="YahooScraperElo",
    version='2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pandas==1.0.0',
        'YahooScrapingTools @ git+https://github.com/riders994/YahooScrapingTools.git@v2',
    ],
    python_requires='>=3',
)
