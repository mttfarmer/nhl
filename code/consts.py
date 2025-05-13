sqlQueries = {
    "adj": {
        "bulk_insert": """INSERT INTO Adjustment
        (id, xGId, category, subcategory, amount) values %s"""
    },
    "ana": {
        "bulk_insert": """INSERT INTO Analyst
        (id, username, pw) values %s"""
    },
    "game": {
        "bulk_insert": """INSERT INTO Game 
        (id, season, gameType, limitedScoring, gameDate, venue, venueLocation, 
        startTimeUTC, awayTeamId, homeTeamId, shootoutInUse, otInUse) values %s
        ON CONFLICT (id)
        DO NOTHING"""
    },
    "goal": {
        "bulk_insert": """INSERT INTO Goal 
        (playId, scoringPlayerId, assist1PlayerId, assist2PlayerId, goalieInNetId, eventOwnerTeamId, awayScore, homeScore,
        highlightClipSharingUrl, highlightClipSharingUrlFr, highlightClip, highlightClipFr,
        discreteClip, discreteClipFr, xCoord, yCoord, zoneCode, shotType) values %s
        ON CONFLICT (playId)
        DO NOTHING"""
    },
    "model": {
        "bulk_insert": """INSERT INTO Model
        (id, analystId, definition) values %s
        ON CONFLICT (id)
        DO NOTHING"""
    },
    "play": {
        "bulk_insert": """INSERT INTO Play 
        (id, gameId, eventId, periodDescriptor, timeInPeriod, timeRemaining, situationCode, homeTeamDefendingSide,
        typeCode, typeDescKey, sortOrder, details) values %s
        ON CONFLICT (id)
        DO NOTHING"""
    },
    "player": {
        "bulk_insert": """INSERT INTO Player 
        (id, firstName, lastName, sweaterNumber, positionCode, headshot) values %s
        ON CONFLICT (id)
        DO NOTHING"""
    },
    "shot": {
        "bulk_insert": """INSERT INTO Shot 
        (playId, shootingPlayerId, eventOwnerTeamId, goalieInNetId, xCoord, yCoord, zoneCode, reason,
        awaySOG, homeSOG, shotType) values %s
        ON CONFLICT (playId)
        DO NOTHING"""
    },
    "team": {
        "bulk_insert": """INSERT INTO Team
        (id, teamName, abbreviation, logo, darkLogo, placeName) values %s
        ON CONFLICT (id)
        DO NOTHING"""
    },
    "xg": {
        "bulk_insert": """INSERT INTO xG
        (id, modelId, playId, xG) values %s
        ON CONFLICT (id)
        DO NOTHING"""
    },

    "xgView": {
        "base": """SELECT * FROM xGView"""
    },


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

shotTypes = [
    'wrist',
    'slap',
    'backhand',
    'tip-in',
    'snap',
    'wrap-around',
    'deflected'
]