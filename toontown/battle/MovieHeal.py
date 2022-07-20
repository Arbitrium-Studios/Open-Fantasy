from direct.interval.IntervalGlobal import *
from .BattleProps import *
from .BattleSounds import *
from .BattleBase import *

from direct.directnotify import DirectNotifyGlobal
from . import MovieCamera
import random
from . import MovieUtil
from . import BattleParticles
from . import HealJokes
from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownBattleGlobals import AvPropDamage
from toontown.toon import NPCToons
from . import MovieNPCSOS
from toontown.effects import Splash
from direct.task import Task
from panda3d.otp import CFSpeech, CFTimeout
notify = DirectNotifyGlobal.directNotify.newCategory('MovieHeal')

soundFiles = ('AA_heal_tickle.ogg',
              'AA_heal_telljoke.ogg',
              'AA_heal_smooch.ogg',
              'AA_heal_happydance.ogg',
              'AA_heal_pixiedust.ogg',
              'AA_heal_juggle.ogg', 
              'AA_heal_High_Dive.ogg')#UBER

healPos = Point3(0, 0, 0)
healHpr = Vec3(180.0, 0, 0)
runHealTime = 1.0


def doHeals(heals, hasInteractivePropHealBonus):
    """ doHeals(heals)
        Heals occur in the following order:
        1) level 1 heals one at a time, from right to left
        2) level 2 heals one at a time, from right to left
        etc.
    """
    #print("do Heals")
    if (len(heals) == 0):
        return (None, None)
    track = Sequence()
    for h in heals:
        ival = __doHealLevel(h, hasInteractivePropHealBonus)
        if (ival):
            track.append(ival)

    camDuration = track.getDuration()
    camTrack = MovieCamera.chooseHealShot(heals, camDuration)
    return (track, camTrack)

def __doHealLevel(heal, hasInteractivePropHealBonus):
    """ __doHealLevel(heal)
    """
    #print("doHealLevel")
    level = heal['level']
    if (level == 0):
        return __healTickle(heal, hasInteractivePropHealBonus)
    elif (level == 1):
        return __healJoke(heal, hasInteractivePropHealBonus)
    elif (level == 2):
        return __healSmooch(heal, hasInteractivePropHealBonus)
    elif (level == 3):
        return __healDance(heal, hasInteractivePropHealBonus)
    elif (level == 4):
        return __healSprinkle(heal, hasInteractivePropHealBonus)
    elif (level == 5):
        return __healJuggle(heal, hasInteractivePropHealBonus)
    elif (level == 6):
        return __healDive(heal, hasInteractivePropHealBonus) #UBER
    return None

def __runToHealSpot(heal):
    """ generate a track that does the following:
        a) face the heal spot
        b) run to the heal spot
        c) turn to face the target
    """
    toon = heal['toon']
    battle = heal['battle']
    level = heal['level']

    origPos, origHpr = battle.getActorPosHpr(toon)
    runAnimI = ActorInterval(toon, 'run', duration=runHealTime)
    a = Func(toon.headsUp, battle, healPos)
    b = Parallel(runAnimI, LerpPosInterval(
        toon, runHealTime, healPos, other=battle))

    # For group heals, face the center of the group
    if levelAffectsGroup(HEAL, level):#(level % 2):
        c = Func(toon.setHpr, battle, healHpr)
    else:
        # For single heals, face the target toon
        target = heal['target']['toon']
        targetPos = target.getPos(battle)
        c = Func(toon.headsUp, battle, targetPos)
    return Sequence(a, b, c)

def __returnToBase(heal):
    """ generate a track that does the following:
        a) face the toons starting place
        b) run to the starting place
        c) turn to face the center of the battle
    """
    toon = heal['toon']
    battle = heal['battle']
    origPos, origHpr = battle.getActorPosHpr(toon)
    #print 'ORIG_HPR: %s' % origHpr

    runAnimI = ActorInterval(toon, 'run', duration=runHealTime)
    a = Func(toon.headsUp, battle, origPos)
    b = Parallel(runAnimI, LerpPosInterval(
        toon, runHealTime, origPos, other=battle))
    c = Func(toon.setHpr, battle, origHpr)
    d = Func(toon.loop, 'neutral')
    return Sequence(a, b, c, d)

def __healToon(toon, hp, ineffective, hasInteractivePropHealBonus):
    notify.debug('healToon() - toon: %d hp: %d ineffective: %d' % \
        (toon.doId, hp, ineffective))
    if (ineffective == 1):
        laughter = random.choice(TTLocalizer.MovieHealLaughterMisses)
    else:
        maxDam=AvPropDamage[0][1][0][1]
        if (hp >= maxDam-1):
            laughter = random.choice(TTLocalizer.MovieHealLaughterHits2)
        else:
            laughter = random.choice(TTLocalizer.MovieHealLaughterHits1)
    toon.setChatAbsolute(laughter, CFSpeech | CFTimeout)
    if (hp > 0 and toon.hp != None):
        toon.toonUp(hp, hasInteractivePropHealBonus)
    else:
        notify.debug('__healToon() - toon: %d hp: %d' % (toon.doId, hp))

def __getPartTrack(particleEffect, startDelay, durationDelay, partExtraArgs):
    """ This function returns the default particle track for a suit attack
    animation. Arguments:
        startDelay = time delay before particle effect begins
        durationDelay = time delay before particles are cleaned up
        partExtraArgs = extraArgs for startParticleEffect function, the first
        element of which is always the particle effect (function relies on this)
    """
    pEffect = partExtraArgs[0]
    parent = partExtraArgs[1]
    if (len(partExtraArgs) == 3):
        worldRelative = partExtraArgs[2]
    else:
        worldRelative = 1
    return Sequence(
        Wait(startDelay),
        ParticleInterval(pEffect, parent, worldRelative,
                         duration=durationDelay, cleanup = True),
        )

def __getSoundTrack(level, delay, duration=None, node=None):
    #level: the level of attack, int 0-5
    #delay: time delay before playing sound

    soundEffect = globalBattleSoundCache.getSound(soundFiles[level])

    soundIntervals = Sequence()
    
    if soundEffect:
        if duration:
            playSound = SoundInterval(soundEffect, duration=duration, node=node)
        else:
            playSound = SoundInterval(soundEffect, node=node)
        soundIntervals.append(Wait(delay))
        soundIntervals.append(playSound)

    return soundIntervals


def __healTickle(heal,hasInteractivePropHealBonus):
    """ __healTickle(heal)
    """
    toon = heal['toon']
    target = heal['target']['toon']
    hp = heal['target']['hp']
    ineffective = heal['sidestep']
    level = heal['level']

    # Make a 'sandwich' around the track specific interval
    track = Sequence(__runToHealSpot(heal))
    feather = globalPropPool.getProp('feather')
    feather2 = MovieUtil.copyProp(feather)
    feathers = [feather, feather2]
    hands = toon.getRightHands()

    def scaleFeathers(feathers, toon=toon, target=target):
        toon.pose('tickle', 63)
        toon.update(0) # make sure LOD 0 is posed
        hand = toon.getRightHands()[0]
        horizDistance = Vec3(hand.getPos(render) - target.getPos(render))
        horizDistance.setZ(0)
        distance = horizDistance.length()
        if target.style.torso[0] == 's':
            distance -= 0.5 # for fat toons
        else:
            distance -= 0.3 # for skinny toons
        featherLen = 2.4
        scale = distance / (featherLen * hand.getScale(render)[0])
        for feather in feathers:
            feather.setScale(scale)

    tFeatherScaleUp = 0.5
    dFeatherScaleUp = 0.5
    dFeatherScaleDown = 0.5
    featherTrack = Parallel(
        MovieUtil.getActorIntervals(feathers, 'feather'),
        Sequence(Wait(tFeatherScaleUp),
                 Func(MovieUtil.showProps, feathers, hands),
                 Func(scaleFeathers, feathers),
                 MovieUtil.getScaleIntervals(feathers, dFeatherScaleUp,
                                             MovieUtil.PNT3_NEARZERO,
                                             feathers[0].getScale),
                 ),
        Sequence(Wait(toon.getDuration('tickle') - dFeatherScaleDown),
                 MovieUtil.getScaleIntervals(feathers, dFeatherScaleDown,
                                             None, MovieUtil.PNT3_NEARZERO)
                 ),
        )

    tHeal = 3.

    mtrack = Parallel(featherTrack,
                      ActorInterval(toon, 'tickle'),
                      __getSoundTrack(level, 1, node=toon),
                      Sequence(Wait(tHeal),
                               Func(__healToon, target, hp, ineffective,hasInteractivePropHealBonus),
                               ActorInterval(target, 'cringe',
                                             startTime=20./target.getFrameRate('cringe')
                                             )),
                                
                      )
    
    track.append(mtrack)
    track.append(Func(MovieUtil.removeProps, feathers))
    track.append(__returnToBase(heal))
    track.append(Func(target.clearChat))
    return track

def __healJoke(heal, hasInteractivePropHealBonus):
    """ __healJoke(heal)
    """
    toon = heal['toon']
    targets = heal['target']
    ineffective = heal['sidestep']
    level = heal['level']
    jokeIndex = heal['hpbonus'] % len(HealJokes.toonHealJokes)

    # Make a 'sandwich' around the track specific interval
    track = Sequence(__runToHealSpot(heal))

    # start a multitrack
    tracks = Parallel()

    # frame
    fSpeakPunchline = 58

    tSpeakSetup = 0.
    tSpeakPunchline = 3.
    dPunchLine = 3.
    tTargetReact = tSpeakPunchline + 1.
    dTargetLaugh = 1.5
    tRunBack = tSpeakPunchline + dPunchLine

    tDoSoundAnimation = tSpeakPunchline - \
                        (float(fSpeakPunchline) / toon.getFrameRate('sound'))

    # megaphone track
    megaphone  = globalPropPool.getProp('megaphone')
    megaphone2 = MovieUtil.copyProp(megaphone)
    megaphones = [megaphone, megaphone2]
    hands = toon.getRightHands()

    dMegaphoneScale = 0.5

    tracks.append(Sequence(
        Wait(tDoSoundAnimation),
        Func(MovieUtil.showProps, megaphones, hands),
        MovieUtil.getScaleIntervals(megaphones, dMegaphoneScale,
                                    MovieUtil.PNT3_NEARZERO, MovieUtil.PNT3_ONE),
        Wait(toon.getDuration('sound') - (2.0 * dMegaphoneScale)),
        MovieUtil.getScaleIntervals(megaphones, dMegaphoneScale,
                                    MovieUtil.PNT3_ONE, MovieUtil.PNT3_NEARZERO),
        Func(MovieUtil.removeProps, megaphones)
        ))

    # toon track
    tracks.append(Sequence(
        Wait(tDoSoundAnimation),
        ActorInterval(toon, 'sound')
        ))

    # add sound
    soundTrack = __getSoundTrack(level, 2.0, node=toon)
    tracks.append(soundTrack)

    assert(jokeIndex < len(HealJokes.toonHealJokes))
    joke = HealJokes.toonHealJokes[jokeIndex]
    # the set-up
    tracks.append(Sequence(
        Wait(tSpeakSetup),
        Func(toon.setChatAbsolute, joke[0], CFSpeech | CFTimeout),
        ))
    # the punchline
    tracks.append(Sequence(
        Wait(tSpeakPunchline),
        Func(toon.setChatAbsolute, joke[1], CFSpeech | CFTimeout),
        ))

    # do the target toon reaction(s)
    reactTrack = Sequence(
        Wait(tTargetReact),
        )
    for target in targets:
        targetToon = target['toon']
        hp = target['hp']
        reactTrack.append(
            Func(__healToon, targetToon, hp, ineffective, hasInteractivePropHealBonus)
            )
    reactTrack.append(Wait(dTargetLaugh))
    for target in targets:
        targetToon = target['toon']
        reactTrack.append(Func(targetToon.clearChat))
    tracks.append(reactTrack)

    tracks.append(Sequence(
        Wait(tRunBack),
        Func(toon.clearChat),
        *__returnToBase(heal)))

    # lay down the multitrack
    track.append(tracks)

    return track

def __healSmooch(heal, hasInteractivePropHealBonus):
    """ __healSmooch(heal)
    """
    toon = heal['toon']
    target = heal['target']['toon']
    level = heal['level']
    hp = heal['target']['hp']
    ineffective = heal['sidestep']

    # Make a 'sandwich' around the track specific interval
    track = Sequence(__runToHealSpot(heal))

    lipstick = globalPropPool.getProp('lipstick')
    lipstick2 = MovieUtil.copyProp(lipstick)
    lipsticks = [lipstick, lipstick2]
    rightHands = toon.getRightHands()
    dScale = 0.5
    lipstickTrack = Sequence(
        Func(MovieUtil.showProps,
             lipsticks, rightHands,
             Point3(-0.27, -0.24, -0.95),
             Point3(-118, -10.6, -25.9)),
        MovieUtil.getScaleIntervals(lipsticks, dScale,
                                    MovieUtil.PNT3_NEARZERO, MovieUtil.PNT3_ONE),
        Wait(toon.getDuration('smooch') - (2.*dScale)),
        MovieUtil.getScaleIntervals(lipsticks, dScale,
                                     MovieUtil.PNT3_ONE, MovieUtil.PNT3_NEARZERO),
        Func(MovieUtil.removeProps, lipsticks),
        )

    lips = globalPropPool.getProp('lips')
    dScale = 0.5
    tLips = 2.5
    tThrow = 115. / toon.getFrameRate('smooch')
    dThrow = 0.5

    def getLipPos(toon=toon):
        toon.pose('smooch', 57)
        toon.update(0)
        hand = toon.getRightHands()[0]
        return hand.getPos(render)

    lipsTrack = Sequence(
        Wait(tLips),
        Func(MovieUtil.showProp, lips, render, getLipPos),
        Func(lips.setBillboardPointWorld),
        LerpScaleInterval(lips, dScale, Point3(3, 3, 3),
                          startScale=MovieUtil.PNT3_NEARZERO),
        Wait((tThrow - tLips) - dScale),
        LerpPosInterval(lips, dThrow, Point3(target.getPos() +
                                             Point3(0, 0, target.getHeight()))),
        Func(MovieUtil.removeProp, lips),
        )

    delay = tThrow + dThrow
    mtrack = Parallel(lipstickTrack,
                      lipsTrack,
                      __getSoundTrack(level, 2, node=toon),
                      Sequence(ActorInterval(toon, 'smooch'), *__returnToBase(heal)),
                      Sequence(Wait(delay), ActorInterval(target, 'conked')),
                      Sequence(Wait(delay), Func(__healToon,
                                                 target, hp, ineffective, hasInteractivePropHealBonus)),
                      )
    track.append(mtrack)
    #track.append(__returnToBase(heal))
    track.append(Func(target.clearChat))
    return track

def __healDance(heal, hasInteractivePropHealBonus):
    """ __healDance(heal)
    """
    toon = heal['toon']
    targets = heal['target']
    ineffective = heal['sidestep']
    level = heal['level']

    # Make a 'sandwich' around the track specific interval
    track = Sequence(__runToHealSpot(heal))
    delay = 3.0
    first = 1
    targetTrack = Sequence()
    for target in targets:
        targetToon = target['toon']
        hp = target['hp']
        reactIval = Func(__healToon, targetToon, hp, ineffective, hasInteractivePropHealBonus)
        if (first):
            targetTrack.append(Wait(delay))
            first = 0
        targetTrack.append(reactIval)

    hat = globalPropPool.getProp('hat')
    hat2 = MovieUtil.copyProp(hat)
    hats = [hat, hat2]
    cane = globalPropPool.getProp('cane')
    cane2 = MovieUtil.copyProp(cane)
    canes = [cane, cane2]
    leftHands = toon.getLeftHands()
    rightHands = toon.getRightHands()
    dScale = 0.5
    propTrack = Sequence(
        Func(MovieUtil.showProps,
             hats, rightHands,
             Point3(0.23, 0.09, 0.69),
             Point3(180, 0, 0)),
        Func(MovieUtil.showProps,
             canes, leftHands,
             Point3(-0.28, 0., 0.14),
             Point3(0., 0., -150.)),
        MovieUtil.getScaleIntervals(hats + canes, dScale,
                                    MovieUtil.PNT3_NEARZERO, MovieUtil.PNT3_ONE),
        Wait(toon.getDuration('happy-dance') - (2.*dScale)),
        MovieUtil.getScaleIntervals(hats + canes, dScale,
                                    MovieUtil.PNT3_ONE, MovieUtil.PNT3_NEARZERO),
        Func(MovieUtil.removeProps, hats + canes),
        )

    mtrack = Parallel(propTrack,
                      ActorInterval(toon, 'happy-dance'),
                      __getSoundTrack(level, 0.2, duration=6.4, node=toon),
                      targetTrack)

    # wait a split second before dancing
    track.append(Func(toon.loop, 'neutral'))
    track.append(Wait(0.1))

    track.append(mtrack)
    track.append(__returnToBase(heal))
    for target in targets:
        targetToon = target['toon']
        track.append(Func(targetToon.clearChat))
    return track

def __healSprinkle(heal, hasInteractivePropHealBonus):
    """ __healSprinkle(heal)
    """
    toon = heal['toon']
    target = heal['target']['toon']
    hp = heal['target']['hp']
    ineffective = heal['sidestep']
    level = heal['level']

    # Make a 'sandwich' around the track specific interval
    track = Sequence(__runToHealSpot(heal))

    sprayEffect   = BattleParticles.createParticleEffect(file='pixieSpray')
    dropEffect    = BattleParticles.createParticleEffect(file='pixieDrop')
    explodeEffect = BattleParticles.createParticleEffect(file='pixieExplode')
    poofEffect    = BattleParticles.createParticleEffect(file='pixiePoof')
    wallEffect    = BattleParticles.createParticleEffect(file='pixieWall')

    def face90(toon=toon, target=target):
        # turn the toon so that the right side
        # of his body faces his target
        vec = Point3(target.getPos() - toon.getPos())
        vec.setZ(0)
        temp = vec[0]
        vec.setX(-vec[1])
        vec.setY(temp)
        targetPoint = Point3(toon.getPos() + vec)
        toon.headsUp(render, targetPoint)

    delay = 2.5
    mtrack = Parallel(
        __getPartTrack(sprayEffect, 1.5, 0.5, [sprayEffect, toon, 0]),
        __getPartTrack(dropEffect, 1.9, 2., [dropEffect, target, 0]),
        __getPartTrack(explodeEffect, 2.7, 1.0, [explodeEffect, toon, 0]),
        __getPartTrack(poofEffect, 3.4, 1.0, [poofEffect, target, 0]),
        __getPartTrack(wallEffect, 4.05, 1.2, [wallEffect, toon, 0]),
        __getSoundTrack(level, 2, duration=4.1, node=toon),
        Sequence(Func(face90),
                 ActorInterval(toon, 'sprinkle-dust')),
        Sequence(Wait(delay),
                 Func(__healToon, target, hp, ineffective, hasInteractivePropHealBonus)),
        )
    track.append(mtrack)
    track.append(__returnToBase(heal))
    track.append(Func(target.clearChat))
    return track

def __healJuggle(heal, hasInteractivePropHealBonus):
    """ __healJuggle(heal)
    """
    # Determine if this is an NPC heal
    #print("heal Juggle Anim")
    npcId = 0
    if ('npcId' in heal):
        npcId = heal['npcId']
        toon = NPCToons.createLocalNPC(npcId)
        if (toon == None):
            return None
    else:
        toon = heal['toon']
    targets = heal['target']
    ineffective = heal['sidestep']
    level = heal['level']

    # Make a 'sandwich' around the track specific interval
    if (npcId != 0):
        track = Sequence(MovieNPCSOS.teleportIn(heal, toon))
    else:
        track = Sequence(__runToHealSpot(heal))
    delay = 4.0
    first = 1
    targetTrack = Sequence()
    for target in targets:
        targetToon = target['toon']
        #hp = min(targetToon.hp + target['hp'], targetToon.maxHp)
        hp = target['hp']
        reactIval = Func(__healToon, targetToon, hp, ineffective, hasInteractivePropHealBonus)
        if (first == 1):
            targetTrack.append(Wait(delay))
            first = 0

        targetTrack.append(reactIval)

    cube = globalPropPool.getProp('cubes')
    cube2 = MovieUtil.copyProp(cube)
    cubes = [cube, cube2]
    hips = [toon.getLOD(toon.getLODNames()[0]).find("**/joint_hips"),
            toon.getLOD(toon.getLODNames()[1]).find("**/joint_hips"),
            ]
    cubeTrack = Sequence(
        Func(MovieUtil.showProps, cubes, hips),
        MovieUtil.getActorIntervals(cubes, 'cubes'),
        Func(MovieUtil.removeProps, cubes),
        )

    mtrack = Parallel(cubeTrack,
                      __getSoundTrack(level, 0.7, duration=7.7, node=toon),
                      ActorInterval(toon, 'juggle'),
                      targetTrack)
    track.append(mtrack)
    if (npcId != 0):
        track.append(MovieNPCSOS.teleportOut(heal, toon))
    else:
        track.append(__returnToBase(heal))
    for target in targets:
        targetToon = target['toon']
        track.append(Func(targetToon.clearChat))
    return track
    
def __healDive(heal, hasInteractivePropHealBonus):
    """ __healJuggle(heal)
    """
    # Determine if this is an NPC heal
    #print("heal Dive Anim")
    # Splash object for when toon hits the water
    splash = Splash.Splash(render) #remember to destroy
    splash.reparentTo(render)
    #import pdb; pdb.set_trace()
    npcId = 0
    if ('npcId' in heal):
        npcId = heal['npcId']
        toon = NPCToons.createLocalNPC(npcId)
        if (toon == None):
            return None
    else:
        toon = heal['toon']
    targets = heal['target']
    ineffective = heal['sidestep']
    level = heal['level']
    
    #print("toonScale %s" % (toon.getBodyScale()))

    # Make a 'sandwich' around the track specific interval
    if (npcId != 0):
        track = Sequence(MovieNPCSOS.teleportIn(heal, toon))
    else:
        track = Sequence(__runToHealSpot(heal))
    delay = 7.0
    first = 1
    targetTrack = Sequence()
    for target in targets:
        targetToon = target['toon']
        #hp = min(targetToon.hp + target['hp'], targetToon.maxHp)
        hp = target['hp']
        reactIval = Func(__healToon, targetToon, hp, ineffective, hasInteractivePropHealBonus)
        if (first == 1):
            targetTrack.append(Wait(delay))
            first = 0

        targetTrack.append(reactIval)
        
    thisBattle = heal['battle']
    toonsInBattle = thisBattle.toons

    glass = globalPropPool.getProp('glass')
    glass.setScale(4.0)
    glass.setHpr(0.0, 90.0, 0.0)
    ladder = globalPropPool.getProp('ladder')#MovieUtil.copyProp(cube)
    #placeNode = MovieUtil.copyProp(glass)
    placeNode =  NodePath("lookNode")
    diveProps = [glass, ladder]#, placeNode]
    ladderScale = (toon.getBodyScale() / 0.66)
    scaleUpPoint = Point3(.50, .5 , .45) * ladderScale
    basePos = toon.getPos()
    
    glassOffset = Point3(0,1.1,0.2)
    glassToonOffset = Point3(0,1.2,0.2)
    splashOffset = Point3(0,1.0,0.4)
    ladderOffset = Point3(0,4,0)
    ladderToonSep = Point3(0,1,0) * ladderScale
    diveOffset = Point3(0,0,10)
    divePos = add3(add3(ladderOffset, diveOffset), ladderToonSep)
    ladder.setH(toon.getH())
    glassPos = render.getRelativePoint(toon, glassOffset)#add3(basePos, glassOffset)
    glassToonPos = render.getRelativePoint(toon, glassToonOffset)
    ladderPos  = render.getRelativePoint(toon, ladderOffset)
    climbladderPos = render.getRelativePoint(toon, add3(ladderOffset, ladderToonSep))#add3(basePos, ladderOffset)
    divePos = render.getRelativePoint(toon, divePos)
    topDivePos = render.getRelativePoint(toon, diveOffset)
    
    lookBase = render.getRelativePoint(toon, ladderOffset)
    lookTop = render.getRelativePoint(toon, add3(ladderOffset, diveOffset))
    LookGlass = render.getRelativePoint(toon, glassOffset)
    
    splash.setPos(splashOffset)
    
    walkToLadderTime = 1.0
    climbTime = 5.0
    diveTime = 1.0
    ladderGrowTime = 1.5
    splash.setPos(glassPos)
    toonNode = toon.getGeomNode()
    #nameTagNode =  NodePath(toon.nametag.getNametag3d())
    #nameTagNode =  NodePath(toon.getHeadParts()[0])
    #placeNode =  NodePath("lookNode")
    
    placeNode.reparentTo(render)
    placeNode.setScale(5.0)
    #placeNode.attachNewNode("lookNode")
    placeNode.setPos(toon.getPos(render))
    placeNode.setHpr(toon.getHpr(render))
    
    toonscale = toonNode.getScale()
    toonFacing = toon.getHpr()
    
    #for someToon in toonsInBattle:
    #    someToon.startStareAt(nameTagNode, Point3(0,0,3))
    #toonsLook(toonsInBattle, placeNode, Point3(0,0,3))
    
    
    propTrack = Sequence(
        #Func(MovieUtil.showProps, cubes, hips),
        Func(MovieUtil.showProp, glass, render, glassPos),
        Func(MovieUtil.showProp, ladder, render, ladderPos),
        Func(toonsLook, toonsInBattle, placeNode, Point3(0,0,0)),
        Func(placeNode.setPos, lookBase),
        LerpScaleInterval(ladder, ladderGrowTime, scaleUpPoint,
                        startScale=MovieUtil.PNT3_NEARZERO),
        Func(placeNode.setPos, lookTop),
        
        Wait(2.1),
        MovieCamera.toonGroupHighShot(None, 0),
        Wait(2.1),
        Func(placeNode.setPos, LookGlass),
        Wait(0.4),
        MovieCamera.allGroupLowShot(None, 0),
        Wait(1.8),

        
        LerpScaleInterval(ladder, ladderGrowTime, MovieUtil.PNT3_NEARZERO,
                        startScale=scaleUpPoint),
        Func(MovieUtil.removeProps, diveProps),
        #Func(MovieUtil.removeProps, placeNode),
        )

    mtrack = Parallel(propTrack,
                      __getSoundTrack(level, 0.6, duration=9.0, node=toon),
                      Sequence(
                              Parallel(
                                    Sequence(
                                        ActorInterval(toon, 'walk', loop = 0, duration = walkToLadderTime),
                                        ActorInterval(toon, 'neutral', loop = 0, duration = 0.1),
                                    ),
                              LerpPosInterval(toon, walkToLadderTime, climbladderPos),
                              Wait(ladderGrowTime),
                              ),
                              Parallel(
                                        ActorInterval(toon, 'climb', loop = 0, endFrame = 116),
                                        Sequence(
                                                Wait(4.6),
                                                #LerpScaleInterval(toon, diveTime*0.1, 0.1),
                                                #Func(toon.doToonAlphaColorScale, VBase4(1, 0.0, 1, 0.0), 0.5),
                                                Func(toonNode.setTransparency, 1),

                                                LerpColorScaleInterval(toonNode, 0.25, VBase4(1, 1.0, 1, 0.0), blendType = 'easeInOut'),
                                                LerpScaleInterval(toonNode, 0.01, 0.1, startScale = toonscale),

                                                
                                                LerpHprInterval(toon, 0.01, toonFacing),
                                                LerpPosInterval(toon, 0.0, glassToonPos),
                                                Func(toonNode.clearTransparency),
                                                Func(toonNode.clearColorScale),
                                                Parallel(
                                                    ActorInterval(toon, 'swim', loop = 1, startTime = 0.0, endTime = 1.00),
                                                    Wait(1.0),
                                                        ),
                                                #
                                                ),
                                        Sequence(
                                                Wait(4.6),
                                                Func(splash.play),
                                                Wait(1.0),
                                                Func(splash.destroy),
                                                ),
                                        ),
                              #ActorInterval(toon, 'walk', loop = 1, duration=walkToLadderTime),
                              #ActorInterval(toon, 'swim', loop = 1, duration=climbTime),
                              #ActorInterval(toon, 'swim', loop = 1, duration=diveTime*1.0),
                              #LerpScaleInterval(toon, diveTime*0.1, 0.1),

                              Wait(0.5),
                              Parallel(
                                      #LerpHprInterval(toon, 0.1, Point3(0,0,0)),
                                      ActorInterval(toon, 'jump', loop = 0, startTime = 0.2),
                                      LerpScaleInterval(toonNode, 0.5, toonscale, startScale = 0.1),
                                      Func(stopLook, toonsInBattle),
                                      )
                              ),
                      targetTrack)
    track.append(mtrack)
    if (npcId != 0):
        track.append(MovieNPCSOS.teleportOut(heal, toon))
    else:
        track.append(__returnToBase(heal))
    for target in targets:
        targetToon = target['toon']
        track.append(Func(targetToon.clearChat))
    return track
    
def add3(t1, t2):
    returnThree = Point3(t1[0]+t2[0], t1[1]+t2[1], t1[2]+t2[2])
    return returnThree
    
def stopLook(toonsInBattle):
    for someToon in toonsInBattle:
        someToon.stopStareAt()

def toonsLook(toons, someNode, offset):
    #print("toonsLook")
    for someToon in toons:
        #someToon.stopStareAt()
        someToon.startStareAt(someNode, offset)
