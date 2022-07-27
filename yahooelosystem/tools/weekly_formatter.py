import logging
import numpy as np
import pandas as pd


KEEP_COLS = ['fgm', 'fga', 'fgpct', 'ftm', 'fta', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks'
             , 'turnovers', 'true_score', 'opponent', 'week', 'roto', 'roto_rank']

ROTO_COLS = ['fgpct', 'ftpct', 'threes', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers']
FLT_COLS = ['fgpct', 'ftpct', 'score']

BAD_GUIDS = {
    'I AM A QUITTER': 'DuckHead',
    'Beepity-Boopity': 'YPMRGP6D6AZCDFMT7LTZQ5NKL4'
}

WEEK = 14
BOARD = {'0': {'matchup': {'week': '1',
   'week_start': '2021-10-19',
   'week_end': '2021-10-24',
   'status': 'postevent',
   'is_playoffs': '0',
   'is_consolation': '0',
   'is_tied': 0,
   'winner_team_key': '410.l.11456.t.10',
   'stat_winners': [{'stat_winner': {'stat_id': '5',
      'winner_team_key': '410.l.11456.t.10'}},
    {'stat_winner': {'stat_id': '8', 'winner_team_key': '410.l.11456.t.1'}},
    {'stat_winner': {'stat_id': '10', 'winner_team_key': '410.l.11456.t.1'}},
    {'stat_winner': {'stat_id': '12', 'winner_team_key': '410.l.11456.t.10'}},
    {'stat_winner': {'stat_id': '15', 'winner_team_key': '410.l.11456.t.10'}},
    {'stat_winner': {'stat_id': '16', 'winner_team_key': '410.l.11456.t.10'}},
    {'stat_winner': {'stat_id': '17', 'winner_team_key': '410.l.11456.t.10'}},
    {'stat_winner': {'stat_id': '18', 'winner_team_key': '410.l.11456.t.1'}},
    {'stat_winner': {'stat_id': '19', 'winner_team_key': '410.l.11456.t.1'}}],
   '0': {'teams': {'0': {'team': [[{'team_key': '410.l.11456.t.1'},
        {'team_id': '1'},
        {'name': 'Ball Drogo'},
        {'is_owned_by_current_login': 1},
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/1'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/fc6132fdfe640e637f18cb1e0d3c9de777a03c61737484d9b1d8b11e03efefd4.png'}}]},
        [],
        {'waiver_priority': 8},
        [],
        {'number_of_moves': '30'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '1',
            'nickname': 'rohanv',
            'guid': 'QOSB6TNJH6AZSUXHZXGSCF6KGY',
            'is_commissioner': '1',
            'is_current_login': '1',
            'image_url': 'https://s.yimg.com/ag/images/4547/23781644087_2d3dc5_64sq.jpg',
            'felo_score': '698',
            'felo_tier': 'silver'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '171/389'}},
          {'stat': {'stat_id': '5', 'value': '.440'}},
          {'stat': {'stat_id': '9007006', 'value': '58/76'}},
          {'stat': {'stat_id': '8', 'value': '.763'}},
          {'stat': {'stat_id': '10', 'value': '64'}},
          {'stat': {'stat_id': '12', 'value': '464'}},
          {'stat': {'stat_id': '15', 'value': '136'}},
          {'stat': {'stat_id': '16', 'value': '76'}},
          {'stat': {'stat_id': '17', 'value': '33'}},
          {'stat': {'stat_id': '18', 'value': '28'}},
          {'stat': {'stat_id': '19', 'value': '58'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '4'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 34}}}]},
     '1': {'team': [[{'team_key': '410.l.11456.t.10'},
        {'team_id': '10'},
        {'name': 'Bing Bong'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/10'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/5fa299772297d1aebc4103aba7fb49e75cf2524cf98c10d76b696b1f7c66f47c.png'}}]},
        [],
        {'waiver_priority': 6},
        [],
        {'number_of_moves': '3'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '10',
            'nickname': 'Alison',
            'guid': 'NIHSTHKSFAGS6M5GEP36QG4T64',
            'image_url': 'https://s.yimg.com/ag/images/4729/38216169420_b3b06b_64sq.jpg',
            'felo_score': '521',
            'felo_tier': 'bronze'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '177/370'}},
          {'stat': {'stat_id': '5', 'value': '.478'}},
          {'stat': {'stat_id': '9007006', 'value': '74/110'}},
          {'stat': {'stat_id': '8', 'value': '.673'}},
          {'stat': {'stat_id': '10', 'value': '42'}},
          {'stat': {'stat_id': '12', 'value': '470'}},
          {'stat': {'stat_id': '15', 'value': '242'}},
          {'stat': {'stat_id': '16', 'value': '123'}},
          {'stat': {'stat_id': '17', 'value': '47'}},
          {'stat': {'stat_id': '18', 'value': '13'}},
          {'stat': {'stat_id': '19', 'value': '60'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '5'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 37}}}]},
     'count': 2}}}},
 '1': {'matchup': {'week': '1',
   'week_start': '2021-10-19',
   'week_end': '2021-10-24',
   'status': 'postevent',
   'is_playoffs': '0',
   'is_consolation': '0',
   'is_tied': 0,
   'winner_team_key': '410.l.11456.t.7',
   'stat_winners': [{'stat_winner': {'stat_id': '5',
      'winner_team_key': '410.l.11456.t.7'}},
    {'stat_winner': {'stat_id': '8', 'winner_team_key': '410.l.11456.t.7'}},
    {'stat_winner': {'stat_id': '10', 'winner_team_key': '410.l.11456.t.7'}},
    {'stat_winner': {'stat_id': '12', 'winner_team_key': '410.l.11456.t.7'}},
    {'stat_winner': {'stat_id': '15', 'winner_team_key': '410.l.11456.t.7'}},
    {'stat_winner': {'stat_id': '16', 'winner_team_key': '410.l.11456.t.7'}},
    {'stat_winner': {'stat_id': '17', 'winner_team_key': '410.l.11456.t.2'}},
    {'stat_winner': {'stat_id': '18', 'winner_team_key': '410.l.11456.t.2'}},
    {'stat_winner': {'stat_id': '19', 'winner_team_key': '410.l.11456.t.2'}}],
   '0': {'teams': {'0': {'team': [[{'team_key': '410.l.11456.t.2'},
        {'team_id': '2'},
        {'name': "CJ M'Gollum"},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/2'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/643c6d7a134f63e0a8176e67a6ae635f4530681d2ad7258e56e194fa7d741f91.jpg'}}]},
        [],
        {'waiver_priority': 9},
        [],
        {'number_of_moves': '39'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '2',
            'nickname': 'Neil',
            'guid': 'YWVPE4432SD4KI54TYIBYSUY4E',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '613',
            'felo_tier': 'silver'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '186/417'}},
          {'stat': {'stat_id': '5', 'value': '.446'}},
          {'stat': {'stat_id': '9007006', 'value': '67/91'}},
          {'stat': {'stat_id': '8', 'value': '.736'}},
          {'stat': {'stat_id': '10', 'value': '49'}},
          {'stat': {'stat_id': '12', 'value': '488'}},
          {'stat': {'stat_id': '15', 'value': '246'}},
          {'stat': {'stat_id': '16', 'value': '143'}},
          {'stat': {'stat_id': '17', 'value': '47'}},
          {'stat': {'stat_id': '18', 'value': '29'}},
          {'stat': {'stat_id': '19', 'value': '79'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '3'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 42}}}]},
     '1': {'team': [[{'team_key': '410.l.11456.t.7'},
        {'team_id': '7'},
        {'name': 'Spicy T'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/7'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/594e05b51caab78865596e01e0eff4706956c821568a31a2df6e5368ebe583c3.jpg'}}]},
        [],
        {'waiver_priority': 11},
        [],
        {'number_of_moves': '26'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '7',
            'nickname': 'ravi',
            'guid': 'VWB4LBHYWJRAQ2E66SHEWFTCRI',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '804',
            'felo_tier': 'platinum'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '265/535'}},
          {'stat': {'stat_id': '5', 'value': '.495'}},
          {'stat': {'stat_id': '9007006', 'value': '93/117'}},
          {'stat': {'stat_id': '8', 'value': '.795'}},
          {'stat': {'stat_id': '10', 'value': '71'}},
          {'stat': {'stat_id': '12', 'value': '694'}},
          {'stat': {'stat_id': '15', 'value': '271'}},
          {'stat': {'stat_id': '16', 'value': '157'}},
          {'stat': {'stat_id': '17', 'value': '33'}},
          {'stat': {'stat_id': '18', 'value': '28'}},
          {'stat': {'stat_id': '19', 'value': '87'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '6'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 41}}}]},
     'count': 2}}}},
 '2': {'matchup': {'week': '1',
   'week_start': '2021-10-19',
   'week_end': '2021-10-24',
   'status': 'postevent',
   'is_playoffs': '0',
   'is_consolation': '0',
   'is_tied': 0,
   'winner_team_key': '410.l.11456.t.3',
   'stat_winners': [{'stat_winner': {'stat_id': '5',
      'winner_team_key': '410.l.11456.t.3'}},
    {'stat_winner': {'stat_id': '8', 'winner_team_key': '410.l.11456.t.3'}},
    {'stat_winner': {'stat_id': '10', 'winner_team_key': '410.l.11456.t.3'}},
    {'stat_winner': {'stat_id': '12', 'winner_team_key': '410.l.11456.t.3'}},
    {'stat_winner': {'stat_id': '15', 'winner_team_key': '410.l.11456.t.3'}},
    {'stat_winner': {'stat_id': '16', 'winner_team_key': '410.l.11456.t.5'}},
    {'stat_winner': {'stat_id': '17', 'winner_team_key': '410.l.11456.t.3'}},
    {'stat_winner': {'stat_id': '18', 'winner_team_key': '410.l.11456.t.5'}},
    {'stat_winner': {'stat_id': '19', 'winner_team_key': '410.l.11456.t.3'}}],
   '0': {'teams': {'0': {'team': [[{'team_key': '410.l.11456.t.3'},
        {'team_id': '3'},
        {'name': 'Every “DeRozan” Has Its Thorn'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/3'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://s.yimg.com/cv/apiv2/default/nba/nba_7.png'}}]},
        [],
        {'waiver_priority': 1},
        [],
        {'number_of_moves': '28'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '3',
            'nickname': 'James',
            'guid': 'PMEMCDE2SSHJ5YKGBVJZ4PI62E',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '651',
            'felo_tier': 'silver'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '193/415'}},
          {'stat': {'stat_id': '5', 'value': '.465'}},
          {'stat': {'stat_id': '9007006', 'value': '73/93'}},
          {'stat': {'stat_id': '8', 'value': '.785'}},
          {'stat': {'stat_id': '10', 'value': '52'}},
          {'stat': {'stat_id': '12', 'value': '511'}},
          {'stat': {'stat_id': '15', 'value': '186'}},
          {'stat': {'stat_id': '16', 'value': '79'}},
          {'stat': {'stat_id': '17', 'value': '44'}},
          {'stat': {'stat_id': '18', 'value': '22'}},
          {'stat': {'stat_id': '19', 'value': '64'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '7'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 38}}}]},
     '1': {'team': [[{'team_key': '410.l.11456.t.5'},
        {'team_id': '5'},
        {'name': 'Lebran Grains'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/5'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://s.yimg.com/cv/apiv2/default/nba/nba_8.png'}}]},
        [],
        {'waiver_priority': 2},
        [],
        {'number_of_moves': 0},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '5',
            'nickname': 'AlexK',
            'guid': 'NVAFN332AJMUVGCGC3CVBDWNQQ',
            'image_url': 'https://s.yimg.com/ag/images/4527/37825480750_3359d6_64sq.jpg',
            'felo_score': '538',
            'felo_tier': 'bronze'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '167/401'}},
          {'stat': {'stat_id': '5', 'value': '.416'}},
          {'stat': {'stat_id': '9007006', 'value': '97/124'}},
          {'stat': {'stat_id': '8', 'value': '.782'}},
          {'stat': {'stat_id': '10', 'value': '33'}},
          {'stat': {'stat_id': '12', 'value': '464'}},
          {'stat': {'stat_id': '15', 'value': '178'}},
          {'stat': {'stat_id': '16', 'value': '131'}},
          {'stat': {'stat_id': '17', 'value': '39'}},
          {'stat': {'stat_id': '18', 'value': '25'}},
          {'stat': {'stat_id': '19', 'value': '66'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '2'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 36}}}]},
     'count': 2}}}},
 '3': {'matchup': {'week': '1',
   'week_start': '2021-10-19',
   'week_end': '2021-10-24',
   'status': 'postevent',
   'is_playoffs': '0',
   'is_consolation': '0',
   'is_tied': 0,
   'winner_team_key': '410.l.11456.t.11',
   'stat_winners': [{'stat_winner': {'stat_id': '5',
      'winner_team_key': '410.l.11456.t.4'}},
    {'stat_winner': {'stat_id': '8', 'winner_team_key': '410.l.11456.t.11'}},
    {'stat_winner': {'stat_id': '10', 'winner_team_key': '410.l.11456.t.11'}},
    {'stat_winner': {'stat_id': '12', 'winner_team_key': '410.l.11456.t.11'}},
    {'stat_winner': {'stat_id': '15', 'winner_team_key': '410.l.11456.t.4'}},
    {'stat_winner': {'stat_id': '16', 'winner_team_key': '410.l.11456.t.11'}},
    {'stat_winner': {'stat_id': '17', 'winner_team_key': '410.l.11456.t.11'}},
    {'stat_winner': {'stat_id': '18', 'winner_team_key': '410.l.11456.t.4'}},
    {'stat_winner': {'stat_id': '19', 'winner_team_key': '410.l.11456.t.4'}}],
   '0': {'teams': {'0': {'team': [[{'team_key': '410.l.11456.t.4'},
        {'team_id': '4'},
        {'name': 'Kennard-ly Wait'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/4'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/3d50711b8229c509a0eb840444e1f22a6b541b492240ffd206cf8b02ad185094.jpg'}}]},
        [],
        {'waiver_priority': 10},
        [],
        {'number_of_moves': '28'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '4',
            'nickname': 'Sahil',
            'guid': 'VFTMFPVMSCHKRTIILW7BM5UIGA',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '810',
            'felo_tier': 'platinum'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '203/406'}},
          {'stat': {'stat_id': '5', 'value': '.500'}},
          {'stat': {'stat_id': '9007006', 'value': '82/104'}},
          {'stat': {'stat_id': '8', 'value': '.788'}},
          {'stat': {'stat_id': '10', 'value': '42'}},
          {'stat': {'stat_id': '12', 'value': '530'}},
          {'stat': {'stat_id': '15', 'value': '222'}},
          {'stat': {'stat_id': '16', 'value': '79'}},
          {'stat': {'stat_id': '17', 'value': '23'}},
          {'stat': {'stat_id': '18', 'value': '27'}},
          {'stat': {'stat_id': '19', 'value': '64'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '4'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 36}}}]},
     '1': {'team': [[{'team_key': '410.l.11456.t.11'},
        {'team_id': '11'},
        {'name': 'The Bealtles'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/11'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/7da47d328489c3977dde03a6a94ae2a525d07d931c89487cecd2bfecd15962be.jpg'}}]},
        [],
        {'waiver_priority': 12},
        [],
        {'number_of_moves': '57'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '3'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '11',
            'nickname': 'Aaron',
            'guid': 'NZ2X6OUUEORPJ3ZFHCL4EBEU6J',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '690',
            'felo_tier': 'silver'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '217/506'}},
          {'stat': {'stat_id': '5', 'value': '.429'}},
          {'stat': {'stat_id': '9007006', 'value': '86/109'}},
          {'stat': {'stat_id': '8', 'value': '.789'}},
          {'stat': {'stat_id': '10', 'value': '62'}},
          {'stat': {'stat_id': '12', 'value': '582'}},
          {'stat': {'stat_id': '15', 'value': '190'}},
          {'stat': {'stat_id': '16', 'value': '111'}},
          {'stat': {'stat_id': '17', 'value': '39'}},
          {'stat': {'stat_id': '18', 'value': '20'}},
          {'stat': {'stat_id': '19', 'value': '72'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '5'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 38}}}]},
     'count': 2}}}},
 '4': {'matchup': {'week': '1',
   'week_start': '2021-10-19',
   'week_end': '2021-10-24',
   'status': 'postevent',
   'is_playoffs': '0',
   'is_consolation': '0',
   'is_tied': 0,
   'winner_team_key': '410.l.11456.t.6',
   'stat_winners': [{'stat_winner': {'stat_id': '5',
      'winner_team_key': '410.l.11456.t.6'}},
    {'stat_winner': {'stat_id': '8', 'winner_team_key': '410.l.11456.t.12'}},
    {'stat_winner': {'stat_id': '10', 'winner_team_key': '410.l.11456.t.6'}},
    {'stat_winner': {'stat_id': '12', 'winner_team_key': '410.l.11456.t.6'}},
    {'stat_winner': {'stat_id': '15', 'winner_team_key': '410.l.11456.t.6'}},
    {'stat_winner': {'stat_id': '16', 'winner_team_key': '410.l.11456.t.6'}},
    {'stat_winner': {'stat_id': '17', 'winner_team_key': '410.l.11456.t.6'}},
    {'stat_winner': {'stat_id': '18', 'winner_team_key': '410.l.11456.t.6'}},
    {'stat_winner': {'stat_id': '19', 'winner_team_key': '410.l.11456.t.12'}}],
   '0': {'teams': {'0': {'team': [[{'team_key': '410.l.11456.t.6'},
        {'team_id': '6'},
        {'name': 'SexLand'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/6'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/30368441810_408ac5a86b.jpg'}}]},
        [],
        {'waiver_priority': 7},
        [],
        {'number_of_moves': '5'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '6',
            'nickname': 'Alex',
            'guid': '5RADOHUTBULBXBWUKY4J275JZE',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '761',
            'felo_tier': 'gold'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '186/379'}},
          {'stat': {'stat_id': '5', 'value': '.491'}},
          {'stat': {'stat_id': '9007006', 'value': '53/74'}},
          {'stat': {'stat_id': '8', 'value': '.716'}},
          {'stat': {'stat_id': '10', 'value': '61'}},
          {'stat': {'stat_id': '12', 'value': '486'}},
          {'stat': {'stat_id': '15', 'value': '187'}},
          {'stat': {'stat_id': '16', 'value': '101'}},
          {'stat': {'stat_id': '17', 'value': '32'}},
          {'stat': {'stat_id': '18', 'value': '26'}},
          {'stat': {'stat_id': '19', 'value': '62'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '7'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 36}}}]},
     '1': {'team': [[{'team_key': '410.l.11456.t.12'},
        {'team_id': '12'},
        {'name': 'Globo Gym Purple Cobras'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/12'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/31752c08aa1e13935d25a330b3e69ba461702197e023d77fc9e9d91160052e47.png'}}]},
        [],
        {'waiver_priority': 3},
        [],
        {'number_of_moves': '1'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '12',
            'nickname': 'James',
            'guid': 'CCYS62GDCHMWDZZZQDTB35DTRE',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '553',
            'felo_tier': 'bronze'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '145/326'}},
          {'stat': {'stat_id': '5', 'value': '.445'}},
          {'stat': {'stat_id': '9007006', 'value': '54/63'}},
          {'stat': {'stat_id': '8', 'value': '.857'}},
          {'stat': {'stat_id': '10', 'value': '46'}},
          {'stat': {'stat_id': '12', 'value': '390'}},
          {'stat': {'stat_id': '15', 'value': '176'}},
          {'stat': {'stat_id': '16', 'value': '96'}},
          {'stat': {'stat_id': '17', 'value': '30'}},
          {'stat': {'stat_id': '18', 'value': '19'}},
          {'stat': {'stat_id': '19', 'value': '57'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '2'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 27}}}]},
     'count': 2}}}},
 '5': {'matchup': {'week': '1',
   'week_start': '2021-10-19',
   'week_end': '2021-10-24',
   'status': 'postevent',
   'is_playoffs': '0',
   'is_consolation': '0',
   'is_tied': 0,
   'winner_team_key': '410.l.11456.t.8',
   'stat_winners': [{'stat_winner': {'stat_id': '5',
      'winner_team_key': '410.l.11456.t.8'}},
    {'stat_winner': {'stat_id': '8', 'winner_team_key': '410.l.11456.t.8'}},
    {'stat_winner': {'stat_id': '10', 'winner_team_key': '410.l.11456.t.8'}},
    {'stat_winner': {'stat_id': '12', 'winner_team_key': '410.l.11456.t.8'}},
    {'stat_winner': {'stat_id': '15', 'winner_team_key': '410.l.11456.t.8'}},
    {'stat_winner': {'stat_id': '16', 'winner_team_key': '410.l.11456.t.9'}},
    {'stat_winner': {'stat_id': '17', 'winner_team_key': '410.l.11456.t.9'}},
    {'stat_winner': {'stat_id': '18', 'winner_team_key': '410.l.11456.t.9'}},
    {'stat_winner': {'stat_id': '19', 'winner_team_key': '410.l.11456.t.9'}}],
   '0': {'teams': {'0': {'team': [[{'team_key': '410.l.11456.t.8'},
        {'team_id': '8'},
        {'name': 'The Young Bane Rises'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/8'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/b21a6ee5662bc4b7453d08adac993c5fbc88476a6e38f9ea5273336545c9efc6.png'}}]},
        [],
        {'waiver_priority': 5},
        [],
        {'number_of_moves': 0},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '0'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '8',
            'nickname': 'Sterling',
            'guid': 'VOKZZSOK4ZQXCRZS4X3C6A2UKM',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '592',
            'felo_tier': 'bronze'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '217/459'}},
          {'stat': {'stat_id': '5', 'value': '.473'}},
          {'stat': {'stat_id': '9007006', 'value': '75/96'}},
          {'stat': {'stat_id': '8', 'value': '.781'}},
          {'stat': {'stat_id': '10', 'value': '72'}},
          {'stat': {'stat_id': '12', 'value': '581'}},
          {'stat': {'stat_id': '15', 'value': '262'}},
          {'stat': {'stat_id': '16', 'value': '105'}},
          {'stat': {'stat_id': '17', 'value': '37'}},
          {'stat': {'stat_id': '18', 'value': '20'}},
          {'stat': {'stat_id': '19', 'value': '73'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '5'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 40}}}]},
     '1': {'team': [[{'team_key': '410.l.11456.t.9'},
        {'team_id': '9'},
        {'name': 'The Jive Turkeys'},
        [],
        {'url': 'https://basketball.fantasysports.yahoo.com/nba/11456/9'},
        {'team_logos': [{'team_logo': {'size': 'large',
            'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/57363467244_7003a0.jpg'}}]},
        [],
        {'waiver_priority': 4},
        [],
        {'number_of_moves': '50'},
        {'number_of_trades': 0},
        {'roster_adds': {'coverage_type': 'week',
          'coverage_value': 11,
          'value': '2'}},
        [],
        {'league_scoring_type': 'headone'},
        [],
        [],
        {'has_draft_grade': 0},
        [],
        [],
        {'managers': [{'manager': {'manager_id': '9',
            'nickname': 'John',
            'guid': 'LNRT67BZLFW4H3EUP2TDHOG74M',
            'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg',
            'felo_score': '849',
            'felo_tier': 'platinum'}}]}],
       {'team_stats': {'coverage_type': 'week',
         'week': '1',
         'stats': [{'stat': {'stat_id': '9004003', 'value': '187/446'}},
          {'stat': {'stat_id': '5', 'value': '.419'}},
          {'stat': {'stat_id': '9007006', 'value': '66/88'}},
          {'stat': {'stat_id': '8', 'value': '.750'}},
          {'stat': {'stat_id': '10', 'value': '67'}},
          {'stat': {'stat_id': '12', 'value': '507'}},
          {'stat': {'stat_id': '15', 'value': '204'}},
          {'stat': {'stat_id': '16', 'value': '121'}},
          {'stat': {'stat_id': '17', 'value': '40'}},
          {'stat': {'stat_id': '18', 'value': '28'}},
          {'stat': {'stat_id': '19', 'value': '67'}}]},
        'team_points': {'coverage_type': 'week', 'week': '1', 'total': '4'},
        'team_remaining_games': {'coverage_type': 'week',
         'week': '1',
         'total': {'remaining_games': 0,
          'live_games': 0,
          'completed_games': 41}}}]},
     'count': 2}}}},
 'count': 6}

STAT_MAP = {
    '9004003': 'fg',
    '9007006': 'ft',
    '10': 'threes',
    '12': 'points',
    '15': 'rebounds',
    '16': 'assists',
    '17': 'steals',
    '18': 'blocks',
    '19': 'turnovers'
}

_logger = logging.getLogger(__file__)


class WeeklyFormatter:
    weeks = dict()
    win_loss_rows = dict()
    matchup_rows = list()

    def __init__(self, summaries=False):
        self.summaries = summaries

    @staticmethod
    def _stat_updater(stat):
        res = dict()
        name = STAT_MAP.get(stat['stat_id'])
        if name:
            if name[0] == 'f':
                if stat['value'] == '/':
                    buckets = {
                        'm': 0,
                        'a': 0,
                        'pct': .5
                    }
                else:
                    v = stat['value'].split('/')
                    buckets = {
                        'm': int(v[0]),
                        'a': int(v[1]),
                        'pct': int(v[0]) / int(v[1])
                    }
                for k, v in buckets.items():
                    res.update({name + k: v})
            else:
                res.update({name: stat['value']})
        return res

    @staticmethod
    def _add_roto(scoreboard):
        stats = []
        for col in ROTO_COLS:
            array = scoreboard[col].values
            temp = array.argsort()
            ranks = np.empty_like(temp)
            ranks[temp] = np.arange(len(array))
            if col == 'turnovers':
                ranks = max(ranks) - ranks
            ranks += 1
            stats.append(ranks)
        rotos = np.array(stats).sum(axis=0)
        scoreboard['roto'] = rotos
        temp = rotos.argsort()
        ranks = np.empty_like(temp)
        ranks[temp] = np.arange(len(rotos) - 1, -1, -1)
        scoreboard['roto_rank'] = ranks + 1
        return scoreboard

    def _create_cat_df(self, weekly_frame):
        weekly_frame['true_score'] = 0.0
        scored = set()
        for team in weekly_frame.index:
            if team not in scored:
                home = weekly_frame.loc[team]
                away = home.opponent
#                 _logger.info('Fixing scores for {home} and {away} for week {week}'.format(home=team, away=away,
#                                                                                           week=week))
                home_score = home.score * 1.0
                try:
                    away_score = weekly_frame.loc[away].score * 1.0
                except KeyError:
                    away_score = 0
                except Exception as e:
                    raise e
                diff = (9 - home_score - away_score) / 2
                home_score += diff
                away_score += diff
                home_score /= 9
                away_score /= 9
                weekly_frame.loc[team, 'true_score'] = home_score
                weekly_frame.loc[away, 'true_score'] = away_score
                scored.add(team)
                scored.add(away)
#                 _logger.info(
#                     'Fixed scores for {home} and {away} for week {week}'.format(home=team, away=away, week=week))

        return self._add_roto(weekly_frame)

    @staticmethod
    def _create_points_df(weekly_frame):
        scored = set()
        for home in weekly_frame.index:
            if home not in scored:
                home_atts = weekly_frame.loc[home]
                away = home_atts.opponent
#                 _logger.info('Fixing scores for {home} and {away} for week {week}'.format(home=team, away=away,
#                                                                                           week=week))
                home_score = home_atts.score
                try:
                    away_score = weekly_frame.loc[away].score
                except KeyError:
                    away_score = 0
                except Exception as e:
                    raise e
                home_score = home_score/(home_score + away_score)
                away_score = 1 - home_score
                weekly_frame.loc[home, 'true_score'] = home_score
                weekly_frame.loc[away, 'true_score'] = away_score
                scored.add(home)
                scored.add(away)
#                 _logger.info(
#                     'Fixed scores for {home} and {away} for week {week}'.format(home=team, away=away, week=week))

        return weekly_frame

    def create_df(self, week):
        scoreboard = self.weeks[str(week)]
        weekly_frame = pd.DataFrame.from_dict(scoreboard, orient='index')
        weekly_frame['true_score'] = 0.0
        if weekly_frame.shape[1] == 3:
            return self._create_points_df(weekly_frame)
        else:
            return self._create_cat_df(weekly_frame)

    @staticmethod
    def _get_guid(team):
        for d in team[0]:
            if isinstance(d, dict):
                name = d.get('name')
                if name:
                    guid_check = BAD_GUIDS.get(name)
                    if guid_check:
                        return BAD_GUIDS[name]
                res = d.get('managers')
                if res:
                    return res[0]['manager']['guid']

    def _get_stats(self, team):
        stat_list = team[1]['team_stats']['stats']
        res = dict()
        for stat in stat_list:
            res.update(self._stat_updater(stat['stat']))
        return res

    @staticmethod
    def _get_team_key(team):
        for d in team[0]:
            if isinstance(d, dict):
                res = d.get('team_key')
                if res:
                    return res

    def _create_win_loss_rows(self, team0, team1, winner):
        return {
            self._get_guid(team0): int(winner == self._get_team_key(team0)),
            self._get_guid(team1): int(winner == self._get_team_key(team1))
        }

    def _create_matchup_rows(self, team0, team1):
        pass

    def _create_weekly_df_rows(self, team0, team1):
        stat0 = self._get_stats(team0)
        stat1 = self._get_stats(team1)

        stat0.update({
            'opponent': self._get_guid(team1),
            'score': float(team0[1]['team_points']['total'])
        })
        stat1.update({
            'opponent': self._get_guid(team0),
            'score': float(team1[1]['team_points']['total'])
        })

        return {
            self._get_guid(team0): stat0,
            self._get_guid(team1): stat1
        }

    def ingest(self, scoreboard, week):
        weekly_dict = dict()
        win_loss_rows = dict()
        matchup_rows = list()
        for event in scoreboard.values():
            if isinstance(event, int):
                break
            matchup = event['matchup']
            if matchup['status'] == 'preevent':
                pass
            elif matchup['status'] in {'midevent', 'postevent'}:
                teams = matchup['0']['teams']
                team0 = teams['0']['team']
                team1 = teams['1']['team']

                weekly_dict.update(self._create_weekly_df_rows(team0, team1))
                if self.summaries:
                    winner = matchup['winner_team_key']
                    win_loss_rows.update(self._create_win_loss_rows(team0, team1, winner))
            else:
                raise ValueError

        self.weeks.update({str(week): weekly_dict})
        if self.summaries:
            self.win_loss_rows.update({'week_{}'.format(week): win_loss_rows})
            self.matchup_rows += matchup_rows


if __name__ == '__main__':
    frm = WeeklyFormatter()
    frm.ingest(BOARD, WEEK)
    print('done')
