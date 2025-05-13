import requests
from nhl import nhlApi

nhl = nhlApi()
def getTeams():
    allTeamsPlaying = nhl.getGamesForDate('2024-10-22')
    homeTeams = [(game['homeTeam']['id'],game['homeTeam']['commonName']['default'],game['homeTeam']['abbrev'],game['homeTeam']['logo'],game['homeTeam']['darkLogo'],game['homeTeam']['placeName']['default'],) for game in allTeamsPlaying]
    awayTeams = [(game['awayTeam']['id'],game['awayTeam']['commonName']['default'],game['awayTeam']['abbrev'],game['awayTeam']['logo'],game['awayTeam']['darkLogo'],game['awayTeam']['placeName']['default'],) for game in allTeamsPlaying]
    return homeTeams + awayTeams