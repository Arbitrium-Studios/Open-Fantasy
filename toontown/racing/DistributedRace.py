from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectLabel import *
from direct.gui.DirectButton import *
from direct.showbase import BulletinBoardWatcher
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPGlobals
from direct.interval.IntervalGlobal import *
from .RaceGag import RaceGag
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import ToonHeadFrame
from toontown.racing.KartDNA import InvalidEntry, getAccessory, getDefaultColor
from pandac.PandaModules import CardMaker, OrthographicLens, LineSegs
from direct.distributed import DistributedSmoothNode
from math import fmod
from math import sqrt
from .RaceGUI import RaceGUI
from . import RaceGlobals
from direct.task.Task import Task
from toontown.hood import SkyUtil
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.battle.BattleProps import *
from toontown.minigame import MinigameRulesPanel
from toontown.racing import Piejectile
from toontown.racing import EffectManager
from toontown.racing import PiejectileManager
from panda3d.toontown import *
class DistributedRace(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRace')
    #notify.setDebug(1)

    ReadyPost = 'RaceReady'
    WinEvent = 'RaceWinEvent'

    BGM_BaseDir = "phase_6/audio/bgm/"
    SFX_BaseDir = "phase_6/audio/sfx/"
    SFX_StartBoop =  SFX_BaseDir + "KART_raceStart1.ogg"
    SFX_StartBoop2 = SFX_BaseDir + "KART_raceStart2.ogg"
    SFX_Applause =   SFX_BaseDir + "KART_Applause_%d.ogg"

    def __init__(self, cr):
        self.qbox=loader.loadModel("phase_6/models/karting/qbox")
        self.boostArrowTexture=loader.loadTexture("phase_6/maps/boost_arrow.jpg", "phase_6/maps/boost_arrow_a.rgb")
        self.boostArrowTexture.setMinfilter(Texture.FTLinear)

        DistributedObject.DistributedObject.__init__(self, cr)
        self.kartMap={}

        self.fsm= ClassicFSM.ClassicFSM('Race',
                              [State.State('join',
                                           self.enterJoin,
                                           self.exitJoin,
                                           ['prep', 'leave']),
                               State.State('prep',
                                           self.enterPrep,
                                           self.exitPrep,
                                           ['tutorial', 'leave']),
                               State.State('tutorial',
                                           self.enterTutorial,
                                           self.exitTutorial,
                                           ['start', 'waiting', 'leave']),
                               State.State('waiting',
                                           self.enterWaiting,
                                           self.exitWaiting,
                                           ['start', 'leave']),

                               State.State('start',
                                           self.enterStart,
                                           self.exitStart,
                                           ['racing', 'leave']),
                               State.State('racing',
                                           self.enterRacing,
                                           self.exitRacing,
                                           ['finished', 'leave']),
                               State.State('finished',
                                           self.enterFinished,
                                           self.exitFinished,
                                           ['leave']),
                               State.State('leave',
                                           self.enterLeave,
                                           self.exitLeave,
                                           []),
                              ],
                               # Initial State
                               'join',
                               # Final State
                               'leave',
                              )



        self.gui = RaceGUI(self)
        base.race=self
        self.currT=0
        self.currLapT=0
        self.currGag=0
        self.tdelay=0
        self.finished=False
        self.thrownGags=[]
        self.effectManager = EffectManager.EffectManager()
        self.piejectileManager = PiejectileManager.PiejectileManager()
        self.lastTimeUpdate=globalClock.getFrameTime()
        self.initGags()
        self.canShoot=True
        self.isUrbanTrack = False
        self.hasFog = False
        self.dummyNode = None
        self.fog = None
        self.bananaSound=base.loader.loadSfx("phase_6/audio/sfx/KART_tossBanana.ogg")
        self.anvilFall=base.loader.loadSfx("phase_6/audio/sfx/KART_Gag_Hit_Anvil.ogg")
        self.accept("leaveRace", self.leaveRace)
        self.toonsToLink=[]
        self.curveTs=[]
        self.curvePoints=[]
        self.localKart=None
        self.musicTrack = None
        self.victory = None
        self.miscTaskNames = []
        self.boostDir = {}
        self.knownPlace = {}
        self.placeFixup = []
        self.curve=None

        self.barricadeSegments = 100.0
        self.outerBarricadeDict = {}
        self.innerBarricadeDict = {}

        # debug
        self.maxLap = 0
        self.oldT =0
        self.debugIt = 0 #1;
        self.startPos = None;

    ################################################
    #Interest Related Functions
    ################################################

    def generate(self):
        self.notify.debug('generate: %s' % self.doId)
        DistributedObject.DistributedObject.generate(self)
        bboard.post('race', self)

        self.roomWatcher = None

        self.cutoff = 0.01

        self.startBoopSfx = base.loader.loadSfx(self.SFX_StartBoop)
        self.startBoop2Sfx = base.loader.loadSfx(self.SFX_StartBoop2)

    def announceGenerate(self):
        self.notify.debug('announceGenerate: %s' % self.doId)
        DistributedObject.DistributedObject.announceGenerate(self)

        # Load and start the track music
        musicFile = self.BGM_BaseDir + \
                    RaceGlobals.TrackDict[self.trackId][7]

        self.raceMusic = base.loader.loadMusic(musicFile)
        base.playMusic(self.raceMusic, looping = 1, volume = 0.8)

        camera.reparentTo(render)

        if self.trackId in (RaceGlobals.RT_Urban_1, RaceGlobals.RT_Urban_1_rev, RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):
            self.isUrbanTrack = True

        # Store old far plane, since we'll be mucking with it
        self.oldFarPlane = base.camLens.getFar()
        #self.notify.debug("oldFarPlane = %d =========================" % self.oldFarPlane)
        base.camLens.setFar(12000)

        localAvatar.startPosHprBroadcast()
        localAvatar.d_broadcastPositionNow()
        DistributedSmoothNode.activateSmoothing(1, 1)
        self.reversed=(self.trackId/2.0>int(self.trackId/2.0))
        for i in range(3):
            base.loader.tick()

        # load a sky
        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky")
        self.sky.setPos(0, 0, 0)
        self.sky.setScale(20.)
        self.sky.setFogOff()

        # Setup fog for certain tracks
        if self.trackId in (RaceGlobals.RT_Urban_1, RaceGlobals.RT_Urban_1_rev, RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):
            self.loadFog()

        # Create world geometry
        self.setupGeom()

        self.startSky()

        for i in range(5):
            base.loader.tick()

    def disable(self):
        self.notify.debug('disable %s' % self.doId)
        if self.musicTrack:
            self.musicTrack.finish()
        self.raceMusic.stop()
        self.stopSky()
        if self.sky is not None:
            self.sky.removeNode()
        if self.dummyNode:
            self.dummyNode.removeNode()
            self.dummyNode = None
        for taskName in self.miscTaskNames:
            taskMgr.remove(taskName)
        taskMgr.remove("raceWatcher")
        self.ignoreAll()
        DistributedSmoothNode.activateSmoothing(1, 0)
        if self.isUrbanTrack:
            self.unloadUrbanTrack()
        if self.fog:
            render.setFogOff()
            del self.fog
            self.fog = None
        if self.geom is not None:
            self.geom.hide()
        # Reset far plane
        base.camLens.setFar(self.oldFarPlane)
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.notify.debug('delete %s' % self.doId)
        if self.gui:
            self.gui.destroy()
            self.gui = None

        if self.geom is not None:
            self.geom.removeNode()
            self.geom = None
            for i in self.gags:
                i.delete()
                del(i)
        self.piejectileManager.delete()
        if(self.curveTs):
            del self.curveTs
        if(self.curvePoints):
            del self.curvePoints
        if(self.curve):
            del self.curve
        if self.victory:
            del self.victory
        del self.fsm
        del self.anvilFall
        del self.bananaSound
        del self.localKart


        DistributedObject.DistributedObject.delete(self)
        taskMgr.remove(self.uniqueName("countdownTimerTask"))
        taskMgr.remove("raceWatcher")
        bboard.remove('race')
        self.ignoreAll()
        del base.race




    #####################################################
    #Client->AI Functions
    #####################################################

    def d_requestThrow(self, x, y, z):
        self.sendUpdate("requestThrow", [x, y, z])

    def d_requestKart(self):
        self.sendUpdate("requestKart", [])


    #####################################
    #AI->Client Non-required Functions
    #####################################

    def waitingForJoin(self):
        self.notify.debug("I got the barrier")
        self.fsm.enterInitialState()

    def racerDisconnected(self, avId):
        self.notify.debug("lost racer: %s" % avId)
        if(avId in self.kartMap):
            #We know that we are some point after the kart map was set up
            if(avId in self.toonsToLink):
                self.toonsToLink.remove(avId)
            #Now remove from kartmap and avIds
            toon = base.cr.doId2do.get(avId, None)
            kart = base.cr.doId2do.get(self.kartMap.get(avId, None), None)
            self.avIds.remove(avId)
            del(self.kartMap[avId])
            self.gui.racerLeft(avId, unexpected = True)
            #remove toon and kart

            if(kart):
                kart.reparentTo(hidden)
            if(toon):
                toon.reparentTo(hidden)

            if(len(self.toonsToLink)==0):
                self.doneBarrier("waitingForPrep")


    def setPlace(self, avId, totalTime, place, entryFee, qualify, winnings, bonus, trophies, circuitPoints, circuitTime):
        if self.fsm.getCurrentState().getName() == 'leaving':
            return

        if avId == localAvatar.doId:
            # play applause
            cheerToPlay = place + (4-self.numRacers)
            # cap this for safety
            if cheerToPlay > 4:
                cheerToPlay = 4
            self.victory=base.loader.loadSfx(self.SFX_Applause % cheerToPlay)
            self.victory.play()

        self.knownPlace[avId] = place

        kart=base.cr.doId2do.get(self.kartMap.get(avId, None), None)
        avatar=base.cr.doId2do.get(avId, None)
        if(avatar):
            self.gui.racerFinished(avId, self.trackId, place, totalTime, entryFee, qualify, winnings, bonus, trophies, circuitPoints, circuitTime)
            taskName = "hideAv: %s" % avId
            taskMgr.doMethodLater(6, avatar.reparentTo, taskName, extraArgs=[hidden])
            self.miscTaskNames.append(taskName)
        if(kart):
            taskName = "hideKart: %s" % self.localKart.doId
            taskMgr.doMethodLater(6, kart.reparentTo, taskName, extraArgs=[hidden])
            self.miscTaskNames.append(taskName)

    def setCircuitPlace(self, avId, place, entryFee, winnings, bonus,trophies):
        print("setting cicruit place")
        if self.fsm.getCurrentState().getName() == 'leaving':
            return

        if avId == localAvatar.doId:
            # play applause
            cheerToPlay = place + (4-self.numRacers)
            self.victory=base.loader.loadSfx(self.SFX_Applause % cheerToPlay)
            self.victory.play()

        # if placeFixup = [1,0], it would mean move known place 0 to place 1
        # and known place 1 to place 0
        oldPlace = 0
        
        if self.knownPlace.get(avId):
            oldPlace = self.knownPlace[avId]
            self.placeFixup.append([oldPlace-1, place-1])

        avatar=base.cr.doId2do.get(avId,None)
        if(avatar):
            print(("circuit trophies %s" % (trophies)))
            print(("winnings %s" % (winnings)))
            #self.gui.racerFinishedCircuit(avId, place, winnings, trophies)
            self.gui.racerFinishedCircuit(avId, oldPlace, entryFee, winnings, bonus,trophies)

    def endCircuitRace(self):
        print(self.placeFixup)
        self.gui.circuitFinished(self.placeFixup)

    def prepForRace(self):
        self.fsm.request("prep")

    def startRace(self, startTime=0):
        self.baseTime = globalClockDelta.networkToLocalTime(startTime)
        self.fsm.request("start")

    def startTutorial(self):
        self.fsm.request("tutorial")

    def genGag(self, slot, number, type):
        self.notify.debug("making gag...")
        if(not self.gags[slot].isActive()):
            #make the gag
            self.gags[slot].genGag(number, type)
        else:
            #uh oh, how did we get here. Suspicion?
            pass

    def dropAnvilOn(self, ownerId, avId, timeStamp):
        kart=base.cr.doId2do.get(self.kartMap.get(avId, None), None)
        if(kart):
            if(avId!=ownerId):
                if(avId==localAvatar.doId):
                    self.anvilFall.play()
                    kart.dropOnMe(timeStamp)
                else:
                    kart.dropOnHim(timeStamp)
            else:
                pass
                #WAH WAH WAH, someone just dropped on themself, so no drop

    def shootPiejectile(self, sourceId, targetId, type = 0):
        kart=base.cr.doId2do.get(self.kartMap.get(sourceId, None), None)
        if(kart):
            self.piejectileManager.addPiejectile(sourceId, targetId, type)
            #if(sourceId==localAvatar.doId):
            #    newPiejectile = Piejectile.Piejectile(sourceId, targetId, type, self.uniqueName('pie'))
            #    self.piejectiles.append(newPiejectile)
            #else:
            #    newPiejectile = Piejectile.Piejectile(sourceId, targetId, type, self.uniqueName('pie'))
            #    self.piejectiles.append(newPiejectile)



    #Transport back to Goofy's Speedway
    def goToSpeedway(self, avIds, reason = RaceGlobals.Exit_UserReq):
        self.notify.debug("goToSpeedway %s %s" % (avIds, reason))
        if(localAvatar.doId in avIds):
            base.loader.endBulkLoad("atRace")
            self.kartCleanup()

            self.doneBarrier("waitingForExit")
            self.sendUpdate("racerLeft", [localAvatar.doId])
            out={"loader": "safeZoneLoader",
                 "where": "playground",
                 "how": "teleportIn",
                 "hoodId": localAvatar.lastHood,
                 "zoneId": localAvatar.lastHood,
                 "shardId": None,
                 "avId": -1,
                 "reason": reason}
            base.cr.playGame.fsm.request("quietZone", [out])



    def kartCleanup(self):
        kart=self.localKart
        if(kart):
            kart.setState("P", 0)
            for i in self.avIds:
                if(i!=localAvatar.doId):
                    toon=base.cr.doId2do.get(i, None)
                    if(toon):
                        toon.stopSmooth()
                        toon.setScale(1)
                        toon.setShear(0, 0, 0)
                        toon.reparentTo(render)
                        kart.doHeadScale(toon, None)

        # We know we're going to the Goofy Speedway zone.  When we
        # get there, we'll be briefly visible in our current
        # position before appearing where we really are (this is a
        # larger bug in Toontown in general).  Unfortunately, our
        # current position is (0, 0, 0), which happens to be
        # embedded in the Kart Shop doors--quite disturbing to
        # other Toons in the zone.  As a hacky workaround, let's
        # set our position somewhere else, say completely inside
        # the Kart Shop model.
        localAvatar.setPos(0, 14, 0)
        localAvatar.sendCurrentPosition()

    #########################################
    #Client And AI recieve functions
    ##########################################

    def heresMyT(self, avId, avNumLaps, avTime, timestamp):
        self.gui.updateRacerInfo(avId, curvetime = avNumLaps + avTime)


    ###########################################
    # AI->Client required Functions
    ###########################################

    def setZoneId(self, zoneId):
        self.zoneId = zoneId

    def setRaceType(self, raceType):
        self.raceType = raceType

    def setCircuitLoop(self, circuitLoop):
        self.circuitLoop = circuitLoop

    def setTrackId(self, id):
        DistributedRace.notify.debug('setTrackId: %s' % id)
        self.trackId = id

    def setAvatars(self, avIds):
        ids=""
        for i in avIds:
            ids += str(i)+" "
        DistributedRace.notify.debug('setAvatars: %s' % ids)
        self.avIds=avIds
        self.avT=[0]*len(self.avIds)

    def setLapCount(self, lapCount):
        self.lapCount=lapCount

    def setStartingPlaces(self, startList):
        self.startingPlaces=startList

    ######################################
    #Join State
    ######################################

    def enterJoin(self):
        self.doneBarrier("waitingForJoin")
        self.notify.debug("entering Join")

    def exitJoin(self):
        pass


    def setEnteredRacers(self, avAndKarts):
        #Now comes the arduous process of linking karts to players
        #import pdb; pdb.set_trace()
        #First, make an avatar/kart request that callsback when they exist
        self.notify.debug("setEnteredRacers %s" % avAndKarts)
        avatarsGone=[]
        avatarsLeft=[]
        self.numRacers = len(avAndKarts)
        for i in avAndKarts:
            if(i[0] in self.avIds):
                self.kartMap[i[0]]=i[1]
                avatarsLeft.append(i[0])

        #We are using sets here because we want to make sure the avatars
        #that we lose at this point don't affect the starting positions
        #in a non-deterministic way.
        for i in self.avIds:
            if i not in avatarsLeft:
                avatarsGone.append(i)
        base.loader.tick()

        for i in avatarsGone:
            self.avIds.remove(i)

        self.toonsToLink=list(self.avIds)

        for i in avAndKarts:
            self.cr.relatedObjectMgr.requestObjects(i, allCallback = self.__gotKartAvatarLink)


    def __gotKartAvatarLink(self, avAndKart):
        self.notify.debug("got a Link")
        toon=avAndKart[0]
        kart=avAndKart[1]
        base.loader.tick()
        if(toon.doId in self.toonsToLink):
            self.toonsToLink.remove(toon.doId)
        if(toon.doId==localAvatar.doId):
            self.localKart=kart

        if(len(self.toonsToLink)==0):
            self.doneBarrier("waitingForPrep")

    ######################################
    #Prep State
    ######################################

    def enterPrep(self):
        assert self.localKart
        self.d_requestKart()
        self.notify.debug('entering Prep State')
        if(self.reversed):
            self.spin=Vec3(180, 0, 0)
        else:
            self.spin=Vec3(0, 0, 0)
        for i in range(4):
            base.loader.tick()

        self.gui.initRaceMode()
        self.gui.initResultMode()

        self.myPos=self.startingPos[self.startingPlaces[self.avIds.index(localAvatar.doId)]]
        self.localKart.setPosHpr(self.myPos[0], self.myPos[1]+self.spin)
        self.localKart.setupLapCollisions()
        if self.dummyNode:
            self.dummyNode.setPosHpr(self.myPos[0], self.myPos[1]+self.spin)
        self.currentPole=self.findSegmentStart()
        self.rabbitPoint=Vec3(0, 0, 0)
        self.doneBarrier("waitingForReady")


    def exitPrep(self):
        pass

    ###########################################################
    #Tutorial State   --  Wait for users to read instructions
    ###########################################################

    def enterTutorial(self):
        self.notify.debug('entering Tutorial State')
        base.loader.endBulkLoad("atRace")
        self.localKart.setPosHpr(self.myPos[0], self.myPos[1]+self.spin)
        base.transitions.irisIn()
        self.rulesDoneEvent="finishedRules"
        self.accept(self.rulesDoneEvent, self.handleRulesDone)
        # The rules panel is an onscreen panel
        self.rulesPanel = MinigameRulesPanel.MinigameRulesPanel(
            "RacingRulesPanel",
            self.getTitle(),
            self.getInstructions(),
            self.rulesDoneEvent, 10)
        self.rulesPanel.load()
        self.rulesPanel.frame.setPos(0, 0, -0.6667)
        self.rulesPanel.enter()


    def exitTutorial(self):
        #Hide the rules
        self.ignore(self.rulesDoneEvent)
        self.rulesPanel.exit()
        self.rulesPanel.unload()
        del self.rulesPanel

    def getTitle(self):
        return TTLocalizer.KartRace_TitleInfo

    def getInstructions(self):
        return TTLocalizer.KartRace_TrackInfo[self.trackId]

    def handleRulesDone(self):
        self.doneBarrier("readRules")
        self.fsm.request("waiting")


    ########################################################
    #Waiting State   -- Until everyone presses start
    ########################################################

    def enterWaiting(self):
        self.waitingLabel = DirectLabel()
        self.waitingLabel['text'] = TTLocalizer.BuildingWaitingForVictors
        self.waitingLabel.setScale(TTLocalizer.DRenterWaiting)

    def exitWaiting(self):
        self.waitingLabel.remove()


    ########################################################
    #Start State   -- Iris In, start Countdown
    ########################################################


    def enterStart(self):
        waitTime = self.baseTime - globalClock.getFrameTime()
        taskName = "enableRaceModeLater"
        taskMgr.doMethodLater(1, self.gui.enableRaceMode, taskName, extraArgs=[])
        self.miscTaskNames.append(taskName)
        for i in self.avIds:
            self.gui.racerEntered(i)
        self.startCountdownClock(waitTime, 0)
        taskMgr.doMethodLater(waitTime, self.fsm.request, 'goToRacing', extraArgs=["racing"])


    def exitStart(self):
        pass

    #########################################################
    #Racing State   -- Racing Task
    #########################################################

    def enterRacing(self):
        self.localKart.setInput(1)
        self.gui.setTimerEnabled(True)
        self.raceTask=taskMgr.add(self.raceWatcher, "raceWatcher")

    def exitRacing(self):
        pass

    def raceWatcher(self, task):
        kart=base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
        assert(kart)

        #if he's so far off that we have to clamp position, bring him back into the track
        if self.localKart.amIClampingPosition():
            self.notify.debug("teleporting kart %d back to main track" % localAvatar.doId)
            self.localKart.setPos(self.curvePoints[self.currentPole])
        
        kartPoint=self.localKart.getPos()
            
        # There are about 4000 poles spread across the racetrack.
        # Together, these define line segments along the track that we
        # use for determining our position.  The more segments we
        # have, the closer the projection is to correct. The good
        # thing is that inaccuracies won't show up on the mini-map due
        # to the 1/1000th scale

        # Figure out via induction which pole we are currently nearest
        # to.

        # We use the variable 'direction' to make sure we don't get
        # caught going back-and-forth between two poles in the
        # following loop.  We assume that we always walk in the same
        # direction from our current pole to the new pole.  If
        # direction suddenly changes sign, we stop there rather than
        # backing up.
        direction = 0

        while True:
            # self.currentPole refers to the closest one behind us
            currPoint = self.curvePoints[self.currentPole]
            nextPole = (self.currentPole + 1) % len(self.curvePoints)
            nextPoint = self.curvePoints[nextPole]

            # Grab the vector from the current pole to the next
            segment = nextPoint - currPoint
            segment.setZ(0)
            segLength2 = segment.lengthSquared()

            # Grab the vector from the kart to the current Pole
            kartVector = kartPoint - currPoint
            kartVector.setZ(0)

            # Project the kart vector onto the segment of track.
            project = (segment * (segment.dot(kartVector) / segLength2))
            projLength2 = project.lengthSquared()

            # Case 1: We moved behind the current pole, jump to previous pole
            if (project.dot(segment) < 0):
                if direction == 1:
                    # We reversed direction; stop here.
                    break
                prevPole = (self.currentPole - 1) % len(self.curvePoints)
                self.currentPole = prevPole
                direction = -1
            # Case 2: We moved beyond the current pole, jump to next pole
            elif (projLength2 > segLength2):
                if direction == -1:
                    # We reversed direction; stop here.
                    break
                self.currentPole = nextPole
                direction = 1
            # else, we have a good projection.  Accept it and carry on.
            else:
                break

        # update the dummy node
        if self.dummyNode:
            self.dummyNode.setPos(kartPoint[0], kartPoint[1], 0)
            self.dummyNode.setHpr(self.localKart.getH(), 0, 0)

        # Grab the parametric position.  Strictly, this should be
        # sqrt(projLength2) / sqrt(segLength2), but the ratio of the
        # squares is cheaper, and it will be good enough if the poles
        # are close enough together.
        t = projLength2 / segLength2
        #t = sqrt(projLength2) / sqrt(segLength2)
        #self.notify.debug("projLength2=%f segLength2=%f t=%f  self.curve.getMaxT()=%f" % (projLength2, segLength2, t, self.curve.getMaxT()))

        if (self.debugIt):
            self.notify.debug("self.debugIt = %d" % self.debugIt)
            import pdb; pdb.set_trace()


        if (nextPole < self.currentPole):
            newT = self.curveTs[self.currentPole]*(1-t)+self.curve.getMaxT()*t
        else:
            newT = self.curveTs[self.currentPole]*(1-t)+self.curveTs[nextPole]*t
        #Check for wrong way
        kartDirection=self.localKart.forward.getPos(render)-self.localKart.getPos(render)
        kartDirection.normalize()
        project.normalize()
        globalDirection=kartDirection.dot(project)
        if(globalDirection<0):
            self.wrongWay=True
        elif(globalDirection>.1):
            self.wrongWay=False

        #Feed the final value into rabbitPoint. We may never need this
        #self.curve.getPoint(newT, self.rabbitPoint)

        # How far around the lap are we now?
        #import pdb; pdb.set_trace()
        newLapT = ((newT-self.startT)/self.curve.getMaxT())%1.0

        # How far around the lap were we last time?  Did we just cross
        # over the starting gate?
        if newLapT - self.currLapT < -0.5:
            # We just crossed over the starting gate, going forwards.
            self.laps += 1
            self.changeMusicTempo(1 + (self.laps * 0.5))
            self.notify.debug('crossed the start line: %s, %s, %s, %s' % (self.laps, self.startT, self.currT, newT))
        elif newLapT - self.currLapT > 0.5:
            # We just crossed over the starting gate, going backwards.
            self.laps -= 1
            self.changeMusicTempo(1 + (self.laps * 0.5))
            self.notify.debug('crossed the start line - wrong way: %s, %s, %s, %s' % (self.laps, self.startT, self.currT, newT))

        # re-set the currT
        self.currT = newT
        self.currLapT = newLapT

        # Update the buildings
        if self.isUrbanTrack:
            self.showBuildings(self.currT)

        now = globalClock.getFrameTime()
        timestamp = globalClockDelta.localToNetworkTime(now)

        if(self.laps==self.lapCount):
            self.sendUpdate("heresMyT", [localAvatar.doId, self.laps, self.currLapT, timestamp])
            self.fsm.request("finished")

        if (self.laps > self.maxLap):
            self.maxLap = self.laps
            self.sendUpdate("heresMyT", [localAvatar.doId, self.laps, self.currLapT, timestamp])

        if (now - self.lastTimeUpdate > 0.5):
            self.lastTimeUpdate = now
            self.sendUpdate("heresMyT", [localAvatar.doId, self.laps, self.currLapT, timestamp])


        self.gui.updateRacerInfo(localAvatar.doId,
                                 curvetime = self.currLapT + self.laps
)
        self.gui.update(now)


        return Task.cont

    #########################################################
    #Finish State   -- disable controls, show victory screen
    #########################################################

    def enterFinished(self):
        #remove the raceWatcher
        taskMgr.remove("raceWatcher")
        self.fadeOutMusic()
        self.localKart.interruptTurbo()
        self.localKart.disableControls()
        taskName = "parkIt"
        taskMgr.doMethodLater(2, self.stopDriving, taskName, extraArgs=[])
        self.miscTaskNames.append(taskName)
        #set the Finished bit
        self.finished=True
        #disable car controls
        camera.reparentTo(render)
        camera.setPos(self.localKart.getPos(render)+Vec3(0, 0, 10))
        camera.setH(self.localKart.getH(render)+180)

        self.gui.disableRaceMode()
        self.gui.enableResultMode()

        #reparentCamera
        localAvatar.reparentTo(hidden)
        self.localKart.reparentTo(hidden)

    def exitFinished(self):
        pass

    def stopDriving(self):
        kart=base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
        assert kart
        cpos=camera.getPos()
        chpr=camera.getHpr()
        localAvatar.reparentTo(hidden)
        self.localKart.reparentTo(hidden)
        # stop smoothing/broadcast after we take control of the kart - prevents out of range crash
        self.localKart.stopSmooth()
        self.localKart.stopPosHprBroadcast()
        camera.setPos(cpos)
        camera.setHpr(chpr)

    ###########################################################
    #Leave State
    ###########################################################

    def enterLeave(self):
        kart=base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
        assert kart
        taskMgr.remove("raceWatcher")
        self.gui.disable()
        if self.localKart:
            self.localKart.disableControls()
        base.transitions.irisOut()
        if (self.raceType == RaceGlobals.Circuit and
            not (len(self.circuitLoop) == 0)):
            # this is a circuit race, and not the last one
            self.sendUpdate("racerLeft", [localAvatar.doId])
        else:
            taskMgr.doMethodLater(1, self.goToSpeedway, "leaveRace",
                                  extraArgs=[[localAvatar.doId], RaceGlobals.Exit_UserReq])

        if self.victory:
            self.victory.stop()
        self.bananaSound.stop()
        self.anvilFall.stop()

    def exitLeave(self):
        pass



    #########################
    ##Countdown Timer Code
    #########################
    def getCountdownColor(self, countdownTimeInt):
        # Return color for countdown clock
        clockNodeColors = [Vec4(0, 1, 0, 1),
                           Vec4(1, 1, 0, 1),
                           Vec4(1, .5, 0, 1),
                           Vec4(1, 0, 0, 1),
                          ]
        i = max(min(countdownTimeInt, len(clockNodeColors)-1), 0)
        return clockNodeColors[i]

    def startCountdownClock(self, countdownTime, ts):
        # Start the countdown clock...
        self.clockNode = TextNode("k")
        self.clockNode.setFont(ToontownGlobals.getSignFont())
        self.clockNode.setAlign(TextNode.ACenter)
        countdownInt = int(countdownTime)
        self.clockNode.setTextColor(self.getCountdownColor(countdownInt))
        self.clockNode.setText(str(countdownInt))
        self.clock = render2d.attachNewNode(self.clockNode)
        rs = TTLocalizer.DRrollScale
        self.clock.setPosHprScale(0, 0, 0,
                                  0, 0, 0,
                                  rs, rs, rs)
        self.clock.hide()
        if ts < countdownTime:
            self.countdown(countdownTime - ts)

    def timerTask(self, task):
        countdownTime = int(task.duration - task.time)
        timeStr = str(countdownTime+1)

        # make sure we don't display any numbers greater than countdown start (3)
        if self.clock.isHidden():
            if (task.duration - task.time) <= task.maxCount:
                self.clock.show()

        # only update the display when needed
        if self.clockNode.getText() != timeStr:
            self.startBoopSfx.play()
            self.clockNode.setText(timeStr)
            self.clockNode.setTextColor(self.getCountdownColor(countdownTime+1))


        if task.time >= task.duration:
            self.startBoop2Sfx.play()
            self.clockNode.setText(TTLocalizer.KartRace_Go)
            self.clockNode.setTextColor(self.getCountdownColor(-1))
            taskMgr.doMethodLater(1, self.endGoSign, "removeGoSign")
            return Task.done
        else:
            return Task.cont

    def endGoSign(self, t):
        self.clock.remove()

    def countdown(self, duration):
        countdownTask = Task(self.timerTask)
        countdownTask.duration = duration
        countdownTask.maxCount = RaceGlobals.RaceCountdown
        taskMgr.remove(self.uniqueName("countdownTimerTask"))
        return taskMgr.add(countdownTask, self.uniqueName("countdownTimerTask"))

    ######################################################
    #Init Functions
    ######################################################

    #Make any of the props we'll need to toss onto the track
    #Anvil isn't here because there is one anvil per car, stored on the car
    def initGags(self):
        self.banana=globalPropPool.getProp('banana')
        self.banana.setScale(2)

        self.pie=globalPropPool.getProp('creampie')
        self.pie.setScale(1)

    #Generate a collision solid that will trigger *event* when a lapChecker
    #node (found on a racing vehicle) is hit
    def makeCheckPoint(self, trigger, location, event):
        cs = CollisionSphere(0, 0, 0, 140)
        cs.setTangible(0)
        triggerEvent="imIn-"+trigger

        cn=CollisionNode(trigger)
        cn.addSolid(cs)
        cn.setIntoCollideMask(BitMask32(0x8000))
        cn.setFromCollideMask(BitMask32(0x8000))
        cnp=NodePath(cn)
        cnp.reparentTo(self.geom)
        cnp.setPos(location)
        self.accept(triggerEvent, event)

    def loadUrbanTrack(self):
        self.dnaStore = DNAStorage()
        loader.loadDNAFile(self.dnaStore, "phase_4/dna/storage.dna")
        loader.loadDNAFile(self.dnaStore, "phase_5/dna/storage_town.dna")
        loader.loadDNAFile(self.dnaStore, "phase_4/dna/storage_TT.dna")
        loader.loadDNAFile(self.dnaStore, "phase_5/dna/storage_TT_town.dna")
        loader.loadDNAFile(self.dnaStore, "phase_8/dna/storage_BR.dna")
        loader.loadDNAFile(self.dnaStore, "phase_8/dna/storage_BR_town.dna")


        dnaFile = "phase_6/dna/urban_track_town.dna"
        if self.trackId in (RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):
            dnaFile = "phase_6/dna/urban_track_town_B.dna"

        node = loader.loadDNAFile(self.dnaStore, dnaFile)
        self.townGeom = self.geom.attachNewNode(node)

        # Stash collisions
        self.townGeom.findAllMatches("**/+CollisionNode").stash()

        # Create bins for buildings
        self.buildingGroups = {}
        self.currBldgInd = {}
        self.currBldgGroups = {}

        # Setup background geometry
        bgGeom = self.geom.find("**/polySurface8")
        if self.dummyNode:
            bgGeom.reparentTo(self.dummyNode)
        else:
            bgGeom.reparentTo(localAvatar)
        bgGeom.setScale(.1)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot)
        bgGeom.node().setEffect(ce)
        bgGeom.setDepthTest(0)
        bgGeom.setDepthWrite(0)
        bgGeom.setBin("background", 102)
        bgGeom.setZ(-1)
        self.bgGeom = bgGeom

        l = self.geom.findAllMatches("**/+ModelNode")
        for n in l:
            n.node().setPreserveTransform(0)
        self.geom.flattenLight()

        maxNum =0
        for side in ['inner', 'outer']:
            # Initialize some variables to be used later
            self.buildingGroups[side] = []
            self.currBldgInd[side] = None
            self.currBldgGroups[side] = None
            i = 0
            while 1:
                bldgGroup = self.townGeom.find("**/Buildings_"+side+"-"+str(i))
                #self.notify.debug("bldgGroup for %s = %s" % (side, str(bldgGroup)))

                if bldgGroup.isEmpty():
                    break;
                #bldgGroup.flattenStrong()
                l = bldgGroup.findAllMatches("**/+ModelNode")
                for n in l:
                    n2 = n.getParent().attachNewNode(n.getName())
                    n.getChildren().reparentTo(n2)
                    n.removeNode()
                # Now that ModelNodes are stripped, flatten as much as possible
                bldgGroup.flattenStrong()

                if (not bldgGroup.getNode(0).getBounds().isEmpty()):
                    self.buildingGroups[side].append(bldgGroup)
                i += 1

            #self.notify.debug("side=%s len(self.buildingGroups[side])=%d" % (side, len(self.buildingGroups[side])))
            #self.notify.debug("bldgGroups= %s" % self.buildingGroups[side])

            if i > maxNum:
                maxNum = i

        #RAU do more special processing on the side streets
        
        for side in ['innersidest', 'outersidest']:
            # Initialize some variables to be used later
            self.buildingGroups[side] = []
            self.currBldgInd[side] = None
            self.currBldgGroups[side] = None
            for i in range(maxNum):
                for barricade in ('innerbarricade', 'outerbarricade'):
                    bldgGroup = self.townGeom.find("**/Buildings_"+side+"-" + barricade + '_' + str(i))
                    if bldgGroup.isEmpty():
                        continue;
                        #break;
                    #self.notify.debug("found bldgGroup %s" % bldgGroup)
                    #bldgGroup.flattenStrong()
                    l = bldgGroup.findAllMatches("**/+ModelNode")
                    for n in l:
                        n2 = n.getParent().attachNewNode(n.getName())
                        n.getChildren().reparentTo(n2)
                        n.removeNode()
                    # Now that ModelNodes are stripped, flatten as much as possible
                    # delay flattening strong until we've done precompute side streets
                    # bldgGroup.flattenStrong()

                    self.buildingGroups[side].append(bldgGroup)





        treeNodes = self.townGeom.findAllMatches("**/prop_tree_*")
        #self.notify.debug("treeNodes.ls() =================================")

        for tree in treeNodes:
            tree.flattenStrong()

        snowTreeNodes = self.townGeom.findAllMatches("**/prop_snow_tree_*")
        for snowTree in snowTreeNodes:
            snowTree.flattenStrong()
            


        # Stash all building gropus initially
        for side in ['inner', 'outer', 'innersidest','outersidest']:
            for grp in self.buildingGroups[side]:
                grp.stash()

        # Show initial group of buildings
        self.showBuildings(0)

    def unloadUrbanTrack(self):
        del self.buildingGroups
        self.townGeom.removeNode()

    def loadFog(self):
        self.hasFog = True
        # Note:  The urban track is polygon heavy.  To counter this, we need to pull
        # the far plane in and hide the clipping with fog.
        if self.isUrbanTrack:
            base.camLens.setFar(650)
        else:
            base.camLens.setFar(650)


        # Create a dummy node to parent sky and background to.  The dummy node follows
        # the car around, but doesn't change z-height or pitch.
        self.dummyNode = render.attachNewNode("dummyNode")

        # Load fog
        if base.wantFog:
            self.fog = Fog("TrackFog")
            self.fog.setColor(Vec4(.6, .7, .8, 1.0))
            if self.isUrbanTrack:
                self.fog.setLinearRange(200.0, 650.0)
            else:
                self.fog.setLinearRange(200.0, 800.0)
            render.setFog(self.fog)

        # Move the sky in so it doesn't get clipped
        self.sky.setScale(1.725)
        self.sky.reparentTo(self.dummyNode)


    def showBuildings(self, t, forceRecompute = False):
        #RAU show buildings expect t to be between 0 and 1, not happening in Urban Track B
        firstTimeCalled = 0        
        if (self.curve):
            t = t / self.curve.getMaxT()
        else:
            firstTimeCalled = 1
            #self.notify.debug("new t=%f" % t)

        if self.reversed:
            t = 1.-t
        numGroupsShown = 5


        for side in ['inner', 'outer']:
            numBldgGroups = len(self.buildingGroups[side])
            # based on a value t, (0 < t < 1), determine which group of buildings to show
            bldgInd = int(t * numBldgGroups)
            bldgInd = bldgInd % numBldgGroups


            if self.trackId in (RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):
                #double check if we really increment bldg ind
                oldBldgInd = int(self.oldT * numBldgGroups)
                newBldgInd = int(t * numBldgGroups)
                #if oldBldgInd == newBldgInd:
                if 0:
                    #force it NOT to update
                    if not firstTimeCalled:
                        bldgInd = self.currBldgInd[side]
                else:                
                    kartPoint = self.startPos                    
                    kart=base.cr.doId2do.get(self.kartMap.get(localAvatar.doId,None),None)
                    if (kart):
                        #import pdb; pdb.set_trace()                        
                        kartPoint=self.localKart.getPos()
                        
                    #kartPoint = Vec3( kartPointPos[0], kartPointPos[1], kartPointPos[2])
                    if not self.currBldgInd[side]:
                        self.currBldgInd[side]=0
                    
                    curInd = self.currBldgInd[side]
                    myCurGroup = self.buildingGroups[side][curInd]
                    prevGrp = (curInd - 1) % numBldgGroups
                    myPrevGroup = self.buildingGroups[side][prevGrp]
                    nextGrp = (curInd + 1) % numBldgGroups                    
                    myNextGroup = self.buildingGroups[side][nextGrp]

                    #curDistance = myCurGroup.getDistance(self.localKart)
                    #prevDistance = myPrevGroup.getDistance(self.localKart)
                    #nextDistance = myNextGroup.getDistance(self.localKart)

                    curVector = myCurGroup.getNode(0).getBounds().getCenter() - kartPoint;
                    curDistance = curVector.lengthSquared()


                    prevVector = myPrevGroup.getNode(0).getBounds().getCenter() - kartPoint
                    prevDistance = prevVector.lengthSquared()


                    nextVector = myNextGroup.getNode(0).getBounds().getCenter() - kartPoint
                    nextDistance = nextVector.lengthSquared()

                        #self.notify.debug("curDistance=%.2f prevDistance=%.2f nextDistance=%.2f" % (curDistance, prevDistance, nextDistance))

                        #self.notify.debug("%s %s %s " % (myPrevGroup.getPos(), myCurGroup.getPos(), myNextGroup.getPos()))

                      
                    if (curDistance <= prevDistance and curDistance <= nextDistance):
                        #force it NOT to udpate
                        bldgInd = self.currBldgInd[side]
                    elif ( prevDistance <= curDistance and prevDistance <= nextDistance):
                        bldgInd = prevGrp
                    elif ( nextDistance <= curDistance and nextDistance <= prevDistance):
                        bldgInd = nextGrp;
                    else:
                        self.notify.warning("unhandled case!!!!")
                        bldgInd = self.currBldgInd[side]

                       
                
                

            if bldgInd != self.currBldgInd[side]:
                #self.notify.debug("bldgInd = %d numBldgGroups=%d" % (bldgInd, numBldgGroups))
                currBldgGroups = self.currBldgGroups[side]
                # Hide all previous bldg groups
                # TODO: it may be inneficient to hide all of them, since we probably only need to hide one
                if currBldgGroups:
                    for i in currBldgGroups:
                        self.buildingGroups[side][i].stash()

                # Show new bldg groups
                prevGrp2 = (bldgInd - 2) % numBldgGroups
                prevGrp = (bldgInd - 1) % numBldgGroups
                currGrp = (bldgInd) % numBldgGroups
                nextGrp = (bldgInd + 1) % numBldgGroups
                nextGrp2 = (bldgInd + 2) % numBldgGroups

                
                self.currBldgGroups[side] = [prevGrp2, prevGrp, currGrp, nextGrp, nextGrp2]


                #self.notify.debug("t=%f  %s currBldgs = %s" % (t, side,str(self.currBldgGroups[side])))
                
                for i in self.currBldgGroups[side]:
                    self.buildingGroups[side][i].unstash()

                #self.notify.debug("self.currBldgInd[%s] = %d" % (side,bldgInd))
                self.currBldgInd[side] = bldgInd


        if (self.currBldgGroups['inner'] != self.currBldgGroups['outer']):
            pass
            #self.notify.warning("assumption of inner same as outer not holding")
            #import pdb; pdb.set_trace()


        if (t != self.oldT):
            self.oldT = t;
         

        #return
        #do special processing for side streets
        if self.trackId in (RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):
            #side street computation follows the reverse curve, so reverse t again
            if (self.reversed):
                t = 1.0 - t
        
            for side in ['innersidest', 'outersidest']:
                segmentInd = int(t * self.barricadeSegments)
                seglmentInd =segmentInd % self.barricadeSegments
            
                if segmentInd != self.currBldgInd[side] or forceRecompute:
                    currBldgGroups = self.currBldgGroups[side]
                    # Hide all previous bldg groups
                    # TODO: it may be inneficient to hide all of them, since we probably only need to hide one
                    #self.notify.debug("segmentInd = %d -----------------" % segmentInd)
                    if currBldgGroups:
                        for i in currBldgGroups:
                           #self.notify.debug("hiding %s" % self.buildingGroups[side][i])
                           self.buildingGroups[side][i].stash()

                    self.currBldgGroups[side]=[]
                    if side == 'innersidest':
                        dict = self.innerBarricadeDict
                    elif side == 'outersidest':
                        dict = self.outerBarricadeDict

                    if segmentInd in dict:
                        self.currBldgGroups[side] = dict[segmentInd]
                
                    #we should have the correct value in currBldgGroups at this point
                    for i in self.currBldgGroups[side]:
                        #self.notify.debug("showing %s" % self.buildingGroups[side][i].getName())
                        self.buildingGroups[side][i].unstash()

                    self.currBldgInd[side] = segmentInd


    #Here we generate the collision solids for the track.
    def setupGeom(self):
        trackFilepath = RaceGlobals.TrackDict[self.trackId][0]
        self.geom = loader.loadModel(trackFilepath)
        for i in range(10):
            base.loader.tick()
        self.geom.reparentTo(render)

        if(self.reversed):
            lapStartPos=self.geom.find("**/lap_start_rev").getPos()
        else:
            lapStartPos=self.geom.find("**/lap_start").getPos()
        self.startPos = lapStartPos
        lapMidPos=self.geom.find("**/lap_middle").getPos()

        for i in range(5):
            base.loader.tick()

        self.startingPos=[]
        posLocators=self.geom.findAllMatches("**/start_pos*")
        for i in range(posLocators.getNumPaths()):
            base.loader.tick()
            self.startingPos.append([posLocators[i].getPos(), posLocators[i].getHpr()])
        self.notify.debug("self.startingPos: %s" % self.startingPos)
        self.wrongWay=False
        self.laps=0

        # If urban track, load buildings from extra DNA
        # NOTE:  Do this after the starting block positions are saved out, since we
        # do some flattening here.  Also do this before genArrows is called since
        # genArrows places some nodes that we don't want flattened.
        if self.isUrbanTrack:
            self.loadUrbanTrack()

        # Generate turbo arrows
        self.genArrows()

        #Okay, tentative plan here to determine point on track.
        #1- subdivide track in to x segments
        #2- determine segment player is in (done only once ideally)
        #3- every frame, make a vector between segment beginning and kart
        #4- dot this against the segment vector
        #5- if the value is less than the length of the segment, use to determine
        #   place on segment
        #6- if the value is negative, go to the previous segment and repeat
        #7- if the value is greater than the length of the segment, go to
        #   the next segment, and repeat
        if(self.reversed):
            self.curve=self.geom.find("**/curve_reverse").node()
        else:
            self.curve=self.geom.find("**/curve_forward").node()

        for i in range(4000):
            self.curvePoints.append(Point3(0, 0, 0))
            self.curve.getPoint((i/4000.0)*(self.curve.getMaxT()-.00000000001), self.curvePoints[-1])
            self.curveTs.append((i/4000.0)*(self.curve.getMaxT()-.00000000001))            

        if self.trackId in (RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):                
            self.precomputeSideStreets()
            

        for i in range(10):
            base.loader.tick()

        self.startT=self.getNearestT(lapStartPos)
        self.oggT=self.getNearestT(lapMidPos)

        self.gags=[]
        gagList=RaceGlobals.TrackDict[self.trackId][4]
        for i in range(len(gagList)):
            self.notify.debug("generating gag: %s" % i)
            self.gags.append(RaceGag(self, i, Vec3(*gagList[i])+Vec3(0, 0, 3)))
        for i in range(5):
            base.loader.tick()


            

    ################################################
    #Track Functions
    ################################################
    def precomputeSideStreets(self):
        
        #the side streets are pretty far apart that we can't use the same technique as the main track
        #precompute which side streets we will show
        farDist = base.camLens.getFar() + 300
        farDistSquared = farDist * farDist

        #import pdb; pdb.set_trace()
        for i in range(int(self.barricadeSegments)):            
            testPoint = Point3(0,0,0)
            self.curve.getPoint(( i / self.barricadeSegments) * (self.curve.getMaxT()-.00000000001), testPoint)
            for side in ('innersidest','outersidest'):
                for bldgGroupIndex in range(len(self.buildingGroups[side])):
                    bldgGroup = self.buildingGroups[side][bldgGroupIndex]
                    if not bldgGroup.getNode(0).getBounds().isEmpty():
                        bldgPoint = bldgGroup.getNode(0).getBounds().getCenter()
                        vector = testPoint - bldgPoint;
                        if (vector.lengthSquared() < farDistSquared):
                            if side == 'innersidest':
                                dict = self.innerBarricadeDict
                            elif side == 'outersidest':
                                dict = self.outerBarricadeDict
                            else:
                                self.notify.error("unhandled side")
                            
                            if i in dict:
                                if not bldgGroupIndex in dict[i]:
                                    dict[i].append(bldgGroupIndex)
                                    #self.notify.debug("%s BarrierDict[%d] = %s" % (side, i, dict[i]))                                
                            else:
                                dict[i] = [bldgGroupIndex]
                                #self.notify.debug("%s BarrierDict[%d] = %s" % (side, i, dict[i]))

                    # do the same test
                    #for the firt child
                    #for childIndex in (0, bldgGroup.getNumChildren() / 2,  bldgGroup.getNumChildren()-1):
                    for childIndex in (0,):
                        if (childIndex >= bldgGroup.getNumChildren()):
                            continue
                    
                        childNodePath = bldgGroup.getChild(childIndex)
                        bldgPoint = childNodePath.node().getBounds().getCenter()
                        vector = testPoint - bldgPoint;
                        if (vector.lengthSquared() < farDistSquared):
                            if side == 'innersidest':
                                dict = self.innerBarricadeDict
                            elif side == 'outersidest':
                                dict = self.outerBarricadeDict
                            else:
                                self.notify.error("unhandled side")
                             
                            if i in dict:
                                if not bldgGroupIndex in dict[i]:
                                   dict[i].append(bldgGroupIndex)
                                   #self.notify.debug("%s BarrierDict[%d] = %s" % (side, i, dict[i])) 
                            else:
                                dict[i] = [bldgGroupIndex]
                                #self.notify.debug("%s BarrierDict[%d] = %s" % (side, i, dict[i]))
                        
        #self.notify.debug("innerBarricadeDict = %s" % self.innerBarricadeDict);
        #self.notify.debug("outerBarricadeDict = %s" % self.outerBarricadeDict);
                            
        for side in ('innersidest','outersidest'):
            for bldgGroup in self.buildingGroups[side]:
                bldgGroup.flattenStrong()

        #we need to call this again, since the first time arround the dictionary was not set up
        if self.isUrbanTrack:
            self.showBuildings(0, forceRecompute = True)
        

    def findSegmentStart(self):
        kart=base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
        assert kart
        minLength2=1000000
        minIndex=-1
        currPoint=Point3(0, 0, 0)
        kartPoint=self.localKart.getPos()
        for i in range(len(self.curvePoints)):
            currPoint=self.curvePoints[i]
            currLength2=(kartPoint-currPoint).lengthSquared()
            if(currLength2<minLength2):
                minLength2=currLength2
                minIndex=i

        #Now we find the appropriate Start
        currPoint=self.curvePoints[minIndex]
        if(minIndex+1==len(self.curvePoints)):
            nextPoint=self.curvePoints[0]
        else:
            nextPoint=self.curvePoints[minIndex+1]
        if(minIndex-1<0):
            prevIndex=len(self.curvePoints)-1
        else:
            prevIndex=minIndex-1


        forwardSegment=nextPoint-currPoint
        if((kartPoint-currPoint).dot(forwardSegment)>0):
            #the kart is in front
            return minIndex
        else:
            #the kart is behind the point
            return prevIndex


    def getNearestT(self, pos):
        minLength2=1000000
        minIndex=-1
        currPoint=Point3(0, 0, 0)
        for i in range(len(self.curvePoints)):
            currPoint=self.curvePoints[i]
            currLength2=(pos-currPoint).lengthSquared()
            if(currLength2<minLength2):
                minLength2=currLength2
                minIndex=i

        #Now we find the appropriate Start
        currPoint=self.curvePoints[minIndex]
        if(minIndex+1==len(self.curvePoints)):
            nextPoint=self.curvePoints[0]
        else:
            nextPoint=self.curvePoints[minIndex+1]
        if(minIndex-1<0):
            prevIndex=len(self.curvePoints)-1
        else:
            prevIndex=minIndex-1


        forwardSegment=nextPoint-currPoint
        if((pos-currPoint).dot(forwardSegment)>0):
            #the pos is in front
            pole=minIndex
        else:
            #the pos is behind the point
            pole=prevIndex

        currPoint=self.curvePoints[pole]
        nextPole=(pole+1)%len(self.curvePoints)
        nextPoint=self.curvePoints[nextPole]

        #Grab the vector from the current pole to the next
        segment=nextPoint-currPoint
        segment.setZ(0)
        segLength2=segment.lengthSquared()

        posVector=pos-currPoint
        posVector.setZ(0)

        #Project the kart vector onto the segment of track.
        #The more segments we have, the closer the projection is to
        #correct. The good thing is that inaccuracies won't show
        #up on the mini-map due to the 1/1000th scale
        project=(segment*(segment.dot(posVector)/segLength2))

        #Grab the parametric position
        percent=project.lengthSquared()/segLength2
        if(nextPole<pole):
            t=self.curveTs[pole]*(1-percent)+self.curve.getMaxT()*percent
        else:
            t=self.curveTs[pole]*(1-percent)+self.curveTs[nextPole]*percent
        return t


    #################################################
    #Racer State Functions
    #################################################

    #The worry with this function is that the clients broadcast it
    #to eachother as well as the server. Hopefully, the AI distance-to-gag
    #check should allow us to flag and/or kick cheaters who send this message
    #out to kill gags
    def hasGag(self, slot, type, index):
        if(self.gags[slot].isActive()):
            self.gags[slot].disableGag()
        else:
            #something's wrong
            pass


    def leaveRace(self):
        self.fsm.request("leave")


    def racerLeft(self, avId):
        if(avId != localAvatar.doId):
            self.gui.racerLeft(avId, unexpected = False)




    ######################################################
    #Sky Functions
    ######################################################

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        if self.hasFog:
            SkyUtil.startCloudSky(self, parent=self.dummyNode, effects = CompassEffect.PRot)
        else:
            SkyUtil.startCloudSky(self, parent=render)

    def stopSky(self):
        taskMgr.remove("skyTrack")


    #######################################################
    #Gag related Functions
    #######################################################

    def pickupGag(self, slot, index):
        self.canShoot=False
        standing=self.gui.racerDict[localAvatar.doId].place-1
        self.currGag=RaceGlobals.GagFreq[standing][index]
        # Pass in the same value to waitingOnGag and doMethodLater.
        cycleTime = 2
        self.gui.waitingOnGag(cycleTime)
        taskMgr.doMethodLater(cycleTime, self.enableShoot, "enableShoot")
        self.sendUpdate("hasGag", [slot, self.currGag, index])


    def shootGag(self):
        if(self.canShoot):
            if(self.currGag==1):
                self.bananaSound.play()
                self.shootBanana()
            elif(self.currGag==2):
                self.d_requestThrow(0, 0, 0)
                self.localKart.startTurbo()
            elif(self.currGag==3):
                self.d_requestThrow(0, 0, 0)
            elif(self.currGag==4):
                self.bananaSound.play()
                self.shootPie()

            self.currGag=0
            self.gui.updateGag(0)

    def enableShoot(self, t):
        self.canShoot=True
        if self.gui:
            self.gui.updateGag(self.currGag)

    def shootBanana(self):
        pos=self.localKart.getPos(render)
        banana=self.banana.copyTo(self.geom)
        banana.setPos(pos)
        self.thrownGags.append(banana)
        self.d_requestThrow(pos[0], pos[1], pos[2])

    def shootPie(self):
        pos=self.localKart.getPos(render)
        #self.localKart.splatPie()
        #pie=self.pie.copyTo(self.geom)
        #pie.setPos(pos)
        #self.thrownGags.append(pie)
        self.d_requestThrow(pos[0], pos[1], pos[2])

    def genArrows(self):
        base.arrows = []
        arrowId = 0
        for boost in RaceGlobals.TrackDict[self.trackId][5]:
            self.genArrow(boost[0], boost[1], arrowId)
            arrowId += 1

    def genArrow(self, pos, hpr, id):
        factory=CardMaker("factory")
        factory.setFrame(-.5, .5, -.5, .5)
        arrowNode=factory.generate()

        arrowRoot=NodePath("root")

        baseArrow=NodePath(arrowNode)
        baseArrow.setTransparency(1)
        baseArrow.setTexture(self.boostArrowTexture)
        baseArrow.reparentTo(arrowRoot)
        arrow2=baseArrow.copyTo(baseArrow)
        arrow2.setPos(0, 0, 1)
        arrow3=arrow2.copyTo(arrow2)
        arrowRoot.setPos(*pos)
        arrowRoot.setHpr(*hpr)
        baseArrow.setHpr(0, -90, 0)
        baseArrow.setScale(24)
        arrowRoot.reparentTo(self.geom)

        trigger="boostArrow"+str(id)
        #cs = CollisionSphere(0, 0, 0, .5)
        cs = CollisionTube(Point3(0.6, -6, 0), Point3(0.6, 54 , 0), 4.8)
        cs.setTangible(0)
        triggerEvent="imIn-"+trigger

        cn=CollisionNode(trigger)
        cn.addSolid(cs)
        cn.setIntoCollideMask(BitMask32(0x8000))
        cn.setFromCollideMask(BitMask32(0x8000))
        cnp=NodePath(cn)
        cnp.reparentTo(arrowRoot)
        self.accept(triggerEvent, self.hitBoostArrow)

        # Compute the forward direction of the boost
        arrowVec = arrow2.getPos(self.geom) - baseArrow.getPos(self.geom)
        arrowVec.normalize()

        # Save it in a dict so we don't have to compute it every time it's hit
        idStr = str(id)
        cnp.setTag('boostId', idStr)
        self.boostDir[idStr] = arrowVec

        #arrowRoot.flattenStrong()
        base.arrows.append(arrowRoot)

    def hitBoostArrow(self, cevent):
        into = cevent.getIntoNodePath()
        idStr = into.getTag('boostId')
        arrowVec = self.boostDir.get(idStr)
        if arrowVec == None:
            print("Unknown boost arrow %s" % (idStr))
            return

        # Get the forward direction of the kart
        fvec = self.localKart.forward.getPos(self.geom) - self.localKart.getPos(self.geom)
        fvec.normalize()

        # Is the kart moving in roughly the same direction as the arrow?
        dotP = arrowVec.dot(fvec)
        if(dotP>.70):
            self.localKart.startTurbo()

    def fadeOutMusic(self):
        if self.musicTrack:
            self.musicTrack.finish()

        curVol = self.raceMusic.getVolume()
        interval = LerpFunctionInterval(self.raceMusic.setVolume, fromData = curVol, toData = 0, duration = 3)
        self.musicTrack = Sequence(interval)
        self.musicTrack.start()

    def changeMusicTempo(self, newPR):
        if self.musicTrack:
            self.musicTrack.finish()

        curPR = self.raceMusic.getPlayRate()
        interval = LerpFunctionInterval(self.raceMusic.setPlayRate, fromData = curPR, toData = newPR, duration = 3)
        self.musicTrack = Sequence(interval)
        self.musicTrack.start()

    def setRaceZone(self, zoneId, trackId):
        #only the appropriate toons should receive this message
        hoodId = self.cr.playGame.hood.hoodId

        base.loader.endBulkLoad("atRace")
        self.kartCleanup()
        self.doneBarrier("waitingForExit")
        self.sendUpdate("racerLeft", [localAvatar.doId])
        out={"loader": "racetrack",
             "where": "racetrack",
             "hoodId": hoodId,
             "zoneId": zoneId,
             "trackId": trackId,
             "shardId": None,
             "reason": RaceGlobals.Exit_UserReq}
        base.cr.playGame.hood.loader.fsm.request("quietZone", [out])
