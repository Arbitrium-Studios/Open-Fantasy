"""DistributedLevel.py: contains the DistributedLevel class"""

from direct.distributed.ClockDelta import *
from pandac.PandaModules import *
from otp.otpbase.PythonUtil import Functor, sameElements, list2dict, uniqueElements
from direct.interval.IntervalGlobal import *
from toontown.distributed.ToontownMsgTypes import *
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.distributed import DistributedObject
from . import Level
from . import LevelConstants
from direct.directnotify import DirectNotifyGlobal
from . import EntityCreator
from direct.gui import OnscreenText
from direct.task import Task
from . import LevelUtil
import random

class DistributedLevel(DistributedObject.DistributedObject,
                       Level.Level):
    """DistributedLevel"""
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLevel')

    WantVisibility = config.GetBool('level-visibility', 1)
    # set this to true to get all distrib objs when showing hidden zones
    ColorZonesAllDOs = 0

    # TODO: move level-model stuff to LevelMgr or FactoryLevelMgr?
    FloorCollPrefix = 'zoneFloor'

    OuchTaskName = 'ouchTask'
    VisChangeTaskName = 'visChange'

    # Override and set this to False to prevent the level from placing
    # the avatar at the origin of a random zone in the absence of an
    # entrancePoint entity.
    EmulateEntrancePoint = True

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        Level.Level.__init__(self)
        self.lastToonZone = None
        self.lastCamZone = 0
        self.titleColor = (1,1,1,1)
        self.titleText = OnscreenText.OnscreenText(
            "",
            fg = self.titleColor,
            shadow = (0,0,0,1),
            font = ToontownGlobals.getSuitFont(),
            pos = (0,-0.5),
            scale = 0.16,
            drawOrder = 0,
            mayChange = 1,
            )

        self.smallTitleText = OnscreenText.OnscreenText(
            "",
            fg = self.titleColor,
            font = ToontownGlobals.getSuitFont(),
            pos = (0.65,0.9),
            scale = 0.08,
            drawOrder = 0,
            mayChange = 1,
            bg = (.5,.5,.5,.5),
            align = TextNode.ARight,
            )
        self.titleTextSequence = None

        self.zonesEnteredList = []
        self.fColorZones = 0
        self.scenarioIndex = 0

    def generate(self):
        DistributedLevel.notify.debug('generate')
        DistributedObject.DistributedObject.generate(self)

        # this dict stores entity reparents if the parent hasn't been
        # created yet
        self.parent2pendingChildren = {}

        # if the AI sends us a full spec, it will be put here
        self.curSpec = None

        # Most (if not all) of the timed entities of levels
        # run on looping intervals that are started once based on
        # the level's start time.
        # This sync request is *NOT* guaranteed to finish by the time
        # the entities get created.
        # We should listen for any and all time-sync events and re-sync
        # all our entities at that time.
        if base.cr.timeManager is not None:
            base.cr.timeManager.synchronize('DistributedLevel.generate')
        else:
            self.notify.warning('generate(): no TimeManager!')


    # the real required fields
    def setLevelZoneId(self, zoneId):
        # this is the zone that the level is in; we should listen to this
        # zone the entire time we're in here
        self.levelZone = zoneId

    def setPlayerIds(self, avIdList):
        self.avIdList = avIdList
        assert base.localAvatar.doId in self.avIdList

    def setEntranceId(self, entranceId):
        self.entranceId = entranceId

    def getEntranceId(self):
        return self.entranceId

    # "required" fields (these ought to be required fields, but
    # the AI level obj doesn't know the data values until it has been
    # generated.)
    def setZoneIds(self, zoneIds):
        DistributedLevel.notify.debug('setZoneIds: %s' % zoneIds)
        self.zoneIds = zoneIds

    def setStartTimestamp(self, timestamp):
        DistributedLevel.notify.debug('setStartTimestamp: %s' % timestamp)
        self.startTime = globalClockDelta.networkToLocalTime(timestamp,bits=32)

        # ugly hack: we treat a few DC fields as if they were required,
        # and use 'levelAnnounceGenerate()' in place of regular old
        # announceGenerate(). Note that we have to call
        # gotAllRequired() in the last 'faux-required' DC update
        # handler. If you add another field, move this to the last one.
        self.privGotAllRequired()

        """
        # this is no longer used
    def setScenarioIndex(self, scenarioIndex):
        self.scenarioIndex = scenarioIndex

        # ugly hack: we treat a few DC fields as if they were required,
        # and use 'levelAnnounceGenerate()' in place of regular old
        # announceGenerate(). Note that we have to call
        # gotAllRequired() in the last 'faux-required' DC update
        # handler. If you add another field, move this to the last one.
        self.privGotAllRequired()
        """

    def privGotAllRequired(self):
        self.levelAnnounceGenerate()
    def levelAnnounceGenerate(self):
        pass

    def initializeLevel(self, levelSpec):
        """subclass should call this as soon as it's located its level spec.
        Must be called after obj has been generated."""
        if __dev__:
            # if we're in dev, give the server the opportunity to send us
            # a full spec
            self.candidateSpec = levelSpec
            self.sendUpdate('requestCurrentLevelSpec',
                            [hash(levelSpec),
                             levelSpec.entTypeReg.getHashStr()])
        else:
            self.privGotSpec(levelSpec)

    if __dev__:
        def reportModelSpecSyncError(self, msg):
            DistributedLevel.notify.error(
                '%s\n'
                '\n'
                'your spec does not match the level model\n'
                'use SpecUtil.updateSpec, then restart your AI and client' %
                (msg))

        def setSpecDeny(self, reason):
            DistributedLevel.notify.error(reason)
            
        def setSpecSenderDoId(self, doId):
            DistributedLevel.notify.debug('setSpecSenderDoId: %s' % doId)
            blobSender = base.cr.doId2do[doId]

            def setSpecBlob(specBlob, blobSender=blobSender, self=self):
                blobSender.sendAck()
                from .LevelSpec import LevelSpec
                spec = eval(specBlob)
                if spec is None:
                    spec = self.candidateSpec
                del self.candidateSpec
                self.privGotSpec(spec)

            if blobSender.isComplete():
                setSpecBlob(blobSender.getBlob())
            else:
                evtName = self.uniqueName('specDone')
                blobSender.setDoneEvent(evtName)
                self.acceptOnce(evtName, setSpecBlob)

    def privGotSpec(self, levelSpec):
        Level.Level.initializeLevel(self, self.doId, levelSpec,
                                    self.scenarioIndex)

        # all of the local entities have been created now.
        # TODO: have any of the distributed entities been created at this point?

        # there should not be any pending reparents left at this point
        # TODO: is it possible for a local entity to be parented to a
        # distributed entity? I think so!
        # Yes, it is. Don't do this check.
        #assert len(self.parent2pendingChildren) == 0
        # make sure the zoneNums from the model match the zoneNums from
        # the zone entities
        modelZoneNums = self.zoneNums
        specZoneNums = list(self.zoneNum2zoneId.keys())
        if not sameElements(modelZoneNums, specZoneNums):
            self.reportModelSpecSyncError(
                'model zone nums (%s) do not match spec zone nums (%s)' %
                (modelZoneNums, specZoneNums))

        # load stuff
        self.initVisibility()
        self.placeLocalToon()

    def announceLeaving(self):
        """call this just before leaving the level; this may result in
        the factory being destroyed on the AI"""
        DistributedLevel.notify.debug('announceLeaving')
        self.doneBarrier()

    def placeLocalToon(self, moveLocalAvatar=True):
        initialZoneEnt = None
        # the entrancePoint entities register themselves with us
        if self.entranceId in self.entranceId2entity:
            epEnt = self.entranceId2entity[self.entranceId]
            if moveLocalAvatar:
                epEnt.placeToon(base.localAvatar,
                                self.avIdList.index(base.localAvatar.doId),
                                len(self.avIdList))
            initialZoneEnt = self.getEntity(epEnt.getZoneEntId())
        elif self.EmulateEntrancePoint:
            self.notify.debug('unknown entranceId %s' % self.entranceId)
            if moveLocalAvatar:
                base.localAvatar.reparentTo(render)
                base.localAvatar.setPosHpr(0,0,0,0,0,0)
            self.notify.debug('showing all zones')
            self.setColorZones(1)
            # put the toon in a random zone to start
            zoneEntIds = list(self.entType2ids['zone'])
            zoneEntIds.remove(LevelConstants.UberZoneEntId)
            if len(zoneEntIds):
                zoneEntId = random.choice(zoneEntIds)
                initialZoneEnt = self.getEntity(zoneEntId)
                if moveLocalAvatar:
                    base.localAvatar.setPos(
                        render,
                        initialZoneEnt.getZoneNode().getPos(render))
            else:
                initialZoneEnt = self.getEntity(
                    LevelConstants.UberZoneEntId)
                if moveLocalAvatar:
                    base.localAvatar.setPos(render,0,0,0)

        if initialZoneEnt is not None:
            # kickstart the visibility
            self.enterZone(initialZoneEnt.entId)

    def createEntityCreator(self):
        """Create the object that will be used to create Entities.
        Inheritors, override if desired."""
        return EntityCreator.EntityCreator(level=self)

    def onEntityTypePostCreate(self, entType):
        """listen for certain entity types to be created"""
        Level.Level.onEntityTypePostCreate(self, entType)
        # NOTE: these handlers are private in order to avoid overriding
        # similar handlers in base classes
        if entType == 'levelMgr':
            self.__handleLevelMgrCreated()

    def __handleLevelMgrCreated(self):
        # as soon as the levelMgr has been created, load up the model
        # and extract zone info. We need to do this before any entities
        # get parented to the level!
        levelMgr = self.getEntity(LevelConstants.LevelMgrEntId)
        self.geom = levelMgr.geom

        # find the zones in the model and fix them up
        self.zoneNum2node = LevelUtil.getZoneNum2Node(self.geom)

        self.zoneNums = list(self.zoneNum2node.keys())
        self.zoneNums.sort()
        self.zoneNumDict = list2dict(self.zoneNums)
        DistributedLevel.notify.debug('zones from model: %s' % self.zoneNums)

        # give the level a chance to muck with the model before the entities
        # get placed
        self.fixupLevelModel()
        
    def fixupLevelModel(self):
        # fix up the floor collisions for walkable zones *before*
        # any entities get put under the model
        for zoneNum,zoneNode in list(self.zoneNum2node.items()):
            # don't do this to the uberzone
            if zoneNum == LevelConstants.UberZoneEntId:
                continue
            # if this is a walkable zone, fix up the model
            allColls = zoneNode.findAllMatches('**/+CollisionNode')
            # which of them, if any, are floors?
            floorColls = []
            for coll in allColls:
                bitmask = coll.node().getIntoCollideMask()
                if not (bitmask & ToontownGlobals.FloorBitmask).isZero():
                    floorColls.append(coll)
            if len(floorColls) > 0:
                # rename the floor collision nodes, and make sure no other
                # nodes under the ZoneNode have that name
                floorCollName = '%s%s' % (DistributedLevel.FloorCollPrefix,
                                          zoneNum)
                others = zoneNode.findAllMatches(
                    '**/%s' % floorCollName)
                for other in others:
                    other.setName('%s_renamed' % floorCollName)
                for floorColl in floorColls:
                    floorColl.setName(floorCollName)

                # listen for zone enter events from floor collisions
                def handleZoneEnter(collisionEntry,
                                    self=self, zoneNum=zoneNum):
                    self.toonEnterZone(zoneNum)
                    floorNode = collisionEntry.getIntoNode()
                    if floorNode.hasTag('ouch'):
                        ouchLevel = int(self.getFloorOuchLevel())
                        self.startOuch(ouchLevel)
                self.accept('enter%s' % floorCollName, handleZoneEnter)

                # also listen for zone exit events for the sake of the
                # ouch system
                def handleZoneExit(collisionEntry,
                                   self=self, zoneNum=zoneNum):
                    floorNode = collisionEntry.getIntoNode()
                    if floorNode.hasTag('ouch'):
                        self.stopOuch()
                self.accept('exit%s' % floorCollName, handleZoneExit)

    def getFloorOuchLevel(self):
        # override this to make dangerous ground do more damage
        return 1
    
    def announceGenerate(self):
        DistributedLevel.notify.debug('announceGenerate')
        DistributedObject.DistributedObject.announceGenerate(self)

    def disable(self):
        DistributedLevel.notify.debug('disable')

        # geom is owned by the levelMgr
        if hasattr(self, 'geom'):
            del self.geom

        self.shutdownVisibility()
        self.destroyLevel()
        self.ignoreAll()

        # NOTE:  this should be moved to FactoryInterior
        if self.titleTextSequence:
            self.titleTextSequence.finish()
            self.titleTextSequence = None
        if self.smallTitleText:
            self.smallTitleText.cleanup()
            self.smallTitleText = None
        if self.titleText:
            self.titleText.cleanup()
            self.titleText = None
        self.zonesEnteredList = []

        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        DistributedLevel.notify.debug('delete')
        DistributedObject.DistributedObject.delete(self)
        # make sure the ouch task is stopped
        self.stopOuch()
        
    def requestReparent(self, entity, parentId, wrt=False):
        if __debug__:
            # some things (like cogs) are not actually entities yet;
            # they don't have an entId. Big deal, let it go through.
            if hasattr(entity, 'entId'):
                assert entity.entId != parentId
        parent = self.getEntity(parentId)
        if parent is not None:
            # parent has already been created
            if wrt:
                entity.wrtReparentTo(parent.getNodePath())
            else:
                entity.reparentTo(parent.getNodePath())
        else:
            # parent hasn't been created yet; schedule the reparent
            DistributedLevel.notify.debug(
                'entity %s requesting reparent to %s, not yet created' %
                (entity, parentId))

            entity.reparentTo(hidden)

            # if this parent doesn't already have another child pending,
            # do some setup
            if parentId not in self.parent2pendingChildren:
                self.parent2pendingChildren[parentId] = []

                # do the reparent(s) once the parent is initialized
                def doReparent(parentId=parentId, self=self, wrt=wrt):
                    assert parentId in self.parent2pendingChildren
                    parent=self.getEntity(parentId)
                    for child in self.parent2pendingChildren[parentId]:
                        DistributedLevel.notify.debug(
                            'performing pending reparent of %s to %s' %
                            (child, parent))
                        if wrt:
                            child.wrtReparentTo(parent.getNodePath())
                        else:
                            child.reparentTo(parent.getNodePath())
                    del self.parent2pendingChildren[parentId]
                    self.ignore(self.getEntityCreateEvent(parentId))
                    
                self.accept(self.getEntityCreateEvent(parentId), doReparent)

            self.parent2pendingChildren[parentId].append(entity)
    
    def getZoneNode(self, zoneEntId):
        return self.zoneNum2node.get(zoneEntId)

    def warpToZone(self, zoneNum):
        """put avatar at the origin of the given zone"""
        zoneNode = self.getZoneNode(zoneNum)
        if zoneNode is None:
            return
        base.localAvatar.setPos(zoneNode,0,0,0)
        base.localAvatar.setHpr(zoneNode,0,0,0)
        self.enterZone(zoneNum)

    def showZone(self, zoneNum):
        zone = self.getZoneNode(zoneNum)
        zone.unstash()
        zone.clearColor()

    def setColorZones(self, fColorZones):
        self.fColorZones = fColorZones
        self.resetVisibility()

    def getColorZones(self):
        return self.fColorZones

    def hideZone(self, zoneNum):
        zone = self.getZoneNode(zoneNum)
        if self.fColorZones:
            zone.unstash()
            zone.setColor(1,0,0)
        else:
            zone.stash()

    def setTransparency(self, alpha, zone=None):
        self.geom.setTransparency(1)
        if zone is None:
            node = self.geom
        else:
            node = self.getZoneNode(zoneNum)
        node.setAlphaScale(alpha)

    def initVisibility(self):
        # start out with every zone visible, since none of the zones have
        # been hidden
        self.curVisibleZoneNums = list2dict(self.zoneNums)
        # the UberZone is always visible, so it's not included in the
        # zones' viz lists
        del self.curVisibleZoneNums[LevelConstants.UberZoneEntId]
        # we have not entered any zone yet
        self.curZoneNum = None

        self.visChangedThisFrame = 0
        self.fForceSetZoneThisFrame = 0

        # listen for camera-ray/floor collision events
        def handleCameraRayFloorCollision(collEntry, self=self):
            name = collEntry.getIntoNode().getName()
            self.notify.debug('camera floor ray collided with: %s' % name)
            prefixLen = len(DistributedLevel.FloorCollPrefix)
            if (name[:prefixLen] == DistributedLevel.FloorCollPrefix):
                try:
                    zoneNum = int(name[prefixLen:])
                except:
                    DistributedLevel.notify.warning(
                        'Invalid zone floor collision node: %s'
                        % name)
                else:
                    self.camEnterZone(zoneNum)
        self.accept('on-floor', handleCameraRayFloorCollision)

        # if no viz, listen to all the zones
        if not DistributedLevel.WantVisibility:
            zoneNums = list(self.zoneNums)
            zoneNums.remove(LevelConstants.UberZoneEntId)
            # make sure a setZone goes out on the first frame
            self.forceSetZoneThisFrame()
            self.setVisibility(zoneNums)

        # send out any zone changes at the end of the frame, just before
        # rendering
        taskMgr.add(self.visChangeTask,
                    self.uniqueName(DistributedLevel.VisChangeTaskName),
                    priority=49)

    def shutdownVisibility(self):
        taskMgr.remove(self.uniqueName(DistributedLevel.VisChangeTaskName))

    def toonEnterZone(self, zoneNum, ouchLevel=None):
        """
        zoneNum is an int.
        ouchLevel is a ??.
        
        The avatar (and not necessarily the camera) has entered
        a zone.
        See camEnterZone()
        """
        DistributedLevel.notify.debug('toonEnterZone%s' % zoneNum)

        if zoneNum != self.lastToonZone:
            self.lastToonZone = zoneNum
            self.notify.debug("toon is standing in zone %s" % zoneNum)
            messenger.send("factoryZoneChanged", [zoneNum])

    def camEnterZone(self, zoneNum):
        """
        zoneNum is an int.
        
        The camera (and not necessarily the avatar) has entered
        a zone.
        See toonEnterZone()
        """
        DistributedLevel.notify.debug('camEnterZone%s' % zoneNum)
        self.enterZone(zoneNum)

        if zoneNum != self.lastCamZone:
            self.lastCamZone = zoneNum
            self.smallTitleText.hide()
            self.spawnTitleText()

    def lockVisibility(self, zoneNum=None, zoneId=None):
        """call this to lock the visibility to a particular zone
        pass in either network zoneId or zoneNum

        this was added for battles in the HQ factories; if you engage a suit
        in zone A with your camera in zone B, and you don't call this func,
        your client will remain in zone B. If there's a door between A and B,
        and it closes, zone B might disappear, along with the suit and the
        battle objects.
        """
        assert zoneNum is None or zoneId is None
        assert not ((zoneNum is None) and (zoneId is None))
        if zoneId is not None:
            zoneNum = self.getZoneNumFromId(zoneId)

        self.notify.debug('lockVisibility to zoneNum %s' % zoneNum)
        self.lockVizZone = zoneNum
        self.enterZone(self.lockVizZone)

    def unlockVisibility(self):
        """release the visibility lock"""
        self.notify.debug('unlockVisibility')
        if not hasattr(self, 'lockVizZone'):
            self.notify.warning('visibility already unlocked')
        else:
            del self.lockVizZone
            self.updateVisibility()
            

    def enterZone(self, zoneNum):
        DistributedLevel.notify.debug("entering zone %s" % zoneNum)

        if not DistributedLevel.WantVisibility:
            return
        
        if zoneNum == self.curZoneNum:
            return

        if zoneNum not in self.zoneNumDict:
            DistributedLevel.notify.error(
                'no ZoneEntity for this zone (%s)!!' % zoneNum)

        self.updateVisibility(zoneNum)

    def updateVisibility(self, zoneNum=None):
        """update the visibility assuming that we're in the specified
        zone; don't check to see if it's the zone we're already in"""
        #self.notify.debug('updateVisibility %s' % globalClock.getFrameCount())
        if zoneNum is None:
            zoneNum = self.curZoneNum
            if zoneNum is None:
                return
        if hasattr(self, 'lockVizZone'):
            zoneNum = self.lockVizZone
            
        zoneEnt = self.getEntity(zoneNum)
        # use dicts to efficiently ensure that there are no duplicates
        visibleZoneNums = list2dict([zoneNum])
        visibleZoneNums.update(list2dict(zoneEnt.getVisibleZoneNums()))

        if not __debug__:
            # HACK
            # make sure that the visibility list includes the zone that the toon
            # is standing in
            if self.lastToonZone not in visibleZoneNums:
                # make sure there IS a last zone
                if self.lastToonZone is not None:
                    self.notify.warning(
                        'adding zoneNum %s to visibility list '
                        'because toon is standing in that zone!' %
                        self.lastToonZone)
                    visibleZoneNums.update(list2dict([self.lastToonZone]))

        # we should not have the uberZone in the list at this point
        zoneEntIds = list(self.entType2ids['zone'])
        zoneEntIds.remove(LevelConstants.UberZoneEntId)
        if len(zoneEntIds):
            assert not LevelConstants.UberZoneEntId in visibleZoneNums

        # this flag will prevent a network msg from being sent if
        # the list of visible zones has not changed
        vizZonesChanged = 1
        # figure out which zones are new and which are going invisible
        # use dicts because 'x in dict' is faster than 'x in list'
        addedZoneNums = []
        removedZoneNums = []
        allVZ = dict(visibleZoneNums)
        allVZ.update(self.curVisibleZoneNums)
        for vz,dummy in list(allVZ.items()):
            new = vz in visibleZoneNums
            old = vz in self.curVisibleZoneNums
            if new and old:
                continue
            if new:
                addedZoneNums.append(vz)
            else:
                removedZoneNums.append(vz)

        if (not addedZoneNums) and (not removedZoneNums):
            DistributedLevel.notify.debug(
                'visible zone list has not changed')
            vizZonesChanged = 0
        else:
            # show the new, hide the old
            DistributedLevel.notify.debug('showing zones %s' %
                                          addedZoneNums)
            for az in addedZoneNums:
                self.showZone(az)
            DistributedLevel.notify.debug('hiding zones %s' %
                                          removedZoneNums)
            for rz in removedZoneNums:
                self.hideZone(rz)

        # it's important for us to send a setZone request on the first
        # frame, whether or not the visibility is different from what
        # we already have
        if vizZonesChanged or self.fForceSetZoneThisFrame:
            self.setVisibility(list(visibleZoneNums.keys()))
            self.fForceSetZoneThisFrame = 0

        self.curZoneNum = zoneNum
        self.curVisibleZoneNums = visibleZoneNums

    def setVisibility(self, vizList):
        """
        vizList is a list of visible zone numbers.
        """
        # if we're showing all zones, get all the DOs
        if self.fColorZones and DistributedLevel.ColorZonesAllDOs:
            vizList = list(self.zoneNums)
            vizList.remove(LevelConstants.UberZoneEntId)
        # convert the zone numbers into their actual zoneIds
        # always include Toontown and factory uberZones
        uberZone = self.getZoneId(LevelConstants.UberZoneEntId)
        # the level itself is in the 'level zone'
        visibleZoneIds = [OTPGlobals.UberZone, self.levelZone, uberZone]
        for vz in vizList:
            if vz is not LevelConstants.UberZoneEntId:
                visibleZoneIds.append(self.getZoneId(vz))
        assert uniqueElements(visibleZoneIds)
        DistributedLevel.notify.debug('new viz list: %s' % visibleZoneIds)

        base.cr.sendSetZoneMsg(self.levelZone, visibleZoneIds)

    def resetVisibility(self):
        # start out with every zone visible, since none of the zones have
        # been hidden
        self.curVisibleZoneNums = list2dict(self.zoneNums)
        # the UberZone is always visible, so it's not included in the
        # zones' viz lists
        del self.curVisibleZoneNums[LevelConstants.UberZoneEntId]
        # Make sure every zone is visible
        for vz,dummy in list(self.curVisibleZoneNums.items()):
            self.showZone(vz)
        # Redo visibility using current zone num
        self.updateVisibility()

    def handleVisChange(self):
        """the zone visibility lists have changed on-the-fly"""
        Level.Level.handleVisChange(self)
        self.visChangedThisFrame = 1

    def forceSetZoneThisFrame(self):
        # call this to ensure that a setZone call will be generated this frame
        self.fForceSetZoneThisFrame = 1

    def visChangeTask(self, task):
        # this runs just before igLoop; if viz lists have changed
        # this frame, updates the visibility and sends out a setZoneMsg
        if self.visChangedThisFrame or self.fForceSetZoneThisFrame:
            self.updateVisibility()
            self.visChangedThisFrame = 0
        return Task.cont

    if __dev__:
        # level editing stuff
        def setAttribChange(self, entId, attribName, valueStr, username):
            """every time the spec is edited, we get this message
            from the AI"""
            value = eval(valueStr)
            self.levelSpec.setAttribChange(entId, attribName, value, username)

    def spawnTitleText(self):
        def getDescription(zoneNum, self=self):
            ent = self.entities.get(zoneNum)
            if ent and hasattr(ent, 'description'):
                return ent.description
            return None

        description = getDescription(self.lastCamZone)
        if description and description != '':
            if self.titleTextSequence:
                self.titleTextSequence.finish()
                self.titleTextSequence = None
            self.smallTitleText.setText(description)
            self.titleText.setText(description)
            self.titleText.setColor(Vec4(*self.titleColor))
            self.titleText.setFg(self.titleColor)

            # Only show the big title once per session.
            # If we've already seen it, just show the small title

            titleSeq = None
            if not self.lastCamZone in self.zonesEnteredList:
                self.zonesEnteredList.append(self.lastCamZone)
                titleSeq = Sequence(
                    Func(self.hideSmallTitleText),
                    Func(self.showTitleText),
                    Wait(0.1),
                    Wait(6.0),
                    self.titleText.colorInterval(0.5, Vec4(self.titleColor[0],
                                                  self.titleColor[1],
                                                  self.titleColor[2],
                                                  self.titleColor[3]),
                                                  
                                             startColor=Vec4(self.titleColor[0],
                                                  self.titleColor[1],
                                                  self.titleColor[2],
                                                  0.0)
                    ))
            smallTitleSeq = Sequence(Func(self.hideTitleText),
                                          Func(self.showSmallTitle))
            if titleSeq:
                self.titleTextSequence = Sequence(titleSeq, smallTitleSeq,  name=self.uniqueName('titleText'))
            else:
                self.titleTextSequence = Sequence(smallTitleSeq, name=self.uniqueName('titleText'))
            self.titleTextSequence.start()
            
            
    def showInfoText(self, text = "hello world"):
        description = text
        if description and description != '':
            if self.titleTextSeq:
                self.titleTextSeq.finish()
                self.titleTextSeq = None
            self.smallTitleText.setText(description)
            self.titleText.setText(description)
            self.titleText.setColor(Vec4(*self.titleColor))
            self.titleText.setFg(self.titleColor)

            # Only show the big title once per session.
            # If we've already seen it, just show the small title

            titleSeq = None
            titleSeq = Sequence(
                Func(self.hideSmallTitle),
                Func(self.showTitleText),
                Wait(0.1),
                Wait(3.0),
                self.titleText.colorInterval(0.5, Vec4(self.titleColor[0],
                                              self.titleColor[1],
                                              self.titleColor[2],
                                              self.titleColor[3]), 
                                         startColor= Vec4(self.titleColor[0],
                                              self.titleColor[1],
                                              self.titleColor[2],
                                              0.0)
                ))

            if titleSeq:
               self.titleTextSequence = Sequence(titleSeq, self.uniqueName("titleText"))
            self.titleTextSeq.start()
        
    def showTitleText(self):
        assert DistributedLevel.notify.debug("hideTitleTextTask()")
        self.titleText.show()

    def hideTitleText(self):
        assert DistributedLevel.notify.debug("hideTitleTextTask()")
        if self.titleText:
            self.titleText.hide()

    def showSmallTitle(self):
        # make sure large title is hidden
        if self.titleText:
            self.titleText.hide()
        # show the small title
        self.smallTitleText.show()

    
    def hideSmallTitleText(self):
        assert DistributedLevel.notify.debug("hideTitleTextTask()")
        if self.smallTitleText:
            self.smallTitleText.hide()


    # Ouch!
    def startOuch(self, ouchLevel, period=2):
        self.notify.debug('startOuch %s' % ouchLevel)
        if not hasattr(self, 'doingOuch'):
            def doOuch(task, self=self, ouchLevel=ouchLevel, period=period):
                self.b_setOuch(ouchLevel)
                self.lastOuchTime = globalClock.getFrameTime()
                taskMgr.doMethodLater(period, doOuch,
                                      DistributedLevel.OuchTaskName)

            # check to make sure we haven't done an ouch too recently
            delay = 0
            if hasattr(self, 'lastOuchTime'):
                curFrameTime = globalClock.getFrameTime()
                timeSinceLastOuch = (curFrameTime - self.lastOuchTime)
                if timeSinceLastOuch < period:
                    delay = period - timeSinceLastOuch

            if delay > 0:
                taskMgr.doMethodLater(
                        period, doOuch,
                        DistributedLevel.OuchTaskName)
            else:
                doOuch(None)
            self.doingOuch = 1

    def stopOuch(self):
        if hasattr(self, 'doingOuch'):
            taskMgr.remove(DistributedLevel.OuchTaskName)
            del self.doingOuch

    def b_setOuch(self, penalty, anim=None):
        self.notify.debug('b_setOuch %s' % penalty)
        av = base.localAvatar

        # play the stun track (flashing toon) 
        if not av.isStunned:
            self.d_setOuch(penalty)
            self.setOuch(penalty, anim)

    def d_setOuch(self, penalty):
        self.sendUpdate("setOuch", [penalty])

    def setOuch(self, penalty, anim = None):
        if anim == "Squish":
            if base.cr.playGame.getPlace():
                base.cr.playGame.getPlace().fsm.request('squished')
        elif anim == "Fall":
            if base.cr.playGame.getPlace():
                base.cr.playGame.getPlace().fsm.request('fallDown')
            
        av = base.localAvatar
        av.stunToon()
        av.playDialogueForString("!")
        
    def complexVis(self):
        return 1
