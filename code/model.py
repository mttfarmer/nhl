import pandas
import datetime
from consts import defaultModel, situationCodeMap

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
        #508 is blocked shot. ignore for now, nhl api does not provide shotType on blocked shots
        return typeCode in [506,507]
    
    def eventIsGoal(self, typeCode):
        return typeCode == 505

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
            if shot['details']['xCoord'] > 0 and len([event for event in eventsBefore if 'details' in event and 'xCoord' in event['details'] and event['details']['xCoord'] < 25]) > 0:
                return True
            # If shot event xCoord negative, check if any event has xCoord > -25
            elif shot['details']['xCoord'] < 0 and len([event for event in eventsBefore if 'details' in event and 'xCoord' in event['details'] and event['details']['xCoord'] > -25]) > 0:
                return True
            return False
        except:
            print('problemshot:', shot)
            print(eventsBefore)
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
                last = data['plays'][i]
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
        #TODO: make this configurable
        base_df = pandas.read_excel('xg_base.xlsx')
        format = ['xG_base', 'x coordinate', 'y coordinate']
        select = base_df[format]
        locScore = self.getLocScore(select, str(abs(shot['details']['xCoord'])), str(shot['details']['yCoord']))
        adjustedScore, adjustments = self.applyAdjustments(data, shot, locScore)
        return (adjustedScore, adjustments)
    
    
    def applyAdjustments(self, data, shot, locScore):
        adjustments = []
        strengthState = self.getStrengthState(data, shot)
        scoreState = self.getScoreState(data, shot, 'home' if shot['details']['eventOwnerTeamId'] == data['homeTeam']['id'] else 'away')
        shotType = shot['details']['shotType']
        isRebound = self.isShotRebound(data, shot)
        isRush = self.isShotRush(data, shot)

        adjustments.append({'category': 'shotType', 'subcategory': shotType, 'adjustmentValue': self.model[strengthState]["shotType"][shotType]})
        adjustments.append({'category': 'scoreState', 'subcategory': scoreState, 'adjustmentValue': self.model[strengthState]["scoreState"][scoreState]})
        if isRebound:
            adjustments.append({'category': 'rebound', 'adjustmentValue': self.model[strengthState]['rebound']})
        if isRush:
            adjustments.append({'category': 'rush', 'adjustmentValue': self.model[strengthState]['rush']})

        adjValues = [adjustment['adjustmentValue'] for adjustment in adjustments]
        for adj in adjValues:
            locScore = locScore*adj
        return (locScore, adjustments)
