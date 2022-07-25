from panda3d.core import *
from toontown.toonbase.ToontownGlobals import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from toontown.safezone import SafeZoneLoader
import random
from toontown.launcher import DownloadForceAcknowledge
from toontown.estate import House
from toontown.estate import Estate
from toontown.estate import HouseGlobals
import random
import math
from toontown.coghq import MovingPlatform
from direct.directnotify import DirectNotifyGlobal

class EstateLoader(SafeZoneLoader.SafeZoneLoader):
    """
    EstateLoader class
    """

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateLoader")
    
    # special methods

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        del self.fsm
        self.fsm = ClassicFSM.ClassicFSM('EstateLoader', [State.State('start', self.enterStart, self.exitStart, ['quietZone', 'estate', 'house']),
         State.State('estate', self.enterEstate, self.exitEstate, ['quietZone']),
         State.State('house', self.enterHouse, self.exitHouse, ['quietZone']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['house', 'estate']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')
        self.musicFile = 'phase_5.5/audio/bgm/estate_theme.ogg'
        self.activityMusicFile = 'phase_5.5/audio/bgm/estate_interior.ogg'
        self.dnaFile = 'phase_5.5/dna/estate_1.dna'
        self.safeZoneStorageDNAFile = None
        
        self.cloudSwitch = 0
        
        self.id = MyEstate
        self.estateOwnerId = None
        self.branchZone = None        
        self.houseDoneEvent = "houseDone"
        self.estateDoneEvent = "estateDone"
        #self.estateDNAFile = "phase_5.5/dna/estate_1.dna"
        #self.estateStorageDNAFile = "phase_5.5/dna/storage_estate.dna"
        self.enteredHouse = None
        self.houseNode = [None] * 6
        self.houseModels = [None] * HouseGlobals.NUM_HOUSE_TYPES
        self.houseId2house = {}
        self.barrel = None
        self.clouds = []
        self.cloudTrack = None
        self.sunMoonNode = None
        self.fsm.enterInitialState()
        
    def load(self):
        assert(self.notify.debug("load()"))
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.music = base.loader.loadMusic(self.musicFile)
        self.houseMusic = base.loader.loadMusic(self.activityMusicFile)
        self.underwaterSound = base.loader.loadSfx('phase_4/audio/sfx/AV_ambient_water.ogg')
        self.swimSound = base.loader.loadSfx('phase_4/audio/sfx/AV_swim_single_stroke.ogg')
        self.submergeSound = base.loader.loadSfx('phase_5.5/audio/sfx/AV_jump_in_water.ogg')
        self.birdSound = map(base.loader.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg', 'phase_4/audio/sfx/SZ_TC_bird2.ogg', 'phase_4/audio/sfx/SZ_TC_bird3.ogg'])
        self.cricketSound = map(base.loader.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg', 'phase_4/audio/sfx/SZ_TC_bird2.ogg', 'phase_4/audio/sfx/SZ_TC_bird3.ogg'])
        if base.goonsEnabled:
            #self.testHouse = loader.loadModel("phase_5.5/models/estate/houseA.bam")
            #self.testHouse.reparentTo(self.geom)
            #self.testHouse.setPos(-130,-30,0.025)
            #self.testHouse.setScale(.7)
            # for gag bin testing:
            invModel = loader.loadModel("phase_3.5/models/gui/inventory_icons")
            # Find all the inventory models and cache them
            self.invModels = []
            from toontown.toonbase import ToontownBattleGlobals
            for track in xrange(len(ToontownBattleGlobals.AvPropsNew)):
                itemList = []
                for item in xrange(len(ToontownBattleGlobals.AvPropsNew[track])):
                    itemList.append(invModel.find('**/' + ToontownBattleGlobals.AvPropsNew[track][item]))

                self.invModels.append(itemList)
            invModel.removeNode()
            #self.feather = self.invModels[0][0]
            #self.feather.reparentTo(self.testHouse)
            del invModel
        
    def unload(self):
        assert(self.notify.debug("unload()"))
        self.ignoreAll()

        # release the estate zone
        # remove ourselves from the current estate
        base.cr.estateMgr.leaveEstate()
        
        self.estateOwnerId = None
        self.estateZoneId = None
        if self.place:
            self.place.exit()
            self.place.unload()
            del self.place
        del self.underwaterSound
        del self.swimSound
        del self.submergeSound
        del self.birdSound
        del self.cricketSound

        for node in self.houseNode:
            node.removeNode()
        del self.houseNode
        for model in self.houseModels:
            model.removeNode()
        del self.houseModels
        del self.houseId2house
        if self.sunMoonNode:
            self.sunMoonNode.removeNode()
            del self.sunMoonNode
            self.sunMoonNode = None
        if self.clouds:
            for cloud in self.clouds:
                cloud[0].removeNode()
                #cloud[0].destroy()
                del cloud[1]
            del self.clouds
        if self.barrel:
            self.barrel.removeNode()
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def enter(self, requestStatus):
        self.estateOwnerId = requestStatus.get('ownerId', base.localAvatar.doId)
        base.localAvatar.inEstate = 1
        # load up the cloud platforms
        self.loadCloudPlatforms()
        if base.cloudPlatformsEnabled and 0:
            self.setCloudSwitch(1)
            pass
        if self.cloudSwitch:
            self.setCloudSwitch(self.cloudSwitch)
            
            
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        assert(self.notify.debug("exit()"))
        self.ignoreAll()
        base.cr.cache.flush()
        base.localAvatar.stopChat()
        base.localAvatar.inEstate = 0
        SafeZoneLoader.SafeZoneLoader.exit(self)

    def createSafeZone(self, dnaFile):
        assert(self.notify.debug("createEstate()"))
        SafeZoneLoader.SafeZoneLoader.createSafeZone(self,dnaFile)

        # load the houses now
        self.loadHouses()

        # load the sun and moon
        self.loadSunMoon()
        
    """
    # DCR: this function doesn't seem to be used
    def createEstate(self, dnaFile):
        # This function is copied from SafeZoneLoader.  It would be nice
        # to have one function that does this for both SafeZoneLoader
        # and EstateLoader.  First though, just keep this function
        # simple, and then consolidate later if applicable.
        assert(self.notify.debug("createEstate()"))
        # Create a DNA Store
        self.dnaStore = DNAStorage()
        # We'd rather share the font models where possible, so
        # we'll replace some of the fonts the dna store loaded
        # with the corresponding fonts we already have in memory.
        self.dnaStore.storeFont("humanist", getInterfaceFont())
        self.dnaStore.storeFont("mickey", getSignFont())
        # Load the safe zone specific models and textures
        loader.loadDNAFile(self.dnaStore, self.estateStorageDNAFile)
        # Load the actual safe zone dna
        self.notify.debug( "Loading dnaFile = %s " % dnaFile)
        node = loader.loadDNAFile(self.dnaStore, dnaFile)

        if node.getNumParents() == 1:
            # If the node already has a parent arc when it's loaded, we must
            # be using the level editor and we want to preserve that arc.
            self.geom = NodePath(node.getParent(0))
            self.geom.reparentTo(hidden)
        else:
            # Otherwise, we should create a new arc for the node.
            self.geom = hidden.attachNewNode(node)
        # Make the vis dictionaries
        self.makeDictionaries(self.dnaStore)
        self.createAnimatedProps(self.nodeList)
        # Flatten the safe zone
        self.geom.flattenMedium()
        
        # Preload all textures in neighborhood
        gsg = base.win.getGsg()
        if gsg:
            self.geom.prepareScene(gsg)

        # load the houses now
        self.loadHouses()
    """
            
    def loadHouses(self):
        for i in xrange(HouseGlobals.NUM_HOUSE_TYPES):
            self.houseModels[i] = loader.loadModel(HouseGlobals.houseModels[i])

        for i in xrange(6):
            posHpr = HouseGlobals.houseDrops[i]
            self.houseNode[i] = self.geom.attachNewNode("esHouse_"+str(i))
            self.houseNode[i].setPosHpr(*posHpr)


    def loadSunMoon(self):
        self.sun = loader.loadModel("phase_4/models/props/sun.bam")
        self.moon = loader.loadModel("phase_5.5/models/props/moon.bam")
        # create a new node to hold the sun and moon. just set the pitch according to daytime
        self.sunMoonNode = self.geom.attachNewNode("sunMoon")
        self.sunMoonNode.setPosHpr(0,0,0,0,0,0)
        if self.sun:
            self.sun.reparentTo(self.sunMoonNode)
            self.sun.setY(270)
            self.sun.setScale(2)
            self.sun.setBillboardPointEye()
        if self.moon:
            self.moon.setP(180)
            self.moon.reparentTo(self.sunMoonNode)
            self.moon.setY(-270)
            self.moon.setScale(15)
            self.moon.setBillboardPointEye()

        # start out at day time
        self.sunMoonNode.setP(30)

    """
    def makeDictionaries(self, dnaStore):
        assert(self.notify.debug("makeDictionaries()"))
        # A list of all visible nodes
        self.nodeList = []
        # There should only be one vis group
        for i in range(dnaStore.getNumDNAVisGroups()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            groupName = base.cr.hoodMgr.extractGroupName(groupFullName)
            groupNode = self.geom.find("**/" + groupFullName)
            if groupNode.isEmpty():
                self.notify.error("Could not find visgroup")
            self.nodeList.append(groupNode)

        # Now that we have extracted the vis groups we do not need
        # the dnaStore to keep them around
        # Remove all references to the safezone specific models and textures
        self.dnaStore.resetPlaceNodes()
        self.dnaStore.resetDNAGroups()
        self.dnaStore.resetDNAVisGroups()
        self.dnaStore.resetDNAVisGroupsAI()
        """
        
    # start state
    # Defined in SafeZoneLoader.py
    
    # estate state 
    
    def enterEstate(self, requestStatus):
        self.notify.debug("enterEstate: requestStatus = %s" % requestStatus)
        ownerId = requestStatus.get("ownerId")
        if ownerId:
            self.estateOwnerId = ownerId
        zoneId = requestStatus['zoneId']
        self.notify.debug('enterEstate, ownerId = %s, zoneId = %s' % (self.estateOwnerId, zoneId))
        self.accept(self.estateDoneEvent, self.handleEstateDone)
        self.place = Estate.Estate(self, self.estateOwnerId, zoneId, self.fsm.getStateNamed('estate'), self.estateDoneEvent)
        base.cr.playGame.setPlace(self.place)
        self.place.load()
        self.place.enter(requestStatus)
        self.estateZoneId = zoneId
        
    def exitEstate(self):
        self.notify.debug("exitEstate")
        self.ignore(self.estateDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place) 
        base.cr.cache.flush()
        return

    def handleEstateDone(self, doneStatus = None):
        if not doneStatus:
            doneStatus = self.place.getDoneStatus()
        how = doneStatus['how']
        shardId = doneStatus['shardId']
        hoodId = doneStatus['hoodId']
        zoneId = doneStatus['zoneId']
        avId = doneStatus.get('avId', -1)
        ownerId = doneStatus.get('ownerId', -1)
        if shardId or hoodId != MyEstate:
            self.notify.debug('estate done, and we are backing out to a different hood/shard')
            self.notify.debug('hoodId = %s, avId = %s' % (hoodId, avId))
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
            return
        if how in ['tunnelIn',
         'teleportIn',
         'doorIn',
         'elevatorIn']:
            self.notify.debug('staying in estateloader')
            self.fsm.request('quietZone', [doneStatus])
        else:
            self.notify.error("Exited hood with unexpected mode %s" % (how))

    # house state

    def enterHouse(self, requestStatus):
        assert(self.notify.debug("enterHouse()"))
        ownerId = requestStatus.get("ownerId")
        if ownerId:
            self.estateOwnerId = ownerId 
        self.acceptOnce(self.houseDoneEvent, self.handleHouseDone)
        self.place = House.House(self, self.estateOwnerId, self.fsm.getStateNamed('house'), self.houseDoneEvent)
        base.cr.playGame.setPlace(self.place)
        self.place.load()
        self.place.enter(requestStatus)
        
    def exitHouse(self):
        assert(self.notify.debug("exitHouse()"))
        self.ignore(self.houseDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place=None
        base.cr.playGame.setPlace(self.place)
        return

    def handleHouseDone(self, doneStatus = None):
        if not doneStatus:
            doneStatus = self.place.getDoneStatus()
        shardId = doneStatus['shardId']
        hoodId = doneStatus['hoodId']
        if shardId or hoodId != MyEstate:
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
            return
        how = doneStatus['how']
        if how in ['tunnelIn',
         'teleportIn',
         'doorIn',
         'elevatorIn']:
            self.fsm.request('quietZone', [doneStatus])
        else:
            self.notify.error("Exited hood with unexpected mode %s" % (how))

    # quietZone state
    # Defined in SafeZoneLoader.py

    # SDN: check whether using SafeZoneLoaders function works here
    def handleQuietZoneDone(self):
        status=self.quietZoneStateData.getRequestStatus()
        assert(self.notify.debug("handleQuietZoneDone()\n  status="
                +str(status)))
        # Change to the destination state:
        self.fsm.request(status["where"], [status])

    # final state
    # Defined in SafeZoneLoader.py
    
    # utility functions
    def atMyEstate(self):
        if self.estateOwnerId:
            if self.estateOwnerId == base.localAvatar.getDoId():
                return 1
            else:
                return 0
        else:
            self.notify.warning("We aren't in an estate")

    # we have to keep around a reference to the last entered house
    # so the distributed door can always know which house it
    # belongs to
    def setHouse(self, houseId):
        try:
            houseDo = base.cr.doId2do[houseId]
            self.enteredHouse = houseDo.house
        except KeyError:
            self.notify.debug( "can't find house: %d" % houseId)
        
            
    def startCloudPlatforms(self):
        assert(self.notify.debug("startClouds"))
        return
        if len(self.clouds):
            self.cloudTrack = self.__cloudTrack()
            self.cloudTrack.loop()
        
    def stopCloudPlatforms(self):
        assert(self.notify.debug("stopClouds"))
        if self.cloudTrack:
            self.cloudTrack.pause()
            del self.cloudTrack
            self.cloudTrack = None

    def __cloudTrack(self):
        track = Parallel()
        for cloud in self.clouds:
            axis = cloud[1]
            pos = cloud[0].getPos(render)
            newPos = pos + axis * 30
            reversePos = pos - axis * 30
            track.append(Sequence(LerpPosInterval(cloud[0], 10, newPos), LerpPosInterval(cloud[0], 20, reversePos), LerpPosInterval(cloud[0], 10, pos)))

        return track

    def debugGeom(self, decomposed):
        print('numPrimitives = %d' % decomposed.getNumPrimitives())
        for primIndex in xrange(decomposed.getNumPrimitives()):
            prim = decomposed.getPrimitive(primIndex)
            print('prim = %s' % prim)
            print('isIndexed = %d' % prim.isIndexed())            
            print('prim.getNumPrimitives = %d' % prim.getNumPrimitives())
            for basicPrim in xrange(prim.getNumPrimitives()):
                print('%d start=%d' % (basicPrim, prim.getPrimitiveStart(basicPrim)))
                print('%d end=%d' % (basicPrim, prim.getPrimitiveEnd(basicPrim)))

    def loadOnePlatform(self, version, radius, zOffset, score, multiplier):
        self.notify.debug('loadOnePlatform version=%d' % version)
        cloud = NodePath('cloud-%d-%d' % (score, multiplier))
        cloudModel = loader.loadModel('phase_5.5/models/estate/bumper_cloud')
        cc = cloudModel.copyTo(cloud)

        # rename the collision polys
        colCube = cc.find("**/collision")
        colCube.setName("cloudSphere-0")

        # position and scale this cloud
        dTheta = 2.0*math.pi/self.numClouds
        cloud.reparentTo(self.cloudOrigin)
        axes = [Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1)]
        cloud.setPos(radius * math.cos(version * dTheta), radius * math.sin(version * dTheta), 4 * random.random() + zOffset)
        cloud.setScale(4.0)

        self.clouds.append([cloud, random.choice(axes)])    


    def loadSkyCollision(self):
        """
        Put a collision plane in the sky so he doesn't fly too high up
        """
        plane = CollisionPlane(Plane(Vec3(0, 0, -1), Point3(0, 0, 300)))
        plane.setTangible(0)
        planeNode = CollisionNode("cloudSphere-0")
        planeNode.addSolid(plane)
        self.cloudOrigin.attachNewNode(planeNode)

        
    def loadCloudPlatforms(self):      
        self.cloudOrigin = self.geom.attachNewNode("cloudOrigin")
        self.cloudOrigin.setZ(30)

        self.loadSkyCollision()
        
        self.numClouds = 12

        pinballScore = PinballScoring[PinballCloudBumperLow]
        for i in xrange(12):
            self.loadOnePlatform(i, 40, 0, pinballScore[0], pinballScore[1])

        pinballScore = PinballScoring[PinballCloudBumperMed]
        for i in xrange(12):
            self.loadOnePlatform(i, 60, 40, pinballScore[0], pinballScore[1])

        pinballScore = PinballScoring[PinballCloudBumperHigh]
        for i in xrange(12):
            self.loadOnePlatform(i, 20, 80, pinballScore[0], pinballScore[1])
            
        self.cloudOrigin.stash()
        
    def setCloudSwitch(self, on):
        self.cloudSwitch = on
        if hasattr(self, "cloudOrigin"):
            if on:
                self.cloudOrigin.unstash()
            else:
                self.cloudOrigin.stash()
