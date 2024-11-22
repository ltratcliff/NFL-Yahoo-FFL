import pandas as pd
from yahoo_oauth import OAuth2
import json
from json import dumps
import datetime
import requests
import logging

logging.getLogger('yahoo_oauth').setLevel(logging.INFO)

oauth = OAuth2(None, None, from_file='./auth/oauth2yahoo.json')
if not oauth.token_is_valid():
    oauth.refresh_access_token()

league_id = "466034"


def UpdateYahooLeagueInfo():
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/game/nfl'
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()
    with open('YahooGameInfo.json', 'w') as outfile:
        json.dump(r, outfile)

    game_key = r['fantasy_content']['game'][0]['game_key']  # game key as type-string
    return game_key


def UpdateScoreboards(game_key):
    week = GetGameWeek()
    url = f'https://fantasysports.yahooapis.com/fantasy/v2/league/{game_key}.l.{league_id}/scoreboard;week={str(week)}'
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()
    file_name = 'scoreboard.json'
    with open(f'{file_name}', 'w') as outfile:
        json.dump(r, outfile)
    PrintScores(r)
    return

def GetGameWeek():
    today = datetime.datetime.now()
    today = today.replace(tzinfo=datetime.timezone.utc)
    r = requests.get("http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/calendar/ondays?lang=en&region=us")
    data = r.json()
    for i in range(0,17):
        start = datetime.datetime.fromisoformat(data['sections'][1]['entries'][i]['startDate'])
        end = datetime.datetime.fromisoformat(data['sections'][1]['entries'][i]['endDate'])
        if start <= today <= end:
            return data['sections'][1]['entries'][i]['value']

def PrintScores(scores):
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
        print(f"{team1_name:26} {team1_score} - {team2_score} {team2_name:20}")


def main():
    game_key = UpdateYahooLeagueInfo()
    UpdateScoreboards(game_key)

if __name__ == "__main__":
    main()
