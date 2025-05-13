CREATE TABLE Adjustment
(
  id          VARCHAR NOT NULL,
  xGId        VARCHAR NOT NULL,
  category    VARCHAR,
  subcategory VARCHAR,
  amount      FLOAT  ,
  PRIMARY KEY (id)
);

CREATE TABLE Analyst
(
  id       VARCHAR NOT NULL,
  username VARCHAR,
  pw       VARCHAR,
  PRIMARY KEY (id)
);

CREATE TABLE Game
(
  id             INT     NOT NULL,
  season         INT    ,
  gameType       INT    ,
  limitedScoring BOOL   ,
  gameDate       VARCHAR,
  venue          VARCHAR,
  venueLocation  VARCHAR,
  startTimeUTC   VARCHAR,
  shootoutInUse  BOOL   ,
  otInUse        BOOL   ,
  awayTeamId     INT     NOT NULL,
  homeTeamId     INT     NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Goal
(
  playId                    VARCHAR NOT NULL,
  scoringPlayerId           INT     NOT NULL,
  assist1PlayerId           INT    ,
  assist2PlayerId           INT    ,
  goalieInNetId             INT    ,
  eventOwnerTeamId          INT     NOT NULL,
  awayScore                 INT    ,
  homeScore                 INT    ,
  highlightClipSharingUrl   VARCHAR,
  highlightClipSharingUrlFr VARCHAR,
  highlightClip             bigint ,
  highlightClipFr           bigint ,
  discreteClip              bigint ,
  discreteClipFr            bigint ,
  xCoord                    INT    ,
  yCoord                    INT    ,
  zoneCode                  VARCHAR,
  shotType                  VARCHAR,
  PRIMARY KEY (playId)
);

CREATE TABLE Model
(
  id         VARCHAR NOT NULL,
  analystId  VARCHAR NOT NULL,
  definition JSON   ,
  ver        int    ,
  PRIMARY KEY (id)
);

CREATE TABLE Play
(
  id                    VARCHAR NOT NULL,
  gameId                INT     NOT NULL,
  eventId               VARCHAR NOT NULL,
  periodDescriptor      JSON   ,
  timeInPeriod          VARCHAR,
  timeRemaining         VARCHAR,
  situationCode         VARCHAR,
  homeTeamDefendingSide VARCHAR,
  typeCode              INT    ,
  typeDescKey           VARCHAR,
  sortOrder             INT    ,
  details               JSON   ,
  PRIMARY KEY (id)
);

CREATE TABLE Player
(
  id            INT     NOT NULL,
  firstName     VARCHAR,
  lastName      VARCHAR,
  sweaterNumber INT    ,
  positionCode  VARCHAR,
  headshot      VARCHAR,
  PRIMARY KEY (id)
);

CREATE TABLE RosterSpot
(
  playerId INT NOT NULL,
  gameId   INT NOT NULL
);

CREATE TABLE Shift
(
  id               INT     NOT NULL,
  detailCode       INT    ,
  duration         VARCHAR,
  endTime          VARCHAR,
  eventDescription VARCHAR,
  eventDetails     VARCHAR,
  eventNumber      INT    ,
  gameId           INT    ,
  hexValue         VARCHAR,
  period           INT    ,
  shiftNumber      INT    ,
  startTime        VARCHAR,
  typeCode         INT    ,
  playerId         INT     NOT NULL,
  teamId           INT     NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Shot
(
  playId           VARCHAR NOT NULL,
  shootingPlayerId INT     NOT NULL,
  eventOwnerTeamId INT     NOT NULL,
  goalieInNetId    INT    ,
  xCoord           INT    ,
  yCoord           INT    ,
  zoneCode         VARCHAR,
  reason           VARCHAR,
  awaySOG          INT    ,
  homeSOG          INT    ,
  shotType         VARCHAR,
  PRIMARY KEY (playId)
);

CREATE TABLE Team
(
  id           INT     NOT NULL,
  teamName     VARCHAR,
  abbreviation VARCHAR,
  logo         VARCHAR,
  darkLogo     VARCHAR,
  placeName    VARCHAR,
  PRIMARY KEY (id)
);

CREATE TABLE xG
(
  id      VARCHAR NOT NULL,
  modelId VARCHAR NOT NULL,
  playId  VARCHAR NOT NULL,
  xG      FLOAT  ,
  PRIMARY KEY (id)
);

ALTER TABLE Play
  ADD CONSTRAINT FK_Game_TO_Play
    FOREIGN KEY (gameId)
    REFERENCES Game (id);

ALTER TABLE Model
  ADD CONSTRAINT FK_Analyst_TO_Model
    FOREIGN KEY (analystId)
    REFERENCES Analyst (id);

ALTER TABLE xG
  ADD CONSTRAINT FK_Model_TO_xG
    FOREIGN KEY (modelId)
    REFERENCES Model (id);

ALTER TABLE Adjustment
  ADD CONSTRAINT FK_xG_TO_Adjustment
    FOREIGN KEY (xGId)
    REFERENCES xG (id);

ALTER TABLE RosterSpot
  ADD CONSTRAINT FK_Player_TO_RosterSpot
    FOREIGN KEY (playerId)
    REFERENCES Player (id);

ALTER TABLE RosterSpot
  ADD CONSTRAINT FK_Game_TO_RosterSpot
    FOREIGN KEY (gameId)
    REFERENCES Game (id);

ALTER TABLE Game
  ADD CONSTRAINT FK_Team_TO_Game
    FOREIGN KEY (awayTeamId)
    REFERENCES Team (id);

ALTER TABLE Game
  ADD CONSTRAINT FK_Team_TO_Game1
    FOREIGN KEY (homeTeamId)
    REFERENCES Team (id);

ALTER TABLE Shift
  ADD CONSTRAINT FK_Player_TO_Shift
    FOREIGN KEY (playerId)
    REFERENCES Player (id);

ALTER TABLE Shift
  ADD CONSTRAINT FK_Team_TO_Shift
    FOREIGN KEY (teamId)
    REFERENCES Team (id);

ALTER TABLE Shot
  ADD CONSTRAINT FK_Play_TO_Shot
    FOREIGN KEY (playId)
    REFERENCES Play (id);

ALTER TABLE Shot
  ADD CONSTRAINT FK_Player_TO_Shot
    FOREIGN KEY (shootingPlayerId)
    REFERENCES Player (id);

ALTER TABLE Shot
  ADD CONSTRAINT FK_Team_TO_Shot
    FOREIGN KEY (eventOwnerTeamId)
    REFERENCES Team (id);

ALTER TABLE Shot
  ADD CONSTRAINT FK_Player_TO_Shot1
    FOREIGN KEY (goalieInNetId)
    REFERENCES Player (id);

ALTER TABLE Goal
  ADD CONSTRAINT FK_Player_TO_Goal
    FOREIGN KEY (scoringPlayerId)
    REFERENCES Player (id);

ALTER TABLE Goal
  ADD CONSTRAINT FK_Player_TO_Goal1
    FOREIGN KEY (assist1PlayerId)
    REFERENCES Player (id);

ALTER TABLE Goal
  ADD CONSTRAINT FK_Player_TO_Goal2
    FOREIGN KEY (assist2PlayerId)
    REFERENCES Player (id);

ALTER TABLE xG
  ADD CONSTRAINT FK_Play_TO_xG
    FOREIGN KEY (playId)
    REFERENCES Play (id);

ALTER TABLE Goal
  ADD CONSTRAINT FK_Play_TO_Goal
    FOREIGN KEY (playId)
    REFERENCES Play (id);

ALTER TABLE Goal
  ADD CONSTRAINT FK_Player_TO_Goal3
    FOREIGN KEY (goalieInNetId)
    REFERENCES Player (id);

ALTER TABLE Goal
  ADD CONSTRAINT FK_Team_TO_Goal
    FOREIGN KEY (eventOwnerTeamId)
    REFERENCES Team (id);


CREATE VIEW xGView AS 
select distinct
  p.id,
  p.gameid,
  p.timeinperiod,
  p.timeremaining,
  p.situationcode,
  p.typecode,
  p.typedesckey,
  p.perioddescriptor->>'number' as period,
  coalesce(s.shootingplayerid, g.scoringplayerid) as shooterid,
  coalesce(s.eventownerteamid, g.eventownerteamid) as eventownerteamid,
  coalesce(s.goalieinnetid, g.goalieinnetid) as goalieinnetid,
  coalesce(s.xcoord, g.xcoord) as xcoord,
  coalesce(s.ycoord, g.ycoord) as ycoord,
  coalesce(s.zonecode, g.zonecode) as zonecode,
  s.reason,
  s.awaysog,
  s.homesog,
  coalesce(s.shottype, g.shottype) as shottype,
  g.assist1playerid,
  g.assist2playerid,
  g.homescore,
  g.awayscore,
  g.highlightclipsharingurl,
  x.modelid,
  x.xg,
  shooter.firstname as shooterFirstName,
  shooter.lastName as shooterLastName,
  shooter.sweaternumber as shooterNumber,
  shooter.positioncode as shooterPosition,
  shooter.headshot as shooterHeadshot,
  a1.firstname as a1FirstName,
  a1.lastName as a1LastName,
  a1.sweaternumber as a1Number,
  a1.positioncode as a1Position,
  a1.headshot as a1Headshot,
  a2.firstname as a2FirstName,
  a2.lastName as a2LastName,
  a2.sweaternumber as a2Number,
  a2.positioncode as a2Position,
  a2.headshot as a2Headshot,
  goalie.firstname as goalieFirstName,
  goalie.lastName as goalieLastName,
  goalie.sweaternumber as goalieNumber,
  goalie.positioncode as goaliePosition,
  goalie.headshot as goalieHeadshot,
  ga.season,
  ga.gamedate
from play p 
  left join shot s on s.playId = p.id 
  left join goal g on g.playId = p.id 
  left join xG x on x.playId = p.id
  left join player shooter on shooter.id = s.shootingplayerid or shooter.id = g.scoringplayerid
  left join player a1 on a1.id = g.assist1playerid
  left join player a2 on a2.id = g.assist2playerid
  left join player goalie on goalie.id = g.goalieInNetId or goalie.id = s.goalieInNetId
  left join game ga on ga.id = p.gameid
where p.typecode in  (505,506,507)
  and p.situationcode in ('1551','1541','1531','1431','1441','1331','1451','1351','1341');
INSERT INTO Analyst (id) values ('basic-free');

INSERT INTO Model (id, ver, analystId, definition)
VALUES ('basic-free', 0, 'basic-free', '{
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
}')
  
  