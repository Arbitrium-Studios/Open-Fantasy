import math
from panda3d.core import Point3
from toontown.toonbase import ToontownGlobals

# in seconds, how many seconds do we wait for them to decide
InputTimeout = 15

# in secons, how many seconds do we wait for the tire movie to finish
TireMovieTimeout = 120

MinWall = (-20.0, -15.0) # lower left corner of fence
MaxWall = (20.0, 15.0) # upper right corner of fence

TireRadius = 1.5 # in feet

WallMargin = 1 + TireRadius
StartingPositions = ( Point3(MinWall[0] + WallMargin, # bottomLeft
                             MinWall[1] + WallMargin,
                             TireRadius),
                      Point3(MaxWall[0] - WallMargin, # topRight
                             MaxWall[1] - WallMargin,
                             TireRadius),
                      Point3(MinWall[0] + WallMargin, # topLeft
                             MaxWall[1] - WallMargin,
                             TireRadius),
                      Point3(MaxWall[0] - WallMargin, # bottomRight
                             MinWall[1] + WallMargin,
                             TireRadius),
                      )
                          
NumMatches = 3 # how many matches for the whole game
NumRounds = 2 # how many rounds per match

# how many points do you get when you're at dead center,
# key is number of players
PointsDeadCenter = {
    0: 5,
    1: 5,
    2: 5,
    3: 4,
    4: 3,
    }
PointsInCorner = 1 # how many points do you get when you're as far as you can be
FarthestLength = math.sqrt( ((MaxWall[0]-TireRadius) * (MaxWall[0]-TireRadius)) + ((MaxWall[1]-TireRadius)*(MaxWall[1]-TireRadius)))
BonusPointsForPlace = (3, 2, 1, 0) # Bonus points awarded for 1st, 2nd, 3rd, 4th

ExpandFeetPerSec = 5 # how fast does the scoring circle expand
#ScoreIncreaseDuration = 3 # how long does a players score increase

ScoreCountUpRate  = 0.15 # in seconds how long does increasint a point take

ShowScoresDuration = 4. # in seconds, how long to display the player's score

# for each safezone, how many treasures do we put
NumTreasures = {
     ToontownGlobals.ToontropolisPlaza : 2,
     ToontownGlobals.ToontropolisDocks : 2,
     ToontownGlobals.FloweringGrove : 2, 
     ToontownGlobals.TheLandOfMusic: 2,
     ToontownGlobals.TundraWonderland: 1,
     ToontownGlobals.TwilightDreamland: 1,
     }

# for each safezone, how many penalties do we put
NumPenalties = {
     ToontownGlobals.ToontropolisPlaza : 0,
     ToontownGlobals.ToontropolisDocks : 1,
     ToontownGlobals.FloweringGrove : 1, 
     ToontownGlobals.TheLandOfMusic: 1,
     ToontownGlobals.TundraWonderland: 2,
     ToontownGlobals.TwilightDreamland: 2,
     }

# for each safezone, where the obstacles go
Obstacles = {
     ToontownGlobals.ToontropolisPlaza : (),
     ToontownGlobals.ToontropolisDocks : ((0,0),),
     ToontownGlobals.FloweringGrove : ((MinWall[0]/2,0), (MaxWall[0]/2,0)), 
     ToontownGlobals.TheLandOfMusic: ((0,MinWall[1]/2), (0, MaxWall[1]/2)), 
     ToontownGlobals.TundraWonderland: ((MinWall[0]/2,0),
                                 (MaxWall[0]/2 , 0),
                                 (0,MinWall[1]/2),
                                 (0,MaxWall[1]/2) ), 
     ToontownGlobals.TwilightDreamland: ( ( MinWall[0]/2, MinWall[1]/2),
                                         ( MinWall[0]/2, MaxWall[1]/2),
                                         ( MaxWall[0]/2, MinWall[1]/2),
                                         ( MaxWall[0]/2, MaxWall[1]/2),
                                         ),
     }

# for each safezone, if we use cubic obstacles (false means cylindrical)
ObstacleShapes = {
     ToontownGlobals.ToontropolisPlaza : True ,
     ToontownGlobals.ToontropolisDocks : True ,
     ToontownGlobals.FloweringGrove : True, 
     ToontownGlobals.TheLandOfMusic: True, 
     ToontownGlobals.TundraWonderland: False, 
     ToontownGlobals.TwilightDreamland: False ,
     }
    
