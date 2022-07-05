from .MazeBase import MazeBase
from . import MazeData


class Maze(MazeBase):

    def __init__(self, mapName, mazeData=None,
                 cellWidth=MazeData.CELL_WIDTH):
        if mazeData is None:
            mazeData = MazeData.mazeData
        model = loader.loadModel(mapName)
        mData = mazeData[mapName]
        self.treasurePosList = mData['treasurePosList']
        self.numTreasures = len(self.treasurePosList)
        MazeBase.__init__(self, model, mData, cellWidth)
