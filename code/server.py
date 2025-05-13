from flask import Flask, jsonify, request, make_response
import psycopg2
import logging
import os
import consts
import json

import psycopg2.extras
import daily_runner

postgres = psycopg2.connect(
    database="postgres",
    host="postgres",
    user="postgres",
    password=os.environ['POSTGRES_PW'],
    port="5432",
    options=f'-c search_path=mhockey'
)
postgres.autocommit = True
cursor = postgres.cursor()
app = Flask(__name__)
#daily
@app.route('/daily', methods=['GET'])
def run_daily():
    daily_runner.main()

    return make_response('OK', 200)

# @app.route('/game/<game_id>', methods=['GET'])
# def get_game(game_id):

#     return make_response(data, 200)

@app.route('/xg', methods=['GET'])
def get_xg(model):
    pass
@app.route('/game/bulk', methods=['POST'])
def post_game():
    data = request.get_json()
    insert_values = []
    for game in data['games']:
        insert_values.append((
            game['id'],
            game['season'],
            game['gameType'], 
            game['limitedScoring'],
            game['gameDate'],
            game['venue']['default'], 
            game['venueLocation']['default'],
            game['startTimeUTC'],
            game['awayTeam']['id'],
            game['homeTeam']['id'],
            game['shootoutInUse'],
            game['otInUse']
            ))
    psycopg2.extras.execute_values(
        cursor, consts.sqlQueries['game']['bulk_insert'], insert_values
    )
    postgres.commit()
    return make_response("OK", 200)

@app.route('/play/bulk', methods=['POST'])
def post_play():
    data = request.get_json()
    insert_values = []
    for play in data['plays']:
        if 'details' in play:
            details = play['details']
        else:
            details = {}
        insert_values.append((
            play['id'],
            play['gameId'],
            play['eventId'], 
            json.dumps(play['periodDescriptor']),
            play['timeInPeriod'],
            play['timeRemaining'], 
            play['situationCode'],
            play['homeTeamDefendingSide'],
            play['typeCode'],
            play['typeDescKey'],
            play['sortOrder'],
            json.dumps(details)
            ))
    psycopg2.extras.execute_values(
        cursor, consts.sqlQueries['play']['bulk_insert'], insert_values
    )
    postgres.commit()
    return make_response("OK", 200)

@app.route('/player/bulk', methods=['POST'])
def post_player():
    data = request.get_json()
    insert_values = []
    for player in data['players']:
        insert_values.append((
            player['id'],
            player['firstName'],
            player['lastName'],
            player['sweaterNumber'],
            player['positionCode'],
            player['headshot']
            ))
    psycopg2.extras.execute_values(
        cursor, consts.sqlQueries['player']['bulk_insert'], insert_values
    )
    postgres.commit()
    return make_response("OK", 200)

@app.route('/model', methods=['POST'])
def post_model():
    data = request.get_json()
    return make_response("OK", 200)

@app.route('/model/<user_id>', methods=['GET'])
def get_user_models(user_id):
    data = []
    models = []
    for model in data:
        model['_id'] = str(model['_id'])
        models.append(model)
    return make_response(models, 200)

@app.route('/model/<model_id>', methods=['PUT'])
def put_model(model_id):
    data = request.get_json()
    pass

@app.route('/shot/bulk', methods=['POST'])
def post_shot():
    data = request.get_json()
    insert_values = []

    for shot in data['shots']:
        if 'reason' in shot:
            reason = shot['reason']
        else:
            reason = ''
        if 'awaySOG' in shot:
            awaySOG = shot['awaySOG']
        else:
            awaySOG = None
        if 'homeSOG' in shot:
            homeSOG = shot['homeSOG']
        else:
            homeSOG = None
        insert_values.append((
            shot['playId'],
            shot['shootingPlayerId'],
            shot['eventOwnerTeamId'],
            shot['goalieInNetId'],
            shot['xCoord'],
            shot['yCoord'],
            shot['zoneCode'],
            reason,
            awaySOG,
            homeSOG,
            shot['shotType']
            ))
    psycopg2.extras.execute_values(
        cursor, consts.sqlQueries['shot']['bulk_insert'], insert_values
    )
    postgres.commit()
    return make_response("OK", 200)

@app.route('/adjustment/bulk', methods=['POST'])
def post_adjustment():
    data = request.get_json()
    insert_values = []

    for adjustment in data['adjustments']:
        if 'subcategory' in adjustment:
            subcategory = adjustment['subcategory']
        else:
            subcategory = None
        insert_values.append((
            adjustment['id'],
            adjustment['xGId'],
            adjustment['category'],
            subcategory,
            adjustment['adjustmentValue']
        ))
    psycopg2.extras.execute_values(
        cursor, consts.sqlQueries['adj']['bulk_insert'], insert_values
    )
    postgres.commit()
    return make_response("OK", 200)

@app.route('/xg/bulk', methods=['POST'])
def post_xG():
    data = request.get_json()
    insert_values = []

    for xG in data['xG']:
        insert_values.append((
            xG['id'],
            xG['modelId'],
            xG['shotId'],
            xG['xG'],
        ))
    psycopg2.extras.execute_values(
        cursor, consts.sqlQueries['xg']['bulk_insert'], insert_values
    )
    postgres.commit()
    return make_response("OK", 200)

@app.route('/goal/bulk', methods=['POST'])
def post_goal():
    data = request.get_json()
    insert_values = []

    for goal in data['goals']:
        a1 = None
        a2 = None
        highlightClipSharingUrl = None
        highlightClip = None
        goalieInNetId = None
        if 'assist1PlayerId' in goal:
            a1 = goal['assist1PlayerId']
        if 'assist2PlayerId' in goal:
            a2 = goal['assist2PlayerId']
        if 'highlightClipSharingUrl' in goal:
            highlightClipSharingUrl = goal['highlightClipSharingUrl']
        if 'highlightClip' in goal:
            highlightClip = goal['highlightClip']
        if 'goalieInNetId' in goal:
            goalieInNetId = goal['goalieInNetId']
        insert_values.append((
            goal['playId'],
            goal['scoringPlayerId'],
            a1,
            a2,
            goalieInNetId,
            goal['eventOwnerTeamId'],
            goal['awayScore'],
            goal['homeScore'],
            highlightClipSharingUrl,
            goal['highlightClipSharingUrlFr'],
            highlightClip,
            goal['highlightClipFr'],
            goal['discreteClip'],
            goal['discreteClipFr'],
            goal['xCoord'],
            goal['yCoord'],
            goal['zoneCode'],
            goal['shotType']
        ))
    psycopg2.extras.execute_values(
        cursor, consts.sqlQueries['goal']['bulk_insert'], insert_values
    )
    postgres.commit()
    return make_response("OK", 200)

#setup
import setup

@app.route('/setup/teams', methods=['GET'])
def setup_teams():
    teams = setup.getTeams()
    psycopg2.extras.execute_values(
        cursor, consts.sqlQueries['team']['bulk_insert'], teams
    )
    postgres.commit()
    return make_response('OK', 200)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')