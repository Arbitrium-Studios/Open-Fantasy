from otp.ai.AIBaseGlobal import *
from panda3d.core import *
from otp.otpbase import PythonUtil
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase.PythonUtil import Functor
from . import DistributedEstateAI
from direct.task.Task import Task
from . import HouseGlobals
import random
import functools
from direct.fsm.FSM import FSM
from toontown.toon import ToonDNA
from toontown.estate.DistributedHouseAI import DistributedHouseAI

#Other classes from toontown stride
class LoadHouseFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('LoadHouseFSM')

    def __init__(self, mgr, estate, houseIndex, toon, callback):
        FSM.__init__(self, 'LoadHouseFSM')
        self.mgr = mgr
        self.estate = estate
        self.houseIndex = houseIndex
        self.toon = toon
        self.callback = callback

        self.done = False

    def start(self):
        # We have a few different cases here:
        if self.toon is None:
            # Case #1: There isn't a Toon in that estate slot. Make a blank house.

            # Because this state completes so fast, we'll use taskMgr to delay
            # it until the next iteration. This solves re-entrancy problems.
            taskMgr.doMethodLater(0.0, self.demand,
                                  'makeBlankHouse-%s' % id(self),
                                  extraArgs=['MakeBlankHouse'])
            return

        self.houseId = self.toon.get('setHouseId', [0])[0]
        if self.houseId  == 0:
            # Case #2: There is a Toon, but no setHouseId. Gotta make one.
            self.demand('CreateHouse')
        else:
            # Case #3: Toon with a setHouseId. Load it.
            self.demand('LoadHouse')

    def enterMakeBlankHouse(self):
        self.house = DistributedHouseAI(self.mgr.air)
        self.house.setHousePos(self.houseIndex)
        self.house.setColor(self.houseIndex)
        self.house.generateWithRequired(self.estate.zoneId)
        self.estate.houses[self.houseIndex] = self.house
        self.demand('Off')

    def enterCreateHouse(self):
        style = ToonDNA.ToonDNA()
        style.makeFromNetString(self.toon['setDNAString'][0])
        
        self.mgr.air.dbInterface.createObject(
            self.mgr.air.dbId,
            self.mgr.air.dclassesByName['DistributedHouseAI'],
            {
                'setName' : [self.toon['setName'][0]],
                'setAvatarId' : [self.toon['ID']],
                'setGender': [0 if style.getGender() == 'm' else 1]
            },
            self.__handleCreate)

    def __handleCreate(self, doId):
        if self.state != 'CreateHouse':
            return

        # Update the avatar's houseId:
        av = self.mgr.air.doId2do.get(self.toon['ID'])
        if av:
            av.b_setHouseId(doId)
        else:
            self.mgr.air.dbInterface.updateObject(
                self.mgr.air.dbId,
                self.toon['ID'],
                self.mgr.air.dclassesByName['DistributedToonAI'],
                {'setHouseId': [doId]})

        self.houseId = doId
        self.demand('LoadHouse')

    def enterLoadHouse(self):
        # Activate the house:
        self.mgr.air.sendActivate(self.houseId, self.mgr.air.districtId, self.estate.zoneId,
                                  self.mgr.air.dclassesByName['DistributedHouseAI'],
                                  {'setHousePos': [self.houseIndex],
                                   'setColor': [self.houseIndex],
                                   'setName': [self.toon['setName'][0]],
                                   'setAvatarId': [self.toon['ID']]})

        # Now we wait for the house to show up... We do this by hanging a messenger
        # hook which the DistributedHouseAI throws once it spawns.
        self.acceptOnce('generate-%d' % self.houseId, self.__gotHouse)

    def __gotHouse(self, house):
        self.house = house
        house.initializeInterior()

        self.estate.houses[self.houseIndex] = self.house

        self.demand('Off')

    def exitLoadHouse(self):
        self.ignore('generate-%d' % self.houseId)

    def enterOff(self):
        self.done = True
        self.callback(self.house)

class LoadPetFSM(FSM):
    def __init__(self, mgr, estate, toon, callback):
        FSM.__init__(self, 'LoadPetFSM')
        self.mgr = mgr
        self.estate = estate
        self.toon = toon
        self.callback = callback

        self.done = False

    def start(self):
        self.petId = self.toon['setPetId'][0]
        if not self.petId in self.mgr.air.doId2do:
            self.mgr.air.sendActivate(self.petId, self.mgr.air.districtId, self.estate.zoneId)
            self.acceptOnce('generate-%d' % self.petId, self.__generated)
        else:
            self.__generated(self.mgr.air.doId2do[self.petId])

    def __generated(self, pet):
        self.pet = pet
        self.estate.pets.append(pet)
        self.demand('Off')

    def enterOff(self):
        self.done = True
        self.callback(self.pet)


class LoadEstateFSM(FSM):
    def __init__(self, mgr, callback):
        FSM.__init__(self, 'LoadEstateFSM')
        self.mgr = mgr
        self.callback = callback

        self.estate = None

    def start(self, accountId, zoneId):
        self.accountId = accountId
        self.zoneId = zoneId
        self.demand('QueryAccount')

    def enterQueryAccount(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.accountId,
                                             self.__gotAccount)

    def __gotAccount(self, dclass, fields):
        if self.state != 'QueryAccount':
            return # We must have aborted or something...

        if dclass != self.mgr.air.dclassesByName['AccountAI']:
            self.mgr.notify.warning('Account %d has non-account dclass %d!' %
                                    (self.accountId, dclass))
            self.demand('Failure')
            return

        self.accountFields = fields

        self.estateId = fields.get('ESTATE_ID', 0)
        self.demand('QueryToons')

    def enterQueryToons(self):
        self.toonIds = self.accountFields.get('ACCOUNT_AV_SET', [0]*6)
        self.toons = {}

        for index, toonId in enumerate(self.toonIds):
            if toonId == 0:
                self.toons[index] = None
                continue
            self.mgr.air.dbInterface.queryObject(
                self.mgr.air.dbId, toonId,
                functools.partial(self.__gotToon, index=index))

    def __gotToon(self, dclass, fields, index):
        if self.state != 'QueryToons':
            return # We must have aborted or something...

        if dclass != self.mgr.air.dclassesByName['DistributedToonAI']:
            self.mgr.notify.warning('Account %d has avatar %d with non-Toon dclass %d!' %
                                    (self.accountId, self.toonIds[index], dclass))
            self.demand('Failure')
            return

        fields['ID'] = self.toonIds[index]
        self.toons[index] = fields
        if len(self.toons) == 6:
            self.__gotAllToons()

    def __gotAllToons(self):
        # Okay, we have all of our Toons, now we can proceed with estate!
        if self.estateId:
            # We already have an estate, load it!
            self.demand('LoadEstate')
        else:
            # We don't have one yet, make one!
            self.demand('CreateEstate')

    def enterCreateEstate(self):
        # We have to ask the DB server to construct a blank estate object...
        self.mgr.air.dbInterface.createObject(
            self.mgr.air.dbId,
            self.mgr.air.dclassesByName['DistributedEstateAI'],
            {},
            self.__handleEstateCreate)

    def __handleEstateCreate(self, estateId):
        if self.state != 'CreateEstate':
            return # We must have aborted or something...
        self.estateId = estateId
        self.demand('StoreEstate')

    def enterStoreEstate(self):
        # store the estate in account
        # congrats however wrote this for forgetting it!
        
        self.mgr.air.dbInterface.updateObject(
            self.mgr.air.dbId,
            self.accountId,
            self.mgr.air.dclassesByName['AccountAI'],
            {'ESTATE_ID': self.estateId},
            {'ESTATE_ID': 0},
            self.__handleStoreEstate)
            
    def __handleStoreEstate(self, fields):
        if fields:
            self.notify.warning("Failed to associate Estate %d with account %d, loading anyway." % (self.estateId, self.accountId))
            
        self.demand('LoadEstate')

    def enterLoadEstate(self):
        # Activate the estate:
        fields = {}
        for i, toon in enumerate(self.toonIds):
            fields['setSlot%dToonId' % i] = (toon,)
            
        self.mgr.air.sendActivate(self.estateId, self.mgr.air.districtId, self.zoneId,
                                  self.mgr.air.dclassesByName['DistributedEstateAI'], fields)

        # Now we wait for the estate to show up... We do this by hanging a messenger
        # hook which the DistributedEstateAI throws once it spawns.
        self.acceptOnce('generate-%d' % self.estateId, self.__gotEstate)

    def __gotEstate(self, estate):
        self.estate = estate
        estate.pets = []

        # Gotcha! Now we need to load houses:
        self.demand('LoadHouses')

    def exitLoadEstate(self):
        self.ignore('generate-%d' % self.estateId)

    def enterLoadHouses(self):
        self.houseFSMs = []

        for houseIndex in range(6):
            fsm = LoadHouseFSM(self.mgr, self.estate, houseIndex,
                               self.toons[houseIndex], self.__houseDone)
            self.houseFSMs.append(fsm)
            fsm.start()

    def __houseDone(self, house):
        if self.state != 'LoadHouses':
            # We aren't loading houses, so we probably got cancelled. Therefore,
            # the only sensible thing to do is simply destroy the house.
            house.requestDelete()
            return

        # A houseFSM just finished! Let's see if all of them are done:
        if all(houseFSM.done for houseFSM in self.houseFSMs):
            self.demand('LoadPets')

    def enterLoadPets(self):
        self.petFSMs = []
        for houseIndex in range(6):
            toon = self.toons[houseIndex]
            if toon and toon['setPetId'][0] != 0:
                fsm = LoadPetFSM(self.mgr, self.estate, toon, self.__petDone)
                self.petFSMs.append(fsm)
                fsm.start()

        if not self.petFSMs:
            taskMgr.doMethodLater(0, lambda: self.demand('Finished'), 'nopets', extraArgs=[])

    def __petDone(self, pet):
        if self.state != 'LoadPets':
            pet.requestDelete()
            return

        # A petFSM just finished! Let's see if all of them are done:
        if all(petFSM.done for petFSM in self.petFSMs):
            self.demand('Finished')

    def enterFinished(self):
        self.callback(True)

    def enterFailure(self):
        self.cancel()

        self.callback(False)

    def cancel(self):
        if self.estate:
            self.estate.destroy()
            self.estate = None

        self.demand('Off')



class LoadPetFSM(FSM):
    def __init__(self, mgr, estate, toon, callback):
        FSM.__init__(self, 'LoadPetFSM')
        self.mgr = mgr
        self.estate = estate
        self.toon = toon
        self.callback = callback

        self.done = False

    def start(self):
        self.petId = self.toon['setPetId'][0]
        if not self.petId in self.mgr.air.doId2do:
            self.mgr.air.sendActivate(self.petId, self.mgr.air.districtId, self.estate.zoneId)
            self.acceptOnce('generate-%d' % self.petId, self.__generated)
        else:
            self.__generated(self.mgr.air.doId2do[self.petId])

    def __generated(self, pet):
        self.pet = pet
        self.estate.pets.append(pet)
        self.demand('Off')

    def enterOff(self):
        self.done = True
        self.callback(self.pet)

TELEPORT_TO_OWNER_ONLY = 0

class EstateManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManagerAI")
    #notify.setDebug(True)

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.previousZone = None
        self.refCount = {}      # dict of lists containing avId's visiting an estate. keyed on owner's avId
        self.estateZone = {}    # dict of tuple of [zoneId, isOwner, userName] keyed on avId
        self.estate = {}        # dict of DistributedEstateAI's keyed on avId
        self.house = {}         # dict of lists of DistributedHouseAI's keyed on avId
        self.account2avId = {}  # mapping of userName to avId that created estate
        self.toBeDeleted = {}   # temporary list of av's to be deleted after a delay
        self.zone2owner = {}    # get the owner of a zone
        self.houseZone2estateZone = {}
        self.avId2pendingEnter = {} # table of avatars that are on their way to an estate
        self.petOperations  = []
        # Number of seconds between spontaneous heals
        self.healFrequency = 30 # seconds
        self.toon2estate = {}
        self.estate2toons = {}
        self.estate2timeout = {}
        self.zone2toons = {}


        self.randomGenerator = random.Random()

        return None

    #def delete(self):
        #self.notify.debug("BASE: delete: deleting EstateManagerAI object")
       # self.ignoreAll()
       # DistributedObjectAI.DistributedObjectAI.delete(self)
        #for estate in list(self.estate.values()):
         #   estate.requestDelete()
            # This automatically gets called by the server
            # estate.delete()
        #for hList in list(self.house.values()):
          #  for house in hList:
         #       house.requestDelete()
                # This automatically gets called by the server
                # house.delete()
        #del self.account2avId
        #del self.avId2pendingEnter
        #del self.refCount
        #del self.estateZone
        #del self.randomGenerator


    def getOwnerFromZone(self, zoneId):
        # returns doId of estate owner given a zoneId
        # zoneId can be estate exterior or house interior
        # returns None if zone not found
        estateZoneId = self.houseZone2estateZone.get(zoneId, zoneId)
        return self.zone2owner.get(estateZoneId)

    ## -----------------------------------------------------------
    ## Zone allocation and enter code
    ## -----------------------------------------------------------

    def getEstateZone(self, avId):
        # Credit to Toontown Stride
        senderId = self.air.getAvatarIdFromSender()
        accId = self.air.getAccountIdFromSender()

        toon = self.air.doId2do.get(senderId)
        if not toon:
            self.air.writeServerEvent('suspicious', senderId, 'Sent getEstateZone() but not on district!')
            return

        # If there's an avId included, then the Toon is interested in visiting a
        # friend. We do NOT load the estate, we simply see if it's already up...
        if avId and avId != senderId:
            av = self.air.doId2do.get(avId)
            if av and av.dclass == self.air.dclassesByName['DistributedToonAI']:
                estate = self._lookupEstate(av)
                if estate:
                    # Yep, there it is!
                    avId = estate.owner.doId
                    zoneId = estate.zoneId
                    self._mapToEstate(toon, estate)
                    self._unloadEstate(toon) # In case they're doing estate->estate TP.
                    self.sendUpdateToAvatarId(senderId, 'setEstateZone', [avId, zoneId])

            # Bummer, couldn't find avId at an estate...
            self.sendUpdateToAvatarId(senderId, 'setEstateZone', [0, 0])
            return

        # The Toon definitely wants to go to his own estate...

        estate = getattr(toon, 'estate', None)
        if estate:
            # They already have an estate loaded, so let's just return it:
            self._mapToEstate(toon, toon.estate)
            self.sendUpdateToAvatarId(senderId, 'setEstateZone', [senderId, estate.zoneId])

            # If a timeout is active, cancel it:
            if estate in self.estate2timeout:
                self.estate2timeout[estate].remove()
                del self.estate2timeout[estate]

            return

        if getattr(toon, 'loadEstateFSM', None):
            # We already have a loading operation underway; ignore this second
            # request since the first operation will setEstateZone() when it
            # finishes anyway.
            return

        zoneId = self.air.allocateZone()



        def estateLoaded(success):
            if success:
                senderAv.estate = senderAv.loadEstateFSM.estate
                senderAv.estate.owner = senderAv
                self._mapToEstate(senderAv, senderAv.estate)
                if hasattr(senderAv, 'enterEstate'):
                    senderAv.enterEstate(senderId, zoneId)

                self.sendUpdateToAvatarId(senderId, 'setEstateZone', [senderId, zoneId])
            else:
                # Estate loading failed??!
                self.sendUpdateToAvatarId(senderId, 'setEstateZone', [0, 0])

                # Might as well free up the zoneId as well.
                self.air.deallocateZone(zoneId)
                del self.zone2owner[zoneId]

            senderAv.loadEstateOperation = None

        self.acceptOnce(self.air.getAvatarExitEvent(senderAv.doId), self._unloadEstate, extraArgs=[senderAv])


        self.zone2owner[zoneId] = avId
        senderAv.loadEstateOperation = LoadEstateFSM(self, estateLoaded)
        senderAv.loadEstateOperation.start()

    def getAvEnterEvent(self):
        return 'avatarEnterEstate'

    def getAvExitEvent(self, avId=None):
        # listen for all exits or a particular exit
        # event args:
        #  if avId given: none
        #  if avId not given: avId, ownerId, zoneId
        if avId is None:
            return 'avatarExitEstate'
        else:
            return 'avatarExitEstate-%s' % avId

    def __enterEstate(self, avId, ownerId):
        # Tasks that should always get called when entering an estate

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])

        # Toonup
        try:
            av = self.air.doId2do[avId]
            av.startToonUp(self.healFrequency)
        except:
            self.notify.info("couldn't start toonUpTask for av %s" % avId)

    def _listenForToonEnterEstate(self, avId, ownerId, zoneId):
        #self.notify.debug('_listenForToonEnterEstate(avId=%s, ownerId=%s, zoneId=%s)' % (avId, ownerId, zoneId))
        if avId in self.avId2pendingEnter:
            self.notify.warning(
                '_listenForToonEnterEstate(avId=%s, ownerId=%s, zoneId=%s): '
                '%s already in avId2pendingEnter. overwriting' % (
                avId, ownerId, zoneId, avId))
        self.avId2pendingEnter[avId] = (ownerId, zoneId)
        self.accept(DistributedObjectAI.
                    DistributedObjectAI.staticGetLogicalZoneChangeEvent(avId),
                    Functor(self._toonChangedZone, avId))

    def _toonLeftBeforeArrival(self, avId):
        #self.notify.debug('_toonLeftBeforeArrival(avId=%s)' % avId)
        if avId not in self.avId2pendingEnter:
            self.notify.warning('_toonLeftBeforeArrival: av %s not in table' %
                                avId)
            return
        ownerId, zoneId = self.avId2pendingEnter[avId]
        self.notify.warning(
            '_toonLeftBeforeArrival: av %s left server before arriving in '
            'estate (owner=%s, zone=%s)' % (avId, ownerId, zoneId))
        del self.avId2pendingEnter[avId]

    def _toonChangedZone(self, avId, newZoneId, oldZoneId):
        #self.notify.debug('_toonChangedZone(avId=%s, newZoneId=%s, oldZoneId=%s)' % (avId, newZoneId, oldZoneId))
        if avId not in self.avId2pendingEnter:
            self.notify.warning('_toonChangedZone: av %s not in table' %
                                avId)
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.notify.warning('_toonChangedZone(%s): av not present' % avId)
            return
        ownerId, estateZoneId = self.avId2pendingEnter[avId]
        estateZoneIds = self.getEstateZones(ownerId)
        if newZoneId in estateZoneIds:
            del self.avId2pendingEnter[avId]
            self.ignore(DistributedObjectAI.
                        DistributedObjectAI.staticGetLogicalZoneChangeEvent(avId))
            self.announceToonEnterEstate(avId, ownerId, estateZoneId)

    def announceToonEnterEstate(self, avId, ownerId, zoneId):
        """ announce to the rest of the system that a toon is entering
        an estate """
        EstateManagerAI.notify.debug('announceToonEnterEstate: %s %s %s' %
                                     (avId, ownerId, zoneId))
        messenger.send(self.getAvEnterEvent(), [avId, ownerId, zoneId])

    def announceToonExitEstate(self, avId, ownerId, zoneId):
        """ announce to the rest of the system that a toon is exiting
        an estate """
        EstateManagerAI.notify.debug('announceToonExitEstate: %s %s %s' %
                                     (avId, ownerId, zoneId))
        messenger.send(self.getAvExitEvent(avId))
        messenger.send(self.getAvExitEvent(), [avId, ownerId, zoneId])

    def getEstateZones(self, ownerId):
        # returns all zoneIds that belong to this estate
        zones = []
        estate = self.estate.get(ownerId)
        if estate is not None:
            if not hasattr(estate, 'zoneId'):
                self.notify.warning('getEstateZones: estate %s (owner %s) has no \'zoneId\'' %
                                    (estate.doId, ownerId))
            else:
                zones.append(estate.zoneId)
        houses = self.house.get(ownerId)
        if houses is not None:
            for house in houses:
                if not hasattr(house, 'interiorZoneId'):
                    self.notify.warning('getEstateZones: estate %s (owner %s) house has no interiorZoneId')
                else:
                    zones.append(house.interiorZoneId)
        return zones

    def getEstateHouseZones(self, ownerId):
        # returns all zoneIds that belong to houses on this estate
        zones = []
        houses = self.house.get(ownerId)
        if houses is not None:
            for house in houses:
                if not hasattr(house, 'interiorZoneId'):
                    self.notify.warning('getEstateHouseZones: (owner %s) house has no interiorZoneId')
                else:
                    zones.append(house.interiorZoneId)
        return zones

    def __sendZoneToClient(self, recipient, ownerId):
        try:
            zone = self.estateZone[ownerId][0]
            owner = self.zone2owner[zone]
            self.sendUpdateToAvatarId(recipient, "setEstateZone", [owner, zone])
        except:
            self.notify.warning("zone did not exist for estate owner %d, and visitor %d" % (ownerId, recipient))
            self.sendUpdateToAvatarId(recipient, "setEstateZone", [0, 0])

    def __createEstateZoneAndObjects(self, avId, isOwner, ownerId, name):
        # assume this is only called when isOwner == 1

        # stop any cleanup tasks that might be pending for this avId
        # (note: we might be in a case where we aren't in the toBeDeleted list
        # and still have a cleanup task pending.  this happens when we switch
        # shards)
        self.__stopCleanupTask(avId)

        # first check that we aren't in the toBeDeleted list
        avZone = self.toBeDeleted.get(avId)
        if avZone:

            # move our info back to estateZone
            self.setEstateZone(avId, avZone)
            del self.toBeDeleted[avId]
            return

        # check if our account has an estate created under a different avatar
        if self.__checkAccountSwitchedAvatars(name, avId):
            return

        # request the zone for the owners estate
        zoneId = self.air.allocateZone()
        self.setEstateZone(avId, [zoneId, isOwner, name]) # [zoneId, isOwner, userName (if owner)]
        self.account2avId[name] = avId
        self.zone2owner[zoneId] = avId

        # start a ref count for this zone id
        self.refCount[zoneId] = []

        # don't send a message back yet since the estate is not filled
        # in.  Do this later.
        #self.sendUpdateToAvatarId(avId, "setEstateZone", [avId, zoneId])

        # create the estate and generate the zone
        #callback = PythonUtil.Functor(self.handleGetEstate, avId, ownerId)
        #self.air.getEstate(avId, zoneId, callback)

    def __removeReferences(self, avId, zoneId):
        try:
            self.clearEstateZone(avId)
            self.refCount[zoneId].remove(avId)
        except:
            self.notify.debug("we weren't in the refcount for %s." % zoneId)
            pass

    def setEstateZone(self, index, info):
        self.estateZone[index] = info

        #print some debug info
        frame = sys._getframe(1)
        lineno = frame.f_lineno
        defName = frame.f_code.co_name
        #str = "%s(%s):Added %s:estateZone=%s" % (defName, lineno, index, self.estateZone)
        str = "%s(%s):Added %s:%s" % (defName, lineno, index, info)
        self.notify.debug(str)

    def clearEstateZone(self, index):
        assert index in self.estateZone

        #print some debug info
        frame = sys._getframe(1)
        lineno = frame.f_lineno
        defName = frame.f_code.co_name
        #str = "%s(%s):Removed %s:estateZone=%s" % (defName, lineno, index, self.estateZone)
        str = "%s(%s):Removed %s:%s" % (defName, lineno, index, self.estateZone[index])
        self.notify.debug(str)

        del self.estateZone[index]

    def __addReferences(self, avId, ownerId):
        avZone = self.estateZone.get(ownerId)
        if avZone:
            zoneId = avZone[0]
            self.setEstateZone(avId, [zoneId, 0, ""])  # [zoneId, isOwner, userName (if owner)]
            ref = self.refCount.get(zoneId)
            if ref:
                ref.append(avId)
            else:
                self.refCount[zoneId] = [avId]

    def __checkAccountSwitchedAvatars(self, name, ownerId):
        self.notify.debug("__checkAccountSwitchedAvatars")
        prevAvId = self.account2avId.get(name)
        if prevAvId:
            self.notify.debug("we indeed did switch avatars")
            # the estate exists, remap all references from prevAvId
            # to ownerId

            # first stop the cleanup task
            self.__stopCleanupTask(prevAvId)

            # now remap references
            self.account2avId[name] = ownerId

            #if self.estateZone.has_key(prevAvId):
            if prevAvId in self.toBeDeleted:
                self.setEstateZone(ownerId, self.toBeDeleted[prevAvId])
                del self.toBeDeleted[prevAvId]
            return 1
        return 0

    def handleGetEstate(self, avId, ownerId, estateId, estateVal,
                        numHouses, houseId, houseVal, petIds, valDict = None):
        self.notify.debug("handleGetEstate %s" % avId)
        # this function is called after the estate data is pulled
        # from the database.  the houseAI object is initialized
        # here, and if values don't exist for certain db fields
        # default values are given.

        # Note:  this is the place where randomized default values
        # should be assigned to the toons house.  For example:
        # door types, windows, colors, house selection, garden placement
        # etc.  The first time the toon visits his house, these
        # defaults will be computed and stored.

        # Note:  this function is only called by the owner of the estate

        # there is a chance that the owner will already have left (by
        # closing the window).  We need to handle that gracefully.

        if ownerId not in self.estateZone:
            self.notify.warning("Estate info was requested, but the owner left before it could be recived: %d" % estateId)
            return
        elif not avId in self.air.doId2do:
            self.notify.warning("Estate owner %s in self.estateZone, but not in doId2do" % avId)
            return

        # create the DistributedEstateAI object for this avId
        if avId in self.estateZone:
            if estateId in self.air.doId2do:
                self.notify.warning("Already have distobj %s, not generating again" % (estateId))
            else:
                self.notify.info('start estate %s init, owner=%s, frame=%s' %
                                 (estateId, ownerId, globalClock.getFrameCount()))

                # give the estate a time seed
                estateZoneId = self.estateZone[avId][0]
                ts = time.time() % HouseGlobals.DAY_NIGHT_PERIOD
                self.randomGenerator.seed(estateId)
                dawn = HouseGlobals.DAY_NIGHT_PERIOD * self.randomGenerator.random()
                estateAI = DistributedEstateAI.DistributedEstateAI(self.air, avId,
                                                                   estateZoneId, ts, dawn, valDict)
                # MPG - We should make sure this works across districts
                estateAI.dbObject = 1
                estateAI.generateWithRequiredAndId(estateId,
                                                   self.air.districtId,
                                                   estateZoneId)

                estateAI.initEstateData(estateVal, numHouses, houseId, houseVal)
                estateAI.setPetIds(petIds)
                self.estate[avId] = estateAI

                # create the DistributedHouseAI's.  This was originally done by the EstateAI
                # but we need to move it here so we can explicitly control when the
                # DistributedHouse objects get deleted from the stateserver.
                self.house[avId] = [None] * numHouses
                for i in range(numHouses):
                    if houseId[i] in self.air.doId2do:
                        self.notify.warning("doId of house %s conflicts with a %s!" % (houseId[i], self.air.doId2do[houseId[i]].__class__.__name__))

                    else:
                        house = DistributedHouseAI.DistributedHouseAI(self.air,
                                                                      houseId[i],
                                                                      estateId, estateZoneId, i)

                        # get house information
                        house.initFromServerResponse(houseVal[i])
                        self.house[avId][i] = house

                        # Now that we have all the data loaded, officially
                        # generate the distributed object

                        house.dbObject = 1

                        # MPG - We should make sure this works across districts
                        house.generateWithRequiredAndId(houseId[i],
                                                        self.air.districtId,
                                                        estateZoneId)

                        house.setupEnvirons()

                        # Finally, make sure that the house has a good owner,
                        # and then tell the client the house is ready.
                        house.checkOwner()

                        estateAI.houseList.append(house)

                estateAI.postHouseInit()

                #get us a list of the owners of the houses
                avIdList = []
                for id in houseId:
                    avHouse = simbase.air.doId2do.get(id)
                    avIdList.append(avHouse.ownerId)

                if simbase.wantPets:
                    self.notify.debug('creating pet collisions for estate %s' %
                                     estateId)
                    estateAI.createPetCollisions()

                # create a pond bingo manager ai for the new estate
                if simbase.wantBingo:
                    self.notify.info('creating bingo mgr for estate %s' %
                                     estateId)
                    self.air.createPondBingoMgrAI(estateAI)

                self.notify.info('finish estate %s init, owner=%s' %
                                 (estateId, ownerId))

                estateAI.gardenInit(avIdList)

        # Now that the zone is set up, send the notification back to
        # the client.
        self.__sendZoneToClient(avId, ownerId)
        zoneId = self.estateZone[ownerId][0]
        self._listenForToonEnterEstate(avId, ownerId, zoneId)

    ## -----------------------------------------------------------
    ## Cleanup and exit functions
    ## -----------------------------------------------------------

    def exitEstate(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        self.notify.debug("exitEstate(%s)" % avId)
        # This function is called from client in the normal case,
        # such as teleporting out, door out, exiting the game, etc
        self.__exitEstate(avId)

        self._unmapFromEstate(av)
        self._unloadEstate(av)

    def __handleUnexpectedExit(self, avId):
        self.notify.debug("we got an unexpected exit on av: %s:  deleting." % avId)
        taskMgr.remove("estateToonUp-" + str(avId))
        if avId in self.avId2pendingEnter:
            self._toonLeftBeforeArrival(avId)
        self.__exitEstate(avId)
        return None

    def __exitEstate(self, avId):
       # self.notify.debug("__exitEstate(%d)" % avId)
        # This is called whenever avId leaves an estate.
        # Determine if avId is the owner.  If so, set
        # a timer to cleanup all of the estate resources
        # and to kick all visitors out.  If we aren't the
        # owner, just remove references of avId from the estate
        avZone = self.estateZone.get(avId)
        if avZone:
            zoneId = avZone[0]
            ownerId = self.zone2owner[zoneId]
            self.announceToonExitEstate(avId, ownerId, zoneId)
            if avZone[1]:
                self.notify.debug("__exitEstate: av %d owns estate" % avId)
                # avId owns the estate
                ownerId = avId

                # warn visitors they have n seconds to finish what they were doing
                self.__warnVisitors(avZone[0])

                # start timers to kick people out and cleanup our resources
                if self.air:
                    self.ignore(self.air.getAvatarExitEvent(avId))
                taskMgr.doMethodLater(HouseGlobals.BOOT_GRACE_PERIOD,
                                      PythonUtil.Functor(self.__bootVisitorsAndCleanup, avId, avZone[0]),
                                      "bootVisitorsAndCleanup-"+str(avId))

                # remove avId references from estateZone
                self.clearEstateZone(avId)
                self.toBeDeleted[avId] = avZone
            else:
                self.notify.debug("__exitEstate: av %d doesn't own estate" % avId)
                # avId doesn't own this estate, just remove references to avId
                # from the data structures
                if avId in self.estateZone:
                    self.clearEstateZone(avId)
                try:
                    self.refCount[avZone[0]].remove(avId)
                except:
                    self.notify.debug("wasn't in refcount: %s, %s" % (avZone[0], avId))
        else:
            self.notify.debug("__exitEstate can't find zone for {0}".format(avId))

        # stop the healing
        if avId in self.air.doId2do:
            # Find the avatar
            av = self.air.doId2do[avId]
            # Stop healing them
            av.stopToonUp()

    def _cleanupEstate(self, avId, zoneId, task):
        self.notify.debug("cleanupEstate avId = %s, zoneId = %s" % (avId, zoneId))
        # we should always be cleaning up things from the toBeDeleted list,
        # not directly from estateZone

        # remove all 'hanging' entries left in estateZone
        # this is caused by:
        #   friend A is visting friend B
        #   friend B exits his estate
        #   friend C attempts to visit friend A at the same time
        for someAvId, avZone in list(self.estateZone.items()):
            if avZone[0] == zoneId:
                # This may be a slow client that just hasn't reported back.
                # If the toon is still in the zone, announce that they've
                # left before cleaning up the tables. When they report in that
                # they've left (client->AI: exitEstate), the code will not
                # find the avatar in the tables and will ignore.
                avatar = simbase.air.doId2do.get(someAvId)
                if ((avatar) and
                    (hasattr(avatar, "estateZones")) and
                    (zoneId in avatar.estateZones) and
                    (avatar.zoneId in avatar.estateZones)):
                    ownerId = self.zone2owner[zoneId]
                    self.notify.warning(
                        "forcing announcement of toon %s exit from %s %s" %
                        (someAvId, ownerId, zoneId))
                    self.announceToonExitEstate(someAvId, ownerId, zoneId)

                self.notify.warning(
                    "Manually removing (bad) entry in estateZone: %s" %
                    someAvId)
                self.clearEstateZone(someAvId)

        # give our zoneId back to the air
        self.air.deallocateZone(zoneId)
        avZone = self.toBeDeleted.get(avId)
        if avZone:
            if avZone[2] != "":
                if avZone[2] in self.account2avId:
                    self.notify.debug( "removing %s from account2avId" % avZone[2])
                    del self.account2avId[avZone[2]]
            del self.toBeDeleted[avId]
            del self.zone2owner[avZone[0]]

        # delete estate and houses from state server
        self.__deleteEstate(avId)

        # stop listening for unexpectedExit
        self.ignore(self.air.getAvatarExitEvent(avId))

        # refcount should be empty, just delete
        if zoneId in self.refCount:
            del self.refCount[zoneId]

        return Task.done

    def __stopCleanupTask(self, avId):
        self.notify.debug("stopCleanupTask %s" % avId)
        taskMgr.remove("cleanupEstate-"+str(avId))
        taskMgr.remove("bootVisitorsAndCleanup-"+str(avId))
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])


    def __deleteEstate(self, avId):
        # remove all our objects from the stateserver
        self.notify.debug("__deleteEstate(avId=%s)" % avId)

        # delete from state server
        if avId in self.estate:
            if self.estate[avId] != None:
                self.estate[avId].destroyEstateData()
                self.notify.debug('DistEstate requestDelete, doId=%s' %
                                  getattr(self.estate[avId], 'doId'))
                self.estate[avId].requestDelete()
                # This automatically gets called by the server
                # self.estate[avId].delete()
                del self.estate[avId]
        # delete the houses
        houses = self.house.get(avId)
        if houses:
            for i in range(len(houses)):
                if self.house[avId][i]:
                    self.house[avId][i].requestDelete()
                    # This automatically gets called by the server
                    # self.house[avId][i].delete()
            del self.house[avId]

    """
    def __bootVisitors(self, zoneId, task):
        try:
            visitors = self.refCount[zoneId][:]
            for avId in visitors:
                self.__bootAv(avId, zoneId)
        except:
            # refCount might have already gotten deleted
            pass
        return Task.done
    """

    def __bootVisitorsAndCleanup(self, ownerId, zoneId, task):
        try:
            visitors = self.refCount[zoneId][:]
            for avId in visitors:
                self.__bootAv(avId, zoneId, ownerId)
        except:
            # refCount might have already gotten deleted
            pass
        taskMgr.doMethodLater(HouseGlobals.CLEANUP_DELAY_AFTER_BOOT,
                              PythonUtil.Functor(self._cleanupEstate, ownerId, zoneId),
                              "cleanupEstate-"+str(ownerId))
        return Task.done

    def __bootAv(self, avId, zoneId, ownerId, retCode=1):
        messenger.send("bootAvFromEstate-"+str(avId))
        self.sendUpdateToAvatarId(avId, "sendAvToPlayground", [avId, retCode])
        if avId in self.toBeDeleted:
            del self.toBeDeleted[avId]
        try:
            self.refCount[zoneId].remove(avId)
        except:
            self.notify.debug("didn't have refCount[%s][%s]" % (zoneId,avId))
            pass

    def __warnVisitors(self, zoneId):
        visitors = self.refCount.get(zoneId)
        if visitors:
            for avId in visitors:
                self.sendUpdateToAvatarId(avId, "sendAvToPlayground", [avId, 0])

    def removeFriend(self, ownerId, avId):
        self.notify.debug("removeFriend ownerId = %s, avId = %s" % (ownerId, avId))
        # check if ownerId is in an estate
        ownZone = self.estateZone.get(ownerId)
        if ownZone:
            if ownZone[1]:
                # owner is in his own estate.  kick out avId if he is
                # in the owner's estate.
                avZone = self.estateZone.get(avId)
                if avZone:
                    if avZone[0] == ownZone[0]:
                        # avId is indeed in owner's estate.  boot him
                        self.__bootAv(avId, ownZone[0], ownerId, retCode=2)
                    else:
                        print("visitor not in owners estate")
                else:
                    print("av is not in an estate")

        else:
            print("owner not in estate")

    ## -----------------------------------------------------------
    ## April fools stuff
    ## -----------------------------------------------------------

    def startAprilFools(self):
        self.sendUpdate("startAprilFools",[])

    def stopAprilFools(self):
        self.sendUpdate("stopAprilFools",[])



    # Credit to Toontown Stride

    def _unloadEstate(self, toon):
        if getattr(toon, 'estate', None):
            estate = toon.estate
            if estate not in self.estate2timeout:
                self.estate2timeout[estate] = \
                    taskMgr.doMethodLater(HouseGlobals.BOOT_GRACE_PERIOD,
                                          self._cleanupEstate,
                                          estate.uniqueName('emai-cleanup-task'),
                                          extraArgs=[estate])
            self._sendToonsToPlayground(toon.estate, 0) # This is a warning only...

        if getattr(toon, 'loadEstateFSM', None):
            self.air.deallocateZone(toon.loadEstateFSM.zoneId)
            toon.loadEstateFSM.cancel()
            toon.loadEstateFSM = None

        self.ignore(self.air.getAvatarExitEvent(toon.doId))

    def _mapToEstate(self, toon, estate):
        self._unmapFromEstate(toon)
        self.estate2toons.setdefault(estate, []).append(toon)
        self.toon2estate[toon] = estate

        if hasattr(toon, 'enterEstate'):
            toon.enterEstate(estate.owner.doId, estate.zoneId)

    def _unmapFromEstate(self, toon):
        estate = self.toon2estate.get(toon)
        if not estate:
             return
        del self.toon2estate[toon]

        try:
            self.estate2toons[estate].remove(toon)
        except (KeyError, ValueError):
            pass
        
        if hasattr(toon, 'exitEstate'):
            toon.exitEstate()
        
    def _sendToonsToPlayground(self, estate, reason):
        for toon in self.estate2toons.get(estate, []):
            self.sendUpdateToAvatarId(toon.doId, 'sendAvToPlayground',
                                      [toon.doId, reason])

