from nhl import nhlApi
from model import xGModel
from datetime import date
import pandas
nhl = nhlApi()
model = xGModel()


def main():

    todayGames = nhl.getGamesForDate(date.today().strftime("2025-01-28"))
    gameIds = [game["id"] for game in todayGames]
    print(len(gameIds))
    for gameId in gameIds:
        game = nhl.getPlayByPlayData(gameId)
        #505: goal, 506: shot-on-goal, 507: missed-shot
        shots = [event for event in game["plays"] if model.eventIsShot(event["typeCode"])]
        for shot in shots:
            shot['xG'] = model.gradeShot(game, shots[0])
            shot['gameId'] = game['id']
            
    print(len(shots))
    print(shots)

if __name__ == '__main__':
    main()