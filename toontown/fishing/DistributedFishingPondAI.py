from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from .DistributedFishingTargetAI import DistributedFishingTargetAI
from .DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from . import FishingTargetGlobals

class DistributedFishingPondAI(DistributedObjectAI):
    notify = directNotify.newCategory("DistributedFishingPondAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.area = None
        self.targets = {}
        self.spots = {}
        self.bingoMgr = None
    
    def announceGenerate(self):
        if self.air.newsManager.isHolidayRunning(ToontownGlobals.FISH_BINGO, ToontownGlobals.SILLY_SATURDAY):
            self.startBingo()

        self.accept('startBingo', self.startBingo)
        self.accept('stopBingo', self.stopBingo)
        DistributedObjectAI.announceGenerate(self)
    
    def delete(self):
        self.ignoreAll()
        DistributedObjectAI.delete(self)

    def start(self):
        for _ in range(FishingTargetGlobals.getNumTargets(self.area)):
            fishingTarget = DistributedFishingTargetAI(simbase.air)
            fishingTarget.setPondDoId(self.doId)
            fishingTarget.generateWithRequired(self.zoneId)
    
    def startBingo(self):
        if self.bingoMgr:
            self.notify.warning('Tried to start bingo while already started!')
            return

        self.bingoMgr = DistributedPondBingoManagerAI(self.air)
        self.bingoMgr.setPondDoId(self.getDoId())
        self.bingoMgr.generateWithRequired(self.zoneId)
        self.bingoMgr.createGame()
    
    def stopBingo(self):
        if not self.bingoMgr:
            self.notify.warning('Tried to stop bingo but not started!')
            return

        self.bingoMgr.requestDelete()
        self.bingoMgr = None

    def hitTarget(self, target):
        avId = self.air.getAvatarIdFromSender()
        if self.targets.get(target) is None:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to hit nonexistent fishing target!')
            return
        spot = self.hasToon(avId)
        if spot:
            spot.rewardIfValid(target)
            return
        self.air.writeServerEvent('suspicious', avId, 'Toon tried to catch fish while not fishing!')

    def addTarget(self, target):
        self.targets[target.doId] = target

    def addSpot(self, spot):
        self.spots[spot.doId] = spot

    def setArea(self, area):
        self.area = area

    def getArea(self):
        return self.area

    def hasToon(self, avId):
        for spot in self.spots:
            if self.spots[spot].avId == avId:
                return self.spots[spot]
