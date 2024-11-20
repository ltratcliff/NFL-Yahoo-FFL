import pandas as pd
from yahoo_oauth import OAuth2
import json
from json import dumps
import datetime
import requests

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
    with open(f'/tmp/{file_name}', 'w') as outfile:
        json.dump(r, outfile)
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


def main():
    game_key = UpdateYahooLeagueInfo()
    UpdateScoreboards(game_key)

if __name__ == "__main__":
    main()
