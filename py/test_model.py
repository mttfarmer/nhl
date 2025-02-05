import unittest
import pandas
from code.model import xGModel
import json

class TestModelApi(unittest.TestCase):
    base_df = pandas.read_excel('xg_base.xlsx')
    format = ['xG_base', 'x coordinate', 'y coordinate']
    select = base_df[format]
    model = xGModel()
    with open('test_files/play-by-play.json', 'r', encoding='utf8') as f:
        pbp = json.load(f)['plays']
    def test_getLocScore(self):
        score = self.model.getLocScore(self.select, '30', '38.5')
        self.assertEqual(score, 0.011655011655011656, 'Score does not match.')

    def test_getEventsBeforeTime(self):
        testEvent = {
            "eventId": 9,
            "periodDescriptor": {
                "number": 1,
                "periodType": "REG",
                "maxRegulationPeriods": 3
            },
            "timeInPeriod": "03:17",
            "timeRemaining": "16:43",
            "situationCode": "1551",
            "homeTeamDefendingSide": "left",
            "typeCode": 516,
            "typeDescKey": "stoppage",
            "sortOrder": 56,
            "details": {
                "reason": "goalie-stopped-after-sog"
            }
        }
        events = self.model.getEventsBeforeEvent(self.pbp, testEvent, 2)
        print(events)
        self.assertEqual(len(events), 2, 'Wrong number of events.')

if __name__ == '__main__':
    unittest.main()