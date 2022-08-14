


class GardenAI:
    # TODO
    def __init__(self, air, gardenMgr, avId):
        return
        
    def destroy(self):
        return

    def load(self, estate):
        return

    def placePlot(self, treeIndex):
        return

    def getNullPlant(self):
        return

    def reconsiderAvatarOrganicBonus(self):
        return

    def hasTree(self, track, index):
        return

    def getTree(self, track, index):
        return

    def plantTree(self, treeIndex, value, plot=None, waterLevel=-1, lastCheck=0, growthLevel=0, lastHarvested=0,
                  ownerIndex=-1, plotId=-1, pos=None, generate=True):
        return

    def placeStatuary(self, data, plot=None, plotId=-1, ownerIndex=-1, pos=None, generate=True):
        return

    def plantFlower(self, flowerIndex, species, variety, plot=None, waterLevel=-1, lastCheck=0, growthLevel=0,
                    ownerIndex=-1, plotId=-1, generate=True):
        return
   
    @staticmethod
    def S_pack(data, lastCheck, index, growthLevel):
        return
    
    @staticmethod
    def S_unpack(x):
       return

    def update(self):
        return


class GardenManagerAI:
    # TODO
    notify = DirectNotifyGlobal.directNotify.newCategory('GardenManagerAI')

    def __init__(self, air, estate):
        return

    def loadGarden(self, avId):
        return

    def destroy(self):
        return