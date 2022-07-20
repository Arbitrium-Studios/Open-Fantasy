from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from otp.avatar import Avatar
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from direct.fsm import FSM
from direct.fsm import State
from toontown.toonbase import TTLocalizer
from toontown.battle import BattleParticles
from . import Suit
from direct.task.Task import Task
from . import SuitDNA
from toontown.battle import BattleProps
from otp.otpbase.PythonUtil import Functor
import string
from panda3d.otp import  *
GenericModel = "phase_9/models/char/bossCog"


ModelDict = {
    "s": ("phase_9/models/char/sellbotBoss"),
    "m": ("phase_10/models/char/cashbotBoss"),
    "l": ("phase_11/models/char/lawbotBoss"),
    "c": ("phase_12/models/char/bossbotBoss"),
    }

AnimList = (
    "Ff_speech", "ltTurn2Wave", "wave", "Ff_lookRt", "turn2Fb",
    "Ff_neutral", "Bb_neutral", "Ff2Bb_spin", "Bb2Ff_spin",
    "Fb_neutral", "Bf_neutral", "Fb_firstHit",
    "Fb_downNeutral", "Fb_downHit", "Fb_fall",
    "Fb_down2Up", "Fb_downLtSwing", "Fb_downRtSwing",
    "Fb_DownThrow", "Fb_UpThrow", "Fb_jump", "golf_swing"
 )

class BossCog(Avatar.Avatar):
    """
    The BossCog is the big supervisor Cog that we have to fight at the
    end of the CogHQ level.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('BossCog')

    healthColors = Suit.Suit.healthColors
    healthGlowColors = Suit.Suit.healthGlowColors

    def __init__(self):
        Avatar.Avatar.__init__(self)
        self.setFont(ToontownGlobals.getSuitFont())
        self.setPlayerType(NametagGroup.CCSuit)
        self.setPickable(0)

        self.doorA = None
        self.doorB = None
        self.bubbleL = None
        self.bubbleR = None

        # These variables are used to track the current state for
        # animation when you call doAnimate().
        self.raised = 1
        self.forward = 1
        self.happy = 1
        self.dizzy = 0
        self.nowRaised = 1
        self.nowForward = 1
        self.nowHappy = 1
        self.currentAnimIval = None
        self.queuedAnimIvals = []

        self.treadsLeftPos = 0
        self.treadsRightPos = 0

        self.healthBar = None
        self.healthCondition = 0

        # We don't need to uniquify these since there is only one
        # BossCog on a client at any given time.
        self.animDoneEvent = 'BossCogAnimDone'
        self.animIvalName = 'BossCogAnimIval'

    def delete(self):
        Avatar.Avatar.delete(self)
        self.removeHealthBar()
        self.setDizzy(0)
        self.stopAnimate()
        if self.doorA:
            self.doorA.request('Off')
            self.doorB.request('Off')
            self.doorA = None
            self.doorB = None

    def setDNAString(self, dnaString):
        self.dna = SuitDNA.SuitDNA()
        self.dna.makeFromNetString(dnaString)
        self.setDNA(self.dna)

    def setDNA(self, dna):
        if self.style:
            pass
        else:
            # store the DNA
            self.style = dna

            self.generateBossCog()

            # this no longer works in the Avatar init!
            # I moved it here for lack of a better place
            # make the drop shadow
            self.initializeDropShadow()
            if base.wantNametags:
                self.initializeNametag3d()

    def generateBossCog(self):
        self.throwSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_frisbee_gears.ogg')
        self.swingSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_swipe.ogg')
        self.spinSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_spin.ogg')
        self.rainGearsSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_raining_gears.ogg')
        self.swishSfx = loader.loadSfx('phase_5/audio/sfx/General_throw_miss.ogg')
        self.boomSfx = loader.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.ogg')
        self.deathSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_big_death.ogg')
        self.upSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_raise_up.ogg')
        self.downSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_collapse.ogg')
        self.reelSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_reeling_backwards.ogg')
        #self.treadsSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_tractor_treads.ogg')
        self.birdsSfx = loader.loadSfx('phase_4/audio/sfx/SZ_TC_bird1.ogg')
        self.dizzyAlert = loader.loadSfx('phase_5/audio/sfx/AA_sound_aoogah.ogg')
        self.grunt = loader.loadSfx('phase_9/audio/sfx/Boss_COG_VO_grunt.ogg')
        self.murmur = loader.loadSfx('phase_9/audio/sfx/Boss_COG_VO_murmur.ogg')
        self.statement = loader.loadSfx('phase_9/audio/sfx/Boss_COG_VO_statement.ogg')
        self.question = loader.loadSfx('phase_9/audio/sfx/Boss_COG_VO_question.ogg')

        self.dialogArray = [
            self.grunt, self.murmur, self.statement, self.question, self.statement, self.statement
            ]
        
        dna = self.style
        filePrefix = ModelDict[dna.dept]
        # TODO: bosscogs have unique 'legs'
        #if dna.dept == 'c':
        #    self.loadModel(filePrefix + "-legs-zero", "legs")
        #else:
        #    self.loadModel(GenericModel + "-legs-zero", "legs")
        self.loadModel(GenericModel + "-legs-zero", "legs")
        self.loadModel(filePrefix + "-torso-zero", "torso")
        self.loadModel(filePrefix + "-head-zero", "head")

        # This is true if the head model has two faces: happy on the
        # front side, angry on the back side (e.g. sellbot).  It's
        # false if the head model only has a front side (which is
        # presumably angry, e.g. cashbot).
        self.twoFaced = (dna.dept == 's')

        self.attach("head", "torso", "joint34")
        self.attach("torso", "legs", "joint_pelvis")

        # He might need an extra node to rotate for going up ramps.
        self.rotateNode = self.attachNewNode('rotate')
        geomNode = self.getGeomNode()
        geomNode.reparentTo(self.rotateNode)

        # A node for hosting the "rain of gears" particle attack.
        self.frontAttack = self.rotateNode.attachNewNode('frontAttack')
        self.frontAttack.setPos(0, -10, 10)
        self.frontAttack.setScale(2)

        self.setHeight(26)
        self.nametag3d.setScale(2)

        for partName in ("legs", "torso", "head"):
            animDict = {}
            for anim in AnimList:
                animDict[anim] = "%s-%s-%s" % (GenericModel, partName, anim)

            self.loadAnims(animDict, partName)

        # We might need some stars if he gets dizzy.
        self.stars = BattleProps.globalPropPool.getProp('stun')
        self.stars.setPosHprScale(7, 0, 0, 0, 0, -90, 3, 3, 3)
        self.stars.loop('stun')

        # Establish local control over some of the joints.
        self.pelvis = self.getPart("torso")
        self.pelvisForwardHpr = VBase3(0, 0, 0)
        self.pelvisReversedHpr = VBase3(-180, 0, 0)
        self.neck = self.getPart("head")
        self.neckForwardHpr = VBase3(0, 0, 0)
        # -540 makes him spin his head once and a half to switch directions.
        self.neckReversedHpr = VBase3(0, -540, 0)

        self.axle = self.find('**/joint_axle')

        self.doorA = self.__setupDoor(
            '**/joint_doorFront', 'doorA', self.doorACallback,
            VBase3(0, 0, 0), VBase3(0, 0, -80),
            CollisionPolygon(Point3(5, -4, 0.32), Point3(0, -4, 0),
                             Point3(0, 4, 0), Point3(5, 4, 0.32)))

        self.doorB = self.__setupDoor(
            '**/joint_doorRear', 'doorB', self.doorBCallback,
            VBase3(0, 0, 0), VBase3(0, 0, 80),
            CollisionPolygon(Point3(-5, 4, 0.84), Point3(0, 4, 0),
                               Point3(0, -4, 0), Point3(-5, -4, 0.84)))

        # Get the treads in there.  They come from a separate model.
        treadsModel = loader.loadModel('%s-treads' % (GenericModel))
        treadsModel.reparentTo(self.axle)
        self.treadsLeft = treadsModel.find('**/right_tread')
        self.treadsRight = treadsModel.find('**/left_tread')

        self.doorA.request('Closed')
        self.doorB.request('Closed')

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)
        
        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)
        
    def generateHealthBar(self):
        """
        Create a health meter for the suit and put it on his chest
        """
        self.removeHealthBar()

        chestNull = self.find('**/joint_lifeMeter')
        if chestNull.isEmpty():
            return

        # Create health button for the suit
        model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = model.find('**/minnieCircle')
        button.setScale(6.0)
        button.setP(-20)
        button.setColor(self.healthColors[0])
        button.reparentTo(chestNull)
        self.healthBar = button
        glow = BattleProps.globalPropPool.getProp('glow')
        glow.reparentTo(self.healthBar)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(self.healthGlowColors[0])
        button.flattenLight()

        self.healthBarGlow = glow
        self.healthCondition = 0

    def updateHealthBar(self):
        if self.healthBar == None:
            return
        
        health = 1.0 - (float(self.bossDamage) / float(self.bossMaxDamage))
        if (health > 0.95):
            condition = 0
        elif (health > 0.7):
            condition = 1
        elif (health > 0.3):
            condition = 2
        elif (health > 0.05):
            condition = 3
        elif (health > 0.0):
            # This should be blinking red
            condition = 4
        else:
            # This should be blinking red even faster
            condition = 5 

        if (self.healthCondition != condition):
            if (condition == 4):
                blinkTask = Task.loop(Task(self.__blinkRed), 
                                      Task.pause(0.75),
                                      Task(self.__blinkGray),
                                      Task.pause(0.1))
                taskMgr.add(blinkTask, self.uniqueName('blink-task'))
            elif (condition == 5):
                if (self.healthCondition == 4):
                    taskMgr.remove(self.uniqueName('blink-task'))
                blinkTask = Task.loop(Task(self.__blinkRed), 
                                      Task.pause(0.25),
                                      Task(self.__blinkGray),
                                      Task.pause(0.1))
                taskMgr.add(blinkTask, self.uniqueName('blink-task'))
            else:
                self.healthBar.setColor(self.healthColors[condition],1)
                self.healthBarGlow.setColor(self.healthGlowColors[condition],1)
            self.healthCondition = condition

    def __blinkRed(self, task):
        self.healthBar.setColor(self.healthColors[3],1)
        self.healthBarGlow.setColor(self.healthGlowColors[3],1)
        if (self.healthCondition == 5):
            self.healthBar.setScale(1.17)
        return Task.done

    def __blinkGray(self, task):
        self.healthBar.setColor(self.healthColors[4],1)
        self.healthBarGlow.setColor(self.healthGlowColors[4],1)
        if (self.healthCondition == 5):
            self.healthBar.setScale(1.0)
        return Task.done

    def removeHealthBar(self):
        if self.healthBar:
            self.healthBar.removeNode()
            self.healthBar = None
        if (self.healthCondition == 4 or self.healthCondition == 5):
            taskMgr.remove(self.uniqueName('blink-task'))
        self.healthCondition = 0

    def reverseHead(self):
        # Call this before playing an animation that shows him happy
        # when he should be angry, or vice-versa.
        self.neck.setHpr(self.neckReversedHpr)

    def forwardHead(self):
        # Call this to undo the effects of reverseHead().
        self.neck.setHpr(self.neckForwardHpr)

    def reverseBody(self):
        # Call this before playing an animation that shows him facing
        # the wrong direction.
        self.pelvis.setHpr(self.pelvisReversedHpr)

    def forwardBody(self):
        # Call this to undo the effects of reverseBody().
        self.pelvis.setHpr(self.pelvisForwardHpr)
        
    def getShadowJoint(self):
        return self.getGeomNode()

    def getNametagJoints(self):
        """
        Return the CharacterJoint that animates the nametag, in a list.
        """
        return []

    def getDialogueArray(self):
        return self.dialogArray

    def doorACallback(self, isOpen):
        # Called whenever doorA opens or closes.
        pass

    def doorBCallback(self, isOpen):
        # Called whenever doorB opens or closes.
        pass

    # Get intervals that rolls the left and right treads forward or
    # backward from the current position.
    def __rollTreadsInterval(self, object, start = 0, duration = 0, rate = 1):
        def rollTexMatrix(t, object = object):
            object.setTexOffset(TextureStage.getDefault(), t, 0)

        return LerpFunctionInterval(rollTexMatrix, fromData = start,
                                    toData = start + rate * duration,
                                    duration = duration)

    def rollLeftTreads(self, duration, rate):
        start = self.treadsLeftPos
        self.treadsLeftPos += duration * rate
        return self.__rollTreadsInterval(
            self.treadsLeft, start = start, duration = duration, rate = rate)

    def rollRightTreads(self, duration, rate):
        start = self.treadsRightPos
        self.treadsRightPos += duration * rate
        return self.__rollTreadsInterval(
            self.treadsRight, start = start, duration = duration, rate = rate)

    # Manage the doors on the bottom that open and close for Cogs to
    # walk out.

    class DoorFSM(FSM.FSM):
        def __init__(self, name, animate, callback,
                     openedHpr, closedHpr, uniqueName):
            FSM.FSM.__init__(self, name)
            self.animate = animate
            self.callback = callback
            self.openedHpr = openedHpr
            self.closedHpr = closedHpr
            self.uniqueName = uniqueName
            self.ival=0
            self.openSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_door_open.ogg')
            self.closeSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_door_close.ogg')

            self.request('Closed')

        def filterOpening(self, request, args):
            if (request == 'close'):
                return 'Closing'
            return self.defaultFilter(request, args)
        
        def enterOpening(self):
            intervalName = self.uniqueName('open-%s' % (self.animate.getName()))

            self.callback(0)
            ival = Parallel(
                SoundInterval(self.openSfx, node = self.animate, volume = 0.2),
                self.animate.hprInterval(1, self.openedHpr,
                                    blendType = 'easeInOut'),
                Sequence(Wait(0.2), Func(self.callback, 1)),
                name = intervalName)
            ival.start()
            self.ival = ival

        def exitOpening(self):
            self.ival.pause()
            self.ival = None

        def filterOpened(self, request, args):
            if (request == 'close'):
                return 'Closing'
            return self.defaultFilter(request, args)

        def enterOpened(self):
            self.animate.setHpr(self.openedHpr)
            self.callback(1)

        def filterClosing(self, request, args):
            if (request == 'open'):
                return 'Opening'
            return self.defaultFilter(request, args)

        def enterClosing(self):
            intervalName = self.uniqueName('close-%s' % (self.animate.getName()))

            self.callback(1)
            ival = Parallel(
                SoundInterval(self.closeSfx, node = self.animate, volume = 0.2),
                self.animate.hprInterval(1, self.closedHpr,
                                    blendType = 'easeInOut'),
                Sequence(Wait(0.8), Func(self.callback, 0)),
                name = intervalName)
            ival.start()
            self.ival = ival

        def exitClosing(self):
            self.ival.pause()
            self.ival = None

        def filterClosed(self, request, args):
            if (request == 'open'):
                return 'Opening'
            return self.defaultFilter(request, args)

        def enterClosed(self):
            self.animate.setHpr(self.closedHpr)
            self.callback(0)

    
    def __setupDoor(self, jointName, name, callback,
                    openedHpr, closedHpr, cPoly):
        # Find the door joint in the model and set it up for
        # animation.
        joint = self.find(jointName)

        children = joint.getChildren()
        animate = joint.attachNewNode(name)
        children.reparentTo(animate)

        # Put the collision polygon there too.
        cnode = CollisionNode('BossZap')
        cnode.setCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.WallBitmask | ToontownGlobals.CameraBitmask)
        cnode.addSolid(cPoly)
        animate.attachNewNode(cnode)

        # Now we create a tiny FSM to manage the door's state.
        fsm = self.DoorFSM(name, animate, callback,
                           openedHpr, closedHpr, self.uniqueName)

        return fsm

    ### doAnimate and related functions ###

    ## These functions are used to maintain a steady state of
    ## animation on the boss.  To play a particular animation, call
    ## doAnimate(anim = animName).  The animation will be queued for
    ## playing when the Boss finishes his current cycle; to play it
    ## immediately (and get a "pop" in the animation), pass now = 1.

    ## When the list of currently queued animations is exhausted, the
    ## boss will automatically switch back into whatever neutral cycle
    ## is appropriate based on his last-played animation.

    def doAnimate(self, anim = None, now = 0, queueNeutral = 1,
                  raised = None, forward = None, happy = None):
        # Queue a particular cycle for playback, or start the
        # smart-playback mechanism.  See comments above.

        #self.notify.debug('BossCog.doAnimate anim=%s now=%s queueNeutral=%s raised=%s forward=%s happy=%s' % (anim, now,queueNeutral, raised, forward, happy))
        
        if now:
            # Blow away the currently playing animation and saved
            # queue; we want to see this animation now.
            self.stopAnimate()

        if not self.twoFaced:
            # If he's only got one face, it's always "happy", or
            # forward.
            happy = 1

        if raised == None:
            raised = self.raised
        if forward == None:
            forward = self.forward
        if happy == None:
            happy = self.happy
        if now:
            self.raised = raised
            self.forward = forward
            self.happy = happy

        if self.currentAnimIval == None:
            self.accept(self.animDoneEvent, self.__getNextAnim)

        else:
            # If we already have an animation playing, no need to
            # queue up the neutral cycle.
            queueNeutral = 0

        ival, changed = self.__getAnimIval(anim, raised, forward, happy)

        if changed or queueNeutral:
            # Queue up and/or play the particular requested anim.
            self.queuedAnimIvals.append((ival, self.raised, self.forward, self.happy))
            if self.currentAnimIval == None:
                self.__getNextAnim()

    def stopAnimate(self):
        # Stop the currently playing and currently queued animations.
        self.ignore(self.animDoneEvent)
        self.queuedAnimIvals = []
        if self.currentAnimIval:
            self.currentAnimIval.setDoneEvent('')
            self.currentAnimIval.finish()
            self.currentAnimIval = None
        self.raised = self.nowRaised
        self.forward = self.nowForward
        self.happy = self.nowHappy

    def __getNextAnim(self):
        # Picks the next animation in the queue when the current
        # animation runs out.
        if self.queuedAnimIvals:
            ival, raised, forward, happy = self.queuedAnimIvals[0]
            del self.queuedAnimIvals[0]
        else:
            ival, changed = self.__getAnimIval(None, self.raised, self.forward, self.happy)
            raised = self.raised
            forward = self.forward
            happy = self.happy

        if self.currentAnimIval:
            self.currentAnimIval.setDoneEvent('')
            self.currentAnimIval.finish()
        self.currentAnimIval = ival
        self.currentAnimIval.start()
        self.nowRaised = raised
        self.nowForward = forward
        self.nowHappy = happy

    def __getAnimIval(self, anim, raised, forward, happy):
        # Returns an interval to play the indicated animation, and
        # also updates the internal state according to the nature of
        # the animation.
        ival, changed = self.__doGetAnimIval(anim, raised, forward, happy)
        seq = Sequence(ival, name = self.animIvalName)
        seq.setDoneEvent(self.animDoneEvent)
        return seq, changed

    def __doGetAnimIval(self, anim, raised, forward, happy):
        # First, we might need to insert some transition animations to
        # match the new one.

        if (raised == self.raised and forward == self.forward and happy == self.happy):
            # We are not changing state.
            return self.getAnim(anim), (anim != None)

        # We are changing state.  Figure out how to get there.
        startsHappy = self.happy
        endsHappy = self.happy
        ival = Sequence()

        if raised and not self.raised:
            # Pop up first.
            upIval = self.getAngryActorInterval('Fb_down2Up')

            if self.forward:
                ival = upIval
            else:
                ival = Sequence(
                    Func(self.reverseBody),
                    upIval,
                    Func(self.forwardBody))
            ival = Parallel(SoundInterval(self.upSfx, node = self),
                            ival)

        if forward != self.forward:
            # Spin to new facing.                
            if forward:
                animName = 'Bb2Ff_spin'
            else:
                animName = 'Ff2Bb_spin'
            ival = Sequence(ival, ActorInterval(self, animName))
            startsHappy = 1
            endsHappy = 1

        startNeckHpr = self.neckForwardHpr
        endNeckHpr = self.neckForwardHpr
        if self.happy != startsHappy:
            startNeckHpr = self.neckReversedHpr
        if happy != endsHappy:
            endNeckHpr = self.neckReversedHpr

        if startNeckHpr != endNeckHpr:
            ival = Sequence(
                Func(self.neck.setHpr, startNeckHpr),
                ParallelEndTogether(
                ival,
                Sequence(self.neck.hprInterval(0.5, endNeckHpr,
                                               startHpr = startNeckHpr,
                                               blendType = 'easeInOut'),
                         Func(self.neck.setHpr, self.neckForwardHpr))))

        elif endNeckHpr != self.neckForwardHpr:
            ival = Sequence(Func(self.neck.setHpr, startNeckHpr),
                            ival,
                            Func(self.neck.setHpr, self.neckForwardHpr))

        if not raised and self.raised:
            # Pop down after.
            downIval = self.getAngryActorInterval('Fb_down2Up', playRate = -1)

            if forward:
                ival = Sequence(ival, downIval)
            else:
                ival = Sequence(
                    ival,
                    Func(self.reverseBody),
                    downIval,
                    Func(self.forwardBody))

            ival = Parallel(SoundInterval(self.downSfx, node = self),
                            ival)

        self.raised = raised
        self.forward = forward
        self.happy = happy

        # Now tack on the animation we're trying for.
        if anim != None:
            ival = Sequence(ival, self.getAnim(anim))

        return ival, 1

    def setDizzy(self, dizzy):
        if dizzy and not self.dizzy:
            base.playSfx(self.dizzyAlert)
            
        self.dizzy = dizzy
        if dizzy:
            self.stars.reparentTo(self.neck)
            base.playSfx(self.birdsSfx, looping = 1)
        else:
            self.stars.detachNode()
            self.birdsSfx.stop()

    def getAngryActorInterval(self, animName, **kw):
        # Returns an ActorInterval to play the indicated angry
        # animation.  If self.happy is true, flips the head around to
        # show the happy (or only) face while playing it.
        if self.happy:
            ival = Sequence(
                Func(self.reverseHead),
                ActorInterval(self, animName, **kw),
                Func(self.forwardHead))
        else:
            ival = ActorInterval(self, animName, **kw)

        return ival

    def getAnim(self, anim):
        # A low-level function to return an interval to play the
        # indicated animation, and update the internal state as if the
        # animation has been played.  This may be called by external
        # objects.
        ival = None
        if anim == None:
            # Neutral cycle
            partName = None

            if self.happy:
                animName = 'Ff_neutral'
            else:
                animName = 'Fb_neutral'

            if self.raised:
                # Play the animation on the whole boss.
                ival = ActorInterval(self, animName)
            else:
                # Play the animation on the upper part of the boss
                # only, and play the lowered animation on the legs.
                ival = Parallel(ActorInterval(self, animName,
                                              partName = ['torso', 'head']),
                                ActorInterval(self, 'Fb_downNeutral',
                                              partName = 'legs'))

            if not self.forward:
                ival = Sequence(
                    Func(self.reverseBody),
                    ival,
                    Func(self.forwardBody))
            
        elif anim == 'down2Up':
            ival = Parallel(SoundInterval(self.upSfx, node = self),
                            self.getAngryActorInterval('Fb_down2Up'))
                
            self.raised = 1

        elif anim == 'up2Down':
            # We fake this animation by playing down2Up backward.
            ival = Parallel(SoundInterval(self.downSfx, node = self),
                            self.getAngryActorInterval('Fb_down2Up', playRate = -1))

            self.raised = 0
            
        elif anim == 'throw':
            self.doAnimate(None, raised = 1, happy = 0, queueNeutral = 0)

            ival = Parallel(Sequence(SoundInterval(self.throwSfx, node = self), duration = 0),
                            self.getAngryActorInterval('Fb_UpThrow'))

        elif anim == 'hit':
            if self.raised:
                # Hits always knock us down.
                self.raised = 0
                ival = self.getAngryActorInterval('Fb_firstHit')
            else:
                ival = self.getAngryActorInterval('Fb_downHit')

            ival = Parallel(SoundInterval(self.reelSfx, node = self), ival)

        elif anim == 'ltSwing' or anim == 'rtSwing':
            self.doAnimate(None, raised = 0, happy = 0, queueNeutral = 0)

            if anim == 'ltSwing':
                ival = Sequence(Track((0, self.getAngryActorInterval('Fb_downLtSwing')),
                                      (0.9, SoundInterval(self.swingSfx, node = self)),
                                      (1, Func(self.bubbleL.unstash))),
                                Func(self.bubbleL.stash))
            else:
                ival = Sequence(Track((0, self.getAngryActorInterval('Fb_downRtSwing')),
                                      (0.9, SoundInterval(self.swingSfx, node = self)),
                                      (1, Func(self.bubbleR.unstash))),
                                Func(self.bubbleR.stash))

        elif anim == 'frontAttack':
            # This is a bit hacky, and involves code defined in
            # DistributedSellbotBoss.py.
            self.doAnimate(None, raised = 1, happy = 0, queueNeutral = 0)

            pe = BattleParticles.loadParticleFile('bossCogFrontAttack.ptf')

            # Keep the head reversed so we play the spin animation
            # with the sad face showing.
            ival = Sequence(
                Func(self.reverseHead),
                ActorInterval(self, 'Bb2Ff_spin'),
                Func(self.forwardHead))

            if self.forward:
                # The animation starts with the torso reversed; undo this.
                ival = Sequence(
                    Func(self.reverseBody),
                    ParallelEndTogether(ival,
                                        self.pelvis.hprInterval(0.5, self.pelvisForwardHpr,
                                                                blendType = 'easeInOut')),
                    )
                
            ival = Sequence(Track((0, ival),
                                  (0, SoundInterval(self.spinSfx, node = self)),
                                  (0.9, Parallel(SoundInterval(self.rainGearsSfx, node = self),
                                                 ParticleInterval(pe, self.frontAttack, worldRelative = 0,
                                                                  duration = 1.5, cleanup = True),
                                                 duration = 0)),
                                  (1.9, Func(self.bubbleF.unstash)),
                                  ),
                            Func(self.bubbleF.stash))
            self.forward = 1
            self.happy = 0
            self.raised = 1

        elif anim == 'areaAttack':
            # This is hacky too, just like above.
            if self.twoFaced:
                self.doAnimate(None, raised = 1, happy = 0, queueNeutral = 0)
            else:
                #RAU the lawbot is one faced
                self.doAnimate(None, raised = 1, happy = 1, queueNeutral = 1)

            ival = Parallel(ActorInterval(self, 'Fb_jump'),
                            Sequence(SoundInterval(self.swishSfx, duration = 1.1, node = self),
                                     SoundInterval(self.boomSfx, duration = 1.9)),
                            Sequence(Wait(1.21),
                                     Func(self.announceAreaAttack)))
            if self.twoFaced:
                self.happy = 0
            else:
                self.happy = 1
            
            self.raised = 1

        elif anim == 'Fb_fall':
            ival = Parallel(ActorInterval(self, 'Fb_fall'),
                            Sequence(SoundInterval(self.reelSfx, node = self),
                                     SoundInterval(self.deathSfx)))

        elif isinstance(anim, str):
            ival = ActorInterval(self, anim)

        else:
            # It must be an interval to play directly.
            ival = anim

        return ival
