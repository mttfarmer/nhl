import unittest
from code.nhl import nhlApi

class TestNhlApi(unittest.TestCase):
    def test_getGamesForDate(self):
        nhl = nhlApi()
        games = nhl.getGamesForDate('2023-11-10')
        ids = [x['id'] for x in games]
        self.assertEqual(ids, [2023020204, 2023020205, 2023020206, 2023020207, 2023020208, 2023020209], 'ID list does not match.')
    
    def test_getPlayByPlayData(self):
        nhl = nhlApi()
        pbp = nhl.getPlayByPlayData('2024020664')
        self.assertEqual(pbp["gameDate"], "2025-01-10")

    def test_getShiftData(self):
        nhl = nhlApi()
        shifts = nhl.getShiftData('2024020664')
        self.assertEqual(shifts["total"], 739)
    
    def test_getPlayersOnIceAtTime(self):
        nhl = nhlApi()
        shifts = nhl.getShiftData('2024020664')
        players = nhl.getPlayersOnIceAtTime(shifts["data"], 1, "05:12")
        self.assertEqual([player["id"] for player in players], [14891507, 14891425, 14891429, 14891525, 14891563, 14891570, 14891582, 14891587, 14891593, 14891606, 14891609, 14891613])

if __name__ == '__main__':
    unittest.main()