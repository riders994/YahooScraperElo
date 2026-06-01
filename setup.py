from setuptools import setup, find_packages

setup(
    name="YahooScraperElo",
    version='2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pandas==3.0.3',
        'yahoo_fantasy_api==2.12.3',
        'numpy==2.4.6',
    ],
    python_requires='>=3',
)
