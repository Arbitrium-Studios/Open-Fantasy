import math
from pandac.PandaModules import Point3
from toontown.toonbase import ToontownGlobals
InputTimeout = 15
TireMovieTimeout = 120
MinWall = (-20.0, -15.0)
MaxWall = (20.0, 15.0)
TireRadius = 1.5
WallMargin = 1 + TireRadius
StartingPositions = (Point3(MinWall[0] + WallMargin, MinWall[1] + WallMargin, TireRadius),
                     Point3(
    MaxWall[0] - WallMargin,
    MaxWall[1] - WallMargin,
    TireRadius),
    Point3(MinWall[0] + WallMargin, MaxWall[1] - WallMargin, TireRadius),
    Point3(MaxWall[0] - WallMargin, MinWall[1] + WallMargin, TireRadius))
NumMatches = 3
NumRounds = 2
PointsDeadCenter = {0: 5,
                    1: 5,
                    2: 5,
                    3: 4,
                    4: 3}
PointsInCorner = 1
FarthestLength = math.sqrt((MaxWall[0] -
                            TireRadius) *
                           (MaxWall[0] -
                            TireRadius) +
                           (MaxWall[1] -
                            TireRadius) *
                           (MaxWall[1] -
                            TireRadius))
BonusPointsForPlace = (3,
                       2,
                       1,
                       0)
ExpandFeetPerSec = 5
ScoreCountUpRate = 0.15
ShowScoresDuration = 4.0
NumTreasures = {ToontownGlobals.ToontownCenter: 2,
                ToontownGlobals.ToontownShipyards: 2,
                ToontownGlobals.FloweringGrove: 2,
                ToontownGlobals.TheLandOfMusic: 2,
                ToontownGlobals.TundraWonderland: 1,
                ToontownGlobals.TwilightDreamland: 1}
NumPenalties = {ToontownGlobals.ToontownCenter: 0,
                ToontownGlobals.ToontownShipyards: 1,
                ToontownGlobals.FloweringGrove: 1,
                ToontownGlobals.TheLandOfMusic: 1,
                ToontownGlobals.TundraWonderland: 2,
                ToontownGlobals.TwilightDreamland: 2}
Obstacles = {ToontownGlobals.ToontownCenter: (),
             ToontownGlobals.ToontownShipyards: ((0, 0),),
             ToontownGlobals.FloweringGrove: ((MinWall[0] / 2, 0), (MaxWall[0] / 2, 0)),
             ToontownGlobals.TheLandOfMusic: ((0, MinWall[1] / 2), (0, MaxWall[1] / 2)),
             ToontownGlobals.TundraWonderland: ((MinWall[0] / 2, 0),
                                         (MaxWall[0] / 2, 0),
                                         (0, MinWall[1] / 2),
                                         (0, MaxWall[1] / 2)),
             ToontownGlobals.TwilightDreamland: ((MinWall[0] / 2, MinWall[1] / 2),
                                                (MinWall[0] / 2,
                                                 MaxWall[1] / 2),
                                                (MaxWall[0] / 2,
                                                 MinWall[1] / 2),
                                                (MaxWall[0] / 2, MaxWall[1] / 2))}
ObstacleShapes = {ToontownGlobals.ToontownCenter: True,
                  ToontownGlobals.ToontownShipyards: True,
                  ToontownGlobals.FloweringGrove: True,
                  ToontownGlobals.TheLandOfMusic: True,
                  ToontownGlobals.TundraWonderland: False,
                  ToontownGlobals.TwilightDreamland: False}
