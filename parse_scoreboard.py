import json

scores = json.loads(open('scoreboard.json').read())
matchups = scores['fantasy_content']['league'][1]['scoreboard']['0']['matchups'].keys()

for i in matchups:
    if i == 'count':
        continue
    match = scores['fantasy_content']['league'][1]['scoreboard']['0']['matchups'][i]
    team1 = match['matchup']['0']['teams']['0']
    team2 = match['matchup']['0']['teams']['1']
    team1_name = team1['team'][0][2]['name']
    team2_name = team2['team'][0][2]['name']
    team1_score = team1['team'][1]['team_points']['total']
    team2_score = team2['team'][1]['team_points']['total']
    print(f"{team1_name} {team1_score} - {team2_score} {team2_name}")