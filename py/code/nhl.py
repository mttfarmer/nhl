import requests

class nhlApi:
    @staticmethod
    def getGamesForDate(date):
        r = requests.get(f'https://api-web.nhle.com/v1/schedule/{date}')
        r = r.json()
        games = r['gameWeek'][0]['games']
        return games
    @staticmethod
    def getPlayByPlayData(gameId):
        r = requests.get(f'https://api-web.nhle.com/v1/gamecenter/{gameId}/play-by-play')
        r = r.json()
        return r
    @staticmethod
    def getShiftData(gameId):
        r = requests.get(f'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gameId}')
        r = r.json()
        return r
    @staticmethod
    def getPlayersOnIceAtTime(shiftData, period, timestamp):
        targetShifts = [shift for shift in shiftData if shift["period"] == period and timestamp >= shift["startTime"] and timestamp <= shift["endTime"]]
        return targetShifts
