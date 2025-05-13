from nhl import nhlApi
from model import xGModel
from datetime import date
from consts import situationCodeMap, shotTypes
import requests
import uuid
import api_handler
nhl = nhlApi()
model = xGModel()

def writeData():
    todayGames = nhl.getGamesForDate(date.today().strftime("2025-01-28"))
    gameIds = [game["id"] for game in todayGames]
    print(len(gameIds))
    pbp = []
    dailyPlays = []
    dailyShots = []
    dailyGoals = []
    dailyxG = []
    dailyAdjustments = []
    dailyPlayers = []
    for gameId in gameIds:
        game = nhl.getPlayByPlayData(gameId)
        dailyPlayers += [
            {'id': player['playerId'], 
             'firstName': player['firstName']['default'], 
             'lastName': player['lastName']['default'], 
             'sweaterNumber': player['sweaterNumber'], 
             'positionCode': player['positionCode'], 
             'headshot': player['headshot']
             } for player in game['rosterSpots']]
        pbp.append(game)
        # #505: goal, 506: shot-on-goal, 507: missed-shot, 508: blocked-shot
        for play in game["plays"]:
            play['id'] = f'{str(gameId)}-{str(play['eventId'])}'
            play['gameId'] = game['id']
            dailyPlays.append(play)
            if model.eventIsShot(play["typeCode"]) or model.eventIsGoal(play["typeCode"]):
                shot = play['details']
                if play['situationCode'] not in situationCodeMap['home'].keys() or shot['shotType'] not in shotTypes:
                    continue
                xG, adjustments = model.gradeShot(game, play)

                xG = {"xG": xG}
                xG['id'] = str(uuid.uuid4())
                #TODO: make this real
                xG['modelId'] = "basic-free"
                xG['shotId'] = play['id']
                dailyxG.append(xG)

                dailyAdjustments += [{'id': str(uuid.uuid4()), 'xGId': xG['id'], **adjustment} for adjustment in adjustments]

                shot['playId'] = play['id']
                if model.eventIsGoal(play["typeCode"]):
                    dailyGoals.append(shot)
                elif model.eventIsShot(play["typeCode"]):
                    dailyShots.append(shot)

    # print('shots:', dailyShots)
    # print('goals:', dailyGoals)
    # print('xG', dailyxG)
    # print('adj', dailyAdjustments)

    try:
        api_handler.bulkPostPlayers(dailyPlayers)
        api_handler.bulkPostGames([{k: p[k] for k in p.keys() - {'plays', 'rosterSpots'}} for p in pbp])
        api_handler.bulkPostPlays(dailyPlays)
        api_handler.bulkPostShots(dailyShots)
        api_handler.bulkPostGoals(dailyGoals)

    except Exception as e:
        print('AERROR', e)

# def getActiveModels():
#     pass
# def writexG():

#     api_handler.bulkPostxG(dailyxG)
#     api_handler.bulkPostAdjustments(dailyAdjustments)
#     pass