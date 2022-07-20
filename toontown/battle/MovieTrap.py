from direct.interval.IntervalGlobal import *
from .BattleBase import *
from .BattleProps import *
from .BattleSounds import *

from . import MovieUtil
from . import MovieCamera
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownBattleGlobals
from direct.actor import Actor
from direct.particles import ParticleEffect
from . import BattleParticles
from . import BattleProps
from . import MovieNPCSOS
from .MovieSound import createSuitResetPosTrack

notify = DirectNotifyGlobal.directNotify.newCategory('MovieTrap')

def doTraps(traps):
    """ Traps occur simultaneously - if more than one trap is
        thrown at the same suit, they explode
    """
    if (len(traps) == 0):
        return (None, None)

    npcArrivals, npcDepartures, npcs = MovieNPCSOS.doNPCTeleports(traps)

    hasUberTrapConflict = False

    # Group the traps by targeted suit
    suitTrapsDict = {}
    for trap in traps:
        targets = trap['target']
        if (len(targets) == 1):
            suitId = targets[0]['suit'].doId
            if (suitId in suitTrapsDict):
                suitTrapsDict[suitId].append(trap)
            else:
                suitTrapsDict[suitId] = [trap]
        else:
            # We're dealing with an NPC trap, which can have multiple
            # targets - we only want to use the first valid target, 
            # however, to avoid tossing too many traps
            for target in targets:
                suitId = target['suit'].doId
                if (suitId not in suitTrapsDict):
                    suitTrapsDict[suitId] = [trap]
                    break
            if trap['level'] == UBER_GAG_LEVEL_INDEX:
                if len(traps) > 1:
                    hasUberTrapConflict = True
                for oneTarget in trap['target']:
                    suit = oneTarget['suit']
                    if suit.battleTrap != NO_TRAP:
                        #we can get here in a 3 suit battle, by placing quicksand then doing train
                        hasUberTrapConflict = True
                    

    suitTrapLists = list(suitTrapsDict.values())

    mtrack = Parallel()
    for trapList in suitTrapLists:
        # Set the appropriate trapProps for use with this trap
        trapPropList = []
        for i in range(len(trapList)):
            trap = trapList[i]
            level = trap['level']
            if (level == 0): # banana
                banana = globalPropPool.getProp('banana')
                banana2 = MovieUtil.copyProp(banana)
                trapPropList.append([banana, banana2])
            elif (level == 1): # rake
                rake = globalPropPool.getProp('rake')
                rake2 = MovieUtil.copyProp(rake)
                rake.pose('rake', 0)
                rake2.pose('rake', 0)
                trapPropList.append([rake, rake2])
            elif (level == 2): # marbles
                marbles = globalPropPool.getProp('marbles')
                marbles2 = MovieUtil.copyProp(marbles)
                trapPropList.append([marbles, marbles2])
            elif (level == 3): # quicksand
                trapPropList.append([globalPropPool.getProp('quicksand')])
            elif (level == 4): # trapdoor
                trapPropList.append([globalPropPool.getProp('trapdoor')])
            elif (level == 5): # tnt
                tnt = globalPropPool.getProp('tnt')
                tnt2 = MovieUtil.copyProp(tnt)
                trapPropList.append([tnt, tnt2])
            elif (level == 6): # tnt #UBER
                tnt = globalPropPool.getProp('traintrack') #('trapdoor') 
                tnt2 = MovieUtil.copyProp(tnt)
                trapPropList.append([tnt, tnt2])
            else:
                notify.warning('__doTraps() - Incorrect trap level: \
                %d' % level)
                
        if (len(trapList) == 1) and not hasUberTrapConflict:
            # Trap is successfully placed
            ival = __doTrapLevel(trapList[0], trapPropList[0])
            if (ival):
                mtrack.append(ival)
        else:
            assert(len(trapList) > 1 or hasUberTrapConflict)
            subMtrack = Parallel()
            for i in range(len(trapList)):
                trap = trapList[i]
                trapProps = trapPropList[i]
                ival = __doTrapLevel(trap, trapProps, explode=1)
                if (ival):
                    subMtrack.append(ival)
            mtrack.append(subMtrack)

    trapTrack = Sequence(npcArrivals, mtrack, npcDepartures)

    camDuration = mtrack.getDuration()
    enterDuration = npcArrivals.getDuration()
    exitDuration = npcDepartures.getDuration()
    camTrack = MovieCamera.chooseTrapShot(traps, camDuration, enterDuration,
                                                exitDuration)
    return (trapTrack, camTrack)

def __doTrapLevel(trap, trapProps, explode=0):
    """ __doTrapLevel(trap)
    """
    level = trap['level']
    if (level == 0):
        return __trapBanana(trap, trapProps, explode)
    elif (level == 1):
        return __trapRake(trap, trapProps, explode)
    elif (level == 2):
        return __trapMarbles(trap, trapProps, explode)
    elif (level == 3):
        return __trapQuicksand(trap, trapProps, explode)
    elif (level == 4):
        return __trapTrapdoor(trap, trapProps, explode)
    elif (level == 5):
        return __trapTNT(trap, trapProps, explode)
    elif (level == 6):
        return __trapTrain(trap, trapProps, explode)
    return None

def getSoundTrack(fileName, delay=0.01, duration=None, node=None):
    """ This functions returns the standard sound track, which involves one sound
    effect with a possible delay beforehand and an optional duration specification.
    """

    soundEffect = globalBattleSoundCache.getSound(fileName)

    if duration:
        return Sequence(Wait(delay),
                        SoundInterval(soundEffect, duration=duration, node=node))
    else:
        return Sequence(Wait(delay),
                        SoundInterval(soundEffect, node=node))


def __createThrownTrapMultiTrack(trap, propList, propName, propPos=None,
                                 propHpr=None, anim=0, explode=0):
    toon = trap['toon']
    level = trap['level']
    battle = trap['battle']
    target = trap['target']
    suit = target[0]['suit']
    targetPos = suit.getPos(battle)
    thrownProp = propList[0]
    unthrownProp = propList[1]

    # Different toon body types throw at different times
    torso = toon.style.torso
    torso = torso[0] # only want the first letter (s, m, l)
    if (torso == 'l'):
        throwDelay = 2.3
    elif (torso == 'm'):
        throwDelay = 2.3
    else:
        throwDelay = 1.9
        
    throwDuration = 0.9
    animBreakPoint = throwDelay + throwDuration
    animDelay = 3.1
    # All the traps use the default trap distance, except the rake (gets stepped into)
    trapTrack = ToontownBattleGlobals.TRAP_TRACK
    trapTrackNames = ToontownBattleGlobals.AvProps[trapTrack]
    trapName = trapTrackNames[level]

    hands = toon.getRightHands()
    propTrack = Sequence()
    if propPos and propHpr:
        propTrack.append(Func(MovieUtil.showProps, propList,
                              hands, propPos, propHpr))
    else:
        propTrack.append(Func(MovieUtil.showProps, propList, hands))

    if (anim == 1):
        pTracks = Parallel()
        for prop in propList:
            pTracks.append(ActorInterval(prop, propName,
                                         duration=animBreakPoint))
        propTrack.append(pTracks)

    throwTrack = Sequence()
    throwTrack.append(Wait(throwDelay))
    # Must hide the unthrown prop so there doesn't appear to be two, since the
    # thrown prop will be parented to the battle and therefore visible for
    # every level of detail
    throwTrack.append(Func(unthrownProp.reparentTo, hidden))
    # Update on the toon to be sure that all LOD's see the same thrown trap right
    throwTrack.append(Func(toon.update))

    # Set the trap prop as the suit's trap prop
    if (suit.battleTrap != NO_TRAP):
        notify.debug('trapSuit() - trap: %d destroyed existing trap: %d' % \
                     (level, suit.battleTrap))
        battle.removeTrap(suit)
    if (trapName == 'rake'):
        trapProp = globalPropPool.getProp('rake-react')
    else:
        trapProp = MovieUtil.copyProp(thrownProp)
    suit.battleTrapProp = trapProp
    suit.battleTrap = level
    suit.battleTrapIsFresh = 1

    # Each prop varies slightly for the throw
    if (trapName == 'banana'):
        trapPoint, trapHpr = battle.getActorPosHpr(suit)
        trapPoint.setY(MovieUtil.SUIT_TRAP_DISTANCE)
        slidePoint = Vec3(trapPoint.getX(), trapPoint.getY()-2, trapPoint.getZ())
        throwingTrack = createThrowingTrack(
            thrownProp, slidePoint, duration=0.9, parent=battle)
        moveTrack = LerpPosInterval(thrownProp, 0.8, pos=trapPoint,
                                    other=battle)
        animTrack = ActorInterval(thrownProp, propName,
                                  startTime=animBreakPoint)
        slideTrack = Parallel(moveTrack, animTrack)
        motionTrack = Sequence(throwingTrack, slideTrack)
        hprTrack = LerpHprInterval(thrownProp, 1.7, hpr=Point3(0, 0, 0))
        soundTrack = getSoundTrack('TL_banana.ogg', node=toon)
        scaleTrack = LerpScaleInterval(thrownProp, 1.7, scale=MovieUtil.PNT3_ONE)
        throwTrack.append(Wait(0.25)) # Wait a bit more before throwing
        throwTrack.append(Func(thrownProp.wrtReparentTo, suit))
        throwTrack.append(Parallel(motionTrack, hprTrack, scaleTrack, soundTrack))
    elif (trapName == 'tnt'): # Tnt must start its fuse (particle effect)
        trapPoint, trapHpr = battle.getActorPosHpr(suit)
        trapPoint.setY(MovieUtil.SUIT_TRAP_TNT_DISTANCE - 3.9)
        trapPoint.setZ(trapPoint.getZ() + 0.4)
        throwingTrack = createThrowingTrack(
            thrownProp, trapPoint, duration=throwDuration, parent=battle)
        hprTrack = LerpHprInterval(thrownProp, 0.9, hpr=Point3(0, 90, 0))
        scaleTrack = LerpScaleInterval(thrownProp, 0.9, scale=MovieUtil.PNT3_ONE)
        soundTrack = getSoundTrack('TL_dynamite.ogg', delay=0.8, duration=0.7, node=suit)
        throwTrack.append(Wait(0.2)) # Wait a bit more before throwing
        throwTrack.append(Parallel(throwingTrack, hprTrack, scaleTrack, soundTrack))
    elif (trapName == 'marbles'): # Marbles aren't tossed but lerped
        trapPoint, trapHpr = battle.getActorPosHpr(suit)
        trapPoint.setY(MovieUtil.SUIT_TRAP_MARBLES_DISTANCE)
        flingDuration = 0.2
        rollDuration = 1.0
        throwDuration = flingDuration + rollDuration
        landPoint = Point3(0, trapPoint.getY()+2, trapPoint.getZ())
        throwPoint = Point3(0, trapPoint.getY(), trapPoint.getZ())
        moveTrack = Sequence(
            Func(thrownProp.wrtReparentTo, suit),
            Func(thrownProp.setHpr, Point3(94, 0, 0)),
            LerpPosInterval(thrownProp, flingDuration, pos=landPoint, other=suit),
            LerpPosInterval(thrownProp, rollDuration, pos=throwPoint, other=suit),
            )
        animTrack = ActorInterval(thrownProp, propName,
                                  startTime=throwDelay+0.9)
        scaleTrack = LerpScaleInterval(thrownProp, throwDuration,
                                       scale=MovieUtil.PNT3_ONE)
        soundTrack = getSoundTrack('TL_marbles.ogg', delay=0.1, node=toon)
        throwTrack.append(Wait(0.2)) # Need to wait a bit more before throwing
        throwTrack.append(Parallel(moveTrack, animTrack, scaleTrack, soundTrack))
    elif (trapName == 'rake'):
        trapPoint, trapHpr = battle.getActorPosHpr(suit)
        trapPoint.setY(MovieUtil.SUIT_TRAP_RAKE_DISTANCE)
        throwDuration = 1.1
        throwingTrack = createThrowingTrack(
            thrownProp, trapPoint, duration=throwDuration, parent=suit)
        hprTrack = LerpHprInterval(thrownProp, throwDuration,
                                   hpr=VBase3(63.43, -90.00, 63.43))
        scaleTrack = LerpScaleInterval(thrownProp, 0.9,
                                       scale=Point3(0.7, 0.7, 0.7))
        soundTrack = SoundInterval(globalBattleSoundCache.getSound('TL_rake_throw_only.ogg'), duration=1.1, node=suit)

        throwTrack.append(Wait(0.2))
        throwTrack.append(Parallel(throwingTrack, hprTrack, scaleTrack, soundTrack))
    else:
        notify.warning('__createThrownTrapMultiTrack() - Incorrect trap: \
                         %s thrown from toon' % trapName)
        
    def placeTrap(trapProp, suit, battle=battle, trapName=trapName):
        # In case multiple traps are thrown to the same spot, we must return (doing
        # nothing) if the trapProp we have has actually been removed and replaced
        # by another trap (it won't exist anymore)
        if not trapProp or trapProp.isEmpty():
            return
        trapProp.wrtReparentTo(suit)
        trapProp.show()
        # Set the new trap prop
        # All the traps use the default trap distance, except the rake
        if (trapName == 'rake'):
            # The rake will actually be completed replaced with a different rake model
            # which has a different animation on it for when the rake is stepped on
            trapProp.setPos(0, MovieUtil.SUIT_TRAP_RAKE_DISTANCE, 0)
            # reorient the rake correctly to be stepped on
            trapProp.setHpr(Point3(0, 270, 0))
            trapProp.setScale(Point3(0.7, 0.7, 0.7))
            # The rake must be a specific distance from each suit for that
            # suit to be able to walk into the rake
            rakeOffset = MovieUtil.getSuitRakeOffset(suit)
            trapProp.setY(trapProp.getY() + rakeOffset)
        elif (trapName == 'banana'):
            trapProp.setHpr(0, 0, 0)
            trapProp.setPos(0, MovieUtil.SUIT_TRAP_DISTANCE, -0.35)
            trapProp.pose(trapName, trapProp.getNumFrames(trapName) - 1)
        elif (trapName == 'marbles'):
            trapProp.setHpr(Point3(94, 0, 0))
            trapProp.setPos(0, MovieUtil.SUIT_TRAP_MARBLES_DISTANCE, 0)
            trapProp.pose(trapName, trapProp.getNumFrames(trapName) - 1)
        elif (trapName == 'tnt'):
            trapProp.setHpr(0, 90, 0)
            trapProp.setPos(0, MovieUtil.SUIT_TRAP_TNT_DISTANCE, 0.4)
        else:
            notify.warning('placeTrap() - Incorrect trap: %s placed on a suit' \
                            % trapName)


    # Need hidden node to take the place of the exploding trap prop, we'll parent
    # the explosion itself to this hidden node
    dustNode = hidden.attachNewNode("DustNode")
    def placeDustExplosion(dustNode=dustNode, thrownProp=thrownProp, battle=battle):
        dustNode.reparentTo(battle)
        dustNode.setPos(thrownProp.getPos(battle))

    if (explode == 1): # If the trap prop collides with other traps, destroy it
        throwTrack.append(Func(thrownProp.wrtReparentTo, hidden))
        throwTrack.append(Func(placeDustExplosion))
        throwTrack.append(createCartoonExplosionTrack(
            dustNode, 'dust', explosionPoint=Point3(0, 0, 0)))
        throwTrack.append(Func(battle.removeTrap, suit))
    else:
        throwTrack.append(Func(placeTrap, trapProp, suit))
        # If the trap is the tnt, start the fuse on the trapProp we just placed
        if (trapName == 'tnt'):
            tip = trapProp.find("**/joint_attachEmitter")
            sparks = BattleParticles.createParticleEffect(file='tnt')
            trapProp.sparksEffect = sparks
            throwTrack.append(Func(sparks.start, tip))
    throwTrack.append(Func(MovieUtil.removeProps, propList))

    # If using the tnt, must add in a track for the sparks particle effect
#    if (trapName == 'tnt'):
#        tip = thrownProp.find("**/joint_attachEmitter")
#        sparks = BattleParticles.createParticleEffect(file='tnt')
#        sparksTrack = Sequence(
#            Func(sparks.start, tip),
#            Wait(throwDelay+throwDuration),
#            Func(sparks.cleanup),
#            )
#        throwTrack = Parallel(throwTrack, sparksTrack)

    toonTrack = Sequence(
        Func(toon.headsUp, battle, targetPos),
        ActorInterval(toon, 'toss'),
        Func(toon.loop, 'neutral'),
        )
    return Parallel(propTrack, throwTrack, toonTrack)

def __createPlacedTrapMultiTrack(trap, prop, propName, propPos=None,
                                 propHpr=None, explode=0, visibleOnlyForThisSuitId = None):
    toon = trap['toon']
    if ('npc' in trap):
        toon = trap['npc']
    level = trap['level']
    battle = trap['battle']
    origHpr = toon.getHpr(battle)
    trapPoint = Point3(0, MovieUtil.SUIT_TRAP_DISTANCE, 0.025)
    trapDelay = 2.5
    hands = toon.getLeftHands()

    def placeDustExplosion(dustNode, trapProp, battle):
        dustNode.reparentTo(battle)
        dustNode.setPos(trapProp.getPos(battle))

    trapTracks = Parallel()

    firstTime = 1
    targets = trap['target']
    for target in targets:
        suit = target['suit']
        suitPos = suit.getPos(battle)
        targetPos = suitPos
        trapProp = MovieUtil.copyProp(prop)

        showThisTrap = True
        if visibleOnlyForThisSuitId and visibleOnlyForThisSuitId != suit.doId :
            showThisTrap = False
            
        trapTrack = Sequence()
        trapTrack.append(Wait(trapDelay))
        if showThisTrap:
            notify.debug('showing trap %s for %d' % (trapProp.getName(), suit.doId))
            trapTrack.append(Func(trapProp.show))
        else:
            notify.debug('hiding trap %s for %d' % (trapProp.getName(), suit.doId))
            trapTrack.append(Func(trapProp.hide))
        trapTrack.append(Func(trapProp.setScale, Point3(0.1, 0.1, 0.1)))
        trapTrack.append(Func(trapProp.reparentTo, suit))
        trapTrack.append(Func(trapProp.setPos, trapPoint))
        trapTrack.append(LerpScaleInterval(trapProp, 1.2, Point3(1.7, 1.7, 1.7)))

        if (explode == 1): # If the trap prop collides with another trap, destroy it
            # Need hidden node to take the place of the exploding trap prop, 
            # we'll parent the explosion itself to this hidden node
            dustNode = hidden.attachNewNode("DustNode")

            trapTrack.append(Func(trapProp.wrtReparentTo, hidden))
            trapTrack.append(Func(placeDustExplosion, dustNode, trapProp,
                                        battle))
            trapTrack.append(createCartoonExplosionTrack(
                dustNode, 'dust', explosionPoint=Point3(0, 0, 0)))
            trapTrack.append(Func(MovieUtil.removeProp, trapProp))
            trapTrack.append(Func(battle.removeTrap, suit))

        else:

            # Set the trap prop as the suit's trap prop
            if (suit.battleTrap != NO_TRAP):
                notify.debug('trapSuit() - trap: %d destroyed existing trap: %d' % (level, suit.battleTrap))
                battle.removeTrap(suit)
            suit.battleTrapProp = trapProp
            suit.battleTrap = level
            suit.battleTrapIsFresh = 1

        trapTracks.append(trapTrack)

    button = globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    
    toonTrack = Sequence()
    toonTrack.append(Func(MovieUtil.showProps, buttons, hands))
    toonTrack.append(Func(toon.headsUp, battle, suitPos))
    toonTrack.append(ActorInterval(toon, 'pushbutton'))
    toonTrack.append(Func(MovieUtil.removeProps, buttons))
    toonTrack.append(Func(toon.loop, 'neutral'))
    toonTrack.append(Func(toon.setHpr, battle, origHpr))

    if (propName == 'quicksand'):
        propSound = globalBattleSoundCache.getSound('TL_quicksand.ogg')
    else:
        propSound = globalBattleSoundCache.getSound('TL_trap_door.ogg')

    buttonSound = globalBattleSoundCache.getSound('AA_drop_trigger_box.ogg')        
    soundTrack = Sequence(
        Wait(2.3),
        SoundInterval(buttonSound, duration = 0.67, node=toon),
        Wait(0.3),
        SoundInterval(propSound, duration=0.5, node=toon),
        )

    return Parallel(trapTracks, toonTrack, soundTrack)

def __trapBanana(trap, trapProps, explode):
    """ __trapBanana(trap)
    """
    toon = trap['toon']
    suit = trap['target'][0]['suit']
    notify.debug('toon: %s lays banana peel in front of suit: %d' % \
        (toon.getName(), suit.doId))
    bananas = trapProps
    return __createThrownTrapMultiTrack(trap, bananas, 'banana', anim=1, explode=explode)

def __trapRake(trap, trapProps, explode):
    """ __trapRake(trap)
    """
    toon = trap['toon']
    suit = trap['target'][0]['suit']
    notify.debug('toon: %s lays rake in front of suit: %d' % \
        (toon.getName(), suit.doId))
    rakes = trapProps
    return __createThrownTrapMultiTrack(trap, rakes, 'rake', anim=1, explode=explode)

def __trapMarbles(trap, trapProps, explode):
    """ __trapMarbles(trap)
    """
    toon = trap['toon']
    suit = trap['target'][0]['suit']
    notify.debug('toon: %s lays marbles in front of suit: %d' % \
        (toon.getName(), suit.doId))
    bothMarbles = trapProps
    pos = Point3(0, 0, 0)
    hpr = Point3(0, 0, -30)
    return __createThrownTrapMultiTrack(trap, bothMarbles, 'marbles',
                                        pos, hpr, anim=1, explode=explode)

def __trapQuicksand(trap, trapProps, explode):
    """ __trapQuicksand(trap)
    """
    toon = trap['toon']
    suit = trap['target'][0]['suit']
    notify.debug('toon: %s lays quicksand in front of suit: %d' % \
        (toon.getName(), suit.doId))
    quicksand = trapProps[0]
    return __createPlacedTrapMultiTrack(trap, quicksand, 'quicksand', explode=explode)

def __trapTrapdoor(trap, trapProps, explode):
    """ __trapTrapdoor(trap)
    """
    toon = trap['toon']
    if ('npc' in trap):
        toon = trap['npc']
    targets = trap['target']
    for target in targets:
        suit = target['suit']
        notify.debug('toon: %s lays trapdoor in front of suit: %d' % \
            (toon.getName(), suit.doId))
    trapdoor = trapProps[0]
    return __createPlacedTrapMultiTrack(trap, trapdoor, 'trapdoor', explode=explode)

def __trapTNT(trap, trapProps, explode):
    """ __trapTNT(trap)
    """
    toon = trap['toon']
    suit = trap['target'][0]['suit']
    notify.debug('toon: %s lays TNT in front of suit: %d' % \
        (toon.getName(), suit.doId))
    tnts = trapProps
    return __createThrownTrapMultiTrack(trap, tnts, 'tnt', anim=0, explode=explode)

def __trapTrain(trap, trapProps, explode):
    """ __trapTraun(trap, trapProps, explode)
    Do some funky stuff since we want to place only 1 train track, not 4
    """
    toon = trap['toon']
    if ('npc' in trap):
        toon = trap['npc']
    targets = trap['target']
    battle = trap['battle']

    visibleOnlyForThisSuitId = 0
    centerSuit = None
    closestXDistance = 10000
    for target in targets:
        suit = target['suit']
        suitPoint, suitHpr = battle.getActorPosHpr(suit)        
        xDistance = abs(suitPoint.getX())
        if xDistance < closestXDistance:
            visibleOnlyForThisSuitId = suit.doId
            closestXDistance = xDistance
            centerSuit = suit
        notify.debug('toon: %s doing traintrack in front of suit: %d' % \
            (toon.getName(), suit.doId))
        
    traintrack = trapProps[0]
    
    #return __createPlacedTrapMultiTrack(trap, trapdoor, 'trapdoor', explode=explode,
    #                                    visibleOnlyForThisSuitId = visibleOnlyForThisSuitId )
    return __createPlacedGroupTrapTrack (trap, traintrack, 'traintrack', centerSuit,
                                         explode=explode )



def createThrowingTrack(object, target, duration=1.0, parent=render, gravity=-32.144):

    values = {}
    values['origin'] = None
    values['velocity'] = None
    def calcOriginAndVelocity(object=object, target=target, values=values,
                     duration=duration, parent=parent, gravity=gravity):
        object.wrtReparentTo(parent)
        values['origin'] = object.getPos(parent)
        origin = object.getPos(parent)
        # Calculate the initial velocity required for the object to land at the target
        values['velocity'] = ((target[2]-origin[2]) - (0.5*gravity*duration*duration)) \
                             / duration
        
    def throwPos(t, object, duration, target, values=values, gravity=-32.144):
        if (values['origin'] != None):
            origin = values['origin']
        else:
            origin = object.getPos()

        if (values['velocity'] != None):
            velocity = values['velocity']
        else:
            velocity = 16

        x = origin[0]*(1-t) + target[0]*t
        y = origin[1]*(1-t) + target[1]*t
        time = t*duration
        z = origin[2] + velocity*time + (0.5*gravity*time*time)
        object.setPos(x, y, z)

    return Sequence(
        Func(calcOriginAndVelocity),
        LerpFunctionInterval(throwPos, fromData=0., toData=1., duration=duration,
                             extraArgs=[object, duration, target])
        )

def createCartoonExplosionTrack(parent, animName, explosionPoint=None):
    explosionTrack = Sequence()
    explosion = BattleProps.globalPropPool.getProp(animName)
    explosion.setBillboardPointEye()
    if not explosionPoint:
        explosionPoint = Point3(0, 3.6, 2.1)
    if (animName == 'dust'):
        scale = Point3(0.1, 0.9, 1)
    explosionTrack.append(Func(explosion.reparentTo, parent))
    explosionTrack.append(Func(explosion.setPos, explosionPoint))
    explosionTrack.append(Func(explosion.setScale, scale))
    explosionTrack.append(ActorInterval(explosion, animName))
    explosionTrack.append(Func(MovieUtil.removeProp, explosion))
    return explosionTrack


def __createPlacedGroupTrapTrack(trap, prop, propName, centerSuit,propPos=None,
                                 propHpr=None,  explode=0, ):
    """
    mainly to make the train track appear.  We only want one, and parented to the battle
    """
    toon = trap['toon']
    if ('npc' in trap):
        toon = trap['npc']
    level = trap['level']
    battle = trap['battle']
    origHpr = toon.getHpr(battle)
    #5 was determined empirically
    trapPoint = Point3(0, 5 - MovieUtil.SUIT_TRAP_DISTANCE, 0.025)
    trapDelay = 2.5
    hands = toon.getLeftHands()

    def placeDustExplosion(dustNode, trapProp, battle):
        dustNode.reparentTo(battle)
        dustNode.setPos(trapProp.getPos(battle))

    trapTracks = Parallel()

    firstTime = 1
    targets = trap['target']
    #for target in targets:
    if True:
        suit = centerSuit # target['suit']
        suitPos = suit.getPos(battle)
        targetPos = suitPos
        trapProp = MovieUtil.copyProp(prop)

        showThisTrap = True
        #if visibleOnlyForThisSuitId and visibleOnlyForThisSuitId != suit.doId :
        #    showThisTrap = False

        trapTrack = Sequence()
        trapTrack.append(Wait(trapDelay))
        if showThisTrap:
            notify.debug('showing trap %s for %d' % (trapProp.getName(), suit.doId))
            trapTrack.append(Func(trapProp.show))
        else:
            notify.debug('hiding trap %s for %d' % (trapProp.getName(), suit.doId))
            trapTrack.append(Func(trapProp.hide))
        trapTrack.append(Func(trapProp.setScale, Point3(0.1, 0.1, 0.1)))
        trapTrack.append(Func(trapProp.reparentTo, battle))
        trapTrack.append(Func(trapProp.setPos, trapPoint))
        trapTrack.append(Func(trapProp.setH, 0))
        trapTrack.append(LerpScaleInterval(trapProp, 1.2, Point3(1.0, 1.0, 1.0)))

        if (explode == 1): # If the trap prop collides with another trap, destroy it
            # Need hidden node to take the place of the exploding trap prop, 
            # we'll parent the explosion itself to this hidden node
            dustNode = hidden.attachNewNode("DustNode")

            removeTrapsParallel = Parallel()

            oneTrapTrack = Sequence()
            oneTrapTrack.append(Func(trapProp.wrtReparentTo, hidden))
            oneTrapTrack.append(Func(placeDustExplosion, dustNode, trapProp,
                                        battle))
            oneTrapTrack.append(createCartoonExplosionTrack(
                dustNode, 'dust', explosionPoint=Point3(0, 0, 0)))
            oneTrapTrack.append(Func(MovieUtil.removeProp, trapProp))
            #oneTrapTrack.append(Func(battle.removeTrap, suit))

            removeTrapsParallel.append(oneTrapTrack)

            #we need to remove the battle traps of the other suits too
            for target in trap['target']:
                otherSuit = target['suit']
                #if otherSuit != suit and otherSuit.battleTrapProp:
                if otherSuit.battleTrapProp:
                    otherDustNode = hidden.attachNewNode("DustNodeOtherSuit")
                    otherTrapTrack = Sequence()
                    otherTrapTrack.append(Func(otherSuit.battleTrapProp.wrtReparentTo, hidden))
                    otherTrapTrack.append(Func(placeDustExplosion, dustNode, otherSuit.battleTrapProp,
                                             battle))
                    otherTrapTrack.append(createCartoonExplosionTrack(
                        otherDustNode, 'dust', explosionPoint=Point3(0, 0, 0)))
                    otherTrapTrack.append(Func(battle.removeTrap, otherSuit))
                    removeTrapsParallel.append(otherTrapTrack)

            trapTrack.append(removeTrapsParallel)
        else:
            # Set the trap prop as the suit's trap prop
            if (suit.battleTrap != NO_TRAP):
                notify.debug('trapSuit() - trap: %d destroyed existing trap: %d' % (level, suit.battleTrap))
                battle.removeTrap(suit)
            suit.battleTrapProp = trapProp
            suit.battleTrap = level
            suit.battleTrapIsFresh = 1

            #check if we have a case of a train trap appearing under a lured suit
            unlureSuits = Parallel()
            for target in targets:
                kbbonus = target['kbbonus']
                if (kbbonus == 0):
                    unluredSuit = target['suit']
                    suitTrack = Sequence()
                    suitTrack.append(createSuitResetPosTrack(unluredSuit, battle))
                    suitTrack.append(Func(battle.unlureSuit, unluredSuit))
                    unlureSuits.append(suitTrack)
            trapTrack.append(unlureSuits)

            #also set up the other suits
            for otherSuit in battle.suits:
                if not otherSuit == suit:
                    if (otherSuit.battleTrap != NO_TRAP):
                        notify.debug('trapSuit() - trap: %d destroyed existing trap: %d' % (level, suit.battleTrap))
                        battle.removeTrap(otherSuit)
                    otherSuit.battleTrapProp = trapProp
                    otherSuit.battleTrap = level
                    otherSuit.battleTrapIsFresh = 1
        trapTracks.append(trapTrack)

    button = globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    
    toonTrack = Sequence()
    toonTrack.append(Func(MovieUtil.showProps, buttons, hands))
    toonTrack.append(Func(toon.headsUp, battle, suitPos))
    toonTrack.append(ActorInterval(toon, 'pushbutton'))
    toonTrack.append(Func(MovieUtil.removeProps, buttons))
    toonTrack.append(Func(toon.loop, 'neutral'))
    toonTrack.append(Func(toon.setHpr, battle, origHpr))

    if (propName == 'quicksand'):
        propSound = globalBattleSoundCache.getSound('TL_quicksand.ogg')
    elif (propName == 'traintrack'):
        propSound = globalBattleSoundCache.getSound('TL_train_track_appear.ogg')
    else:
        propSound = globalBattleSoundCache.getSound('TL_trap_door.ogg')

    buttonSound = globalBattleSoundCache.getSound('AA_drop_trigger_box.ogg')
    #timing of prop sound is from the start of the button press
    soundTrack = Sequence(
        Wait(2.3),
        Parallel(
            SoundInterval(buttonSound, duration = 0.67, node=toon),
            SoundInterval(propSound, node=toon)),
        )
    

    return Parallel(trapTracks, toonTrack, soundTrack)
