from direct.directnotify import DirectNotifyGlobal
from . import DistributedCountryClubAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import CountryClubLayout
from direct.showbase import DirectObject
import random

CountryClubId2Layouts = {
    ToontownGlobals.BossbotCountryClubIntA : (0, 1, 2, ),
    ToontownGlobals.BossbotCountryClubIntB : (3, 4, 5, ),
    ToontownGlobals.BossbotCountryClubIntC : (6, 7, 8, ),
    }

class CountryClubManagerAI(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('CountryClubManagerAI')

    # magic-word override
    countryClubId = None

    def __init__(self, air):
        DirectObject.DirectObject.__init__(self)
        self.air = air

    def getDoId(self):
        # DistributedElevatorAI needs this
        return 0

    def createCountryClub(self, countryClubId, players):
        # check for ~countryClubId
        for avId in players:
            if bboard.has('countryClubId-%s' % avId):
                countryClubId = bboard.get('countryClubId-%s' % avId)
                break

        numFloors = 1 # ToontownGlobals.CountryClubNumFloors[countryClubId]
        layoutIndex = None

        floor = 0 #random.randrange(numFloors)
        # check for ~countryClubFloor
        for avId in players:
            if bboard.has('countryClubFloor-%s' % avId):
                floor = bboard.get('countryClubFloor-%s' % avId)
                # bounds check
                floor = max(0, floor)
                floor = min(floor, numFloors-1)
                break

        # check for ~countryClubRoom
        for avId in players:
            if bboard.has('countryClubRoom-%s' % avId):
                roomId = bboard.get('countryClubRoom-%s' % avId)
                for i in range(numFloors):
                    layout = CountryClubLayout.CountryClubLayout(countryClubId, i)
                    if roomId in layout.getRoomIds():
                        floor = i
                else:
                    from toontown.coghq import CountryClubRoomSpecs
                    roomName = CountryClubRoomSpecs.BossbotCountryClubRoomId2RoomName[roomId]
                    CountryClubManagerAI.notify.warning(
                        'room %s (%s) not found in any floor of countryClub %s' %
                        (roomId, roomName, countryClubId))

        countryClubZone = self.air.allocateZone()
        if layoutIndex is None:
            layoutIndex = random.choice(CountryClubId2Layouts[countryClubId])        
        countryClub = DistributedCountryClubAI.DistributedCountryClubAI(
            self.air, countryClubId, countryClubZone, floor, players, layoutIndex)
        countryClub.generateWithRequired(countryClubZone)
        return countryClubZone
