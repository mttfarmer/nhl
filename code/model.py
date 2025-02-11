import pandas
import datetime
defaultModel = {
"5v5": {
    "rebound": 2.130,
    "rush": 1.671,
    "shotType": {
        "wrist": 0.865,
        "slap": 1.168,
        "backhand": 0.657,
        "tip-in": 0.697,
        "snap": 1.137,
        "wrap-around": 0.356,
        "deflected": 0.683
    },
    "scoreState": {
        "minusThreePlus": 0.953,
        "minusTwo": 0.991,
        "minusOne": 0.980,
        "even": 0.971,
        "plusOne": 1.031,
        "plusTwo": 1.109,
        "plusThreePlus": 1.107
    }
},

"4v4": {
    "rebound": 2.014,
    "rush": 1.617,
    "shotType": {
        "wrist": 0.953,
        "slap": 1.291,
        "backhand": 0.686,
        "tip-in": 0.830,
        "snap": 1.299,
        "wrap-around": 0.618,
        "deflected": 0.629
    },
    "scoreState": {
        "minusThreePlus": 1.024,
        "minusTwo": 1.028,
        "minusOne": 1.054,
        "even": 0.934,
        "plusOne": 1.133,
        "plusTwo": 1.128,
        "plusThreePlus": 1.170
    }
},

"3v3": {
    "rebound": 1.254,
    "rush": 1.778,
    "shotType": {
        "wrist": 1.285,
        "slap": 2.218,
        "backhand": 1.037,
        "tip-in": 1.239,
        "snap": 2.033,
        "wrap-around": 0.848,
        "deflected": 1.187
    },
    "scoreState": {
        "minusThreePlus": 1,
        "minusTwo": 1,
        "minusOne": 1,
        "even": 1,
        "plusOne": 1,
        "plusTwo": 1,
        "plusThreePlus": 1
    }
}
,
"ppv4": {
    "rebound": 1.854,
    "rush": 1.567,
    "shotType": {
        "wrist": 1.199,
        "slap": 1.962,
        "backhand": 0.793,
        "tip-in": 0.930,
        "snap": 1.712,
        "wrap-around": 0.615,
        "deflected": 0.868
    },
    "scoreState": {
        "minusThreePlus": 0.961,
        "minusTwo": 0.963,
        "minusOne": 0.986,
        "even": 0.995,
        "plusOne": 1.023,
        "plusTwo": 1.032,
        "plusThreePlus": 1.109
    }
}
,
"ppv3": {
    "rebound": 1.544,
    "rush": 1.279,
    "shotType": {
        "wrist": 1.905,
        "slap": 3.310,
        "backhand": 1.220,
        "tip-in": 1.476,
        "snap": 2.632,
        "wrap-around": 1.117,
        "deflected": 1.640
    },
    "scoreState": {
        "minusThreePlus": 1,
        "minusTwo": 1,
        "minusOne": 1,
        "even": 1,
        "plusOne": 1,
        "plusTwo": 1,
        "plusThreePlus": 1
    }
}
,
"sh": {
    "rebound": 1.709,
    "rush": 1.755,
    "shotType": {
        "wrist": 1.037,
        "slap": 1.018,
        "backhand": 0.929,
        "tip-in": 0.943,
        "snap": 1.444,
        "wrap-around": 0.669,
        "deflected": 0.974
    },
    "scoreState": {
        "minusThreePlus": 0.959,
        "minusTwo": 0.900,
        "minusOne": 0.908,
        "even": 0.990,
        "plusOne": 1.034,
        "plusTwo": 1.158,
        "plusThreePlus": 1.161
    }
}
,
"rushSeconds": 4,
"reboundSeconds":2
}

situationCodeMap = {
    'home': {
    '1551': '5v5',
    '1541': 'ppv4',
    '1531': 'ppv3',
    '1431': 'ppv3',
    '1441': '4v4',
    '1331': '3v3',
    '1451': 'sh',
    '1351': 'sh',
    '1341': 'sh'
    },
    'away': {
    '1551': '5v5',
    '1541': 'sh',
    '1531': 'sh',
    '1431': 'sh',
    '1441': '4v4',
    '1331': '3v3',
    '1451': 'ppv4',
    '1351': 'ppv3',
    '1341': 'ppv3'    
    }
}
class xGModel:
    def __init__(self, model=defaultModel):
        self.model = model
    @staticmethod
    def getLocScore(base, xInput,yInput):
        score = ''
        for index, row in base.iterrows():
            if eval(row['x coordinate'].replace('x', xInput)) and (type(row['y coordinate']) != float and eval(row['y coordinate'].replace('y', yInput))) or (eval(row['x coordinate'].replace('x', xInput)) and type(row['y coordinate']) == float):
                score = row['xG_base']
                break
        return score
    
    def eventIsShot(self, typeCode):
        return typeCode in [505,506,507]

    def isShotRebound(self, data, shot):
        # Get all events from 2 seconds before shotTimestamp
        eventsBefore = self.getEventsBeforeEvent(data['plays'], shot, self.model["reboundSeconds"])
        # If there is a shot event within 2 seconds before shotTimestamp, shot is a rebound shot
        if len([event for event in eventsBefore if self.eventIsShot(event['typeCode'])]) > 0:
            return True
        return False
    

    def isShotRush(self, data, shot):
        try:
            # Get all events from 4 seconds before shotTimestamp
            eventsBefore = self.getEventsBeforeEvent(data['plays'], shot, self.model["rushSeconds"])
            # If shot event xCoord positive, check if any event has xCoord < 25
            if shot['details']['xCoord'] > 0 and len([event for event in eventsBefore if event['details']['xCoord'] < 25]) > 0:
                return True
            # If shot event xCoord negative, check if any event has xCoord > -25
            elif shot['details']['xCoord'] < 0 and len([event for event in eventsBefore if event['details']['xCoord'] > -25]) > 0:
                return True
            return False
        except:
            print('problemshot:', shot)
            raise

    def getStrengthState(self, data, shot):
        homeId = data['homeTeam']['id']
        if shot['details']['eventOwnerTeamId'] == homeId:
            return situationCodeMap['home'][shot['situationCode']]
        else:
            return situationCodeMap['away'][shot['situationCode']]
    
    def getScoreState(self, data, shot, team):
        last = False
        for i in range(data['plays'].index(shot)):
            if data['plays'][i]['typeCode'] == 505:
                last = data[i]
        if last:
            if team == 'home':
                difference = last['details']['homeScore'] - last['details']['awayScore']
            else:
                difference = last['details']['awayScore'] - last['details']['homeScore']
        else:
            difference = 0
        
        if difference <= -3:
            return 'minusThreePlus'
        elif difference == -2:
            return 'minusTwo'
        elif difference == -1:
            return 'minusOne'
        elif difference == 0:
            return 'even'
        elif difference == 1:
            return 'plusOne'
        elif difference == 2:
            return 'plusTwo'
        elif difference >= 3:
            return 'plusThreePlus'
    @staticmethod
    def getRinkBias(arena=""):
        return 1
    
    @staticmethod
    def getSeasonAdjustment(season=""):
        return 1
    
    @staticmethod
    def isWithinXSeconds(time1_str, time2_str, x):
        """time1 - before time2"""
        time1 = datetime.datetime.strptime(time1_str, "%M:%S")
        time2 = datetime.datetime.strptime(time2_str, "%M:%S")

        time_diff = time2 - time1

        return 0 <= time_diff.total_seconds() <= x
        
    def getEventsBeforeEvent(self, data, event, secondsBefore):
        events = [play for play in data if self.isWithinXSeconds(play['timeInPeriod'], event['timeInPeriod'], secondsBefore) and event['eventId'] != play['eventId']]
        return events
    
    def gradeShot(self, data, shot):
        if shot['situationCode'] not in situationCodeMap['home'].keys():
            return False
        #TODO: make this configurable
        base_df = pandas.read_excel('xg_base.xlsx')
        format = ['xG_base', 'x coordinate', 'y coordinate']
        select = base_df[format]
        locScore = self.getLocScore(select, str(abs(shot['details']['xCoord'])), str(shot['details']['yCoord']))
        adjustedScore = self.applyAdjustments(data, shot, locScore)
        return adjustedScore
    
    
    def applyAdjustments(self, data, shot, locScore):
        adjustments = {}
        strengthState = self.getStrengthState(data, shot)
        scoreState = self.getScoreState(data, shot, 'home' if shot['details']['eventOwnerTeamId'] == data['homeTeam']['id'] else 'away')
        shotType = shot['details']['shotType']
        isRebound = self.isShotRebound(data, shot)
        isRush = self.isShotRush(data, shot)

        adjustments['shotType'] = {'adjustmentType': 'shotType', 'category': shotType, 'adjustmentValue': self.model[strengthState]["shotType"][shotType]}
        adjustments['scoreState'] = {'adjustmentType': 'scoreState', 'category': scoreState, 'adjustmentValue': self.model[strengthState]["scoreState"][scoreState]}
        if isRebound:
            adjustments['rebound'] = {'adjustmentType': 'rebound', 'adjustmentValue': self.model[strengthState]['rebound']}
        if isRush:
            adjustments['rush'] = {'adjustmentType': 'rush', 'adjustmentValue': self.model[strengthState]['rush']}

        adjValues = [value['adjustmentValue'] for value in adjustments.values()]
        for adj in adjValues:
            locScore = locScore*adj

        return locScore
