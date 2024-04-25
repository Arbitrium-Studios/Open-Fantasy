from direct.directnotify import DirectNotifyGlobal
from . import ZoneUtil
from toontown.building import DistributedBuildingMgrAI
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.suit import DistributedSuitPlannerAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone import DistributedButterflyAI
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from pandac.PandaModules import *
from panda3d.toontown import *
from toontown.toon import NPCToons


class HoodDataAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('HoodDataAI')

    def __init__(self, air, zoneId, canonicalHoodId):
        self.air = air
        self.zoneId = zoneId
        self.canonicalHoodId = canonicalHoodId
        self.treasurePlanner = None
        self.buildingManagers = []
        self.suitPlanners = []
        self.doId2do = {}
        self.replacementHood = None
        self.redirectingToMe = []
        self.fishingPonds = []
        self.hoodPopulation = 0
        self.pgPopulation = 0
        return

    def startup(self):
        self.createFishingPonds()
        self.createPartyPeople()
        self.createBuildingManagers()
        self.createSuitPlanners()

    def shutdown(self):
        self.setRedirect(None)
        if self.treasurePlanner:
            self.treasurePlanner.stop()
            self.treasurePlanner.deleteAllTreasuresNow()
            self.treasurePlanner = None
        for suitPlanner in self.suitPlanners:
            suitPlanner.requestDelete()
            del self.air.suitPlanners[suitPlanner.zoneId]

        self.suitPlanners = []
        for buildingManager in self.buildingManagers:
            buildingManager.cleanup()
            del self.air.buildingManagers[buildingManager.branchID]

        self.buildingManagers = []
        ButterflyGlobals.clearIndexes(self.zoneId)
        del self.fishingPonds
        for distObj in list(self.doId2do.values()):
            distObj.requestDelete()

        del self.doId2do
        del self.air
        return

    def addDistObj(self, distObj):
        self.doId2do[distObj.doId] = distObj

    def removeDistObj(self, distObj):
        del self.doId2do[distObj.doId]

    def createPartyPeople(self):
        partyHats = []
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
            dnaData = self.air.dnaDataMap.get(zone[0], None)
            if isinstance(dnaData, DNAData):
                foundPartyHats = self.air.findPartyHats(dnaData, zoneId)
                partyHats += foundPartyHats

        for distObj in partyHats:
            self.addDistObj(distObj)

        return

    def findFishingPonds(self, dnaGroup, zoneId, area):
        fishingPonds = []
        fishingPondGroups = []
        if isinstance(dnaGroup, DNAGroup) and ('fishing_pond' in dnaGroup.getName()):
            fishingPondGroups.append(dnaGroup)

            fishingPond = DistributedFishingPondAI(simbase.air)
            fishingPond.setArea(area)
            fishingPond.generateWithRequired(zoneId)
            fishingPond.start()
            fishingPonds.append(fishingPond)
        elif isinstance(dnaGroup, DNAVisGroup):
            zoneId = int(dnaGroup.getName().split(':')[0])
        for i in range(dnaGroup.getNumChildren()):
            (foundFishingPonds, foundFishingPondGroups) = self.findFishingPonds(dnaGroup.at(i), zoneId, area)
            fishingPonds.extend(foundFishingPonds)
            fishingPondGroups.extend(foundFishingPondGroups)
        return (fishingPonds, fishingPondGroups)

    def findFishingSpots(self, dnaGroup, fishingPond):
        fishingSpots = []
        if isinstance(dnaGroup, DNAGroup) and ('fishing_spot' in dnaGroup.getName()):
            fishingSpot = DistributedFishingSpotAI(simbase.air)
            fishingSpot.setPondDoId(fishingPond.doId)
            x, y, z = dnaGroup.getPos()
            h, p, r = dnaGroup.getHpr()
            fishingSpot.setPosHpr(x, y, z, h, p, r)
            fishingSpot.generateWithRequired(fishingPond.zoneId)

            fishingSpots.append(fishingSpot)
        for i in range(dnaGroup.getNumChildren()):
            foundFishingSpots = self.findFishingSpots(dnaGroup.at(i), fishingPond)
            fishingSpots.extend(foundFishingSpots)
        return fishingSpots

    def createFishingPonds(self):
        self.fishingPonds = []
        fishingPondGroups = []
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
            dnaData = self.air.dnaDataMap.get(zone[0], None)
            if isinstance(dnaData, DNAData):
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                (foundFishingPonds, foundFishingPondGroups) = self.findFishingPonds(dnaData, zoneId, area)
                self.fishingPonds.extend(foundFishingPonds)
                fishingPondGroups.extend(foundFishingPondGroups)
        for fishingPond in self.fishingPonds:
            NPCToons.createNpcsInZone(self.air, fishingPond.zoneId)
        fishingSpots = []
        for (dnaGroup, fishingPond) in zip(fishingPondGroups, self.fishingPonds):
            fishingSpots.extend(self.findFishingSpots(dnaGroup, fishingPond))


        for distObj in self.fishingPonds:
            self.addDistObj(distObj)
            npcs = NPCToons.createNpcsInZone(self.air, distObj.zoneId)
            for npc in npcs:
                self.addDistObj(npc)

        fishingSpots = []
        for dnaGroup, distPond in zip(fishingPondGroups, self.fishingPonds):
            fishingSpots += self.air.findFishingSpots(dnaGroup, distPond)

        for distObj in fishingSpots:
            self.addDistObj(distObj)

        return

    def createBuildingManagers(self):
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            if zone[1]:
                zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
                dnaStore = self.air.dnaStoreMap[zone[0]]
                mgr = DistributedBuildingMgrAI.DistributedBuildingMgrAI(
                    self.air, zoneId, dnaStore, self.air.trophyMgr)
                self.buildingManagers.append(mgr)
                self.air.buildingManagers[zoneId] = mgr

    def createSuitPlanners(self):
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            if zone[2]:
                zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
                sp = DistributedSuitPlannerAI.DistributedSuitPlannerAI(
                    self.air, zoneId)
                sp.generateWithRequired(zoneId)
                sp.d_setZoneId(zoneId)
                sp.initTasks()
                self.suitPlanners.append(sp)
                self.air.suitPlanners[zoneId] = sp

    def createButterflies(self, playground):
        ButterflyGlobals.generateIndexes(self.zoneId, playground)
        for i in range(0, ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for j in range(0, ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                bfly = DistributedButterflyAI.DistributedButterflyAI(
                    self.air, playground, i, self.zoneId)
                bfly.generateWithRequired(self.zoneId)
                bfly.start()
                self.addDistObj(bfly)

    def setRedirect(self, replacementHood):
        if self.replacementHood:
            self.replacementHood[0].redirectingToMe.remove(self)
        self.replacementHood = replacementHood
        if self.replacementHood:
            self.replacementHood[0].redirectingToMe.append(self)

    def hasRedirect(self):
        return self.replacementHood is not None

    def getRedirect(self):
        if self.replacementHood is None:
            return self
        else:
            return self.replacementHood[0].getRedirect()
        return

    def incrementPopulation(self, zoneId, increment):
        self.hoodPopulation += increment
        if ZoneUtil.isPlayground(zoneId):
            self.pgPopulation += increment

    def getHoodPopulation(self):
        population = self.hoodPopulation
        for hood in self.redirectingToMe:
            population += hood.getHoodPopulation()

        return population

    def getPgPopulation(self):
        population = self.pgPopulation
        for pg in self.redirectingToMe:
            population += pg.getPgPopulation()

        return population
