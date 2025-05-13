import requests, json

baseUrl = 'http://localhost:5000/'

def bulkPostGames(games):
    r = requests.post(baseUrl+'game/bulk', json.dumps({"games": games}), headers={'Content-Type': 'application/json'})
    return r

def bulkPostPlays(plays):
    r = requests.post(baseUrl+'play/bulk', json.dumps({"plays": plays}), headers={'Content-Type': 'application/json'})
    return r

def bulkPostShots(shots):
    r = requests.post(baseUrl+'shot/bulk', json.dumps({"shots": shots}), headers={'Content-Type': 'application/json'})
    return r
def bulkPostGoals(goals):
    r = requests.post(baseUrl+'goal/bulk', json.dumps({"goals": goals}), headers={'Content-Type': 'application/json'})
    return r
def bulkPostPlayers(players):
    r = requests.post(baseUrl+'player/bulk', json.dumps({"players": players}), headers={'Content-Type': 'application/json'})
    return r
def bulkPostxG(xG):
    r = requests.post(baseUrl+'xg/bulk', json.dumps({"xG": xG}), headers={'Content-Type': 'application/json'})
    return r
def bulkPostAdjustments(adjustments):
    r = requests.post(baseUrl+'adjustment/bulk', json.dumps({"adjustments": adjustments}), headers={'Content-Type': 'application/json'})
    return r

