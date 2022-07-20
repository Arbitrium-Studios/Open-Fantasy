"""DistributedLevelAI.py: contains the DistributedLevelAI class"""

from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObjectAI
from . import Level
from direct.directnotify import DirectNotifyGlobal
from . import EntityCreatorAI
from otp.otpbase.PythonUtil import Functor, weightedChoice

class DistributedLevelAI(DistributedObjectAI.DistributedObjectAI,
                         Level.Level):
    """DistributedLevelAI"""
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLevelAI')

    def __init__(self, air, zoneId, entranceId, avIds):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        Level.Level.__init__(self)
        # these are required fields
        self.zoneId = zoneId
        self.entranceId = entranceId
                      
        if len(avIds) <= 0 or len(avIds) > 4:
            self.notify.warning('How do we have this many avIds? avIds: %s' %avIds)
        assert len(avIds) > 0 and len(avIds) <= 4
        assert 0 not in avIds
        assert None not in avIds
        self.avIdList = avIds
        self.numPlayers = len(self.avIdList)
        # this is the list of avatars that are actually present
        self.presentAvIds = list(self.avIdList)
        self.notify.debug("expecting avatars: %s" % str(self.avIdList))

        if __dev__:
            self.modified = 0
            
    def setLevelSpec(self, levelSpec):
        self.levelSpec = levelSpec

    def generate(self, levelSpec = None):
        self.notify.debug('generate')
        DistributedObjectAI.DistributedObjectAI.generate(self)
        
        if levelSpec == None:
            levelSpec = self.levelSpec
    
        self.initializeLevel(levelSpec)

        # self.zoneIds comes from LevelMgrAI
        self.sendUpdate('setZoneIds', [self.zoneIds])
        self.sendUpdate('setStartTimestamp', [self.startTimestamp])
        # this is no longer used
        #self.sendUpdate('setScenarioIndex', [self.scenarioIndex])
        if __dev__:
            assert self.scenarioIndex == 0

    def getLevelZoneId(self):
        """no entities should be generated in the level's zone; it causes
        nasty race conditions on the client if there are entities in the
        same zone with the level"""
        return self.zoneId

    def getPlayerIds(self):
        return self.avIdList

    def getEntranceId(self):
        return self.entranceId

    def getBattleCreditMultiplier(self):
        return 1.

    def delete(self, deAllocZone=True):
        self.notify.debug('delete')
        if __dev__:
            self.removeAutosaveTask()
        self.destroyLevel()
        self.ignoreAll()
        if deAllocZone:
            self.air.deallocateZone(self.zoneId)
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def initializeLevel(self, levelSpec):
        # record the level's start time so that we can sync the clients
        self.startTime = globalClock.getRealTime()
        self.startTimestamp = globalClockDelta.localToNetworkTime(
            self.startTime, bits=32)

        # choose a scenario
        # make list of lists: [(weight, scenarioIndex), ...]
        lol = list(zip([1] * levelSpec.getNumScenarios(),
                  list(range(levelSpec.getNumScenarios()))))
        scenarioIndex = weightedChoice(lol)

        Level.Level.initializeLevel(self, self.doId, levelSpec, scenarioIndex)

        if __dev__:
            # listen for requests to save the spec
            self.accept(self.editMgrEntity.getSpecSaveEvent(), self.saveSpec)

        # listen for avatar disconnects
        for avId in self.avIdList:
            self.acceptOnce(self.air.getAvatarExitEvent(avId),
                            Functor(self.handleAvatarDisconnect, avId))

        # set up a barrier that will clear when all avs have left or
        # disconnected
        self.allToonsGoneBarrier = self.beginBarrier(
            'allToonsGone', self.avIdList, 3*24*60*60, self.allToonsGone)

    def handleAvatarDisconnect(self, avId):
        try:
            self.presentAvIds.remove(avId)
            DistributedLevelAI.notify.warning('av %s has disconnected' % avId)
        except:
            DistributedLevelAI.notify.warning(
                'got disconnect for av %s, not in list' % avId)
        if not self.presentAvIds:
            self.allToonsGone([])

    def allToonsGone(self, toonsThatCleared):
        DistributedLevelAI.notify.info('allToonsGone')
        if hasattr(self, 'allToonsGoneBarrier'):
            self.ignoreBarrier(self.allToonsGoneBarrier)
            del self.allToonsGoneBarrier
        for avId in self.avIdList:
            self.ignore(self.air.getAvatarExitEvent(avId))
        self.requestDelete()

    def createEntityCreator(self):
        """Create the object that will be used to create Entities.
        Inheritors, override if desired."""
        return EntityCreatorAI.EntityCreatorAI(level=self)

    def setOuch(self, penalty):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        self.notify.debug("setOuch %s" % penalty)
        # make sure penalty is > 0
        if av and (penalty > 0):
            av.takeDamage(penalty)
            # this should be done in DistributedToonAI; do we ever go sad
            # without losing our gags?
            if av.getHp() <= 0:
                av.inventory.zeroInv()
                av.d_setInventory(av.inventory.makeNetString())
        
    def requestCurrentLevelSpec(self, specHash, entTypeRegHash):
        senderId = self.air.getAvatarIdFromSender()

        self.notify.info('av %s: specHash %s, entTypeRegHash %s' %
                         (senderId, specHash, entTypeRegHash))

        if not __dev__:
            # client is running in dev mode and we're not; that won't fly
            self.notify.info("client is in dev mode and we are not")
            self.sendUpdateToAvatarId(
                senderId, 'setSpecDeny',
                ['AI server is not running in dev mode. '
                 'Set want-dev to false on your client or true on the AI.'])
            return

        # first check the typeReg hash -- if it doesn't match, the
        # client should not be connecting. Their entityTypeRegistry
        # is different from ours.
        srvHash = self.levelSpec.entTypeReg.getHashStr()
        self.notify.info('srv entTypeRegHash %s' % srvHash)
        if srvHash != entTypeRegHash:
            self.sendUpdateToAvatarId(
                senderId, 'setSpecDeny',
                ['EntityTypeRegistry hashes do not match! '
                 '(server:%s, client:%s' % (srvHash, entTypeRegHash)])
            return

        # now compare the hashes of the client and server specs
        if hash(self.levelSpec) != specHash:
            self.notify.info('spec hashes do not match, sending our spec')
            spec = self.levelSpec
            useDisk=simbase.config.GetBool('spec-by-disk', 1)
        else:
            self.notify.info('spec hashes match, sending null spec')
            spec = None
            # don't need to hit disk if we're just sending 'None' over the wire
            useDisk = 0
        specStr = repr(spec)

        from direct.directutil import DistributedLargeBlobSenderAI
        largeBlob = DistributedLargeBlobSenderAI.\
                    DistributedLargeBlobSenderAI(
            self.air, self.zoneId, senderId, specStr,
            useDisk=useDisk)
        self.sendUpdateToAvatarId(senderId,
                                  'setSpecSenderDoId', [largeBlob.doId])

    if __dev__:
        # level editors should call this func to tweak attributes of level
        # entities
        def setAttribChange(self, entId, attribName, value, username='SYSTEM'):
            DistributedLevelAI.notify.info(
                "setAttribChange(%s): %s, %s = %s" %
                (username, entId, attribName, repr(value)))
            # send a copy to the client-side level obj FIRST
            # (it may be a message that creates an entity)
            self.sendUpdate('setAttribChange',
                            [entId, attribName, repr(value), username])
            self.levelSpec.setAttribChange(entId, attribName, value, username)

            self.modified = 1
            self.scheduleAutosave()

        # backups are made every N minutes, starting from the time that
        # the first edit is made
        AutosavePeriod = simbase.config.GetFloat(
            'level-autosave-period-minutes', 5)

        def scheduleAutosave(self):
            if hasattr(self, 'autosaveTask'):
                return
            self.autosaveTaskName = self.uniqueName('autosaveSpec')
            self.autosaveTask = taskMgr.doMethodLater(
                DistributedLevelAI.AutosavePeriod * 60,
                self.autosaveSpec,
                self.autosaveTaskName)

        def removeAutosaveTask(self):
            if hasattr(self, 'autosaveTask'):
                taskMgr.remove(self.autosaveTaskName)
                del self.autosaveTask

        def autosaveSpec(self, task=None):
            self.removeAutosaveTask()
            if self.modified:
                DistributedLevelAI.notify.info('autosaving spec')
                filename = self.levelSpec.getFilename()
                filename = '%s.autosave' % filename
                self.levelSpec.saveToDisk(filename, makeBackup=0)

        def saveSpec(self, task=None):
            DistributedLevelAI.notify.info('saving spec')
            self.removeAutosaveTask()
            if not self.modified:
                DistributedLevelAI.notify.info('no changes to save')
                return
            self.levelSpec.saveToDisk()
            self.modified = 0
