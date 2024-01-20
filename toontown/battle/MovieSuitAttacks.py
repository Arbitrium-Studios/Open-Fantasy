from tokenize import Triple
from panda3d.otp import *
from toontown.toonbase.ToontownGlobals import *
from .SuitBattleGlobals import *
from direct.interval.IntervalGlobal import *
from .BattleBase import *
from .BattleProps import *
from toontown.suit.SuitDNA import *
from .BattleBase import *
from .BattleSounds import *
from . import MovieCamera
from direct.directnotify import DirectNotifyGlobal
from . import MovieUtil
from direct.particles import ParticleEffect
from . import BattleParticles
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
notify = DirectNotifyGlobal.directNotify.newCategory('MovieSuitAttacks')


def __doDamage(toon, dmg, died):
    if dmg > 0 and toon.hp is not None:
        toon.takeDamage(dmg)
    return


def __showProp(prop, parent, pos, hpr=None, scale=None):
    prop.reparentTo(parent)
    prop.setPos(pos)
    if hpr:
        prop.setHpr(hpr)
    if scale:
        prop.setScale(scale)


def __animProp(prop, propName, propType='actor'):
    if 'actor' == propType:
        prop.play(propName)
    elif 'model' == propType:
        pass
    else:
        self.notify.error('No such propType as: %s' % propType)


def __suitFacePoint(suit, zOffset=0):
    pnt = suit.getPos()
    pnt.setZ(pnt[2] + suit.shoulderHeight + 0.3 + zOffset)
    return Point3(pnt)


def __toonFacePoint(toon, zOffset=0, parent=render):
    pnt = toon.getPos(parent)
    pnt.setZ(pnt[2] + toon.shoulderHeight + 0.3 + zOffset)
    return Point3(pnt)


def __toonTorsoPoint(toon, zOffset=0):
    pnt = toon.getPos()
    pnt.setZ(pnt[2] + toon.shoulderHeight - 0.2)
    return Point3(pnt)


def __toonGroundPoint(attack, toon, zOffset=0, parent=render):
    pnt = toon.getPos(parent)
    battle = attack['battle']
    pnt.setZ(battle.getZ(parent) + zOffset)
    return Point3(pnt)


def __toonGroundMissPoint(attack, prop, toon, zOffset=0):
    point = __toonMissPoint(prop, toon)
    battle = attack['battle']
    point.setZ(battle.getZ() + zOffset)
    return Point3(point)


def __toonMissPoint(prop, toon, yOffset=0, parent=None):
    if parent:
        p = __toonFacePoint(toon) - prop.getPos(parent)
    else:
        p = __toonFacePoint(toon) - prop.getPos()
    v = Vec3(p)
    baseDistance = v.length()
    v.normalize()
    if parent:
        endPos = prop.getPos(parent) + v * (baseDistance + 5 + yOffset)
    else:
        endPos = prop.getPos() + v * (baseDistance + 5 + yOffset)
    return Point3(endPos)


def __toonMissBehindPoint(toon, parent=render, offset=0):
    point = toon.getPos(parent)
    point.setY(point.getY() - 5 + offset)
    return point


def __throwBounceHitPoint(prop, toon):
    startPoint = prop.getPos()
    endPoint = __toonFacePoint(toon)
    return __throwBouncePoint(startPoint, endPoint)


def __throwBounceMissPoint(prop, toon):
    startPoint = prop.getPos()
    endPoint = __toonFacePoint(toon)
    return __throwBouncePoint(startPoint, endPoint)


def __throwBouncePoint(startPoint, endPoint):
    midPoint = startPoint + (endPoint - startPoint) / 2.0
    midPoint.setZ(0)
    return Point3(midPoint)


def doSuitAttack(attack):
    notify.debug('building suit attack in doSuitAttack: %s' % attack['name'])
    name = attack['id']
    if name == AUDIT:
        suitTrack = doAudit(attack)
    elif name == BITE:
        suitTrack = doBite(attack)
    elif name == BOUNCE_CHECK:
        suitTrack = doBounceCheck(attack)
    elif name == BRAIN_STORM or name == LEGAL_STORM:
        suitTrack = doBrainStorm(attack)
    elif name == BUZZ_WORD:
        suitTrack = doBuzzWord(attack)
    elif name == CALCULATE:
        suitTrack = doCalculate(attack)
    elif name == CANNED:
        suitTrack = doCanned(attack)
    elif name == CHOMP:
        suitTrack = doChomp(attack)
    elif name == CIGAR_SMOKE:
        suitTrack = doCigarSmoke(attack)
    elif name == CLIPON_TIE:
        suitTrack = doClipOnTie(attack)
    elif name == CRUNCH:
        suitTrack = doCrunch(attack)
    elif name == DEMOTION:
        suitTrack = doDemotion(attack)
    elif name == DOUBLE_TALK:
        suitTrack = doDoubleTalk(attack)
    elif name == DOUBLE_WINDSOR or name == HALF_WINDSOR:
        suitTrack = doWindsor(attack)
    elif name == DOWNSIZE:
        suitTrack = doDownsize(attack)
    elif name == EVICTION_NOTICE:
        suitTrack = doEvictionNotice(attack)
    elif name == EVIL_EYE:
        suitTrack = doEvilEye(attack)
    elif name == FILIBUSTER:
        suitTrack = doFilibuster(attack)
    elif name == FILL_WITH_LEAD:
        suitTrack = doFillWithLead(attack)
    elif name == FINGER_WAG:
        suitTrack = doFingerWag(attack)
    elif name == FIRED:
        suitTrack = doFired(attack)
    elif name == FIVE_O_CLOCK_SHADOW:
        suitTrack = doFiveOClockShadow(attack)
    elif name == FLOOD_THE_MARKET:
        suitTrack = doFloodTheMarket(attack)
    elif name == FOUNTAIN_PEN:
        suitTrack = doFountainPen(attack)
    elif name == FREEZE_ASSETS:
        suitTrack = doFreezeAssets(attack)
    elif name == GAVEL:
        suitTrack = doGavel(attack)
    elif name == GLOWER_POWER:
        suitTrack = doGlowerPower(attack)
    elif name == GUILT_TRIP:
        suitTrack = doGuiltTrip(attack)
    elif name == HANG_UP:
        suitTrack = doHangUp(attack)
    elif name == HEAD_SHRINK:
        suitTrack = doHeadShrink(attack)
    elif name == HOT_AIR:
        suitTrack = doHotAir(attack)
    elif name == JARGON:
        suitTrack = doJargon(attack)
    elif name == KICKBACK:
        suitTrack = doDefault(attack)
    elif name == LEGALESE:
        suitTrack = doLegalese(attack)
    elif name == LIQUIDATE:
        suitTrack = doLiquidate(attack)
    elif name == MARKET_CRASH:
        suitTrack = doMarketCrash(attack)
    elif name == MUMBO_JUMBO:
        suitTrack = doMumboJumbo(attack)
    elif name == PARADIGM_SHIFT:
        suitTrack = doParadigmShift(attack)
    elif name == PECKING_ORDER:
        suitTrack = doPeckingOrder(attack)
    elif name == PENNY_PINCH:
        suitTrack = doPennyPinch(attack)
    elif name == PICK_POCKET:
        suitTrack = doPickPocket(attack)
    elif name == PINK_SLIP:
        suitTrack = doPinkSlip(attack)
    elif name == PLAY_HARDBALL:
        suitTrack = doPlayHardball(attack)
    elif name == POUND_KEY:
        suitTrack = doPoundKey(attack)
    elif name == POWER_TIE:
        suitTrack = doPowerTie(attack)
    elif name == POWER_TRIP:
        suitTrack = doPowerTrip(attack)
    elif name == QUAKE:
        suitTrack = doQuake(attack)
    elif name == RAZZLE_DAZZLE:
        suitTrack = doRazzleDazzle(attack)
    elif name == RED_TAPE:
        suitTrack = doRedTape(attack)
    elif name == RE_ORG:
        suitTrack = doReOrg(attack)
    elif name == RESTRAINING_ORDER:
        suitTrack = doRestrainingOrder(attack)
    elif name == ROLODEX:
        suitTrack = doRolodex(attack)
    elif name == RUBBER_STAMP:
        suitTrack = doRubberStamp(attack)
    elif name == RUB_OUT:
        suitTrack = doRubOut(attack)
    elif name == SACKED:
        suitTrack = doSacked(attack)
    elif name == SANDTRAP:
        suitTrack = doSandTrap(attack)
    elif name == SCHMOOZE:
        suitTrack = doSchmooze(attack)
    elif name == SENSORY_OVERLOAD:
        suitTrack = doDefault(attack)
    elif name == SHAKE:
        suitTrack = doShake(attack)
    elif name == SHRED:
        suitTrack = doShred(attack)
    elif name == SONG_AND_DANCE:
        suitTrack = doSongAndDance(attack)
    elif name == SPEED_DIAL:
        suitTrack = doSpeedDial(attack)
    elif name == SPIN:
        suitTrack = doSpin(attack)
    elif name == STOMPER:
        suitTrack = doStomper(attack)
    elif name == SYNERGY:
        suitTrack = doSynergy(attack)
    elif name == TABULATE:
        suitTrack = doTabulate(attack)
    elif name == TEE_OFF:
        suitTrack = doTeeOff(attack)
    elif name == THROW_BOOK:
        suitTrack = doDefault(attack)
    elif name == TREMOR:
        suitTrack = doTremor(attack)
    elif name == TRIP:
        suitTrack = doTrip(attack)
    elif name == UNDERGROUND_LIQUIDITY:
        suitTrack = doUndergroundLiquidity(attack)
    elif name == WATERCOOLER:
        suitTrack = doWatercooler(attack)
    elif name == WITHDRAWAL:
        suitTrack = doWithdrawal(attack)
    elif name == WRITE_OFF:
        suitTrack = doWriteOff(attack)
    else:
        notify.warning('unknown attack: %d substituting Finger Wag' % name)
        suitTrack = doDefault(attack)
    camTrack = MovieCamera.chooseSuitShot(attack, suitTrack.getDuration())
    battle = attack['battle']
    targets = attack['target']
    groupStatus = attack['group']
    toonHprTrack = Parallel()
    for t in targets:
        toon = t['toon']
        toonHprTrack.append(Sequence(
            Func(toon.headsUp, battle, MovieUtil.PNT3_ZERO),
            Func(toon.loop, 'neutral')
        ))

    suit = attack['suit']
    neutralIval = Func(suit.loop, 'neutral')
    suitTrack = Sequence(suitTrack, neutralIval, toonHprTrack)
    suitPos = suit.getPos(battle)
    resetPos, resetHpr = battle.getActorPosHpr(suit)
    if battle.isSuitLured(suit):
        resetTrack = getResetTrack(suit, battle)
        resetSuitTrack = Sequence(resetTrack, suitTrack)
        waitTrack = Sequence(
            Wait(resetTrack.getDuration()),
            Func(battle.unlureSuit, suit)
        )
        resetCamTrack = Sequence(waitTrack, camTrack)
        return (resetSuitTrack, resetCamTrack)
    else:
        return (suitTrack, camTrack)


def getResetTrack(suit, battle):
    resetPos, resetHpr = battle.getActorPosHpr(suit)
    moveDist = Vec3(suit.getPos(battle) - resetPos).length()
    moveDuration = 0.5
    walkTrack = Sequence(
        Func(suit.setHpr, battle, resetHpr),
        ActorInterval(suit, 'walk', startTime=1, duration=moveDuration, endTime=1e-05),
        Func(suit.loop, 'neutral')
    )
    moveTrack = LerpPosInterval(suit, moveDuration, resetPos, other=battle)
    return Parallel(walkTrack, moveTrack)


def __makeCancelledNodePath():
    tn = TextNode('CANCELLED')
    tn.setFont(getSuitFont())
    tn.setText(TTLocalizer.MovieSuitCancelled)
    tn.setAlign(TextNode.ACenter)
    tntop = hidden.attachNewNode('CancelledTop')
    tnpath = tntop.attachNewNode(tn)
    tnpath.setPosHpr(0, 0, 0, 0, 0, 0)
    tnpath.setScale(1)
    tnpath.setColor(0.7, 0, 0, 1)
    tnpathback = tnpath.instanceUnderNode(tntop, 'backside')
    tnpathback.setPosHpr(0, 0, 0, 180, 0, 0)
    tnpath.setScale(1)
    return tntop


def doDefault(attack):
    notify.debug('building suit attack in doDefault')
    suitName = attack['suitName']
    if attack['group'] == ATK_TGT_SINGLE:
        if suitName == 'f':
            attack['id'] = CLIPON_TIE
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'ClipOnTie'
            attack['animName'] = 'throw-paper'
            return doClipOnTie(attack)
        elif suitName == 'p':
            attack['id'] = WRITE_OFF
            attack['name'] = 'WriteOff'
            attack['animName'] = 'hold-pencil'
            return doWriteOff(attack)
        elif suitName == 'ym':
            attack['id'] = RUBBER_STAMP
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'RubberStamp'
            attack['animName'] = 'rubber-stamp'
            return doRubberStamp(attack)
        elif suitName == 'mm':
            attack['id'] = DEMOTION
            attack['name'] = 'Demotion'
            attack['animName'] = 'magic1'
            return doDemotion(attack)
        elif suitName == 'ds':
            attack['id'] = DOWNSIZE
            attack['name'] = 'Downsize'
            attack['animName'] = 'magic2'
            return doDownsize(attack)
        elif suitName == 'hh':
            attack['id'] = HEAD_SHRINK
            attack['name'] = 'HeadShrink'
            attack['animName'] = 'magic1'
            return doHeadShrink(attack)
        elif suitName == 'cr':
            attack['id'] = PICK_POCKET
            attack['name'] = 'PickPocket'
            attack['animName'] = 'pickpocket'
            return doPickPocket(attack)
        elif suitName == 'tbc':
            attack['id'] = GLOWER_POWER
            attack['name'] = 'GlowerPower'
            attack['animName'] = 'glower'
            return doGlowerPower(attack)
        elif suitName == 'cp':
            attack['id'] = TEE_OFF
            attack['name'] = 'TeeOff'
            attack['animName'] = 'golf-club-swing'
            return doTeeOff(attack)
        elif suitName == 'cc':
            attack['id'] = FREEZE_ASSETS
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'FreezeAssets'
            attack['animName'] = 'glower'
            return doFreezeAssets(attack)
        elif suitName == 'tm':
            attack['id'] = POUND_KEY
            attack['name'] = 'PoundKey'
            attack['animName'] = 'phone'
            return doPoundKey(attack)
        elif suitName == 'nd':
            attack['id'] = ROLODEX
            attack['name'] = 'Rolodex'
            attack['animName'] = 'roll-o-dex'
            return doRolodex(attack)
        elif suitName == 'gh':
            attack['id'] = SCHMOOZE
            attack['name'] = 'Schmooze'
            attack['animName'] = 'speak'
            return doSchmooze(attack)
        elif suitName == 'ms':
            attack['id'] = BRAIN_STORM
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'BrainStorm'
            attack['animName'] = 'effort'
            return doBrainStorm(attack)
        elif suitName == 'tf':
            attack['id'] = DOUBLE_WINDSOR
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'DoubleWindsor'
            attack['animName'] = 'throw-paper'
            return doWindsor(attack)
        elif suitName == 'm':
            attack['id'] = SCHMOOZE
            attack['name'] = 'Schmooze'
            attack['animName'] = 'speak'
            return doSchmooze(attack)
        elif suitName == 'mh':
            attack['id'] = RAZZLE_DAZZLE
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'RazzleDazzle'
            attack['animName'] = 'smile'
            return doRazzleDazzle(attack)
        elif suitName == 'ff':
            attack['id'] = TEE_OFF
            attack['name'] = 'TeeOff'
            attack['animName'] = 'golf-club-swing'
            return doTeeOff(attack)
        elif suitName == 'sc':
            attack['id'] = BOUNCE_CHECK
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'BounceCheck'
            attack['animName'] = 'throw-paper'
            return doBounceCheck(attack)
        elif suitName == 'pp':
            attack['id'] = PENNY_PINCH
            attack['name'] = 'PennyPinch'
            attack['animName'] = 'pickpocket'
            return doPennyPinch(attack)
        elif suitName == 'tw':
            attack['id'] = FREEZE_ASSETS
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'FreezeAssets'
            attack['animName'] = 'glower'
            return doFreezeAssets(attack)
        elif suitName == 'bc':
            attack['id'] = AUDIT
            attack['name'] = 'Audit'
            attack['animName'] = 'phone'
            return doAudit(attack)
        elif suitName == 'nc':
            attack['id'] = CRUNCH
            attack['name'] = 'Crunch'
            attack['animName'] = 'throw-object'
            return doCrunch(attack)
        elif suitName == 'mb':
            attack['id'] = MARKET_CRASH
            attack['name'] = 'MarketCrash'
            attack['animName'] = 'throw-paper'
            return doMarketCrash(attack)
        elif suitName == 'ls':
            attack['id'] = CHOMP
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'Chomp'
            attack['animName'] = 'throw-paper'
            return doChomp(attack)
        elif suitName == 'rb':
            attack['id'] = PICK_POCKET
            attack['name'] = 'PickPocket'
            attack['animName'] = 'pickpocket'
            return doPickPocket(attack)
        elif suitName == 'msv':
            attack['id'] = FREEZE_ASSETS
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'FreezeAssets'
            attack['animName'] = 'glower'
            return doFreezeAssets(attack)
        elif suitName == 'bf':
            attack['id'] = CANNED
            attack['name'] = 'Canned'
            attack['animName'] = 'throw-paper'
            return doCanned(attack)
        elif suitName == 'b':
            attack['id'] = BITE
            attack['name'] = 'Bite'
            attack['animName'] = 'throw-paper'
            return doBite(attack)
        elif suitName == 'dt':
            attack['id'] = DOUBLE_TALK
            attack['name'] = 'DoubleTalk'
            attack['animName'] = 'speak'
            return doDoubleTalk(attack)
        elif suitName == 'ac':
            attack['id'] = RED_TAPE
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'RedTape'
            attack['animName'] = 'throw-object'
            return doRedTape(attack)
        elif suitName == 'bs':
            attack['id'] = RESTRAINING_ORDER
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'RestrainingOrder'
            attack['animName'] = 'throw-paper'
            return doRestrainingOrder(attack)
        elif suitName == 'sd':
            attack['id'] = SPIN
            attack['name'] = 'Spin'
            attack['animName'] = 'magic3'
            return doSpin(attack)
        elif suitName == 'le':
            attack['id'] = LEGALESE
            attack['name'] = 'Legalese'
            attack['animName'] = 'speak'
            return doLegalese(attack)
        elif suitName == 'bw':
            attack['id'] = GAVEL
            attack['name'] = 'Gavel'
            attack['animName'] = 'effort'
            return doGavel(attack)
        elif suitName == 'lc':
            attack['id'] = RESTRAINING_ORDER
            attack['group'] = ATK_TGT_SINGLE
            attack['name'] = 'RestrainingOrder'
            attack['animName'] = 'throw-paper'
            return doRestrainingOrder(attack)
        else:
            attack['id'] = MUMBO_JUMBO
            attack['name'] = 'MumboJumbo'
            attack['animName'] = 'speak'
            return doMumboJumbo(attack)
    else:
        if suitName == 'f':
            attack['id'] = CLIPON_TIE
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'ClipOnTie'
            attack['animName'] = 'throw-paper'
            return doClipOnTie(attack)
        elif suitName == 'p':
            attack['id'] = FOUNTAIN_PEN
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'FountainPen'
            attack['animName'] = 'pen-squirt'
            return doFountainPen(attack)
        elif suitName == 'ym':
            attack['id'] = RUBBER_STAMP
            attacl['group'] = ATK_TGT_GROUP
            attack['name'] = 'RubberStamp'
            attack['animName'] = 'rubber-stamp'
            return doRubberStamp(attack)
        elif suitName == 'mm':
            attack['id'] = FOUNTAIN_PEN
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'FountainPen'
            attack['animName'] = 'pen-squirt'
            return doFountainPen(attack)
        elif suitName == 'ds':
            attack['id'] = FIRED
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'Fired'
            attack['animName'] = 'magic2'
            return doFired(attack)
        elif suitName == 'hh':
            attack['id'] = FOUNTAIN_PEN
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'FountainPen'
            attack['animName'] = 'pen-squirt'
            return doFountainPen(attack)
        elif suitName == 'cr':
            attack['id'] = EVIL_EYE
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'EvilEye'
            attack['animName'] = 'glower'
            return doEvilEye(attack)
        elif suitName == 'tbc':
            attack['id'] = POWER_TRIP
            attack['name'] = 'PowerTrip'
            attack['animName'] = 'magic1'
            return doPowerTrip(attack)
        elif suitName == 'cp':
            attack['id'] = SANDTRAP
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'SandTrap'
            attack['animName'] = 'effort'
            return doSandTrap(attack)
        elif suitName == 'cc':
            attack['id'] = FREEZE_ASSETS
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'FreezeAssets'
            attack['animName'] = 'glower'
            return doFreezeAssets(attack)
        elif suitName == 'nd':
            attack['id'] = SYNERGY
            attack['name'] = 'Synergy'
            attack['animName'] = 'magic3'
            return doSynergy(attack)
        elif suitName == 'gh':
            attack['id'] = FOUNTAIN_PEN
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'FountainPen'
            attack['animName'] = 'pen-squirt'
            return doFountainPen(attack)
        elif suitName == 'ms':
            attack['id'] = SHAKE
            attack['name'] = 'Shake'
            attack['animName'] = 'stomp'
            return doShake(attack)
        elif suitName == 'tf':
            attack['id'] = DOUBLE_WINDSOR
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'DoubleWindsor'
            attack['animName'] = 'throw-paper'
            return doWindsor(attack)
        elif suitName == 'm':
            attack['id'] = PARADIGM_SHIFT
            attack['name'] = 'ParadigmShift'
            attack['animName'] = 'magic2'
            return doParadigmShift(attack)
        elif suitName == 'mh':
            attack['id'] = SONG_AND_DANCE
            attack['name'] = 'SongAndDance'
            attack['animName'] = 'song-and-dance'
            return doSongAndDance(attack)
        elif suitName == 'ff':
            attack['id'] = STOMPER
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'Stomper'
            attack['animName'] = 'effort'
            return doStomper(attack)
        elif suitName == 'sc':
            attack['id'] = BOUNCE_CHECK
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'BounceCheck'
            attack['animName'] = 'throw-paper'
            return doBounceCheck(attack)
        elif suitName == 'pp':
            attack['id'] = FREEZE_ASSETS
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'FreezeAssets'
            attack['animName'] = 'glower'
            return doFreezeAssets(attack)
        elif suitName == 'tw':
            attack['id'] = FREEZE_ASSETS
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'FreezeAssets'
            attack['animName'] = 'glower'
            return doFreezeAssets(attack)
        elif suitName == 'mb':
            attack['id'] = FLOOD_THE_MARKET
            attack['name'] = 'FloodTheMarket'
            attack['animName'] = 'effort'
            return doFloodTheMarket(attack)
        elif suitName == 'ls':
            attack['id'] = CHOMP
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'Chomp'
            attack['animName'] = 'throw-paper'
            return doChomp(attack)
        elif suitName == 'rb':
            attack['id'] = FLOOD_THE_MARKET
            attack['name'] = 'FloodTheMarket'
            attack['animName'] = 'effort'
            return doFloodTheMarket(attack)
        elif suitName == 'msv':
            attack['id'] = FREEZE_ASSETS
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'FreezeAssets'
            attack['animName'] = 'glower'
            return doFreezeAssets(attack)
        elif suitName == 'bf':
            attack['id'] = WATERCOOLER
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'Watercooler'
            attack['animName'] = 'watercooler'
            return doWatercooler(attack)
        elif suitName == 'b':
            attack['id'] = WITHDRAWAL
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'Withdrawal'
            attack['animName'] = 'magic1'
            return doWithdrawal(attack)
        elif suitName == 'ac':
            attack['id'] = SHAKE
            attack['name'] = 'Shake'
            attack['animName'] = 'stomp'
            return doShake(attack)
        elif suitName == 'bs':
            attack['id'] = GUILT_TRIP
            attack['name'] = 'GuiltTrip'
            attack['animName'] = 'magic1'
            return doGuiltTrip(attack)
        elif suitName == 'sd':
            attack['id'] = PARADIGM_SHIFT
            attack['name'] = 'ParadigmShift'
            attack['animName'] = 'magic2'
            return doParadigmShift(attack)
        elif suitName == 'le':
            attack['id'] = LEGAL_STORM
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'LegalStorm'
            attack['animName'] = 'effort'
            return doBrainStorm(attack)
        elif suitName == 'bw':
            attack['id'] = POWER_TRIP
            attack['name'] = 'PowerTrip'
            attack['animName'] = 'magic1'
            return doPowerTrip(attack)
        elif suitName == 'lc':
            attack['id'] = RESTRAINING_ORDER
            attack['group'] = ATK_TGT_GROUP
            attack['name'] = 'RestrainingOrder'
            attack['animName'] = 'throw-paper'
            return doRestrainingOrder(attack)
        else:
            attack['id'] = TRIP
            attack['name'] = 'Trip'
            attack['animName'] = 'magic1'
            return doTrip(attack)


def getSuitTrack(attack, delay=1e-06, splicedAnims=None, playRate=1.0):
    suit = attack['suit']
    battle = attack['battle']
    tauntIndex = attack['taunt']
    target = attack['target']
    toon = target[0]['toon']
    targetPos = toon.getPos(battle)
    taunt = getAttackTaunt(attack['name'], tauntIndex, attack['suitName'])
    trapStorage = {}
    trapStorage['trap'] = None
    track = Sequence(
        Wait(delay),
        Func(suit.setChatAbsolute, taunt, CFSpeech | CFTimeout)
    )

    def reparentTrap(suit=suit, battle=battle, trapStorage=trapStorage):
        trapProp = suit.battleTrapProp
        if trapProp is not None:
            trapProp.wrtReparentTo(battle)
            trapStorage['trap'] = trapProp
        return

    track.append(Func(reparentTrap))
    track.append(Func(suit.headsUp, battle, targetPos))
    if splicedAnims:
        track.append(getSplicedAnimsTrack(splicedAnims, actor=suit))
    else:
        track.append(ActorInterval(suit, attack['animName'], playRate=playRate))
    origPos, origHpr = battle.getActorPosHpr(suit)
    track.append(Func(suit.setHpr, battle, origHpr))

    def returnTrapToSuit(suit=suit, trapStorage=trapStorage):
        trapProp = trapStorage['trap']
        if trapProp is not None:
            if trapProp.getName() == 'traintrack':
                notify.debug('deliberately not parenting traintrack to suit')
            else:
                trapProp.wrtReparentTo(suit)
            suit.battleTrapProp = trapProp
        return

    track.append(Func(returnTrapToSuit))
    track.append(Func(suit.clearChat))
    return track


def getSuitAnimTrack(attack, delay=0, splicedAnims=None, playRate=1.0):
    suit = attack['suit']
    tauntIndex = attack['taunt']
    taunt = getAttackTaunt(attack['name'], tauntIndex, attack['suitName'])
    track = Sequence(
        Wait(delay),
        Func(
            suit.setChatAbsolute,
            taunt,
            CFSpeech | CFTimeout))
    if splicedAnims:
        track.append(getSplicedAnimsTrack(splicedAnims, actor=suit))
    else:
        track.append(ActorInterval(suit, attack['animName'], playRate=playRate))
    track.append(Func(suit.clearChat))
    return track


def getPartTrack(particleEffect, startDelay, durationDelay, partExtraArgs):
    particleEffect = partExtraArgs[0]
    parent = partExtraArgs[1]
    if len(partExtraArgs) > 2:
        worldRelative = partExtraArgs[2]
    else:
        worldRelative = 1
    return Sequence(Wait(startDelay), ParticleInterval(
        particleEffect, parent, worldRelative, duration=durationDelay, cleanup=True))


def getToonTrack(attack, damageDelay=1e-06, damageAnimNames=None, dodgeDelay=0.0001, dodgeAnimNames=None, splicedDamageAnims=None, splicedDodgeAnims=None, target=None, showDamageExtraTime=0.01, showMissedExtraTime=0.5):
    if not target:
        target = attack['target'][0]
    toon = target['toon']
    battle = attack['battle']
    suit = attack['suit']
    suitPos = suit.getPos(battle)
    dmg = target['hp']
    animTrack = Sequence()
    animTrack.append(Func(toon.headsUp, battle, suitPos))
    if dmg > 0:
        animTrack.append(getToonTakeDamageTrack(toon, target['died'], dmg, damageDelay, damageAnimNames, splicedDamageAnims, showDamageExtraTime))
    else:
        animTrack.append(getToonDodgeTrack(target, dodgeDelay, dodgeAnimNames, splicedDodgeAnims, showMissedExtraTime))
    return animTrack


def getToonTracks(attack, damageDelay=1e-06, damageAnimNames=None, dodgeDelay=1e-06, dodgeAnimNames=None, splicedDamageAnims=None, splicedDodgeAnims=None, showDamageExtraTime=0.01, showMissedExtraTime=0.5):
    toonTracks = Parallel()
    targets = attack['target']
    for i in range(len(targets)):
        tgt = targets[i]
        toonTracks.append(getToonTrack(attack, damageDelay, damageAnimNames, dodgeDelay, dodgeAnimNames, splicedDamageAnims, splicedDodgeAnims, target=tgt, showDamageExtraTime=showDamageExtraTime, showMissedExtraTime=showMissedExtraTime))

    return toonTracks


def getToonDodgeTrack(target, dodgeDelay, dodgeAnimNames, splicedDodgeAnims, showMissedExtraTime):
    toon = target['toon']
    toonTrack = Sequence()
    toonTrack.append(Wait(dodgeDelay))
    if dodgeAnimNames:
        for d in dodgeAnimNames:
            if d == 'sidestep':
                toonTrack.append(getAllyToonsDodgeParallel(target))
            else:
                toonTrack.append(ActorInterval(toon, d))

    else:
        toonTrack.append(getSplicedAnimsTrack(splicedDodgeAnims, actor=toon))
    indicatorTrack = Sequence(
        Wait(dodgeDelay + showMissedExtraTime),
        Func(MovieUtil.indicateMissed, toon)
    )
    toonTrack.append(Func(toon.loop, 'neutral'))
    return Parallel(toonTrack, indicatorTrack)


def getAllyToonsDodgeParallel(target):
    toon = target['toon']
    leftToons = target['leftToons']
    rightToons = target['rightToons']
    if len(leftToons) > len(rightToons):
        PoLR = rightToons
        PoMR = leftToons
    else:
        PoLR = leftToons
        PoMR = rightToons
    upper = 1 + 4 * abs(len(leftToons) - len(rightToons))
    if random.randint(0, upper) > 0:
        toonDodgeList = PoLR
    else:
        toonDodgeList = PoMR
    if toonDodgeList is leftToons:
        sidestepAnim = 'sidestep-left'
        soundEffect = globalBattleSoundCache.getSound('AV_side_step.ogg')
    else:
        sidestepAnim = 'sidestep-right'
        soundEffect = globalBattleSoundCache.getSound('AV_jump_to_side.ogg')
    toonTracks = Parallel()
    for t in toonDodgeList:
        toonTracks.append(
            Sequence(
                ActorInterval(t, sidestepAnim),
                Func(t.loop, 'neutral'))
        )

    toonTracks.append(
        Sequence(
            ActorInterval(toon, sidestepAnim),
            Func(toon.loop, 'neutral')
        )
    )
    toonTracks.append(
        Sequence(
            Wait(0.5),
            SoundInterval(soundEffect, node=toon)
        )
    )
    return toonTracks


def getPropTrack(prop, parent, posPoints, appearDelay, remainDelay, scaleUpPoint=Point3(1), scaleUpTime=0.5, scaleDownTime=0.5, startScale=Point3(0.01), anim=0, propName='none', animDuration=0.0, animStartTime=0.0):
    track = Sequence(
        Wait(appearDelay),
        Func(__showProp, prop, parent, *posPoints),
        LerpScaleInterval(prop, scaleUpTime, scaleUpPoint, startScale=startScale)
    )
    if anim == 1:
        track.append(ActorInterval(prop, propName, duration=animDuration, startTime=animStartTime))
        track.append(Wait(remainDelay))
    else:
        track.append(Wait(remainDelay))
        track.append(LerpScaleInterval(prop, scaleDownTime, MovieUtil.PNT3_NEARZERO))
    track.append(Func(MovieUtil.removeProp, prop))
    return track


def getPropAppearTrack(prop, parent, posPoints, appearDelay, scaleUpPoint=Point3(1), scaleUpTime=0.5, startScale=Point3(0.01), poseExtraArgs=None):
    propTrack = Sequence(
        Wait(appearDelay),
        Func(__showProp, prop, parent, *posPoints)
    )
    if poseExtraArgs:
        propTrack.append(Func(prop.pose, *poseExtraArgs))
    propTrack.append(LerpScaleInterval(prop, scaleUpTime, scaleUpPoint, startScale=startScale))
    return propTrack


def getPropThrowTrack(attack, prop, hitPoints=[], missPoints=[], hitDuration=0.5, missDuration=0.5, hitPointNames='none', missPointNames='none', lookAt='none', groundPointOffSet=0, missScaleDown=None, parent=render, target=None):
    if target == None:
        target = attack['target'][0]
    toon = target['toon']
    dmg = target['hp']
    battle = attack['battle']

    def getLambdas(list, prop, toon):
        for i in range(len(list)):
            if list[i] == 'face':
                list[i] = lambda toon = toon: __toonFacePoint(toon)
            elif list[i] == 'miss':
                list[i] = lambda prop = prop, toon = toon: __toonMissPoint(prop, toon)
            elif list[i] == 'bounceHit':
                list[i] = lambda prop = prop, toon = toon: __throwBounceHitPoint(prop, toon)
            elif list[i] == 'bounceMiss':
                list[i] = lambda prop = prop, toon = toon: __throwBounceMissPoint(prop, toon)

        return list

    if hitPointNames != 'none':
        hitPoints = getLambdas(hitPointNames, prop, toon)
    if missPointNames != 'none':
        missPoints = getLambdas(missPointNames, prop, toon)
    propTrack = Sequence()
    propTrack.append(Func(battle.movie.needRestoreRenderProp, prop))
    propTrack.append(Func(prop.wrtReparentTo, parent))
    if lookAt != 'none':
        propTrack.append(Func(prop.lookAt, lookAt))
    if dmg > 0:
        for i in range(len(hitPoints)):
            pos = hitPoints[i]
            propTrack.append(LerpPosInterval(prop, hitDuration, pos=pos))

    else:
        for i in range(len(missPoints)):
            pos = missPoints[i]
            propTrack.append(LerpPosInterval(prop, missDuration, pos=pos))

        if missScaleDown:
            propTrack.append(
                LerpScaleInterval(
                    prop,
                    missScaleDown,
                    MovieUtil.PNT3_NEARZERO))
    propTrack.append(Func(MovieUtil.removeProp, prop))
    propTrack.append(Func(battle.movie.clearRenderProp, prop))
    return propTrack


def getThrowTrack(object, target, duration=1.0, parent=render, gravity=-32.144):
    values = {}

    def calcOriginAndVelocity(object=object, target=target, values=values, duration=duration, parent=parent, gravity=gravity):
        if callable(target):
            target = target()
        object.wrtReparentTo(parent)
        values['origin'] = object.getPos(parent)
        origin = object.getPos(parent)
        values['velocity'] = (target[2] - origin[2] - 0.5 * gravity * duration * duration) / duration

    return Sequence(
        Func(calcOriginAndVelocity),
        LerpFunctionInterval(throwPos, fromData=0.0, toData=1.0, duration=duration, extraArgs=[object, duration, target, values, gravity])
    )


def throwPos(t, object, duration, target, values, gravity=-32.144):
    origin = values['origin']
    velocity = values['velocity']
    if callable(target):
        target = target()
    x = origin[0] * (1 - t) + target[0] * t
    y = origin[1] * (1 - t) + target[1] * t
    time = t * duration
    z = origin[2] + velocity * time + 0.5 * gravity * time * time
    object.setPos(x, y, z)


def getToonTakeDamageTrack(toon, died, dmg, delay, damageAnimNames=None, splicedDamageAnims=None, showDamageExtraTime=0.01):
    toonTrack = Sequence()
    toonTrack.append(Wait(delay))
    if damageAnimNames:
        for d in damageAnimNames:
            if d == 'Squish':
                toonTrack.append(Func(toon.b_setAnimState, 'Squish'))
            else:
                toonTrack.append(ActorInterval(toon, d))

    else:
        splicedAnims = getSplicedAnimsTrack(splicedDamageAnims, actor=toon)
        toonTrack.append(splicedAnims)
    indicatorTrack = Sequence(
        Wait(delay + showDamageExtraTime),
        Func(__doDamage, toon, dmg, died)
    )
    toonTrack.append(Func(toon.loop, 'neutral'))
    if died:
        toonTrack.append(Wait(5.0))
    return Parallel(toonTrack, indicatorTrack)


def getSplicedAnimsTrack(anims, actor=None):
    track = Sequence()
    for nextAnim in anims:
        delay = 1e-06
        if len(nextAnim) >= 2:
            if nextAnim[1] > 0:
                delay = nextAnim[1]
        if len(nextAnim) <= 0:
            track.append(Wait(delay))
        elif len(nextAnim) == 1:
            track.append(ActorInterval(actor, nextAnim[0]))
        elif len(nextAnim) == 2:
            track.append(Wait(delay))
            track.append(ActorInterval(actor, nextAnim[0]))
        elif len(nextAnim) == 3:
            track.append(Wait(delay))
            track.append(ActorInterval(actor, nextAnim[0], startTime=nextAnim[2]))
        elif len(nextAnim) == 4:
            track.append(Wait(delay))
            duration = nextAnim[3]
            if duration < 0:
                startTime = nextAnim[2]
                endTime = startTime + duration
                if endTime <= 0:
                    endTime = 0.01
                track.append(ActorInterval(actor, nextAnim[0], startTime=startTime, endTime=endTime))
            else:
                track.append(ActorInterval(actor, nextAnim[0], startTime=nextAnim[2], duration=duration))
        elif len(nextAnim) == 5:
            track.append(Wait(delay))
            track.append(ActorInterval(nextAnim[4], nextAnim[0], startTime=nextAnim[2], duration=nextAnim[3]))

    return track


def getSplicedLerpAnims(animName, origDuration, newDuration, startTime=0, fps=30, reverse=0):
    anims = []
    addition = 0
    numAnims = origDuration * fps
    timeInterval = newDuration / numAnims
    animInterval = origDuration / numAnims
    if reverse == 1:
        animInterval = -animInterval
    for i in range(0, int(numAnims)):
        anims.append([animName, timeInterval, startTime + addition, animInterval])
        addition += animInterval

    return anims


def hitAtleastOneToon(targets):
    for t in targets:
        if t['hp'] > 0:
            return True
    
    return False


def getSoundTrack(fileName, delay=0.01, duration=0, volume=1, startTime=0, node=None):
    return Sequence(Wait(delay), SoundInterval(globalBattleSoundCache.getSound(fileName), duration=duration, volume=volume, startTime=startTime, node=node))


def getColorTrack(attack, toon, part, color, delay = 0.0, duration = 1.0):
    battle = attack['battle']
    headParts = toon.getHeadParts()
    torsoParts = toon.getTorsoParts()
    legsParts = toon.getLegsParts()

    def changeColor(parts):
        track = Parallel()
        for partNum in xrange(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.setColorScale, color))

        return track

    def resetColor(parts):
        track = Parallel()
        for partNum in xrange(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.clearColorScale))

        return track

    colorTrack = Sequence(
        Wait(delay),
        Func(battle.movie.needRestoreColor)
    )
    if part == 'head' or part == 'all':
        colorTrack.append(changeColor(headParts))
    if part == 'torso' or part == 'all':
        colorTrack.append(changeColor(torsoParts))
    if part == 'legs' or part == 'all':
        colorTrack.append(changeColor(legsParts))
    colorTrack.append(Wait(duration))
    if part == 'head' or part == 'all':
        colorTrack.append(resetColor(headParts))
    if part == 'torso' or part == 'all':
        colorTrack.append(resetColor(torsoParts))
    if part == 'legs' or part == 'all':
        colorTrack.append(resetColor(legsParts))
    colorTrack.append(Func(battle.movie.clearRestoreColor))
    return colorTrack


def doClipOnTie(attack):
    suit = attack['suit']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        tie = globalPropPool.getProp('clip-on-tie')
        throwDelay = {
            'a': 2.17,
            'b': 2.17,
            'c': 1.45
        }
        damageDelay = {
            'a': 3.3,
            'b': 3.3,
            'c': 2.61
        }
        dodgeDelay = {
            'a': 3.1,
            'b': 3.1,
            'c': 2.34
        }
        suitTrack = getSuitTrack(attack)
        posPoints = [Point3(0.66, 0.51, 0.28), VBase3(-69.652, -17.199, 67.96)]
        tiePropTrack = Sequence(getPropAppearTrack(tie, suit.getRightHand(), posPoints, 0.5, MovieUtil.PNT3_ONE, scaleUpTime=0.5, poseExtraArgs=['clip-on-tie', 0]))
        suitType = getSuitBodyType(attack['suitName'])
        if dmg > 0:
            tiePropTrack.append(ActorInterval(tie, 'clip-on-tie', duration=throwDelay[suitType], startTime=1.1))
        else:
            tiePropTrack.append(Wait(throwDelay[suitType]))
        tiePropTrack.append(Func(tie.setHpr, Point3(0, -90, 0)))
        tiePropTrack.append(getPropThrowTrack(attack, tie, [__toonFacePoint(toon)], [__toonGroundPoint(attack, toon, 0.1)], hitDuration=0.4, missDuration=0.8, missScaleDown=1.2))
        toonTrack = getToonTrack(attack, damageDelay[suitType], ['conked'], dodgeDelay[suitType], ['sidestep'])
        throwSound = getSoundTrack('SA_powertie_throw.ogg', delay=throwDelay[suitType] + 1, node=suit)
        return Parallel(suitTrack, toonTrack, tiePropTrack, throwSound)
    else:
        targets = attack['target']
        throwDelay = {
            'a': 2.17,
            'b': 2.17,
            'c': 1.45
        }
        damageDelay = {
            'a': 3.3,
            'b': 3.3,
            'c': 2.61
        }
        dodgeDelay = {
            'a': 3.1,
            'b': 3.1,
            'c': 2.34
        }
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        posPoints = [Point3(0.66, 0.51, 0.28), VBase3(-69.652, -17.199, 67.96)]
        tiePropTracks = Parallel()
        suitType = getSuitBodyType(attack['suitName'])
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            tie = globalPropPool.getProp('clip-on-tie')
            tiePropTrack = Sequence(getPropAppearTrack(tie, suit.getRightHand(), posPoints, 0.5, MovieUtil.PNT3_ONE, scaleUpTime=0.5, poseExtraArgs=['clip-on-tie', 0]))
            if dmg > 0:
                tiePropTrack.append(ActorInterval(tie, 'clip-on-tie', duration=throwDelay[suitType], startTime=1.1))
            else:
                tiePropTrack.append(Wait(throwDelay[suitType]))
            tiePropTrack.append(Func(tie.setHpr, Point3(0, -90, 0)))
            tiePropTrack.append(getPropThrowTrack(attack, tie, [__toonFacePoint(toon)], [__toonGroundPoint(attack, toon, 0.1)], hitDuration=0.4, missDuration=0.8, missScaleDown=1.2, target=t))
            tiePropTracks.append(tiePropTrack)
        toonTracks = getToonTracks(attack, damageDelay[suitType], ['conked'], dodgeDelay[suitType], ['sidestep'])
        throwSound = getSoundTrack('SA_powertie_throw.ogg', delay=throwDelay[suitType] + 1, node=suit)
        return Parallel(suitTrack, toonTracks, tiePropTracks, throwSound)


def doPoundKey(attack):
    suit = attack['suit']
    phone = globalPropPool.getProp('phone')
    receiver = globalPropPool.getProp('receiver')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('PoundKey')
    BattleParticles.setEffectTexture(particleEffect, 'poundsign', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.55, [particleEffect, suit, 0])
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        phonePosPoints = [Point3(-0.23, 0.01, -0.26), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(-0.13, -0.07, -0.06), VBase3(-1.854, 2.434, -177.579)]
        receiverAdjustScale = Point3(0.8, 0.8, 0.8)
        pickupDelay = 0.44
        dialDuration = 3.07
        finalPhoneDelay = 0.01
        scaleUpPoint = Point3(0.75, 0.75, 0.75)
    elif suitType == 'b':
        phonePosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverAdjustScale = MovieUtil.PNT3_ONE
        pickupDelay = 0.74
        dialDuration = 3.07
        finalPhoneDelay = 0.69
        scaleUpPoint = MovieUtil.PNT3_ONE
    else:
        phonePosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        pickupDelay = 0.74
        dialDuration = 3.14
        finalPhoneDelay = 0.62
        scaleUpPoint = MovieUtil.PNT3_ONE
    propTrack = Sequence(
        Wait(0.3),
        Func(__showProp, phone, suit.getLeftHand(), phonePosPoints[0], phonePosPoints[1]),
        Func(__showProp, receiver, suit.getLeftHand(), receiverPosPoints[0], receiverPosPoints[1]),
        LerpScaleInterval(phone, 0.5, scaleUpPoint, MovieUtil.PNT3_NEARZERO),
        Wait(pickupDelay),
        Func(receiver.wrtReparentTo, suit.getRightHand())
    )
    if suitType == 'a' or suitType == 'b':
        propTrack.append(LerpScaleInterval(receiver, 0.01, receiverAdjustScale))
        propTrack.append(LerpPosHprInterval(receiver, 0.0001, Point3(-0.53, 0.21, -0.54), VBase3(-99.49, -35.27, 1.84)))
    else:
        propTrack.append(LerpPosHprInterval(receiver, 0.0001, Point3(-0.45, 0.48, -0.62), VBase3(-87.47, -18.21, 7.82)))
    propTrack.append(Wait(dialDuration))
    propTrack.append(Func(receiver.wrtReparentTo, phone))
    propTrack.append(Wait(finalPhoneDelay))
    propTrack.append(LerpScaleInterval(phone, 0.5, MovieUtil.PNT3_NEARZERO))
    propTrack.append(Func(MovieUtil.removeProps, [receiver, phone]))
    toonTrack = getToonTrack(attack, 2.7, ['cringe'], 1.9, ['sidestep'])
    soundTrack = getSoundTrack('SA_hangup.ogg', delay=1.3, node=suit)
    return Parallel(suitTrack, toonTrack, propTrack, partTrack, soundTrack)


def doShred(attack):
    suit = attack['suit']
    battle = attack['battle']
    paper = globalPropPool.getProp('shredder-paper')
    shredder = globalPropPool.getProp('shredder')
    particleEffect = BattleParticles.createParticleEffect('Shred')
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 3.5, 1.9, [particleEffect, suit, 0])
    paperPosPoints = [Point3(0.59, -0.31, 0.81), VBase3(79.224, 32.576, -179.449)]
    paperPropTrack = getPropTrack(paper, suit.getRightHand(), paperPosPoints, 2.4, 1e-05, scaleUpTime=0.2, anim=1, propName='shredder-paper', animDuration=1.5, animStartTime=2.8)
    shredderPosPoints = [Point3(0, -0.12, -0.34), VBase3(-90.0, -53.77, -0.0)]
    shredderPropTrack = getPropTrack(shredder, suit.getLeftHand(), shredderPosPoints, 1, 3, scaleUpPoint=Point3(4.81, 4.81, 4.81))
    toonTrack = getToonTrack(attack, suitTrack.getDuration() - 1.1, ['conked'], suitTrack.getDuration() - 3.1, ['sidestep'])
    soundTrack = getSoundTrack('SA_shred.ogg', delay=3.4, node=suit)
    return Parallel(suitTrack, paperPropTrack, shredderPropTrack, partTrack, toonTrack, soundTrack)


def doFillWithLead(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    pencil = globalPropPool.getProp('pencil')
    sharpener = globalPropPool.getProp('sharpener')
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect(file='fillWithLeadSpray')
    headSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    torsoSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    legsSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    BattleParticles.setEffectTexture(sprayEffect, 'roll-o-dex', color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(headSmotherEffect, 'roll-o-dex', color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(torsoSmotherEffect, 'roll-o-dex', color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(legsSmotherEffect, 'roll-o-dex', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, 2.5, 1.9, [sprayEffect, suit, 0])
    pencilPosPoints = [Point3(-0.29, -0.33, -0.13), VBase3(160.565, -11.653, -169.244)]
    pencilPropTrack = getPropTrack(pencil, suit.getRightHand(), pencilPosPoints, 0.7, 3.2, scaleUpTime=0.2)
    sharpenerPosPoints = [Point3(0.0, 0.0, -0.03), MovieUtil.PNT3_ZERO]
    sharpenerPropTrack = getPropTrack(sharpener, suit.getLeftHand(), sharpenerPosPoints, 1.3, 2.3, scaleUpPoint=MovieUtil.PNT3_ONE)
    damageAnims = [['conked', suitTrack.getDuration() - 1.5, 1e-05, 1.4],
     ['conked', 1e-05, 0.7, 0.7],
     ['conked', 1e-05, 0.7, 0.7],
     ['conked', 1e-05, 1.4]]
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, dodgeDelay=suitTrack.getDuration() - 3.1, dodgeAnimNames=['sidestep'], showDamageExtraTime=4.5, showMissedExtraTime=1.6)
    animal = toon.style.getAnimal()
    bodyScale = ToontownGlobals.toonBodyScales[animal]
    headEffectHeight = __toonFacePoint(toon).getZ()
    legsHeight = ToontownGlobals.legHeightDict[toon.style.legs] * bodyScale
    torsoEffectHeight = ToontownGlobals.torsoHeightDict[toon.style.torso] * bodyScale / 2 + legsHeight
    legsEffectHeight = legsHeight / 2
    effectX = headSmotherEffect.getX()
    effectY = headSmotherEffect.getY()
    headSmotherEffect.setPos(effectX, effectY - 1.5, headEffectHeight)
    torsoSmotherEffect.setPos(effectX, effectY - 1, torsoEffectHeight)
    legsSmotherEffect.setPos(effectX, effectY - 0.6, legsEffectHeight)
    partDelay = 3.5
    partIvalDelay = 0.7
    partDuration = 1.0
    headTrack = getPartTrack(headSmotherEffect, partDelay, partDuration, [headSmotherEffect, toon, 0])
    torsoTrack = getPartTrack(torsoSmotherEffect, partDelay + partIvalDelay, partDuration, [torsoSmotherEffect, toon, 0])
    legsTrack = getPartTrack(legsSmotherEffect, partDelay + partIvalDelay * 2, partDuration, [legsSmotherEffect, toon, 0])

    def colorParts(parts):
        track = Parallel()
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.setColorScale, Vec4(0, 0, 0, 1)))

        return track

    def resetParts(parts):
        track = Parallel()
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.clearColorScale))

        return track

    if dmg > 0:
        colorTrack = Sequence()
        headParts = toon.getHeadParts()
        torsoParts = toon.getTorsoParts()
        legsParts = toon.getLegsParts()
        colorTrack.append(Wait(partDelay + 0.2))
        colorTrack.append(Func(battle.movie.needRestoreColor))
        colorTrack.append(colorParts(headParts))
        colorTrack.append(Wait(partIvalDelay))
        colorTrack.append(colorParts(torsoParts))
        colorTrack.append(Wait(partIvalDelay))
        colorTrack.append(colorParts(legsParts))
        colorTrack.append(Wait(2.5))
        colorTrack.append(resetParts(headParts))
        colorTrack.append(resetParts(torsoParts))
        colorTrack.append(resetParts(legsParts))
        colorTrack.append(Func(battle.movie.clearRestoreColor))
        return Parallel(suitTrack, pencilPropTrack, sharpenerPropTrack, sprayTrack, headTrack, torsoTrack, legsTrack, colorTrack, toonTrack)
    else:
        return Parallel(suitTrack, pencilPropTrack, sharpenerPropTrack, sprayTrack, toonTrack)


def doFountainPen(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        pen = globalPropPool.getProp('pen')

        def getPenTip(pen=pen):
            tip = pen.find('**/joint_toSpray')
            return tip.getPos(render)

        hitPoint = lambda toon = toon: __toonFacePoint(toon)
        missPoint = lambda prop = pen, toon = toon: __toonMissPoint(prop, toon, 0, parent=render)
        hitSprayTrack = MovieUtil.getSprayTrack(battle, VBase4(0, 0, 0, 1), getPenTip, hitPoint, 0.2, 0.2, 0.2, horizScale=0.1, vertScale=0.1)
        missSprayTrack = MovieUtil.getSprayTrack(battle, VBase4(0, 0, 0, 1), getPenTip, missPoint, 0.2, 0.2, 0.2, horizScale=0.1, vertScale=0.1)
        suitTrack = getSuitTrack(attack)
        propTrack = Sequence(
            Wait(0.01),
            Func(__showProp, pen, suit.getRightHand(), MovieUtil.PNT3_ZERO),
            LerpScaleInterval(pen, 0.5, Point3(1.5, 1.5, 1.5)),
            Wait(1.05)
        )
        if dmg > 0:
            propTrack.append(hitSprayTrack)
        else:
            propTrack.append(missSprayTrack)
        propTrack.append(LerpScaleInterval(pen, 0.5, MovieUtil.PNT3_NEARZERO))
        propTrack.append(Func(MovieUtil.removeProp, pen))
        splashTrack = Sequence()
        if dmg > 0:

            def prepSplash(splash, targetPoint):
                splash.reparentTo(render)
                splash.setPos(targetPoint)
                scale = splash.getScale()
                splash.setBillboardPointWorld()
                splash.setScale(scale)

            splash = globalPropPool.getProp('splash-from-splat')
            splash.setColor(0, 0, 0, 1)
            splash.setScale(0.15)
            splashTrack = Sequence(
                Func(battle.movie.needRestoreRenderProp, splash),
                Wait(1.65),
                Func(prepSplash, splash, __toonFacePoint(toon)),
                ActorInterval(splash, 'splash-from-splat'),
                Func(MovieUtil.removeProp, splash),
                Func(battle.movie.clearRenderProp, splash)
            )
            headParts = toon.getHeadParts()
            splashTrack.append(Func(battle.movie.needRestoreColor))
            for partNum in range(0, headParts.getNumPaths()):
                nextPart = headParts.getPath(partNum)
                splashTrack.append(Func(nextPart.setColorScale, Vec4(0, 0, 0, 1)))

            splashTrack.append(Func(MovieUtil.removeProp, splash))
            splashTrack.append(Wait(2.6))
            for partNum in range(0, headParts.getNumPaths()):
                nextPart = headParts.getPath(partNum)
                splashTrack.append(Func(nextPart.clearColorScale))

            splashTrack.append(Func(battle.movie.clearRestoreColor))
        penSpill = BattleParticles.createParticleEffect(file='penSpill')
        penSpill.setPos(getPenTip())
        penSpillTrack = getPartTrack(penSpill, 1.4, 0.7, [penSpill, pen, 0])
        toonTrack = getToonTrack(attack, 1.81, ['conked'], dodgeDelay=0.11, splicedDodgeAnims=[['duck', 0.01, 0.6]], showMissedExtraTime=1.66)
        soundTrack = getSoundTrack('SA_fountain_pen.ogg', delay=1.6, node=suit)
        return Parallel(suitTrack, toonTrack, propTrack, soundTrack, penSpillTrack, splashTrack)
    else:
        targets = attack['target']

        def getPenTip(pen=pen):
            tip = pen.find('**/joint_toSpray')
            return tip.getPos(render)
        
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        propTrack = Sequence(
            Wait(0.01),
            Func(__showProp, pen, suit.getRightHand(), MovieUtil.PNT3_ZERO),
            LerpScaleInterval(pen, 0.5, Point3(1.5, 1.5, 1.5)),
            Wait(1.05)
        )
        sprayTracks = Parallel()
        splashTracks = Parallel()
        penSpill = BattleParticles.createParticleEffect(file='penSpill')
        penSpill.setPos(getPenTip())
        penSpillTrack = getPartTrack(penSpill, 1.4, 0.7, [penSpill, pen, 0])
        toonTracks = getToonTracks(attack, 1.81, ['conked'], dodgeDelay=0.11, splicedDodgeAnims=[['duck', 0.01, 0.6]], showMissedExtraTime=1.66)
        soundTrack = getSoundTrack('SA_fountain_pen.ogg', delay=1.6, node=suit)
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            hitPoint = lambda toon = toon: __toonFacePoint(toon)
            missPoint = lambda prop = pen, toon = toon: __toonMissPoint(prop, toon, 0, parent=render)
            hitSprayTrack = MovieUtil.getSprayTrack(battle, VBase4(0, 0, 0, 1), getPenTip, hitPoint, 0.2, 0.2, 0.2, horizScale=0.1, vertScale=0.1)
            missSprayTrack = MovieUtil.getSprayTrack(battle, VBase4(0, 0, 0, 1), getPenTip, missPoint, 0.2, 0.2, 0.2, horizScale=0.1, vertScale=0.1)
            if dmg > 0:
                sprayTracks.append(hitSprayTrack)
            else:
                sprayTracks.append(missSprayTrack)
            splashTrack = Sequence()
            if dmg > 0:
                
                def prepSplash(splash, targetPoint):
                    splash.reparentTo(render)
                    splash.setPos(targetPoint)
                    scale = splash.getScale()
                    splash.setBillboardPointWorld()
                    splash.setScale(scale)

                splash = globalPropPool.getProp('splash-from-splat')
                splash.setColor(0, 0, 0, 1)
                splash.setScale(0.15)
                splashTrack = Sequence(
                    Func(battle.movie.needRestoreRenderProp, splash),
                    Wait(1.65),
                    Func(prepSplash, splash, __toonFacePoint(toon)),
                    ActorInterval(splash, 'splash-from-splat'),
                    Func(MovieUtil.removeProp, splash),
                    Func(battle.movie.clearRenderProp, splash)
                )
                headParts = toon.getHeadParts()
                splashTrack.append(Func(battle.movie.needRestoreColor))
                for partNum in range(0, headParts.getNumPaths()):
                    nextPart = headParts.getPath(partNum)
                    splashTrack.append(Func(nextPart.setColorScale, Vec4(0, 0, 0, 1)))

                splashTrack.append(Func(MovieUtil.removeProp, splash))
                splashTrack.append(Wait(2.6))
                for partNum in range(0, headParts.getNumPaths()):
                    nextPart = headParts.getPath(partNum)
                    splashTrack.append(Func(nextPart.clearColorScale))

                splashTrack.append(Func(battle.movie.clearRestoreColor))
            splashTracks.append(splashTrack)
        propTrack.append(sprayTracks)
        propTrack.append(LerpScaleInterval(pen, 0.5, MovieUtil.PNT3_NEARZERO))
        propTrack.append(Func(MovieUtil.removeProp, pen))
        return Parallel(suitTrack, toonTracks, propTrack, soundTrack, penSpillTrack, splashTracks)


def doRubOut(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    pad = globalPropPool.getProp('pad')
    pencil = globalPropPool.getProp('pencil')
    headEffect = BattleParticles.createParticleEffect('RubOut', color=toon.style.getHeadColor())
    torsoEffect = BattleParticles.createParticleEffect('RubOut', color=toon.style.getArmColor())
    legsEffect = BattleParticles.createParticleEffect('RubOut', color=toon.style.getLegColor())
    suitTrack = getSuitTrack(attack)
    padPosPoints = [Point3(-0.66, 0.81, -0.06), VBase3(14.93, -2.29, 180.0)]
    padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 0.5, 2.57)
    pencilPosPoints = [Point3(0.04, -0.38, -0.1), VBase3(-170.223, -3.762, -62.929)]
    pencilPropTrack = getPropTrack(pencil, suit.getRightHand(), pencilPosPoints, 0.5, 2.57)
    toonTrack = getToonTrack(attack, 2.2, ['conked'], 2.0, ['jump'])
    hideTrack = Sequence()
    headParts = toon.getHeadParts()
    torsoParts = toon.getTorsoParts()
    legsParts = toon.getLegsParts()
    animal = toon.style.getAnimal()
    bodyScale = ToontownGlobals.toonBodyScales[animal]
    headEffectHeight = __toonFacePoint(toon).getZ()
    legsHeight = ToontownGlobals.legHeightDict[toon.style.legs] * bodyScale
    torsoEffectHeight = ToontownGlobals.torsoHeightDict[toon.style.torso] * bodyScale / 2 + legsHeight
    legsEffectHeight = legsHeight / 2
    effectX = headEffect.getX()
    effectY = headEffect.getY()
    headEffect.setPos(effectX, effectY - 1.5, headEffectHeight)
    torsoEffect.setPos(effectX, effectY - 1, torsoEffectHeight)
    legsEffect.setPos(effectX, effectY - 0.6, legsEffectHeight)
    partDelay = 2.5
    headTrack = getPartTrack(headEffect, partDelay + 0, 0.5, [headEffect, toon, 0])
    # torsoTrack = getPartTrack(torsoEffect, partDelay + 1.1, 0.5, [torsoEffect, toon, 0])
    # legsTrack = getPartTrack(legsEffect, partDelay + 2.2, 0.5, [legsEffect, toon, 0])
    torsoTrack = getPartTrack(torsoEffect, partDelay + 0, 0.5, [torsoEffect, toon, 0])
    legsTrack = getPartTrack(legsEffect, partDelay + 0, 0.5, [legsEffect, toon, 0])

    def hideParts(parts):
        track = Parallel()
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.setTransparency, 1))
            track.append(LerpFunctionInterval(nextPart.setAlphaScale, fromData=1, toData=0, duration=0.2))

        return track

    def showParts(parts):
        track = Parallel()
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.clearColorScale))
            track.append(LerpFunctionInterval(nextPart.setAlphaScale, duration=0.2))
            track.append(Func(nextPart.clearTransparency))

        return track

    soundTrack = getSoundTrack('SA_rubout.ogg', delay=1.7, node=suit)
    multiTrackList = Parallel(suitTrack, toonTrack, padPropTrack, pencilPropTrack, soundTrack)
    if dmg > 0:
        hideTrack.append(Wait(2.2))
        hideTrack.append(Func(battle.movie.needRestoreColor))
        # hideTrack.append(hideParts(headParts))
        # hideTrack.append(Wait(0.4))
        # hideTrack.append(hideParts(torsoParts))
        # hideTrack.append(Wait(0.4))
        # hideTrack.append(hideParts(legsParts))
        # hideTrack.append(Wait(1))
        hideTrack.append(Parallel(hideParts(headParts), hideParts(torsoParts), hideParts(legsParts)))
        hideTrack.append(Wait(2.4))
        # hideTrack.append(showParts(headParts))
        # hideTrack.append(showParts(torsoParts))
        # hideTrack.append(showParts(legsParts))
        hideTrack.append(Parallel(showParts(headParts), showParts(torsoParts), showParts(legsParts)))
        hideTrack.append(Func(battle.movie.clearRestoreColor))
        multiTrackList.append(hideTrack)
        multiTrackList.append(headTrack)
        multiTrackList.append(torsoTrack)
        multiTrackList.append(legsTrack)
    return multiTrackList


def doFingerWag(attack):
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('FingerWag')
    BattleParticles.setEffectTexture(particleEffect, 'blah', color=Vec4(0.55, 0, 0.55, 1))
    partDelay = {
        'a': 1.3,
        'b': 1.3,
        'c': 1.3
    }
    damageDelay = {
        'a': 2.7,
        'b': 2.7,
        'c': 2.7
    }
    dodgeDelay = {
        'a': 1.7,
        'b': 1.8,
        'c': 2.0
    }
    suitTrack = getSuitTrack(attack)
    suitName = attack['suitName']
    suitType = getSuitBodyType(suitName)
    partTrack = getPartTrack(particleEffect, partDelay[suitType], 2, [particleEffect, suit, 0])
    if suitName == 'mm':
        particleEffect.setPos(0.167, 1.5, 2.731)
    elif suitName == 'tw':
        particleEffect.setPos(0.167, 1.8, 5)
        particleEffect.setHpr(-90.0, -60.0, 180.0)
    elif suitName == 'pp':
        particleEffect.setPos(0.167, 1, 4.1)
    elif suitName == 'bs':
        particleEffect.setPos(0.167, 1, 5.1)
    elif suitName == 'bw':
        particleEffect.setPos(0.167, 1.9, suit.getHeight() - 1.8)
        particleEffect.setP(-110)
    toonTrack = getToonTrack(attack, damageDelay[suitType], ['slip-backward'], dodgeDelay[suitType], ['sidestep'])
    soundTrack = getSoundTrack('SA_finger_wag.ogg', delay=1.3, node=suit)
    return Parallel(suitTrack, toonTrack, partTrack, soundTrack)


def doWriteOff(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    pad = globalPropPool.getProp('pad')
    pencil = globalPropPool.getProp('pencil')
    BattleParticles.loadParticles()
    checkmark = MovieUtil.copyProp(BattleParticles.getParticle('checkmark'))
    checkmark.setBillboardPointEye()
    suitTrack = getSuitTrack(attack)
    padPosPoints = [Point3(-0.25, 1.38, -0.08), VBase3(-19.078, -6.603, -171.594)]
    padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 0.5, 2.57, Point3(1.89, 1.89, 1.89))
    missPoint = lambda checkmark = checkmark, toon = toon: __toonMissPoint(checkmark, toon)
    pencilPosPoints = [Point3(-0.47, 1.08, 0.28), VBase3(21.045, 12.702, -176.374)]
    extraArgsForShowProp = [pencil, suit.getRightHand()]
    extraArgsForShowProp.extend(pencilPosPoints)
    pencilPropTrack = Sequence(
        Wait(0.5),
        Func(__showProp, *extraArgsForShowProp),
        LerpScaleInterval(pencil, 0.5, Point3(1.5, 1.5, 1.5), startScale=Point3(0.01)),
        Wait(2),
        Func(battle.movie.needRestoreRenderProp, checkmark),
        Func(checkmark.reparentTo, render),
        Func(checkmark.setScale, 1.6),
        Func(checkmark.setPosHpr, pencil, 0, 0, 0, 0, 0, 0),
        Func(checkmark.setP, 0),
        Func(checkmark.setR, 0),
        getPropThrowTrack(attack, checkmark, [__toonFacePoint(toon)], [missPoint]),
        Func(MovieUtil.removeProp, checkmark),
        Func(battle.movie.clearRenderProp, checkmark),
        Wait(0.3),
        LerpScaleInterval(pencil, 0.5, MovieUtil.PNT3_NEARZERO),
        Func(MovieUtil.removeProp, pencil)
    )
    toonTrack = getToonTrack(attack, 3.4, ['slip-forward'], 2.4, ['sidestep'])
    soundTrack = Sequence(
        Wait(2.3),
        SoundInterval(globalBattleSoundCache.getSound('SA_writeoff_pen_only.ogg'), duration=0.9, node=suit),
        SoundInterval(globalBattleSoundCache.getSound('SA_writeoff_ding_only.ogg'), node=suit)
    )
    return Parallel(suitTrack, toonTrack, padPropTrack, pencilPropTrack, soundTrack)


def doRubberStamp(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        suitTrack = getSuitTrack(attack)
        stamp = globalPropPool.getProp('rubber-stamp')
        pad = globalPropPool.getProp('pad')
        cancelled = __makeCancelledNodePath()
        suitType = getSuitBodyType(attack['suitName'])
        if suitType == 'a':
            padPosPoints = [Point3(-0.65, 0.83, -0.04), VBase3(5.625, 4.456, -165.125)]
            stampPosPoints = [Point3(-0.64, -0.17, -0.03), MovieUtil.PNT3_ZERO]
        elif suitType == 'c':
            padPosPoints = [Point3(0.19, -0.55, -0.21), VBase3(-166.76, -4.001, -1.658)]
            stampPosPoints = [Point3(-0.64, -0.08, 0.11), MovieUtil.PNT3_ZERO]
        else:
            padPosPoints = [Point3(-0.65, 0.83, -0.04), VBase3(5.625, 4.456, -165.125)]
            stampPosPoints = [Point3(-0.64, -0.17, -0.03), MovieUtil.PNT3_ZERO]
        padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 1e-06, 3.2)
        missPoint = lambda cancelled = cancelled, toon = toon: __toonMissPoint(cancelled, toon)
        propTrack = Sequence(
            Func(__showProp, stamp, suit.getRightHand(), stampPosPoints[0], stampPosPoints[1]),
            LerpScaleInterval(stamp, 0.5, MovieUtil.PNT3_ONE),
            Wait(2.6),
            Func(battle.movie.needRestoreRenderProp, cancelled),
            Func(cancelled.reparentTo, render),
            Func(cancelled.setScale, 0.6),
            Func(cancelled.setPosHpr, stamp, 0.81, -1.11, -0.16, 0, 0, 90),
            Func(cancelled.setP, 0),
            Func(cancelled.setR, 0),
            getPropThrowTrack(attack, cancelled, [__toonFacePoint(toon)], [missPoint]),
            Func(MovieUtil.removeProp, cancelled),
            Func(battle.movie.clearRenderProp, cancelled),
            Wait(0.3),
            LerpScaleInterval(stamp, 0.5, MovieUtil.PNT3_NEARZERO),
            Func(MovieUtil.removeProp, stamp)
        )
        toonTrack = getToonTrack(attack, 3.4, ['conked'], 1.9, ['sidestep'])
        soundTrack = getSoundTrack('SA_rubber_stamp.ogg', delay=1.3, duration=1.1, node=suit)
        return Parallel(suitTrack, toonTrack, propTrack, padPropTrack, soundTrack)
    else:
        targets = attack['target']
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        pad = globalPropPool.getProp('pad')
        suitType = getSuitBodyType(attack['suitName'])
        if suitType == 'a':
            padPosPoints = [Point3(-0.65, 0.83, -0.04), VBase3(5.625, 4.456, -165.125)]
            stampPosPoints = [Point3(-0.64, -0.17, -0.03), MovieUtil.PNT3_ZERO]
        elif suitType == 'c':
            padPosPoints = [Point3(0.19, -0.55, -0.21), VBase3(-166.76, -4.001, -1.658)]
            stampPosPoints = [Point3(-0.64, -0.08, 0.11), MovieUtil.PNT3_ZERO]
        else:
            padPosPoints = [Point3(-0.65, 0.83, -0.04), VBase3(5.625, 4.456, -165.125)]
            stampPosPoints = [Point3(-0.64, -0.17, -0.03), MovieUtil.PNT3_ZERO]
        padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 1e-06, 3.2)
        propTracks = Parallel()
        for t in targets:
            toon = t['toon']
            stamp = globalPropPool.getProp('rubber-stamp')
            cancelled = __makeCancelledNodePath()
            missPoint = lambda cancelled = cancelled, toon = toon: __toonMissPoint(cancelled, toon)
            propTrack = Sequence(
                Func(__showProp, stamp, suit.getRightHand(), stampPosPoints[0], stampPosPoints[1]),
                LerpScaleInterval(stamp, 0.5, MovieUtil.PNT3_ONE),
                Wait(2.6),
                Func(battle.movie.needRestoreRenderProp, cancelled),
                Func(cancelled.reparentTo, render),
                Func(cancelled.setScale, 0.6),
                Func(cancelled.setPosHpr, stamp, 0.81, -1.11, -0.16, 0, 0, 90),
                Func(cancelled.setP, 0),
                Func(cancelled.setR, 0),
                getPropThrowTrack(attack, cancelled, [__toonFacePoint(toon)], [missPoint], target=t),
                Func(MovieUtil.removeProp, cancelled),
                Func(battle.movie.clearRenderProp, cancelled),
                Wait(0.3),
                LerpScaleInterval(stamp, 0.5, MovieUtil.PNT3_NEARZERO),
                Func(MovieUtil.removeProp, stamp)
            )
            propTracks.append(propTrack)
        toonTracks = getToonTracks(attack, 3.4, ['conked'], 1.9, ['sidestep'])
        soundTrack = getSoundTrack('SA_rubber_stamp.ogg', delay=1.3, duration=1.1, node=suit)
        return Parallel(suitTrack, toonTracks, propTracks, padPropTrack, soundTrack)


def doRazzleDazzle(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        sign = globalPropPool.getProp('smile')
        BattleParticles.loadParticles()
        particleEffect = BattleParticles.createParticleEffect('Smile')
        suitTrack = getSuitTrack(attack)
        signPosPoints = [Point3(0.0, -0.42, -0.04),
                         VBase3(105.715, 73.977, 65.932)]
        if dmg > 0:
            hitPoint = lambda toon = toon: __toonFacePoint(toon)
        else:
            hitPoint = lambda particleEffect = particleEffect, toon = toon, suit = suit: __toonMissPoint(particleEffect, toon, parent=suit.getRightHand())
        signPropTrack = Sequence(
            Wait(0.5),
            Func(__showProp, sign, suit.getRightHand(), signPosPoints[0], signPosPoints[1]),
            LerpScaleInterval(sign, 0.5, Point3(1.39, 1.39, 1.39)),
            Wait(0.5),
            Func(battle.movie.needRestoreParticleEffect, particleEffect),
            Func(particleEffect.start, sign),
            Func(particleEffect.wrtReparentTo, render),
            LerpPosInterval(particleEffect, 2.0, pos=hitPoint),
            Func(particleEffect.cleanup),
            Func(battle.movie.clearRestoreParticleEffect, particleEffect)
        )
        signPropAnimTrack = ActorInterval(sign, 'smile', duration=4, startTime=0)
        toonTrack = getToonTrack(attack, 2.6, ['cringe'], 1.9, ['sidestep'])
        soundTrack = getSoundTrack('SA_razzle_dazzle.ogg', delay=1.6, node=suit)
        return Sequence(Parallel(suitTrack, signPropTrack, signPropAnimTrack, toonTrack, soundTrack), Func(MovieUtil.removeProp, sign))
    else:
        targets = attack['target']
        sign = globalPropPool.getProp('smile')
        BattleParticles.loadParticles()
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        signPosPoints = [Point3(0.0, -0.42, -0.04),
                         VBase3(105.715, 73.977, 65.932)]
        signPropTrack = Sequence(
            Wait(0.5),
            Func(__showProp, sign, suit.getRightHand(), signPosPoints[0], signPosPoints[1]),
            LerpScaleInterval(sign, 0.5, Point3(1.39, 1.39, 1.39)),
            Wait(0.5)
        )
        partTracks = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            particleEffect = BattleParticles.createParticleEffect('Smile')
            if dmg > 0:
                hitPoint = lambda toon = toon: __toonFacePoint(toon)
            else:
                hitPoint = lambda particleEffect = particleEffect, toon = toon, suit = suit: __toonMissPoint(particleEffect, toon, parent=suit.getRightHand())
            partTrack = Sequence(
                Func(battle.movie.needRestoreParticleEffect, particleEffect),
                Func(particleEffect.start, sign),
                Func(particleEffect.wrtReparentTo, render),
                LerpPosInterval(particleEffect, 2.0, pos=hitPoint),
                Func(particleEffect.cleanup),
                Func(battle.movie.clearRestoreParticleEffect, particleEffect)
            )
            partTracks.append(partTrack)
        signPropTrack.append(partTracks)
        signPropAnimTrack = ActorInterval(sign, 'smile', duration=4, startTime=0)
        toonTracks = getToonTracks(attack, 2.6, ['cringe'], 1.9, ['sidestep'])
        soundTrack = getSoundTrack('SA_razzle_dazzle.ogg', delay=1.6, node=suit)
        return Sequence(Parallel(suitTrack, signPropTrack, signPropAnimTrack, toonTracks, soundTrack), Func(MovieUtil.removeProp, sign))


def doSynergy(attack):
    suit = attack['suit']
    battle = attack['battle']
    targets = attack['target']
    damageDelay = 1.7
    particleEffect = BattleParticles.createParticleEffect('Synergy')
    waterfallEffect = BattleParticles.createParticleEffect(file='synergyWaterfall')
    suitTrack = getSuitAnimTrack(attack)
    partTrack = getPartTrack(particleEffect, 1.0, 1.9, [particleEffect, suit, 0])
    waterfallTrack = getPartTrack(waterfallEffect, 0.8, 1.9, [waterfallEffect, suit, 0])
    dodgeAnims = [['jump', 0.01, 0, 0.6]]
    dodgeAnims.extend(getSplicedLerpAnims('jump', 0.31, 1.3, startTime=0.6))
    dodgeAnims.append(['jump', 0, 0.91])
    toonTracks = getToonTracks(attack, damageDelay=damageDelay, damageAnimNames=['slip-forward'], dodgeDelay=0.91, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.0)
    synergySoundTrack = getSoundTrack('SA_synergy.ogg', delay=0.9, node=suit)
    if hitAtleastOneToon(targets):
        fallingSoundTrack = getSoundTrack('Toon_bodyfall_synergy.ogg', delay=damageDelay + 0.5, node=suit)
        return Parallel(suitTrack, partTrack, waterfallTrack, synergySoundTrack, fallingSoundTrack, toonTracks)
    else:
        return Parallel(suitTrack, partTrack, waterfallTrack, synergySoundTrack, toonTracks)


def doTeeOff(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        club = globalPropPool.getProp('golf-club')
        ball = globalPropPool.getProp('golf-ball')
        suitTrack = getSuitTrack(attack)
        clubPosPoints = [MovieUtil.PNT3_ZERO, VBase3(63.097, 43.988, -18.435)]
        clubPropTrack = getPropTrack(club, suit.getLeftHand(), clubPosPoints, 0.5, 5.2, Point3(1.1, 1.1, 1.1))
        suitName = attack['suitName']
        if suitName == 'ym':
            ballPosPoints = [Point3(2.1, 0, 0.1)]
        elif suitName == 'tbc':
            ballPosPoints = [Point3(4.1, 0, 0.1)]
        elif suitName == 'm':
            ballPosPoints = [Point3(3.2, 0, 0.1)]
        elif suitName == 'mh':
            ballPosPoints = [Point3(4.2, 0, 0.1)]
        elif suitName == 'rb':
            ballPosPoints = [Point3(4.2, 0, 0.1)]
        else:
            ballPosPoints = [Point3(2.1, 0, 0.1)]
        ballPropTrack = Sequence(
            getPropAppearTrack(ball, suit, ballPosPoints, 1.7, Point3(1.5, 1.5, 1.5)),
            Func(battle.movie.needRestoreRenderProp, ball),
            Func(ball.wrtReparentTo, render),
            Wait(2.15)
        )
        missPoint = lambda ball = ball, toon = toon: __toonMissPoint(ball, toon)
        ballPropTrack.append(getPropThrowTrack(attack, ball, [__toonFacePoint(toon)], [missPoint]))
        ballPropTrack.append(Func(battle.movie.clearRenderProp, ball))
        dodgeDelay = suitTrack.getDuration() - 4.35
        toonTrack = getToonTrack(attack, suitTrack.getDuration() - 2.25, ['conked'], dodgeDelay, ['duck'], showMissedExtraTime=1.7)
        soundTrack = getSoundTrack('SA_tee_off.ogg', delay=4.1, node=suit)
        return Parallel(suitTrack, toonTrack, clubPropTrack, ballPropTrack, soundTrack)
    else:
        targets = attack['target']
        club = globalPropPool.getProp('golf-club')
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        clubPosPoints = [MovieUtil.PNT3_ZERO, VBase3(63.097, 43.988, -18.435)]
        clubPropTrack = getPropTrack(club, suit.getLeftHand(), clubPosPoints, 0.5, 5.2, Point3(1.1, 1.1, 1.1))
        soundTrack = getSoundTrack('SA_tee_off.ogg', delay=4.1, node=suit)
        suitName = attack['suitName']
        if suitName == 'ym':
            ballPosPoints = [Point3(2.1, 0, 0.1)]
        elif suitName == 'tbc':
            ballPosPoints = [Point3(4.1, 0, 0.1)]
        elif suitName == 'm':
            ballPosPoints = [Point3(3.2, 0, 0.1)]
        elif suitName == 'mh':
            ballPosPoints = [Point3(4.2, 0, 0.1)]
        elif suitName == 'rb':
            ballPosPoints = [Point3(4.2, 0, 0.1)]
        else:
            ballPosPoints = [Point3(2.1, 0, 0.1)]
        ballPropTracks = Parallel()
        for t in targets:
            toon = t['toon']
            ball = globalPropPool.getProp('golf-ball')
            ballPropTrack = Sequence(
                getPropAppearTrack(ball, suit, ballPosPoints, 1.7, Point3(1.5, 1.5, 1.5)),
                Func(battle.movie.needRestoreRenderProp, ball),
                Func(ball.wrtReparentTo, render),
                Wait(2.15)
            )
            missPoint = lambda ball = ball, toon = toon: __toonMissPoint(ball, toon)
            ballPropTrack.append(getPropThrowTrack(attack, ball, [__toonFacePoint(toon)], [missPoint]))
            ballPropTrack.append(Func(battle.movie.clearRenderProp, ball))
            ballPropTracks.append(ballPropTrack)
        dodgeDelay = suitTrack.getDuration() - 4.35
        toonTracks = getToonTracks(attack, suitTrack.getDuration() - 2.25, ['conked'], dodgeDelay, ['duck'], showMissedExtraTime=1.7)
        return Parallel(suitTrack, toonTracks, clubPropTrack, ballPropTracks, soundTrack)


def doBrainStorm(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        BattleParticles.loadParticles()
        snowEffect = BattleParticles.createParticleEffect('BrainStorm')
        snowEffect2 = BattleParticles.createParticleEffect('BrainStorm')
        snowEffect3 = BattleParticles.createParticleEffect('BrainStorm')
        if attack['id'] == LEGAL_STORM:
            effectColor = Vec4(0.4, 0, 0, 1)
            BattleParticles.setEffectTexture(snowEffect, 'legalese-hc', color=effectColor)
            BattleParticles.setEffectTexture(snowEffect2, 'legalese-qpq', color=effectColor)
            BattleParticles.setEffectTexture(snowEffect3, 'legalese-vd', color=effectColor)
        else:
            effectColor = Vec4(0.65, 0.79, 0.93, 0.85)
            BattleParticles.setEffectTexture(snowEffect, 'brainstorm-box', color=effectColor)
            BattleParticles.setEffectTexture(snowEffect2, 'brainstorm-env', color=effectColor)
            BattleParticles.setEffectTexture(snowEffect3, 'brainstorm-track', color=effectColor)
        cloud = globalPropPool.getProp('stormcloud')
        partDelay = {
            'a': 1.2,
            'b': 1.2,
            'c': 1.2
        }
        damageDelay = {
            'a': 4.5,
            'b': 4.5,
            'c': 4.5
        }
        dodgeDelay = {
            'a': 3.3,
            'b': 3.3,
            'c': 3.3
        }
        suitTrack = getSuitTrack(attack, delay=0.9)
        initialCloudHeight = suit.height + 3
        cloudPosPoints = [Point3(0, 3, initialCloudHeight), VBase3(180, 0, 0)]
        cloudPropTrack = Sequence(
            Func(cloud.pose, 'stormcloud', 0),
            getPropAppearTrack(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7),
            Func(battle.movie.needRestoreRenderProp, cloud),
            Func(cloud.wrtReparentTo, render)
        )
        targetPoint = __toonFacePoint(toon)
        targetPoint.setZ(targetPoint[2] + 3)
        cloudPropTrack.append(Wait(1.1))
        cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
        suitType = getSuitBodyType(attack['suitName'])
        cloudPropTrack.append(Wait(partDelay[suitType]))
        cloudPropTrack.append(
            Parallel(
                ParticleInterval(snowEffect, cloud, worldRelative=0, duration=2.2, cleanup=True),
                Sequence(
                    Wait(0.5),
                    ParticleInterval(snowEffect2, cloud, worldRelative=0, duration=1.7, cleanup=True)
                ),
                Sequence(
                    Wait(1.0),
                    ParticleInterval(snowEffect3, cloud, worldRelative=0, duration=1.2, cleanup=True)
                ),
                Sequence(
                    ActorInterval(cloud, 'stormcloud', startTime=3, duration=0.5),
                    ActorInterval(cloud, 'stormcloud', startTime=2.5, duration=0.5),
                    ActorInterval(cloud, 'stormcloud', startTime=1, duration=1.5)
                )
            )
        )
        cloudPropTrack.append(Wait(0.4))
        cloudPropTrack.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
        cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
        cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))
        damageAnims = [['cringe', 0.01, 0.4, 0.8],
         ['duck', 1e-06, 1.6]]
        toonTrack = getToonTrack(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], dodgeAnimNames=['sidestep'], showMissedExtraTime=1.1)
        soundTrack = getSoundTrack('SA_brainstorm.ogg', delay=2.6, node=suit)
        return Parallel(suitTrack, toonTrack, cloudPropTrack, soundTrack)
    else:
        targets = attack['target']
        BattleParticles.loadParticles()
        partDelay = {
            'a': 1.2,
            'b': 1.2,
            'c': 1.2
        }
        damageDelay = {
            'a': 4.5,
            'b': 4.5,
            'c': 4.5
        }
        dodgeDelay = {
            'a': 3.3,
            'b': 3.3,
            'c': 3.3
        }
        suitTrack = getSuitAnimTrack(attack, delay=0.9)
        initialCloudHeight = suit.height + 3
        cloudPosPoints = [Point3(0, 3, initialCloudHeight), VBase3(180, 0, 0)]
        cloudPropTracks = Parallel()
        damageAnims = [['cringe', 0.01, 0.4, 0.8],
         ['duck', 1e-06, 1.6]]
        toonTracks = getToonTracks(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], dodgeAnimNames=['sidestep'], showMissedExtraTime=1.1)
        soundTrack = getSoundTrack('SA_brainstorm.ogg', delay=2.6, node=suit)
        for t in targets:
            toon = t['toon']
            snowEffect = BattleParticles.createParticleEffect('BrainStorm')
            snowEffect2 = BattleParticles.createParticleEffect('BrainStorm')
            snowEffect3 = BattleParticles.createParticleEffect('BrainStorm')
            if attack['id'] == LEGAL_STORM:
                effectColor = Vec4(0.4, 0, 0, 1)
                BattleParticles.setEffectTexture(snowEffect, 'legalese-hc', color=effectColor)
                BattleParticles.setEffectTexture(snowEffect2, 'legalese-qpq', color=effectColor)
                BattleParticles.setEffectTexture(snowEffect3, 'legalese-vd', color=effectColor)
            else:
                effectColor = Vec4(0.65, 0.79, 0.93, 0.85)
                BattleParticles.setEffectTexture(snowEffect, 'brainstorm-box', color=effectColor)
                BattleParticles.setEffectTexture(snowEffect2, 'brainstorm-env', color=effectColor)
                BattleParticles.setEffectTexture(snowEffect3, 'brainstorm-track', color=effectColor)
            cloud = globalPropPool.getProp('stormcloud')
            cloudPropTrack = Sequence(
                Func(cloud.pose, 'stormcloud', 0),
                getPropAppearTrack(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7),
                Func(battle.movie.needRestoreRenderProp, cloud),
                Func(cloud.wrtReparentTo, render)
            )
            targetPoint = __toonFacePoint(toon)
            targetPoint.setZ(targetPoint[2] + 3)
            cloudPropTrack.append(Wait(1.1))
            cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
            suitType = getSuitBodyType(attack['suitName'])
            cloudPropTrack.append(Wait(partDelay[suitType]))
            cloudPropTrack.append(
                Parallel(
                    ParticleInterval(snowEffect, cloud, worldRelative=0, duration=2.2, cleanup=True),
                    Sequence(
                        Wait(0.5),
                        ParticleInterval(snowEffect2, cloud, worldRelative=0, duration=1.7, cleanup=True)
                    ),
                    Sequence(
                        Wait(1.0),
                        ParticleInterval(snowEffect3, cloud, worldRelative=0, duration=1.2, cleanup=True)
                    ),
                    Sequence(
                        ActorInterval(cloud, 'stormcloud', startTime=3, duration=0.5),
                        ActorInterval(cloud, 'stormcloud', startTime=2.5, duration=0.5),
                        ActorInterval(cloud, 'stormcloud', startTime=1, duration=1.5)
                    )
                )
            )
            cloudPropTrack.append(Wait(0.4))
            cloudPropTrack.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
            cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
            cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))
            cloudPropTracks.append(cloudPropTrack)
        return Parallel(suitTrack, toonTracks, cloudPropTracks, soundTrack)


def doBuzzWord(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    BattleParticles.loadParticles()
    particleEffects = []
    texturesList = ['buzzwords-crash',
     'buzzwords-inc',
     'buzzwords-main',
     'buzzwords-over',
     'buzzwords-syn']
    for i in range(0, 5):
        effect = BattleParticles.createParticleEffect('BuzzWord')
        if random.random() > 0.5:
            BattleParticles.setEffectTexture(effect, texturesList[i], color=Vec4(1, 0.94, 0.02, 1))
        else:
            BattleParticles.setEffectTexture(effect, texturesList[i], color=Vec4(0, 0, 0, 1))
        particleEffects.append(effect)

    partDelay = {
        'a': 4.0,
        'b': 4.0,
        'c': 4.0
    }
    partDuration = {
        'a': 2.2,
        'b': 2.2,
        'c': 2.2
    }
    damageDelay = {
        'a': 4.5,
        'b': 4.5,
        'c': 4.5
    }
    dodgeDelay = {
        'a': 3.8,
        'b': 3.8,
        'c': 3.8
    }
    suitName = attack['suitName']
    if suitName == 'm':
        for effect in particleEffects:
            effect.setPos(0, 2.8, suit.getHeight() - 2.5)
            effect.setHpr(0, -20, 0)

    elif suitName == 'mm':
        for effect in particleEffects:
            effect.setPos(0, 2.1, suit.getHeight() - 0.8)

    suitTrack = getSuitTrack(attack)
    particleTracks = []
    suitType = getSuitBodyType(suitName)
    for effect in particleEffects:
        particleTracks.append(getPartTrack(effect, partDelay[suitType], partDuration[suitType], [effect, suit, 0]))

    toonTrack = getToonTrack(attack, damageDelay=damageDelay[suitType], damageAnimNames=['cringe'], splicedDodgeAnims=[['duck', dodgeDelay[suitType], 1.4]], showMissedExtraTime=dodgeDelay[suitType] + 0.5)
    soundTrack = getSoundTrack('SA_buzz_word.ogg', delay=3.9, node=suit)
    return Parallel(suitTrack, toonTrack, soundTrack, *particleTracks)


def doDemotion(attack):
    suit = attack['suit']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect('DemotionSpray')
    freezeEffect = BattleParticles.createParticleEffect('DemotionFreeze')
    unFreezeEffect = BattleParticles.createParticleEffect(file='demotionUnFreeze')
    BattleParticles.setEffectTexture(sprayEffect, 'snow-particle')
    BattleParticles.setEffectTexture(freezeEffect, 'snow-particle')
    BattleParticles.setEffectTexture(unFreezeEffect, 'snow-particle')
    facePoint = __toonFacePoint(toon)
    freezeEffect.setPos(0, 0, facePoint.getZ())
    unFreezeEffect.setPos(0, 0, facePoint.getZ())
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(sprayEffect, 0.7, 1.1, [sprayEffect, suit, 0])
    partTrack2 = getPartTrack(freezeEffect, 1.4, 2.9, [freezeEffect, toon, 0])
    partTrack3 = getPartTrack(unFreezeEffect, 6.65, 0.5, [unFreezeEffect, toon, 0])
    damageAnims = [['cringe', 0.01, 0, 0.5]]
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.4, 0.5, startTime=0.5))
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.3, 0.5, startTime=0.9))
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.3, 0.6, startTime=1.2))
    damageAnims.append(['cringe', 2.6, 1.5])
    dodgeAnims = [['duck', 1e-06, 0.8]]
    toonTrack = getToonTrack(attack, damageDelay=1.0, splicedDamageAnims=damageAnims, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.6, showDamageExtraTime=1.3)
    soundTrack = getSoundTrack('SA_demotion.ogg', delay=1.2, node=suit)
    multiTrackList = Parallel(suitTrack, toonTrack, soundTrack, partTrack)
    if dmg > 0:
        multiTrackList.append(partTrack2)
        multiTrackList.append(partTrack3)
    return multiTrackList


def doCanned(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    hips = toon.getHipsParts()
    propDelay = 0.8
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'c':
        suitDelay = 1.13
        dodgeDelay = 3.1
    else:
        suitDelay = 1.83
        dodgeDelay = 3.6
    throwDuration = 1.5
    can = globalPropPool.getProp('can')
    scale = 26
    scaleUpPoint = {
        's': Point3(scale * 2.63, scale * 2.63, scale * 1.9975),
        'm': Point3(scale * 2.63, scale * 2.63, scale * 1.7975),
        'l': Point3(scale * 2.63, scale * 2.63, scale * 2.31)
    }
    canHpr = VBase3(-173.47, -0.42, 162.09)
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(-0.14, 0.15, 0.08), VBase3(-10.584, 11.945, -161.684)]
    throwTrack = Sequence(getPropAppearTrack(can, suit.getRightHand(), posPoints, propDelay, Point3(6, 6, 6), scaleUpTime=0.5))
    propDelay = propDelay + 0.5
    throwTrack.append(Wait(suitDelay))
    hitPoint = toon.getPos(battle)
    hitPoint.setX(hitPoint.getX() + 1.1)
    hitPoint.setY(hitPoint.getY() - 0.5)
    hitPoint.setZ(hitPoint.getZ() + toon.height + 1.1)
    throwTrack.append(Func(battle.movie.needRestoreRenderProp, can))
    throwTrack.append(getThrowTrack(can, hitPoint, duration=throwDuration, parent=battle))
    if dmg > 0:
        can2 = MovieUtil.copyProp(can)
        hips1 = hips.getPath(2)
        hips2 = hips.getPath(1)
        can2Point = Point3(hitPoint.getX(), hitPoint.getY() + 6.4, hitPoint.getZ())
        can2.setPos(can2Point)
        torso = toon.style.torso
        torso = torso[0]
        can2.setScale(scaleUpPoint[torso])
        can2.setHpr(canHpr)
        throwTrack.append(Func(battle.movie.needRestoreHips))
        throwTrack.append(Func(can.wrtReparentTo, hips1))
        throwTrack.append(Func(can2.reparentTo, hips2))
        throwTrack.append(Wait(2.4))
        throwTrack.append(Func(MovieUtil.removeProp, can2))
        throwTrack.append(Func(battle.movie.clearRestoreHips))
        scaleTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpScaleInterval(can, throwDuration, scaleUpPoint[torso])
        )
        hprTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpHprInterval(can, throwDuration, canHpr)
        )
        soundTrack = Sequence(
            Wait(2.6),
            SoundInterval(globalBattleSoundCache.getSound('SA_canned_tossup_only.ogg'), node=suit),
            SoundInterval(globalBattleSoundCache.getSound('SA_canned_impact_only.ogg'), node=toon)
        )
    else:
        land = toon.getPos(battle)
        land.setZ(land.getZ() + 0.7)
        bouncePoint1 = Point3(land.getX(), land.getY() - 1.5, land.getZ() + 2.5)
        bouncePoint2 = Point3(land.getX(), land.getY() - 2.1, land.getZ() - 0.2)
        bouncePoint3 = Point3(land.getX(), land.getY() - 3.1, land.getZ() + 1.5)
        bouncePoint4 = Point3(land.getX(), land.getY() - 4.1, land.getZ() + 0.3)
        throwTrack.append(LerpPosInterval(can, 0.4, land))
        throwTrack.append(LerpPosInterval(can, 0.4, bouncePoint1))
        throwTrack.append(LerpPosInterval(can, 0.3, bouncePoint2))
        throwTrack.append(LerpPosInterval(can, 0.3, bouncePoint3))
        throwTrack.append(LerpPosInterval(can, 0.3, bouncePoint4))
        throwTrack.append(Wait(1.1))
        throwTrack.append(LerpScaleInterval(can, 0.3, MovieUtil.PNT3_NEARZERO))
        scaleTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpScaleInterval(can, throwDuration, Point3(11, 11, 11))
        )
        hprTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpHprInterval(can, throwDuration, canHpr),
            Wait(0.4),
            LerpHprInterval(can, 0.4, Point3(83.27, 19.52, -177.92)),
            LerpHprInterval(can, 0.3, Point3(95.24, -72.09, 88.65)),
            LerpHprInterval(can, 0.2, Point3(-96.34, -2.63, 179.89))
        )
        soundTrack = getSoundTrack('SA_canned_tossup_only.ogg', delay=2.6, node=suit)
    canTrack = Sequence(
        Parallel(throwTrack, scaleTrack, hprTrack),
        Func(MovieUtil.removeProp, can),
        Func(battle.movie.clearRenderProp, can)
    )
    damageAnims = [['struggle', propDelay + suitDelay + throwDuration, 0.01, 0.7],
     ['slip-backward', 0.01, 0.45]]
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'], showDamageExtraTime=propDelay + suitDelay + 2.4)
    return Parallel(suitTrack, toonTrack, canTrack, soundTrack)


def doDownsize(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    damageDelay = 2.3
    sprayEffect = BattleParticles.createParticleEffect(file='downsizeSpray')
    cloudEffect = BattleParticles.createParticleEffect(file='downsizeCloud')
    toonPos = toon.getPos(toon)
    cloudPos = Point3(toonPos.getX(), toonPos.getY(), toonPos.getZ() + toon.getHeight() * 0.55)
    cloudEffect.setPos(cloudPos)
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.28, [sprayEffect, suit, 0])
    cloudTrack = getPartTrack(cloudEffect, 2.1, 1.9, [cloudEffect, toon, 0])
    if dmg > 0:
        initialScale = toon.getScale()
        downScale = Vec3(0.4, 0.4, 0.4)
        shrinkTrack = Sequence(
            Wait(damageDelay + 0.5),
            Func(battle.movie.needRestoreToonScale),
            LerpScaleInterval(toon, 1.0, downScale * 1.1),
            LerpScaleInterval(toon, 0.1, downScale * 0.9),
            LerpScaleInterval(toon, 0.1, downScale * 1.05),
            LerpScaleInterval(toon, 0.1, downScale * 0.95),
            LerpScaleInterval(toon, 0.1, downScale),
            Wait(2.1),
            LerpScaleInterval(toon, 0.5, initialScale * 1.5),
            LerpScaleInterval(toon, 0.15, initialScale * 0.5),
            LerpScaleInterval(toon, 0.15, initialScale * 1.2),
            LerpScaleInterval(toon, 0.15, initialScale * 0.8),
            LerpScaleInterval(toon, 0.15, initialScale),
            Func(battle.movie.clearRestoreToonScale)
        )
    damageAnims = [['juggle', 0.01, 0.87, 0.5],
     ['lose', 0.01, 2.17, 0.93],
     ['lose', 0.01, 3.1, -0.93],
     ['struggle', 0.01, 0.8, 1.8],
     ['sidestep-right', 0.01, 2.97, 1.49]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=0.6, dodgeAnimNames=['sidestep'])
    if dmg > 0:
        return Parallel(suitTrack, sprayTrack, cloudTrack, shrinkTrack, toonTrack)
    else:
        return Parallel(suitTrack, sprayTrack, toonTrack)


def doPinkSlip(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        paper = globalPropPool.getProp('pink-slip')
        throwDelay = 3.03
        throwDuration = 0.5
        suitTrack = getSuitTrack(attack)
        posPoints = [Point3(0.07, -0.06, -0.18), VBase3(-172.075, -26.715, -89.131)]
        paperAppearTrack = Sequence(
            getPropAppearTrack(paper, suit.getRightHand(), posPoints, 0.8, Point3(8, 8, 8), scaleUpTime=0.5),
            Wait(1.73)
        )
        hitPoint = __toonGroundPoint(attack, toon, 0.2, parent=battle)
        paperAppearTrack.append(Func(battle.movie.needRestoreRenderProp, paper))
        paperAppearTrack.append(Func(paper.wrtReparentTo, battle))
        paperAppearTrack.append(LerpPosInterval(paper, throwDuration, hitPoint))
        if dmg > 0:
            paperPause = 0.01
            slidePoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ() + 4)
            landPoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ())
            paperAppearTrack.append(Wait(paperPause))
            paperAppearTrack.append(LerpPosInterval(paper, 0.2, slidePoint))
            paperAppearTrack.append(LerpPosInterval(paper, 1.1, landPoint))
            paperSpinTrack = Sequence(
                Wait(throwDelay),
                LerpHprInterval(paper, throwDuration, VBase3(300, 0, 0)),
                Wait(paperPause),
                LerpHprInterval(paper, 1.3, VBase3(-200, 100, 100))
            )
        else:
            slidePoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ())
            paperAppearTrack.append(LerpPosInterval(paper, 0.5, slidePoint))
            paperSpinTrack = Sequence(
                Wait(throwDelay),
                LerpHprInterval(paper, throwDuration, VBase3(300, 0, 0)),
                LerpHprInterval(paper, 0.5, VBase3(10, 0, 0))
            )
        propTrack = Sequence()
        propTrack.append(Parallel(paperAppearTrack, paperSpinTrack))
        propTrack.append(LerpScaleInterval(paper, 0.4, MovieUtil.PNT3_NEARZERO))
        propTrack.append(Func(MovieUtil.removeProp, paper))
        propTrack.append(Func(battle.movie.clearRenderProp, paper))
        damageAnims = [['jump', 0.01, 0.3, 0.7],
         ['slip-forward', 0.01]]
        toonTrack = getToonTrack(attack, damageDelay=2.81, splicedDamageAnims=damageAnims, dodgeDelay=2.8, dodgeAnimNames=['jump'], showDamageExtraTime=0.9)
        soundTrack = getSoundTrack('SA_pink_slip.ogg', delay=2.9, duration=1.1, node=suit)
        return Parallel(suitTrack, toonTrack, propTrack, soundTrack)
    else:
        targets = attack['target']
        throwDelay = 3.03
        throwDuration = 0.5
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        posPoints = [Point3(0.07, -0.06, -0.18), VBase3(-172.075, -26.715, -89.131)]
        propTracks = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            paper = globalPropPool.getProp('pink-slip')
            paperAppearTrack = Sequence(
                getPropAppearTrack(paper, suit.getRightHand(), posPoints, 0.8, Point3(8, 8, 8), scaleUpTime=0.5),
                Wait(1.73)
            )
            hitPoint = __toonGroundPoint(attack, toon, 0.2, parent=battle)
            paperAppearTrack.append(Func(battle.movie.needRestoreRenderProp, paper))
            paperAppearTrack.append(Func(paper.wrtReparentTo, battle))
            paperAppearTrack.append(LerpPosInterval(paper, throwDuration, hitPoint))
            if dmg > 0:
                paperPause = 0.01
                slidePoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ() + 4)
                landPoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ())
                paperAppearTrack.append(Wait(paperPause))
                paperAppearTrack.append(LerpPosInterval(paper, 0.2, slidePoint))
                paperAppearTrack.append(LerpPosInterval(paper, 1.1, landPoint))
                paperSpinTrack = Sequence(
                    Wait(throwDelay),
                    LerpHprInterval(paper, throwDuration, VBase3(300, 0, 0)),
                    Wait(paperPause),
                    LerpHprInterval(paper, 1.3, VBase3(-200, 100, 100))
                )
            else:
                slidePoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ())
                paperAppearTrack.append(LerpPosInterval(paper, 0.5, slidePoint))
                paperSpinTrack = Sequence(
                    Wait(throwDelay),
                    LerpHprInterval(paper, throwDuration, VBase3(300, 0, 0)),
                    LerpHprInterval(paper, 0.5, VBase3(10, 0, 0))
                )
            propTrack = Sequence()
            propTrack.append(Parallel(paperAppearTrack, paperSpinTrack))
            propTrack.append(LerpScaleInterval(paper, 0.4, MovieUtil.PNT3_NEARZERO))
            propTrack.append(Func(MovieUtil.removeProp, paper))
            propTrack.append(Func(battle.movie.clearRenderProp, paper))
            propTracks.append(propTrack)
        damageAnims = [['jump', 0.01, 0.3, 0.7],
         ['slip-forward', 0.01]]
        toonTracks = getToonTracks(attack, damageDelay=2.81, splicedDamageAnims=damageAnims, dodgeDelay=2.8, dodgeAnimNames=['jump'], showDamageExtraTime=0.9)
        soundTrack = getSoundTrack('SA_pink_slip.ogg', delay=2.9, duration=1.1, node=suit)
        return Parallel(suitTrack, toonTracks, propTracks, soundTrack)


def doReOrg(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    damageDelay = 1.7
    attackDelay = 1.7
    sprayEffect = BattleParticles.createParticleEffect(file='reorgSpray')
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])
    if dmg > 0:
        headParts = toon.getHeadParts()
        print('***********headParts pos=', headParts[0].getPos())
        print('***********headParts hpr=', headParts[0].getHpr())
        headTracks = Parallel()
        for partNum in range(0, headParts.getNumPaths()):
            part = headParts.getPath(partNum)
            x = part.getX()
            y = part.getY()
            z = part.getZ()
            h = part.getH()
            p = part.getP()
            r = part.getR()
            headTracks.append(
                Sequence(
                    Wait(attackDelay),
                    LerpPosInterval(part, 0.1, Point3(x - 0.2, y, z - 0.03)),
                    LerpPosInterval(part, 0.1, Point3(x + 0.4, y, z - 0.03)),
                    LerpPosInterval(part, 0.1, Point3(x - 0.4, y, z - 0.03)),
                    LerpPosInterval(part, 0.1, Point3(x + 0.4, y, z - 0.03)),
                    LerpPosInterval(part, 0.1, Point3(x - 0.2, y, z - 0.04)),
                    LerpPosInterval(part, 0.25, Point3(x, y, z + 2.2)),
                    LerpHprInterval(part, 0.4, VBase3(360, 0, 180)),
                    LerpPosInterval(part, 0.3, Point3(x, y, z + 3.1)),
                    LerpPosInterval(part, 0.15, Point3(x, y, z + 0.3)),
                    Wait(0.15),
                    LerpHprInterval(part, 0.6, VBase3(-745, 0, 180), startHpr=VBase3(0, 0, 180)),
                    LerpHprInterval(part, 0.8, VBase3(25, 0, 180), startHpr=VBase3(0, 0, 180)),
                    LerpPosInterval(part, 0.15, Point3(x, y, z + 1)),
                    LerpHprInterval(part, 0.3, VBase3(h, p, r)),
                    Wait(0.2),
                    LerpPosInterval(part, 0.1, Point3(x, y, z)),
                    Wait(0.9)
                )
            )

        def getChestTrack(part, attackDelay=attackDelay):
            origScale = part.getScale()
            return Sequence(
                Wait(attackDelay),
                LerpHprInterval(part, 1.1, VBase3(180, 0, 0)),
                Wait(1.1),
                LerpHprInterval(part, 1.1, part.getHpr())
            )

        chestTracks = Parallel()
        arms = toon.findAllMatches('**/arms')
        sleeves = toon.findAllMatches('**/sleeves')
        hands = toon.findAllMatches('**/hands')
        print('*************arms hpr=', arms[0].getHpr())
        for partNum in range(0, arms.getNumPaths()):
            chestTracks.append(getChestTrack(arms.getPath(partNum)))
            chestTracks.append(getChestTrack(sleeves.getPath(partNum)))
            chestTracks.append(getChestTrack(hands.getPath(partNum)))

    damageAnims = [['neutral', 0.01, 0.01, 0.5],
     ['juggle', 0.01, 0.01, 1.48],
     ['think', 0.01, 2.28]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=0.01, dodgeAnimNames=['duck'], showDamageExtraTime=2.1, showMissedExtraTime=2.0)
    multiTrackList = Parallel(suitTrack, partTrack, toonTrack)
    if dmg > 0:
        multiTrackList.append(headTracks)
        multiTrackList.append(chestTracks)
    return multiTrackList


def doSacked(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    hips = toon.getHipsParts()
    propDelay = 0.85
    suitDelay = 1.93
    throwDuration = 0.9
    sack = globalPropPool.getProp('sandbag')
    initialScale = Point3(0.65, 1.47, 1.28)
    scaleUpPoint = Point3(1.05, 1.67, 0.98) * 4.1
    sackHpr = VBase3(-154.33, -6.33, 163.8)
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(0.51, -2.03, -0.73), VBase3(90.0, -24.98, 77.73)]
    sackAppearTrack = Sequence(getPropAppearTrack(sack, suit.getRightHand(), posPoints, propDelay, initialScale, scaleUpTime=0.2))
    propDelay = propDelay + 0.2
    sackAppearTrack.append(Wait(suitDelay))
    hitPoint = toon.getPos(battle)
    if dmg > 0:
        hitPoint.setX(hitPoint.getX() + 2.1)
        hitPoint.setY(hitPoint.getY() + 0.9)
        hitPoint.setZ(hitPoint.getZ() + toon.height + 1.2)
    else:
        hitPoint.setZ(hitPoint.getZ() - 0.2)
    sackAppearTrack.append(Func(battle.movie.needRestoreRenderProp, sack))
    sackAppearTrack.append(getThrowTrack(sack, hitPoint, duration=throwDuration, parent=battle))
    if dmg > 0:
        sack2 = MovieUtil.copyProp(sack)
        hips1 = hips.getPath(2)
        hips2 = hips.getPath(1)
        sack2.hide()
        sack2.reparentTo(battle)
        sack2.setPos(Point3(hitPoint.getX(), hitPoint.getY(), hitPoint.getZ()))
        sack2.setScale(scaleUpPoint)
        sack2.setHpr(sackHpr)
        sackAppearTrack.append(Func(battle.movie.needRestoreHips))
        sackAppearTrack.append(Func(sack.wrtReparentTo, hips1))
        sackAppearTrack.append(Func(sack2.show))
        sackAppearTrack.append(Func(sack2.wrtReparentTo, hips2))
        sackAppearTrack.append(Wait(2.4))
        sackAppearTrack.append(Func(MovieUtil.removeProp, sack2))
        sackAppearTrack.append(Func(battle.movie.clearRestoreHips))
        scaleTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpScaleInterval(sack, throwDuration, scaleUpPoint),
            Wait(1.8),
            LerpScaleInterval(sack, 0.3, MovieUtil.PNT3_NEARZERO)
        )
        hprTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpHprInterval(sack, throwDuration, sackHpr)
        )
        sackTrack = Sequence(
            Parallel(sackAppearTrack, scaleTrack, hprTrack),
            Func(MovieUtil.removeProp, sack),
            Func(battle.movie.clearRenderProp, sack)
        )
    else:
        sackAppearTrack.append(Wait(1.1))
        sackAppearTrack.append(LerpScaleInterval(sack, 0.3, MovieUtil.PNT3_NEARZERO))
        sackTrack = Sequence(
            sackAppearTrack,
            Func(MovieUtil.removeProp, sack),
            Func(battle.movie.clearRenderProp, sack)
        )
    damageAnims = [['struggle', 0.01, 0.01, 0.7],
     ['slip-backward', 0.01, 0.45]]
    toonTrack = getToonTrack(attack, damageDelay=propDelay + suitDelay + throwDuration, splicedDamageAnims=damageAnims, dodgeDelay=3.0, dodgeAnimNames=['sidestep'], showDamageExtraTime=1.8, showMissedExtraTime=0.8)
    return Parallel(suitTrack, toonTrack, sackTrack)


def doGlowerPower(attack):
    suit = attack['suit']
    battle = attack['battle']
    leftKnives = []
    rightKnives = []
    for i in range(0, 3):
        leftKnives.append(globalPropPool.getProp('dagger'))
        rightKnives.append(globalPropPool.getProp('dagger'))

    suitTrack = getSuitTrack(attack)
    suitName = attack['suitName']
    if suitName == 'hh':
        leftPosPoints = [Point3(0.3, 4.3, 5.3), MovieUtil.PNT3_ZERO]
        rightPosPoints = [Point3(-0.3, 4.3, 5.3), MovieUtil.PNT3_ZERO]
    elif suitName == 'tbc':
        leftPosPoints = [Point3(0.6, 4.5, 6), MovieUtil.PNT3_ZERO]
        rightPosPoints = [Point3(-0.6, 4.5, 6), MovieUtil.PNT3_ZERO]
    else:
        leftPosPoints = [Point3(0.4, 3.8, 3.7), MovieUtil.PNT3_ZERO]
        rightPosPoints = [Point3(-0.4, 3.8, 3.7), MovieUtil.PNT3_ZERO]
    leftKnifeTracks = Parallel()
    rightKnifeTracks = Parallel()
    for i in range(0, 3):
        knifeDelay = 0.11
        leftTrack = Sequence(
            Wait(1.1),
            Wait(i * knifeDelay),
            getPropAppearTrack(leftKnives[i], suit, leftPosPoints, 1e-06, Point3(0.4, 0.4, 0.4), scaleUpTime=0.1),
            getPropThrowTrack(attack, leftKnives[i], hitPointNames=['face'], missPointNames=['miss'], hitDuration=0.3, missDuration=0.3)
        )
        leftKnifeTracks.append(leftTrack)
        rightTrack = Sequence(
            Wait(1.1),
            Wait(i * knifeDelay),
            getPropAppearTrack(rightKnives[i], suit, rightPosPoints, 1e-06, Point3(0.4, 0.4, 0.4), scaleUpTime=0.1),
            getPropThrowTrack(attack, rightKnives[i], hitPointNames=['face'], missPointNames=['miss'], hitDuration=0.3, missDuration=0.3)
        )
        rightKnifeTracks.append(rightTrack)

    damageAnims = [['slip-backward', 0.01, 0.35]]
    toonTrack = getToonTrack(attack, damageDelay=1.6, splicedDamageAnims=damageAnims, dodgeDelay=0.7, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_glower_power.ogg', delay=1.1, node=suit)
    return Parallel(suitTrack, toonTrack, soundTrack, leftKnifeTracks, rightKnifeTracks)


def doWindsor(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        tie = globalPropPool.getProp('%s-windsor' % ('double' if attack['id'] == DOUBLE_WINDSOR else 'half'))
        throwDelay = 2.17
        damageDelay = 3.4
        dodgeDelay = 2.4
        suitTrack = getSuitTrack(attack)
        posPoints = [Point3(0.02, 0.88, 0.48), VBase3(99, -3, -108.2)]
        tiePropTrack = getPropAppearTrack(tie, suit.getRightHand(), posPoints, 0.5, Point3(7, 7, 7), scaleUpTime=0.5)
        tiePropTrack.append(Wait(throwDelay))
        missPoint = __toonMissBehindPoint(toon, parent=battle)
        missPoint.setX(missPoint.getX() - 1.1)
        missPoint.setZ(missPoint.getZ() + 4)
        hitPoint = __toonFacePoint(toon, parent=battle)
        hitPoint.setX(hitPoint.getX() - 1.1)
        hitPoint.setY(hitPoint.getY() - 0.7)
        hitPoint.setZ(hitPoint.getZ() + 0.9)
        tiePropTrack.append(getPropThrowTrack(attack, tie, [hitPoint], [missPoint], hitDuration=0.4, missDuration=0.8, missScaleDown=0.3, parent=battle))
        damageAnims = [['conked', 0.01, 0.01, 0.4],
         ['cringe', 0.01, 0.7]]
        toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
        throwSound = getSoundTrack('SA_powertie_throw.ogg', delay=throwDelay + 1, node=suit)
        return Parallel(suitTrack, toonTrack, tiePropTrack, throwSound)
    else:
        targets = attack['target']
        throwDelay = 2.17
        damageDelay = 3.4
        dodgeDelay = 2.4
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        posPoints = [Point3(0.02, 0.88, 0.48), VBase3(99, -3, -108.2)]
        tiePropTracks = Parallel()
        for t in targets:
            toon = t['toon']
            tie = globalPropPool.getProp('%s-windsor' % ('double' if attack['id'] == DOUBLE_WINDSOR else 'half'))
            tiePropTrack = getPropAppearTrack(tie, suit.getRightHand(), posPoints, 0.5, Point3(7, 7, 7), scaleUpTime=0.5)
            tiePropTrack.append(Wait(throwDelay))
            missPoint = __toonMissBehindPoint(toon, parent=battle)
            missPoint.setX(missPoint.getX() - 1.1)
            missPoint.setZ(missPoint.getZ() + 4)
            hitPoint = __toonFacePoint(toon, parent=battle)
            hitPoint.setX(hitPoint.getX() - 1.1)
            hitPoint.setY(hitPoint.getY() - 0.7)
            hitPoint.setZ(hitPoint.getZ() + 0.9)
            tiePropTrack.append(getPropThrowTrack(attack, tie, [hitPoint], [missPoint], hitDuration=0.4, missDuration=0.8, missScaleDown=0.3, parent=battle, target=t))
            tiePropTracks.append(tiePropTrack)
        damageAnims = [['conked', 0.01, 0.01, 0.4],
         ['cringe', 0.01, 0.7]]
        toonTracks = getToonTracks(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
        throwSound = getSoundTrack('SA_powertie_throw.ogg', delay=throwDelay + 1, node=suit)
        return Parallel(suitTrack, toonTracks, tiePropTracks, throwSound)


def doHeadShrink(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    damageDelay = 2.1
    dodgeDelay = 1.4
    shrinkSpray = BattleParticles.createParticleEffect(file='headShrinkSpray')
    shrinkCloud = BattleParticles.createParticleEffect(file='headShrinkCloud')
    shrinkDrop = BattleParticles.createParticleEffect(file='headShrinkDrop')
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(shrinkSpray, 0.3, 1.4, [shrinkSpray, suit, 0])
    shrinkCloud.reparentTo(battle)
    adjust = 0.4
    x = toon.getX(battle)
    y = toon.getY(battle) - adjust
    z = 8
    shrinkCloud.setPos(Point3(x, y, z))
    shrinkDrop.setPos(Point3(0, 0 - adjust, 7.5))
    off = 0.7
    cloudPoints = [Point3(x + off, y, z),
     Point3(x + off / 2, y + off / 2, z),
     Point3(x, y + off, z),
     Point3(x - off / 2, y + off / 2, z),
     Point3(x - off, y, z),
     Point3(x - off / 2, y - off / 2, z),
     Point3(x, y - off, z),
     Point3(x + off / 2, y - off / 2, z),
     Point3(x + off, y, z),
     Point3(x, y, z)]
    circleTrack = Sequence()
    for point in cloudPoints:
        circleTrack.append(LerpPosInterval(shrinkCloud, 0.14, point, other=battle))

    cloudTrack = Sequence(
        Wait(1.42),
        Func(battle.movie.needRestoreParticleEffect, shrinkCloud),
        Func(shrinkCloud.start, battle),
        circleTrack,
        circleTrack,
        LerpFunctionInterval(shrinkCloud.setAlphaScale, fromData=1, toData=0, duration=0.7),
        Func(shrinkCloud.cleanup),
        Func(battle.movie.clearRestoreParticleEffect, shrinkCloud)
    )
    shrinkDelay = 0.8
    shrinkDuration = 1.1
    shrinkTrack = Sequence()
    if dmg > 0:
        headParts = toon.getHeadParts()
        initialScale = headParts.getPath(0).getScale()[0]
        shrinkTrack.append(Wait(damageDelay + shrinkDelay))

        def scaleHeadParallel(scale, duration, headParts=headParts):
            headTracks = Parallel()
            for partNum in range(0, headParts.getNumPaths()):
                nextPart = headParts.getPath(partNum)
                headTracks.append(
                    LerpScaleInterval(
                        nextPart, duration, Point3(
                            scale, scale, scale)))

            return headTracks

        shrinkTrack.append(Func(battle.movie.needRestoreHeadScale))
        shrinkTrack.append(scaleHeadParallel(0.6, shrinkDuration))
        shrinkTrack.append(Wait(1.6))
        shrinkTrack.append(scaleHeadParallel(initialScale * 3.2, 0.4))
        shrinkTrack.append(scaleHeadParallel(initialScale * 0.7, 0.4))
        shrinkTrack.append(scaleHeadParallel(initialScale * 2.5, 0.3))
        shrinkTrack.append(scaleHeadParallel(initialScale * 0.8, 0.3))
        shrinkTrack.append(scaleHeadParallel(initialScale * 1.9, 0.2))
        shrinkTrack.append(scaleHeadParallel(initialScale * 0.85, 0.2))
        shrinkTrack.append(scaleHeadParallel(initialScale * 1.7, 0.15))
        shrinkTrack.append(scaleHeadParallel(initialScale * 0.9, 0.15))
        shrinkTrack.append(scaleHeadParallel(initialScale * 1.3, 0.1))
        shrinkTrack.append(scaleHeadParallel(initialScale, 0.1))
        shrinkTrack.append(Func(battle.movie.clearRestoreHeadScale))
        shrinkTrack.append(Wait(0.7))
    dropTrack = getPartTrack(shrinkDrop, 1.5, 2.5, [shrinkDrop, toon, 0])
    damageAnims = [['cringe', 0.01, 0.65, 0.2]]
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.64, 1.0, startTime=0.85))
    damageAnims.append(['cringe', 0.4, 1.49])
    damageAnims.append(['conked', 0.01, 3.6, -1.6])
    damageAnims.append(['conked', 0.01, 3.1, 0.4])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    multiTrackList = Parallel(suitTrack, sprayTrack, cloudTrack, dropTrack, toonTrack, shrinkTrack)
    if dmg > 0:
        soundTrack = Sequence(
            Wait(2.1),
            SoundInterval(globalBattleSoundCache.getSound('SA_head_shrink_only.ogg'), duration=2.1, node=suit),
            Wait(1.6),
            SoundInterval( globalBattleSoundCache.getSound('SA_head_grow_back_only.ogg'), node=suit)
        )
        multiTrackList.append(soundTrack)
    return multiTrackList


def doRolodex(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    rollodex = globalPropPool.getProp('rollodex')
    particleEffect2 = BattleParticles.createParticleEffect(file='rollodexWaterfall')
    particleEffect3 = BattleParticles.createParticleEffect(file='rollodexStream')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        propPosPoints = [Point3(-0.51, -0.03, -0.1), VBase3(89.673, 2.166, 177.786)]
        propScale = Point3(1.2, 1.2, 1.2)
        partDelay = 2.6
        part2Delay = 2.8
        part3Delay = 3.2
        partDuration = 1.6
        part2Duration = 1.9
        part3Duration = 1
        damageDelay = 3.8
        dodgeDelay = 2.5
    elif suitType == 'b':
        propPosPoints = [Point3(0.12, 0.24, 0.01), VBase3(99.032, 5.973, -179.839)]
        propScale = Point3(0.91, 0.91, 0.91)
        partDelay = 2.9
        part2Delay = 3.1
        part3Delay = 3.5
        partDuration = 1.6
        part2Duration = 1.9
        part3Duration = 1
        damageDelay = 4
        dodgeDelay = 2.5
    elif suitType == 'c':
        propPosPoints = [Point3(-0.51, -0.03, -0.1), VBase3(89.673, 2.166, 177.786)]
        propScale = Point3(1.2, 1.2, 1.2)
        partDelay = 2.3
        part2Delay = 2.8
        part3Delay = 3.2
        partDuration = 1.9
        part2Duration = 1.9
        part3Duration = 1
        damageDelay = 3.5
        dodgeDelay = 2.5
    hitPoint = lambda toon = toon: __toonFacePoint(toon)
    partTrack2 = getPartTrack(particleEffect2, part2Delay, part2Duration, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, part3Delay, part3Duration, [particleEffect3, suit, 0])
    suitTrack = getSuitTrack(attack)
    propTrack = getPropTrack(rollodex, suit.getLeftHand(), propPosPoints, 1e-06, 4.7, scaleUpPoint=propScale, anim=0, propName='rollodex', animDuration=0, animStartTime=0)
    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])
    soundTrack = getSoundTrack('SA_rolodex.ogg', delay=2.8, node=suit)
    return Parallel(suitTrack, toonTrack, propTrack, soundTrack, partTrack2, partTrack3)


def doEvilEye(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        eye = globalPropPool.getProp('evil-eye')
        damageDelay = 2.44
        dodgeDelay = 1.64
        suitName = attack['suitName']
        if suitName == 'cr':
            posPoints = [Point3(-0.46, 4.85, 5.28), VBase3(-155.0, -20.0, 0.0)]
        elif suitName == 'tf':
            posPoints = [Point3(-0.4, 3.65, 5.01), VBase3(-155.0, -20.0, 0.0)]
        elif suitName == 'le':
            posPoints = [Point3(-0.64, 4.45, 5.91), VBase3(-155.0, -20.0, 0.0)]
        else:
            posPoints = [Point3(-0.4, 3.65, 5.01), VBase3(-155.0, -20.0, 0.0)]
        appearDelay = 0.8
        suitHoldStart = 1.06
        suitHoldStop = 1.69
        suitHoldDuration = suitHoldStop - suitHoldStart
        eyeHoldDuration = 1.1
        moveDuration = 1.1
        suitSplicedAnims = [['glower', 0.01, 0.01, suitHoldStart]]
        suitSplicedAnims.extend(getSplicedLerpAnims('glower', suitHoldDuration, 1.1, startTime=suitHoldStart))
        suitSplicedAnims.append(['glower', 0.01, suitHoldStop])
        suitTrack = getSuitTrack(attack, splicedAnims=suitSplicedAnims)
        eyeAppearTrack = Sequence(
            Wait(suitHoldStart),
            Func(__showProp, eye, suit, posPoints[0], posPoints[1]),
            LerpScaleInterval(eye, suitHoldDuration, Point3(11, 11, 11)),
            Wait(eyeHoldDuration * 0.3),
            LerpHprInterval(eye, 0.02, Point3(205, 40, 0)),
            Wait(eyeHoldDuration * 0.7),
            Func(battle.movie.needRestoreRenderProp, eye),
            Func(eye.wrtReparentTo, battle)
        )
        toonFace = __toonFacePoint(toon, parent=battle)
        if dmg > 0:
            lerpInterval = LerpPosInterval(eye, moveDuration, toonFace)
        else:
            lerpInterval = LerpPosInterval(eye, moveDuration, Point3(toonFace.getX(), toonFace.getY() - 5, toonFace.getZ() - 2))
        eyeMoveTrack = lerpInterval
        eyeRollTrack = LerpHprInterval(eye, moveDuration, Point3(0, 0, -180))
        eyePropTrack = Sequence(
            eyeAppearTrack,
            Parallel(eyeMoveTrack, eyeRollTrack),
            Func(battle.movie.clearRenderProp, eye),
            Func(MovieUtil.removeProp, eye)
        )
        damageAnims = [['duck', 0.01, 0.01, 1.4],
         ['cringe', 0.01, 0.3]]
        toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, damageDelay=damageDelay, dodgeDelay=dodgeDelay, dodgeAnimNames=['duck'], showDamageExtraTime=1.7, showMissedExtraTime=1.7)
        soundTrack = getSoundTrack('SA_evil_eye.ogg', delay=1.3, node=suit)
        return Parallel(suitTrack, toonTrack, eyePropTrack, soundTrack)
    else:
        targets = attack['target']
        damageDelay = 2.44
        dodgeDelay = 1.64
        suitName = attack['suitName']
        if suitName == 'cr':
            posPoints = [Point3(-0.46, 4.85, 5.28), VBase3(-155.0, -20.0, 0.0)]
        elif suitName == 'tf':
            posPoints = [Point3(-0.4, 3.65, 5.01), VBase3(-155.0, -20.0, 0.0)]
        elif suitName == 'le':
            posPoints = [Point3(-0.64, 4.45, 5.91), VBase3(-155.0, -20.0, 0.0)]
        else:
            posPoints = [Point3(-0.4, 3.65, 5.01), VBase3(-155.0, -20.0, 0.0)]
        appearDelay = 0.8
        suitHoldStart = 1.06
        suitHoldStop = 1.69
        suitHoldDuration = suitHoldStop - suitHoldStart
        eyeHoldDuration = 1.1
        moveDuration = 1.1
        suitSplicedAnims = [['glower', 0.01, 0.01, suitHoldStart]]
        suitSplicedAnims.extend(getSplicedLerpAnims('glower', suitHoldDuration, 1.1, startTime=suitHoldStart))
        suitSplicedAnims.append(['glower', 0.01, suitHoldStop])
        suitTrack = getSuitAnimTrack(attack, delay=1e-06, splicedAnims=suitSplicedAnims)
        eyePropTracks = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            eye = globalPropPool.getProp('evil-eye')
            eyeAppearTrack = Sequence(
                Wait(suitHoldStart),
                Func(__showProp, eye, suit, posPoints[0], posPoints[1]),
                LerpScaleInterval(eye, suitHoldDuration, Point3(11, 11, 11)),
                Wait(eyeHoldDuration * 0.3),
                LerpHprInterval(eye, 0.02, Point3(205, 40, 0)),
                Wait(eyeHoldDuration * 0.7),
                Func(battle.movie.needRestoreRenderProp, eye),
                Func(eye.wrtReparentTo, battle)
            )
            toonFace = __toonFacePoint(toon, parent=battle)
            if dmg > 0:
                lerpInterval = LerpPosInterval(eye, moveDuration, toonFace)
            else:
                lerpInterval = LerpPosInterval(eye, moveDuration, Point3(toonFace.getX(), toonFace.getY() - 5, toonFace.getZ() - 2))
            eyeMoveTrack = lerpInterval
            eyeRollTrack = LerpHprInterval(eye, moveDuration, Point3(0, 0, -180))
            eyePropTrack = Sequence(
                eyeAppearTrack,
                Parallel(eyeMoveTrack, eyeRollTrack),
                Func(battle.movie.clearRenderProp, eye),
                Func(MovieUtil.removeProp, eye)
            )
            eyePropTracks.append(eyePropTrack)
        damageAnims = [['duck', 0.01, 0.01, 1.4],
         ['cringe', 0.01, 0.3]]
        toonTracks = getToonTracks(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['duck'], showDamageExtraTime=1.7, showMissedExtraTime=1.7)
        soundTrack = getSoundTrack('SA_evil_eye.ogg', delay=1.3, node=suit)
        return Parallel(suitTrack, toonTracks, eyePropTracks, soundTrack)


def doPlayHardball(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    ball = globalPropPool.getProp('baseball')
    suitDelay = {
        'a': 1.79,
        'b': 1.79,
        'c': 1.09
    }
    damageDelay = {
        'a': 3.46,
        'b': 3.46,
        'c': 2.76
    }
    dodgeDelay = {
        'a': 2.56,
        'b': 2.56,
        'c': 1.86
    }
    suitTrack = getSuitTrack(attack)
    ballPosPoints = [Point3(0.04, 0.03, -0.31), VBase3(-1.152, 86.581, -76.784)]
    propTrack = Sequence(getPropAppearTrack(ball, suit.getRightHand(), ballPosPoints, 0.8, Point3(5, 5, 5), scaleUpTime=0.5))
    suitType = getSuitBodyType(attack['suitName'])
    propTrack.append(Wait(suitDelay[suitType]))
    propTrack.append(Func(battle.movie.needRestoreRenderProp, ball))
    propTrack.append(Func(ball.wrtReparentTo, battle))
    toonPos = toon.getPos(battle)
    x = toonPos.getX()
    y = toonPos.getY()
    z = toonPos.getZ()
    z = z + 0.2
    if dmg > 0:
        propTrack.append(LerpPosInterval(ball, 0.5, __toonFacePoint(toon, parent=battle)))
        propTrack.append(LerpPosInterval(ball, 0.5, Point3(x, y + 3, z)))
        propTrack.append(LerpPosInterval(ball, 0.4, Point3(x, y + 5, z + 2)))
        propTrack.append(LerpPosInterval(ball, 0.3, Point3(x, y + 6, z)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y + 7, z + 1)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y + 8, z)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y + 8.5, z + 0.6)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y + 9, z + 0.2)))
        propTrack.append(Wait(0.4))
        soundTrack = getSoundTrack('SA_hardball_impact_only.ogg', delay=2.8, node=suit)
    else:
        propTrack.append(LerpPosInterval(ball, 0.5, Point3(x, y + 2, z)))
        propTrack.append(LerpPosInterval(ball, 0.4, Point3(x, y - 1, z + 2)))
        propTrack.append(LerpPosInterval(ball, 0.3, Point3(x, y - 3, z)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y - 4, z + 1)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y - 5, z)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y - 5.5, z + 0.6)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y - 6, z + 0.2)))
        propTrack.append(Wait(0.4))
        soundTrack = getSoundTrack('SA_hardball.ogg', delay=3.1, node=suit)
    propTrack.append(LerpScaleInterval(ball, 0.3, MovieUtil.PNT3_NEARZERO))
    propTrack.append(Func(MovieUtil.removeProp, ball))
    propTrack.append(Func(battle.movie.clearRenderProp, ball))
    damageAnims = [['conked', damageDelay[suitType], 0.01, 0.5],
     ['slip-backward', 0.01, 0.7]]
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], dodgeAnimNames=['sidestep'], showDamageExtraTime=3.9)
    return Parallel(suitTrack, toonTrack, propTrack, soundTrack)


def doPowerTie(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    tie = globalPropPool.getProp('power-tie')
    throwDelay = {
        'a': 2.17,
        'b': 2.17,
        'c': 1.45
    }
    damageDelay = {
        'a': 3.3,
        'b': 3.3,
        'c': 2.61
    }
    dodgeDelay = {
        'a': 3.1,
        'b': 3.1,
        'c': 2.34
    }
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(1.16, 0.24, 0.63), VBase3(171.561, 1.745, -163.443)]
    tiePropTrack = Sequence(getPropAppearTrack(tie, suit.getRightHand(), posPoints, 0.5, Point3(3.5, 3.5, 3.5), scaleUpTime=0.5))
    suitType = getSuitBodyType(attack['suitName'])
    tiePropTrack.append(Wait(throwDelay[suitType]))
    tiePropTrack.append(Func(tie.setBillboardPointEye))
    tiePropTrack.append(getPropThrowTrack(attack, tie, [__toonFacePoint(toon)], [__toonGroundPoint(attack, toon, 0.1)], hitDuration=0.4, missDuration=0.8))
    toonTrack = getToonTrack(attack, damageDelay[suitType], ['conked'], dodgeDelay[suitType], ['sidestep'])
    throwSound = getSoundTrack('SA_powertie_throw.ogg', delay=2.3, node=suit)
    multiTrackList = Parallel(suitTrack, toonTrack, tiePropTrack, throwSound)
    if dmg > 0:
        hitSound = getSoundTrack('SA_powertie_impact.ogg', delay=2.9, node=suit)
        multiTrackList.append(hitSound)
    return multiTrackList


def doCigarSmoke(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    cigar = globalPropPool.getProp('cigar')
    propTrack = getPropTrack(cigar, suit.getRightHand(), [Point3(-0.1, 0.0, -0.2), VBase3(180.0, 0.0, 0.0)], 0.1, 5.0, Point3(5.0, 5.0, 5.0))
    BattleParticles.loadParticles()
    smokeEffect = BattleParticles.createParticleEffect('BuzzWord')
    BattleParticles.setEffectTexture(smokeEffect, 'smoke', Vec4(1, 1, 1, 1))
    smokeEffect.setPosHpr(0.0, 3.25, 7.0, 0.0, -45.0, 0.0)
    partTrack = getPartTrack(smokeEffect, 3.4, 1.5, [smokeEffect, suit, 0])
    suitTrack = getSuitTrack(attack)
    toonTrack = getToonTrack(attack, 3.7, ['cringe'], 3.2, ['sidestep'])
    headParts = toon.getHeadParts()
    torsoParts = toon.getTorsoParts()
    legsParts = toon.getLegsParts()

    def changeColor(parts):
        track = Parallel()
        for partNum in xrange(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.setColorScale, Vec4(0.5, 0.5, 0.5, 1)))

        return track

    def resetColor(parts):
        track = Parallel()
        for partNum in xrange(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.clearColorScale))

        return track

    colorTrack = Sequence()
    multiTrackList = Parallel(suitTrack, toonTrack, propTrack, partTrack)
    if dmg > 0:
        colorTrack.append(Wait(3.7))
        colorTrack.append(Func(battle.movie.needRestoreColor))
        colorTrack.append(
            Parallel(
                changeColor(headParts),
                changeColor(torsoParts),
                changeColor(legsParts)
            )
        )
        colorTrack.append(Wait(3.0))
        colorTrack.append(resetColor(headParts))
        colorTrack.append(resetColor(torsoParts))
        colorTrack.append(resetColor(legsParts))
        colorTrack.append(Func(battle.movie.clearRestoreColor))
    return Parallel(suitTrack, toonTrack, propTrack, partTrack, colorTrack)


def doFloodTheMarket(attack):
    suit = attack['suit']
    particleEffect = BattleParticles.createParticleEffect('Synergy')
    waterfallEffect = BattleParticles.createParticleEffect(file='synergyWaterfall')
    suitTrack = getSuitAnimTrack(attack)
    partTrack = getPartTrack(particleEffect, 1.0, 1.9, [particleEffect, suit, 0])
    waterfallTrack = getPartTrack(waterfallEffect, 0.8, 1.9, [waterfallEffect, suit, 0])
    damageAnims = [['melt'], ['jump', 1.5, 0.4]]
    dodgeAnims = [['jump', 0.01, 0, 0.6]]
    dodgeAnims.extend(getSplicedLerpAnims('jump', 0.31, 1.3, startTime=0.6))
    dodgeAnims.append(['jump', 0, 0.91])
    toonTracks = getToonTracks(attack, damageDelay=0.7, splicedDamageAnims=damageAnims, dodgeDelay=0.91, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.0)
    soundTrack = getSoundTrack('SA_synergy.ogg', delay=0.9, node=suit)
    return Parallel(suitTrack, partTrack, waterfallTrack, soundTrack, toonTracks)


def doDoubleTalk(attack):
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('DoubleTalkLeft')
    particleEffect2 = BattleParticles.createParticleEffect('DoubleTalkRight')
    BattleParticles.setEffectTexture(particleEffect, 'doubletalk-double', color=Vec4(0, 1, 0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'doubletalk-good', color=Vec4(0, 1, 0, 1))
    partDelay = {
        'a': 3.3,
        'b': 3.3,
        'c': 3.3
    }
    damageDelay = {
        'a': 3.5,
        'b': 3.5,
        'c': 3.5
    }
    dodgeDelay = {
        'a': 3.3,
        'b': 3.3,
        'c': 3.3
    }
    suitTrack = getSuitTrack(attack)
    suitType = getSuitBodyType(attack['suitName'])
    partTrack = getPartTrack(particleEffect, partDelay[suitType], 1.8, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, partDelay[suitType], 1.8, [particleEffect2, suit, 0])
    damageAnims = [['duck', 0.01, 0.4, 1.05],
     ['cringe', 1e-06, 0.8]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], splicedDodgeAnims=[['duck', 0.01, 1.4]], showMissedExtraTime=0.9, showDamageExtraTime=0.8)
    soundTrack = getSoundTrack('SA_filibuster.ogg', delay=2.5, node=suit)
    return Parallel(suitTrack, toonTrack, partTrack, partTrack2, soundTrack)


def doFreezeAssets(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        BattleParticles.loadParticles()
        snowEffect = BattleParticles.createParticleEffect('FreezeAssets')
        BattleParticles.setEffectTexture(snowEffect, 'snow-particle')
        cloud = globalPropPool.getProp('stormcloud')
        partDelay = {
            'a': 0.2,
            'b': 0.2,
            'c': 0.2
        }
        damageDelay = {
            'a': 3.5,
            'b': 3.5,
            'c': 3.5
        }
        dodgeDelay = {
            'a': 2.3,
            'b': 2.3,
            'c': 2.3
        }
        suitTrack = getSuitTrack(attack, delay=0.9)
        initialCloudHeight = suit.height + 3
        cloudPosPoints = [Point3(0, 3, initialCloudHeight), MovieUtil.PNT3_ZERO]
        cloudPropTrack = Sequence(
            Func(cloud.pose, 'stormcloud', 0),
            getPropAppearTrack(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7),
            Func(battle.movie.needRestoreRenderProp, cloud),
            Func(cloud.wrtReparentTo, render)
        )
        targetPoint = __toonFacePoint(toon)
        targetPoint.setZ(targetPoint[2] + 3)
        cloudPropTrack.append(Wait(1.1))
        cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
        suitType = getSuitBodyType(attack['suitName'])
        cloudPropTrack.append(Wait(partDelay[suitType]))
        cloudPropTrack.append(ParticleInterval(snowEffect, cloud, worldRelative=0, duration=2.1, cleanup=True))
        cloudPropTrack.append(Wait(0.4))
        cloudPropTrack.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
        cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
        cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))
        damageAnims = [['cringe', 0.01, 0.4, 0.8],
         ['duck', 0.01, 1.6]]
        toonTrack = getToonTrack(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], dodgeAnimNames=['sidestep'], showMissedExtraTime=1.2)
        return Parallel(suitTrack, toonTrack, cloudPropTrack)
    else:
        targets = attack['target']
        BattleParticles.loadParticles()
        partDelay = {
            'a': 0.2,
            'b': 0.2,
            'c': 0.2
        }
        damageDelay = {
            'a': 3.5,
            'b': 3.5,
            'c': 3.5
        }
        dodgeDelay = {
            'a': 2.3,
            'b': 2.3,
            'c': 2.3
        }
        suitTrack = getSuitAnimTrack(attack, delay=0.9)
        initialCloudHeight = suit.height + 3
        cloudPosPoints = [Point3(0, 3, initialCloudHeight), MovieUtil.PNT3_ZERO]
        cloudPropTracks = Parallel()
        damageAnims = [['cringe', 0.01, 0.4, 0.8],
         ['duck', 0.01, 1.6]]
        toonTracks = getToonTracks(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], dodgeAnimNames=['sidestep'], showMissedExtraTime=1.2)
        for t in targets:
            toon = t['toon']
            snowEffect = BattleParticles.createParticleEffect('FreezeAssets')
            BattleParticles.setEffectTexture(snowEffect, 'snow-particle')
            cloud = globalPropPool.getProp('stormcloud')
            cloudPropTrack = Sequence(
                Func(cloud.pose, 'stormcloud', 0),
                getPropAppearTrack(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7),
                Func(battle.movie.needRestoreRenderProp, cloud),
                Func(cloud.wrtReparentTo, render)
            )
            targetPoint = __toonFacePoint(toon)
            targetPoint.setZ(targetPoint[2] + 3)
            cloudPropTrack.append(Wait(1.1))
            cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
            suitType = getSuitBodyType(attack['suitName'])
            cloudPropTrack.append(Wait(partDelay[suitType]))
            cloudPropTrack.append(ParticleInterval(snowEffect, cloud, worldRelative=0, duration=2.1, cleanup=True))
            cloudPropTrack.append(Wait(0.4))
            cloudPropTrack.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
            cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
            cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))
            cloudPropTracks.append(cloudPropTrack)
        return Parallel(suitTrack, toonTracks, cloudPropTracks)


def doHotAir(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect('HotAir')
    baseFlameEffect = BattleParticles.createParticleEffect(file='firedBaseFlame')
    flameEffect = BattleParticles.createParticleEffect('FiredFlame')
    flecksEffect = BattleParticles.createParticleEffect('SpriteFiredFlecks')
    BattleParticles.setEffectTexture(sprayEffect, 'fire')
    BattleParticles.setEffectTexture(baseFlameEffect, 'fire')
    BattleParticles.setEffectTexture(flameEffect, 'fire')
    BattleParticles.setEffectTexture(flecksEffect, 'roll-o-dex', color=Vec4(0.95, 0.95, 0.0, 1))
    sprayDelay = 1.3
    flameDelay = 3.2
    flameDuration = 2.6
    flecksDelay = flameDelay + 0.8
    flecksDuration = flameDuration - 0.8
    damageDelay = 3.6
    dodgeDelay = 2.0
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, sprayDelay, 2.3, [sprayEffect, suit, 0])
    baseFlameTrack = getPartTrack(baseFlameEffect, flameDelay, flameDuration, [baseFlameEffect, toon, 0])
    flameTrack = getPartTrack(flameEffect, flameDelay, flameDuration, [flameEffect, toon, 0])
    flecksTrack = getPartTrack(flecksEffect, flecksDelay, flecksDuration, [flecksEffect, toon, 0])
    damageAnims = [['cringe', 0.01, 0.7, 0.62],
     ['slip-forward', 0.01, 0.4, 1.2],
     ['slip-forward', 0.01, 1.0]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_hot_air.ogg', delay=1.6, node=suit)
    multiTrackList = Parallel(suitTrack, toonTrack, sprayTrack, soundTrack)
    if dmg > 0:
        colorTrack = getColorTrack(attack, toon, 'all', Vec4(0, 0, 0, 1), 4.0, 3.5)
        multiTrackList.append(baseFlameTrack)
        multiTrackList.append(flameTrack)
        multiTrackList.append(flecksTrack)
        multiTrackList.append(colorTrack)
    return multiTrackList


def doPickPocket(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target[0]['hp']
    bill = globalPropPool.getProp('1dollar')
    suitTrack = getSuitTrack(attack)
    billPosPoints = [Point3(-0.01, 0.45, -0.25), VBase3(136.424, -46.434, -129.712)]
    billPropTrack = getPropTrack(bill, suit.getRightHand(), billPosPoints, 0.6, 0.55, scaleUpPoint=Point3(1.41, 1.41, 1.41))
    toonTrack = getToonTrack(attack, 0.6, ['cringe'], 0.01, ['sidestep'])
    multiTrackList = Parallel(suitTrack, toonTrack)
    if dmg > 0:
        soundTrack = getSoundTrack('SA_pick_pocket.ogg', delay=0.2, node=suit)
        multiTrackList.append(billPropTrack)
        multiTrackList.append(soundTrack)
    return multiTrackList


def doSpeedDial(attack):
    suit = attack['suit']
    battle = attack['battle']
    phone = globalPropPool.getProp('phone')
    receiver = globalPropPool.getProp('receiver')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('PoundKey')
    BattleParticles.setEffectTexture(particleEffect, 'poundsign', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack, playRate=2)
    partTrack = Sequence(
        Wait(1.05),
        Parallel(
            ParticleInterval(particleEffect, suit, 0, duration=0.775, cleanup=True),
            ParticleInterval(particleEffect, suit, 0, duration=0.775, cleanup=True)
        )
    )
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        phonePosPoints = [Point3(-0.23, 0.01, -0.26), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(-0.13, -0.07, -0.06), VBase3(-1.854, 2.434, -177.579)]
        receiverAdjustScale = Point3(0.8, 0.8, 0.8)
        pickupDelay = 0.22
        dialDuration = 1.535
        finalPhoneDelay = 0.005
        scaleUpPoint = Point3(0.75, 0.75, 0.75)
    elif suitType == 'b':
        phonePosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverAdjustScale = MovieUtil.PNT3_ONE
        pickupDelay = 0.37
        dialDuration = 1.535
        finalPhoneDelay = 0.345
        scaleUpPoint = MovieUtil.PNT3_ONE
    else:
        phonePosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        pickupDelay = 0.37
        dialDuration = 1.57
        finalPhoneDelay = 0.31
        scaleUpPoint = MovieUtil.PNT3_ONE
    propTrack = Sequence(
        Wait(0.15),
        Func(__showProp, phone, suit.getLeftHand(), phonePosPoints[0], phonePosPoints[1]),
        Func(__showProp, receiver, suit.getLeftHand(), receiverPosPoints[0], receiverPosPoints[1]),
        LerpScaleInterval(phone, 0.25, scaleUpPoint, MovieUtil.PNT3_NEARZERO),
        Wait(pickupDelay),
        Func(receiver.wrtReparentTo, suit.getRightHand())
    )
    if suitType == 'a' or suitType == 'b':
        propTrack.append(LerpScaleInterval(receiver, 0.005, receiverAdjustScale))
        propTrack.append(LerpPosHprInterval(receiver, 0.00005, Point3(-0.53, 0.21, -0.54), VBase3(-99.49, -35.27, 1.84)))
    else:
        propTrack.append(LerpPosHprInterval(receiver, 0.00005, Point3(-0.45, 0.48, -0.62), VBase3(-87.47, -18.21, 7.82)))
    propTrack.append(Wait(dialDuration))
    propTrack.append(Func(receiver.wrtReparentTo, phone))
    propTrack.append(Wait(finalPhoneDelay))
    propTrack.append(LerpScaleInterval(phone, 0.25, MovieUtil.PNT3_NEARZERO))
    propTrack.append(Func(MovieUtil.removeProps, [receiver, phone]))
    toonTrack = getToonTrack(attack, 1.35, ['cringe'], 0.95, ['sidestep'])
    soundEffect = globalBattleSoundCache.getSound('SA_hangup.ogg')
    soundEffect.setPlayRate(2)
    soundTrack = Sequence(
        Wait(0.65),
        SoundInterval(soundEffect, node=suit)
    )
    return Parallel(suitTrack, toonTrack, propTrack, partTrack, soundTrack)


def doFilibuster(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target[0]['hp']
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect2 = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect3 = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect4 = BattleParticles.createParticleEffect(file='filibusterSpray')
    color = Vec4(0.4, 0, 0, 1)
    BattleParticles.setEffectTexture(sprayEffect, 'filibuster-cut', color=color)
    BattleParticles.setEffectTexture(sprayEffect2, 'filibuster-fiscal', color=color)
    BattleParticles.setEffectTexture(sprayEffect3, 'filibuster-impeach', color=color)
    BattleParticles.setEffectTexture(sprayEffect4, 'filibuster-inc', color=color)
    partDelay = 1.3
    partDuration = 1.15
    damageDelay = 2.45
    dodgeDelay = 1.7
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, partDelay, partDuration, [sprayEffect, suit, 0])
    sprayTrack2 = getPartTrack(sprayEffect2, partDelay + 0.8, partDuration, [sprayEffect2, suit, 0])
    sprayTrack3 = getPartTrack(sprayEffect3, partDelay + 1.6, partDuration, [sprayEffect3, suit, 0])
    sprayTrack4 = getPartTrack(sprayEffect4, partDelay + 2.4, partDuration, [sprayEffect4, suit, 0])
    damageAnims = []
    for i in range(0, 3):
        damageAnims.append(['cringe', 1e-05, 0.3, 0.8])

    damageAnims.append(['cringe', 1e-05, 0.3])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_filibuster.ogg', delay=1.1, node=suit)
    multiTrackList = Parallel(suitTrack, toonTrack, soundTrack, sprayTrack, sprayTrack2, sprayTrack3)
    if dmg > 0:
        multiTrackList.append(sprayTrack4)
    return multiTrackList


def doSchmooze(attack):
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    upperEffects = []
    lowerEffects = []
    textureNames = ['schmooze-genius',
     'schmooze-instant',
     'schmooze-master',
     'schmooze-viz']
    for i in range(0, 4):
        upperEffect = BattleParticles.createParticleEffect(file='schmoozeUpperSpray')
        lowerEffect = BattleParticles.createParticleEffect(file='schmoozeLowerSpray')
        BattleParticles.setEffectTexture(upperEffect, textureNames[i], color=Vec4(0, 0, 1, 1))
        BattleParticles.setEffectTexture(lowerEffect, textureNames[i], color=Vec4(0, 0, 1, 1))
        upperEffects.append(upperEffect)
        lowerEffects.append(lowerEffect)

    partDelay = {
        'a': 1.3,
        'b': 1.3,
        'c': 1.3
    }
    suitType = getSuitBodyType(attack['suitName'])
    damageDelay = {
        'a': 1.8,
        'b': 2.5,
        'c': partDelay[suitType] + 1.4
    }
    dodgeDelay = {
        'a': 1.1,
        'b': 1.8,
        'c': 0.9
    }
    suitTrack = getSuitTrack(attack)
    upperPartTracks = Parallel()
    lowerPartTracks = Parallel()
    for i in range(0, 4):
        upperPartTracks.append(getPartTrack(upperEffects[i], partDelay[suitType] + i * 0.65, 0.8, [upperEffects[i], suit, 0]))
        lowerPartTracks.append(getPartTrack(lowerEffects[i], partDelay[suitType] + i * 0.65 + 0.7, 1.0, [lowerEffects[i], suit, 0]))

    damageAnims = []
    for i in range(0, 3):
        damageAnims.append(['conked', 0.01, 0.3, 0.71])

    damageAnims.append(['conked', 0.01, 0.3])
    dodgeAnims = [['duck', 0.01, 0.2, 2.7],
     ['duck', 0.01, 1.22, 1.28],
     ['duck', 0.01, 3.16]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.9, showDamageExtraTime=1.1)
    return Parallel(suitTrack, toonTrack, upperPartTracks, lowerPartTracks)


def doQuake(attack):
    suitTrack = getSuitAnimTrack(attack)
    damageAnims = [['slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01], ['jump', 0.01]]
    toonTracks = getToonTracks(attack, damageDelay=1.8, splicedDamageAnims=damageAnims, dodgeDelay=1.1, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=2.8, showDamageExtraTime=1.1)
    return Parallel(suitTrack, toonTracks)


def doShake(attack):
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)
    damageAnims = [['slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01]]
    toonTracks = getToonTracks(attack, damageDelay=1.1, splicedDamageAnims=damageAnims, dodgeDelay=0.7, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=2.8, showDamageExtraTime=1.1)
    soundTrack = getSoundTrack('SA_tremor.ogg', delay=0.9, node=suit)
    return Parallel(suitTrack, soundTrack, toonTracks)


def doTremor(attack):
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)
    damageAnims = [['slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01]]
    toonTracks = getToonTracks(attack, damageDelay=1.1, splicedDamageAnims=damageAnims, dodgeDelay=0.7, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=2.8, showDamageExtraTime=1.1)
    soundTrack = getSoundTrack('SA_tremor.ogg', delay=0.9, node=suit)
    return Parallel(suitTrack, soundTrack, toonTracks)


def doHangUp(attack):
    suit = attack['suit']
    battle = attack['battle']
    phone = globalPropPool.getProp('phone')
    receiver = globalPropPool.getProp('receiver')
    suitTrack = getSuitTrack(attack) if attack['group'] == ATK_TGT_SINGLE else getSuitAnimTrack(attack, delay=1e-06)
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        phonePosPoints = [Point3(-0.23, 0.01, -0.26), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(-0.13, -0.07, -0.06), VBase3(-1.854, 2.434, -177.579)]
        receiverAdjustScale = Point3(0.8, 0.8, 0.8)
        pickupDelay = 0.44
        dialDuration = 3.07
        finalPhoneDelay = 0.01
        scaleUpPoint = Point3(0.75, 0.75, 0.75)
    elif suitType == 'b':
        phonePosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverAdjustScale = MovieUtil.PNT3_ONE
        pickupDelay = 0.74
        dialDuration = 3.07
        finalPhoneDelay = 0.69
        scaleUpPoint = MovieUtil.PNT3_ONE
    else:
        phonePosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        pickupDelay = 0.74
        dialDuration = 3.14
        finalPhoneDelay = 0.62
        scaleUpPoint = MovieUtil.PNT3_ONE
    propTrack = Sequence(
        Wait(0.3),
        Func(__showProp, phone, suit.getLeftHand(), phonePosPoints[0], phonePosPoints[1]),
        Func(__showProp, receiver, suit.getLeftHand(), receiverPosPoints[0], receiverPosPoints[1]),
        LerpScaleInterval(phone, 0.5, scaleUpPoint, MovieUtil.PNT3_NEARZERO),
        Wait(pickupDelay),
        Func(receiver.wrtReparentTo, suit.getRightHand())
    )
    if suitType == 'a' or suitType == 'b':
        propTrack.append(LerpScaleInterval(receiver, 0.01, receiverAdjustScale))
        propTrack.append(LerpPosHprInterval(receiver, 0.0001, Point3(-0.53, 0.21, -0.54), VBase3(-99.49, -35.27, 1.84)))
    else:
        propTrack.append(LerpPosHprInterval(receiver, 0.0001, Point3(-0.45, 0.48, -0.62), VBase3(-87.47, -18.21, 7.82)))
    propTrack.append(Wait(dialDuration))
    propTrack.append(Func(receiver.wrtReparentTo, phone))
    propTrack.append(Wait(finalPhoneDelay))
    propTrack.append(LerpScaleInterval(phone, 0.5, MovieUtil.PNT3_NEARZERO))
    propTrack.append(Func(MovieUtil.removeProps, [receiver, phone]))
    toonTracks = getToonTracks(attack, 5.5, ['slip-backward'], 4.7, ['jump'])
    soundTrack = getSoundTrack('SA_hangup.ogg', delay=1.3, node=suit)
    return Parallel(suitTrack, toonTracks, propTrack, soundTrack)


def doRedTape(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        tape = globalPropPool.getProp('redtape')
        tubes = []
        for i in range(0, 3):
            tubes.append(globalPropPool.getProp('redtape-tube'))

        suitTrack = getSuitTrack(attack)
        suitType = getSuitBodyType(attack['suitName'])
        if suitType == 'a':
            tapePosPoints = [Point3(-0.24, 0.09, -0.38), VBase3(-1.152, 86.581, -76.784)]
        else:
            tapePosPoints = [Point3(0.24, 0.09, -0.38), VBase3(-1.152, 86.581, -76.784)]
        tapeScaleUpPoint = Point3(0.9, 0.9, 0.24)
        propTrack = Sequence(
            getPropAppearTrack(tape, suit.getRightHand(), tapePosPoints, 0.8, tapeScaleUpPoint, scaleUpTime=0.5),
            Wait(1.73)
        )
        hitPoint = lambda toon = toon: __toonTorsoPoint(toon)
        propTrack.append(getPropThrowTrack(attack, tape, [hitPoint], [__toonGroundPoint(attack, toon, 0.7)]))
        hips = toon.getHipsParts()
        animal = toon.style.getAnimal()
        scale = ToontownGlobals.toonBodyScales[animal]
        legs = toon.style.legs
        torso = toon.style.torso
        torso = torso[0]
        animal = animal[0]
        tubeHeight = -0.8
        if torso == 's':
            scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 0.7975)
        elif torso == 'm':
            scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 0.7975)
        elif torso == 'l':
            scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 1.11)
        if animal == 'h' or animal == 'd':
            tubeHeight = -0.87
            scaleUpPoint = Point3(scale * 1.69, scale * 1.69, scale * 0.67)
        tubePosPoints = [Point3(0, 0, tubeHeight), MovieUtil.PNT3_ZERO]
        tubeTracks = Parallel()
        tubeTracks.append(Func(battle.movie.needRestoreHips))
        for partNum in range(0, hips.getNumPaths()):
            nextPart = hips.getPath(partNum)
            tubeTracks.append(getPropTrack(tubes[partNum], nextPart, tubePosPoints, 3.25, 3.17, scaleUpPoint=scaleUpPoint))

        tubeTracks.append(Func(battle.movie.clearRestoreHips))
        toonTrack = getToonTrack(attack, 3.4, ['struggle'], 2.8, ['jump'])
        soundTrack = getSoundTrack('SA_red_tape.ogg', delay=2.9, node=suit)
        multiTrackList = Parallel(suitTrack, toonTrack, propTrack, soundTrack)
        if dmg > 0:
            multiTrackList.append(tubeTracks)
        return multiTrackList
    else:
        targets = attack['target']
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        suitType = getSuitBodyType(attack['suitName'])
        if suitType == 'a':
            tapePosPoints = [Point3(-0.24, 0.09, -0.38), VBase3(-1.152, 86.581, -76.784)]
        else:
            tapePosPoints = [Point3(0.24, 0.09, -0.38), VBase3(-1.152, 86.581, -76.784)]
        tapeScaleUpPoint = Point3(0.9, 0.9, 0.24)
        propTracks = Parallel()
        tubeTracksMaster = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            tape = globalPropPool.getProp('redtape')
            tubes = []
            for i in range(0, 3):
                tubes.append(globalPropPool.getProp('redtape-tube'))
            
            propTrack = Sequence(
                getPropAppearTrack(tape, suit.getRightHand(), tapePosPoints, 0.8, tapeScaleUpPoint, scaleUpTime=0.5),
                Wait(1.73)
            )
            hitPoint = lambda toon = toon: __toonTorsoPoint(toon)
            propTrack.append(getPropThrowTrack(attack, tape, [hitPoint], [__toonGroundPoint(attack, toon, 0.7)], target=t))
            propTracks.append(propTrack)
            hips = toon.getHipsParts()
            animal = toon.style.getAnimal()
            scale = ToontownGlobals.toonBodyScales[animal]
            legs = toon.style.legs
            torso = toon.style.torso
            torso = torso[0]
            animal = animal[0]
            tubeHeight = -0.8
            if torso == 's':
                scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 0.7975)
            elif torso == 'm':
                scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 0.7975)
            elif torso == 'l':
                scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 1.11)
            if animal == 'h' or animal == 'd':
                tubeHeight = -0.87
                scaleUpPoint = Point3(scale * 1.69, scale * 1.69, scale * 0.67)
            tubePosPoints = [Point3(0, 0, tubeHeight), MovieUtil.PNT3_ZERO]
            tubeTracks = Parallel()
            tubeTracks.append(Func(battle.movie.needRestoreHips))
            for partNum in range(0, hips.getNumPaths()):
                nextPart = hips.getPath(partNum)
                tubeTracks.append(getPropTrack(tubes[partNum], nextPart, tubePosPoints, 3.25, 3.17, scaleUpPoint=scaleUpPoint))

            tubeTracks.append(Func(battle.movie.clearRestoreHips))
            if dmg > 0:
                tubeTracksMaster.append(tubeTracks)
        toonTracks = getToonTracks(attack, 3.4, ['struggle'], 2.8, ['jump'])
        soundTrack = getSoundTrack('SA_red_tape.ogg', delay=2.9, node=suit)
        return Parallel(suitTrack, toonTrack, propTracks, soundTrack, tubeTracksMaster)


def doParadigmShift(attack):
    suit = attack['suit']
    battle = attack['battle']
    targets = attack['target']
    damageDelay = 1.95
    dodgeDelay = 0.95
    sprayEffect = BattleParticles.createParticleEffect('ShiftSpray')
    sprayEffect.setPos(Point3(-5.2, 4.6, 2.7))
    suitTrack = getSuitAnimTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])
    liftTracks = Parallel()
    toonRiseTracks = Parallel()
    for t in targets:
        toon = t['toon']
        dmg = t['hp']
        if dmg > 0:
            liftEffect = BattleParticles.createParticleEffect('ShiftLift')
            liftEffect.setPos(toon.getPos(battle))
            liftEffect.setZ(liftEffect.getZ() - 1.3)
            liftTracks.append(getPartTrack(liftEffect, 1.1, 4.1, [liftEffect, battle, 0]))
            shadow = toon.dropShadow
            fakeShadow = MovieUtil.copyProp(shadow)
            x = toon.getX()
            y = toon.getY()
            z = toon.getZ()
            height = 3
            groundPoint = Point3(x, y, z)
            risePoint = Point3(x, y, z + height)
            shakeRight = Point3(x, y + 0.7, z + height)
            shakeLeft = Point3(x, y - 0.7, z + height)
            shakeTrack = Sequence(
                Wait(damageDelay + 0.25),
                Func(shadow.hide),
                Func(shadow.hide),
                LerpPosInterval(toon, 1.1, risePoint)
            )
            for i in range(0, 17):
                shakeTrack.append(LerpPosInterval(toon, 0.03, shakeLeft))
                shakeTrack.append(LerpPosInterval(toon, 0.03, shakeRight))

            shakeTrack.append(LerpPosInterval(toon, 0.1, risePoint))
            shakeTrack.append(LerpPosInterval(toon, 0.1, groundPoint))
            shakeTrack.append(Func(shadow.show))
            shadowTrack = Sequence(
                Func(battle.movie.needRestoreRenderProp, fakeShadow),
                Wait(damageDelay + 0.25),
                Func(fakeShadow.hide),
                Func(fakeShadow.setScale, 0.27),
                Func(fakeShadow.reparentTo, toon),
                Func(fakeShadow.setPos, MovieUtil.PNT3_ZERO),
                Func(fakeShadow.wrtReparentTo, battle),
                Func(fakeShadow.show),
                LerpScaleInterval(fakeShadow, 0.4, Point3(0.17, 0.17, 0.17)),
                Wait(1.81),
                LerpScaleInterval(fakeShadow, 0.1, Point3(0.27, 0.27, 0.27)),
                Func(MovieUtil.removeProp, fakeShadow),
                Func(battle.movie.clearRenderProp, fakeShadow)
            )
            toonRiseTracks.append(Parallel(shakeTrack, shadowTrack))

    damageAnims = []
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.9, startTime=2.06))
    damageAnims.append(['slip-backward', 0.01, 0.5])
    dodgeAnims = [['jump', 0.01, 0, 0.6]]
    dodgeAnims.extend(getSplicedLerpAnims('jump', 0.31, 1.0, startTime=0.6))
    dodgeAnims.append(['jump', 0, 0.91])
    toonTracks = getToonTracks(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, splicedDodgeAnims=dodgeAnims, showDamageExtraTime=2.7)
    if hitAtleastOneToon(targets):
        soundTrack = getSoundTrack('SA_paradigm_shift.ogg', delay=2.1, node=suit)
        return Parallel(suitTrack, sprayTrack, soundTrack, liftTracks, toonTracks, toonRiseTracks)
    else:
        return Parallel(suitTrack, sprayTrack, liftTracks, toonTracks, toonRiseTracks)


def doPowerTrip(attack):
    suit = attack['suit']
    battle = attack['battle']
    centerColor = Vec4(0.1, 0.1, 0.1, 0.4)
    edgeColor = Vec4(0.4, 0.1, 0.9, 0.7)
    powerBar1 = BattleParticles.createParticleEffect(file='powertrip')
    powerBar2 = BattleParticles.createParticleEffect(file='powertrip2')
    powerBar1.setPos(0, 6.1, 0.4)
    powerBar1.setHpr(-60, 0, 0)
    powerBar2.setPos(0, 6.1, 0.4)
    powerBar2.setHpr(60, 0, 0)
    powerBar1Particles = powerBar1.getParticlesNamed('particles-1')
    powerBar2Particles = powerBar2.getParticlesNamed('particles-1')
    powerBar1Particles.renderer.setCenterColor(centerColor)
    powerBar1Particles.renderer.setEdgeColor(edgeColor)
    powerBar2Particles.renderer.setCenterColor(centerColor)
    powerBar2Particles.renderer.setEdgeColor(edgeColor)
    waterfallEffect = BattleParticles.createParticleEffect('Waterfall')
    waterfallEffect.setScale(11)
    waterfallParticles = waterfallEffect.getParticlesNamed('particles-1')
    waterfallParticles.renderer.setCenterColor(centerColor)
    waterfallParticles.renderer.setEdgeColor(edgeColor)
    suitName = attack['suitName']
    if suitName == 'tbc' or suitName == 'mh' or suitName == 'rb' or suitName == 'mh':
        waterfallEffect.setPos(0, 4, 3.6)
    suitTrack = getSuitAnimTrack(attack)

    def getPowerTrack(effect, suit=suit, battle=battle):
        partTrack = Sequence(
            Wait(1.0),
            Func(battle.movie.needRestoreParticleEffect, effect),
            Func(effect.start, suit),
            Wait(0.4),
            LerpPosInterval(effect, 1.0, Point3(0, 15, 0.4)),
            LerpFunctionInterval(effect.setAlphaScale, fromData=1, toData=0, duration=0.4),
            Func(effect.cleanup), Func(battle.movie.clearRestoreParticleEffect, effect)
        )
        return partTrack

    partTrack1 = getPowerTrack(powerBar1)
    partTrack2 = getPowerTrack(powerBar2)
    waterfallTrack = getPartTrack(waterfallEffect, 0.6, 1.3, [waterfallEffect, suit, 0])
    toonTracks = getToonTracks(attack, 1.8, ['slip-forward'], 1.29, ['jump'])
    return Parallel(suitTrack, partTrack1, partTrack2, waterfallTrack, toonTracks)


def doSandTrap(attack):
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        damageDelay = 1.3
        dodgeDelay = 0.25
        suitTrack = getSuitTrack(attack)
        damageAnims = [['melt'], ['jump', 1.5, 0.4]]
        toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
        puddle = globalPropPool.getProp('quicksand')
        puddle.setHpr(Point3(120, 0, 0))
        puddle.setScale(0.01)
        puddleTrack = Sequence(
            Func(battle.movie.needRestoreRenderProp, puddle),
            Wait(damageDelay - 0.7),
            Func(puddle.reparentTo, battle),
            Func(puddle.setPos, toon.getPos(battle)),
            LerpScaleInterval(puddle, 1.7, Point3(1.7, 1.7, 1.7), startScale=MovieUtil.PNT3_NEARZERO)
        )
        if dmg > 0:
            puddleTrack.append(Wait(3.2))
        else:
            puddleTrack.append(Wait(0.3))
        puddleTrack.append(LerpFunctionInterval(puddle.setAlphaScale, fromData=1, toData=0, duration=0.8))
        puddleTrack.append(Func(MovieUtil.removeProp, puddle))
        puddleTrack.append(Func(battle.movie.clearRenderProp, puddle))
        if dmg > 0:
            soundTrack = getSoundTrack('TL_quicksand.ogg', delay=0.5, node=toon)
        else:
            soundTrack = getSoundTrack('TL_quicksand.ogg', delay=0.5, duration=0.67, node=toon)
        return Parallel(suitTrack, toonTrack, puddleTrack, soundTrack)
    else:
        targets = attack['target']
        damageDelay = 1.3
        dodgeDelay = 0.25
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        damageAnims = [['melt'], ['jump', 1.5, 0.4]]
        toonTracks = getToonTracks(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
        puddleTracks = Parallel()
        soundTracks = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            puddle = globalPropPool.getProp('quicksand')
            puddle.setHpr(Point3(120, 0, 0))
            puddle.setScale(0.01)
            puddleTrack = Sequence(
                Func(battle.movie.needRestoreRenderProp, puddle),
                Wait(damageDelay - 0.7),
                Func(puddle.reparentTo, battle),
                Func(puddle.setPos, toon.getPos(battle)),
                LerpScaleInterval(puddle, 1.7, Point3(1.7, 1.7, 1.7), startScale=MovieUtil.PNT3_NEARZERO)
            )
            if dmg > 0:
                puddleTrack.append(Wait(3.2))
            else:
                puddleTrack.append(Wait(0.3))
            puddleTrack.append(LerpFunctionInterval(puddle.setAlphaScale, fromData=1, toData=0, duration=0.8))
            puddleTrack.append(Func(MovieUtil.removeProp, puddle))
            puddleTrack.append(Func(battle.movie.clearRenderProp, puddle))
            if dmg > 0:
                soundTracks.append(getSoundTrack('TL_quicksand.ogg', delay=0.5, node=toon))
            else:
                soundTracks.append(getSoundTrack('TL_quicksand.ogg', delay=0.5, duration=0.67, node=toon))
        return Parallel(suitTrack, toonTracks, puddleTracks, soundTracks)


def doSongAndDance(attack):
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)
    toonTracks = getToonTracks(attack, 3.9, ['cringe'], 3.9, ['applause'])
    soundTrack = getSoundTrack('AA_heal_happydance.ogg', node=suit)
    return Parallel(suitTrack, toonTracks, soundTrack)


def doStomper(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        if suit.getStyleDept() == 'l':
            stomper = loader.loadModel('phase_11/models/lawbotHQ/LB_square_stomper')
        else:
            stomper = loader.loadModel('phase_9/models/cogHQ/square_stomper')
        shaft = stomper.find('**/shaft')
        shaft.setScale(0.75, 15.0, 0.75)
        suitTrack = getSuitTrack(attack)
        stomperPrepare = SoundInterval(base.loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_switch_depressed.ogg'), node=stomper)
        stomperPrepareTime = stomperPrepare.getDuration()
        stomperLift = SoundInterval(base.loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_stomper_raise.ogg'), node=stomper)
        stomperLiftTime = stomperLift.getDuration()
        smoke = loader.loadModel('phase_4/models/props/test_clouds')
        smoke.reparentTo(toon)
        smoke.setScale(0.5)
        smoke.setColor(0.8, 0.7, 0.5, 1)
        smoke.hide()
        smoke.setBillboardPointEye()
        stomperTrack = Sequence(
            Parallel(
                getPropAppearTrack(stomper, battle, [Point3(toon.getPos(battle).getX(), toon.getPos(battle).getY(), toon.getPos(battle).getZ() + 15), VBase3(0, 270, 0)], 0.0, Point3(1.5, 1, 1.5), stomperPrepareTime),
                stomperPrepare
            ),
            LerpPosInterval(stomper, 0.25, Point3(toon.getPos(battle).getX(), toon.getPos(battle).getY(), toon.getPos(battle).getZ())),
            Parallel(
                SoundInterval(globalBattleSoundCache.getSound('CHQ_FACT_stomper_small.ogg'), node=stomper),
                Sequence(
                    Wait(1.0),
                    Parallel(
                        stomperLift,
                        LerpPosInterval(stomper, stomperLiftTime, Point3(toon.getPos(battle).getX(), toon.getPos(battle).getY(), toon.getPos(battle).getZ() + 15))
                    ),
                    LerpScaleInterval(stomper, 1.5, Point3(0.0, 0.0, 0.0))
                ),
                Sequence(
                    Func(smoke.show),
                    Parallel(
                        LerpScaleInterval(smoke, 0.5, 1),
                        LerpColorScaleInterval(smoke, 0.5, Vec4(0.8, 0.7, 0.5, 0))
                    ),
                    Func(smoke.hide)
                )
            ),
            Func(MovieUtil.removeProp, stomper)
        )
        if dmg > 0:
            toonTrack = Sequence(
                Func(toon.headsUp, battle, suit.getPos(battle)),
                Wait(stomperPrepareTime + 0.25),
                Parallel(
                    Func(toon.enterFlattened),
                    Func(toon.showHpText, -dmg, openEnded=0),
                    Func(__doDamage, toon, dmg, target[0]['died'])
                ),
                Wait(2.5),
                Parallel(
                    Sequence(
                        Wait(0.5),
                        Func(toon.exitFlattened)
                    ),
                    SoundInterval(base.loader.loadSfx('phase_9/audio/sfx/toon_decompress.ogg'), node=toon),
                    Sequence(
                        ActorInterval(toon, 'jump'),
                        Func(toon.loop, 'neutral')
                    )
                )
            )
            if target[0]['died']:
                toonTrack.append(Wait(5.0))
        else:
            toonTrack = Sequence(
                Func(toon.headsUp, battle, suit.getPos(battle)),
                getToonDodgeTrack(target[0], 0.9, ['sidestep'], None, 0.5)
            )
        return Parallel(suitTrack, stomperTrack, toonTrack)
    else:
        targets = attack['target']
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        stomperTracks = Parallel()
        toonTracks = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            if suit.getStyleDept() == 'l':
                stomper = loader.loadModel('phase_11/models/lawbotHQ/LB_square_stomper')
            else:
                stomper = loader.loadModel('phase_9/models/cogHQ/square_stomper')
            shaft = stomper.find('**/shaft')
            shaft.setScale(0.75, 15.0, 0.75)
            stomperPrepare = SoundInterval(base.loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_switch_depressed.ogg'), node=stomper)
            stomperPrepareTime = stomperPrepare.getDuration()
            stomperLift = SoundInterval(base.loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_stomper_raise.ogg'), node=stomper)
            stomperLiftTime = stomperLift.getDuration()
            smoke = loader.loadModel('phase_4/models/props/test_clouds')
            smoke.reparentTo(toon)
            smoke.setScale(0.5)
            smoke.setColor(0.8, 0.7, 0.5, 1)
            smoke.hide()
            smoke.setBillboardPointEye()
            stomperTrack = Sequence(
                Parallel(
                    getPropAppearTrack(stomper, battle, [Point3(toon.getPos(battle).getX(), toon.getPos(battle).getY(), toon.getPos(battle).getZ() + 15), VBase3(0, 270, 0)], 0.0, Point3(1.5, 1, 1.5), stomperPrepareTime),
                    stomperPrepare
                ),
                LerpPosInterval(stomper, 0.25, Point3(toon.getPos(battle).getX(), toon.getPos(battle).getY(), toon.getPos(battle).getZ())),
                Parallel(
                    SoundInterval(globalBattleSoundCache.getSound('CHQ_FACT_stomper_small.ogg'), node=stomper),
                    Sequence(
                        Wait(1.0),
                        Parallel(
                            stomperLift,
                            LerpPosInterval(stomper, stomperLiftTime, Point3(toon.getPos(battle).getX(), toon.getPos(battle).getY(), toon.getPos(battle).getZ() + 15))
                        ),
                        LerpScaleInterval(stomper, 1.5, Point3(0.0, 0.0, 0.0))
                    ),
                    Sequence(
                        Func(smoke.show),
                        Parallel(
                            LerpScaleInterval(smoke, 0.5, 1),
                            LerpColorScaleInterval(smoke, 0.5, Vec4(0.8, 0.7, 0.5, 0))
                        ),
                        Func(smoke.hide)
                    )
                ),
                Func(MovieUtil.removeProp, stomper)
            )
            stomperTracks.append(stomperTrack)
            if dmg > 0:
                toonTrack = Sequence(
                    Func(toon.headsUp, battle, suit.getPos(battle)),
                    Wait(stomperPrepareTime + 0.25),
                    Parallel(
                        Func(toon.enterFlattened),
                        Func(toon.showHpText, -dmg, openEnded=0),
                        Func(__doDamage, toon, dmg, t['died'])
                    ),
                    Wait(2.5),
                    Parallel(
                        Sequence(
                            Wait(0.5),
                            Func(toon.exitFlattened)
                        ),
                        SoundInterval(base.loader.loadSfx('phase_9/audio/sfx/toon_decompress.ogg'), node=toon),
                        Sequence(
                            ActorInterval(toon, 'jump'),
                            Func(toon.loop, 'neutral')
                        )
                    )
                )
                if t['died']:
                    toonTrack.append(Wait(5.0))
            else:
                toonTrack = Sequence(
                    Func(toon.headsUp, battle, suit.getPos(battle)),
                    getToonDodgeTrack(t, 0.9, ['sidestep'], None, 0.5)
                )
            toonTracks.append(toonTrack)
        return Parallel(suitTrack, stomperTracks, toonTracks)


def getThrowEndPoint(suit, toon, battle, whichBounce):
    pnt = toon.getPos(toon)
    if whichBounce == 'one':
        pnt.setY(pnt[1] + 8)
    elif whichBounce == 'two':
        pnt.setY(pnt[1] + 5)
    elif whichBounce == 'threeHit':
        pnt.setZ(pnt[2] + toon.shoulderHeight + 0.3)
    elif whichBounce == 'threeMiss':
        pass
    elif whichBounce == 'four':
        pnt.setY(pnt[1] - 5)
    return Point3(pnt)


def doBounceCheck(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        check = globalPropPool.getProp('bounced-check')
        checkPosPoints = [MovieUtil.PNT3_ZERO, VBase3(95.247, 79.025, 88.849)]
        bounce1Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'one')
        bounce2Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'two')
        hit3Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'threeHit')
        miss3Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'threeMiss')
        bounce4Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'four')
        throwDelay = {
            'a': 2.5,
            'b': 2.5,
            'c': 1.8
        }
        dodgeDelay = {
            'a': 4.3,
            'b': 4.3,
            'c': 3.6
        }
        damageDelay = {
            'a': 5.1,
            'b': 5.1,
            'c': 4.4
        }
        suitTrack = getSuitTrack(attack)
        checkPropTrack = Sequence(getPropAppearTrack(check, suit.getRightHand(), checkPosPoints, 1e-05, Point3(8.5, 8.5, 8.5), startScale=MovieUtil.PNT3_ONE))
        suitType = getSuitBodyType(attack['suitName'])
        checkPropTrack.append(Wait(throwDelay[suitType]))
        checkPropTrack.append(Func(check.wrtReparentTo, toon))
        checkPropTrack.append(Func(check.setHpr, Point3(0, -90, 0)))
        checkPropTrack.append(getThrowTrack(check, bounce1Point, duration=0.5, parent=toon))
        checkPropTrack.append(getThrowTrack(check, bounce2Point, duration=0.9, parent=toon))
        if dmg > 0:
            checkPropTrack.append(getThrowTrack(check, hit3Point, duration=0.7, parent=toon))
        else:
            checkPropTrack.append(getThrowTrack(check, miss3Point, duration=0.7, parent=toon))
            checkPropTrack.append(getThrowTrack(check, bounce4Point, duration=0.7, parent=toon))
            checkPropTrack.append(LerpScaleInterval(check, 0.3, MovieUtil.PNT3_NEARZERO))
        checkPropTrack.append(Func(MovieUtil.removeProp, check))
        toonTrack = getToonTrack(attack, damageDelay[suitType], ['conked'], dodgeDelay[suitType], ['sidestep'])
        soundTracks = Sequence(
            getSoundTrack('SA_pink_slip.ogg', delay=throwDelay[suitType] + 0.5, duration=0.6, node=suit),
            getSoundTrack('SA_pink_slip.ogg', delay=0.4, duration=0.6, node=suit)
        )
        return Parallel(suitTrack, checkPropTrack, toonTrack, soundTracks)
    else:
        targets = attack['target']
        checkPosPoints = [MovieUtil.PNT3_ZERO, VBase3(95.247, 79.025, 88.849)]
        throwDelay = {
            'a': 2.5,
            'b': 2.5,
            'c': 1.8
        }
        dodgeDelay = {
            'a': 4.3,
            'b': 4.3,
            'c': 3.6
        }
        damageDelay = {
            'a': 5.1,
            'b': 5.1,
            'c': 4.4
        }
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        checkPropTracks = Parallel()
        suitType = getSuitBodyType(attack['suitName'])
        toonTracks = getToonTracks(attack, damageDelay[suitType], ['conked'], dodgeDelay[suitType], ['sidestep'])
        soundTracks = Sequence(
            getSoundTrack('SA_pink_slip.ogg', delay=throwDelay[suitType] + 0.5, duration=0.6, node=suit),
            getSoundTrack('SA_pink_slip.ogg', delay=0.4, duration=0.6, node=suit)
        )
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            check = globalPropPool.getProp('bounced-check')
            bounce1Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'one')
            bounce2Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'two')
            hit3Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'threeHit')
            miss3Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'threeMiss')
            bounce4Point = lambda suit = suit, toon = toon, battle = battle: getThrowEndPoint(suit, toon, battle, 'four')
            checkPropTrack = Sequence(
                getPropAppearTrack(check, suit.getRightHand(), checkPosPoints, 1e-05, Point3(8.5, 8.5, 8.5), startScale=MovieUtil.PNT3_ONE),
                Wait(throwDelay[suitType]),
                Func(check.wrtReparentTo, toon),
                Func(check.setHpr, Point3(0, -90, 0)),
                getThrowTrack(check, bounce1Point, duration=0.5, parent=toon),
                getThrowTrack(check, bounce2Point, duration=0.9, parent=toon)
            )
            if dmg > 0:
                checkPropTrack.append(getThrowTrack(check, hit3Point, duration=0.7, parent=toon))
            else:
                checkPropTrack.append(getThrowTrack(check, miss3Point, duration=0.7, parent=toon))
                checkPropTrack.append(getThrowTrack(check, bounce4Point, duration=0.7, parent=toon))
                checkPropTrack.append(LerpScaleInterval(check, 0.3, MovieUtil.PNT3_NEARZERO))
            checkPropTrack.append(Func(MovieUtil.removeProp, check))
            checkPropTracks.append(checkPropTrack)
        return Parallel(suitTrack, checkPropTracks, toonTracks, soundTracks)


def doWatercooler(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        watercooler = globalPropPool.getProp('watercooler')

        def getCoolerSpout(watercooler=watercooler):
            spout = watercooler.find('**/joint_toSpray')
            return spout.getPos(render)

        hitPoint = lambda toon = toon: __toonFacePoint(toon)
        missPoint = lambda prop = watercooler, toon = toon: __toonMissPoint(prop, toon, 0, parent=render)
        hitSprayTrack = MovieUtil.getSprayTrack(battle, Point4(0.75, 0.75, 1.0, 0.8), getCoolerSpout, hitPoint, 0.2, 0.2, 0.2, horizScale=0.3, vertScale=0.3)
        missSprayTrack = MovieUtil.getSprayTrack(battle, Point4(0.75, 0.75, 1.0, 0.8), getCoolerSpout, missPoint, 0.2, 0.2, 0.2, horizScale=0.3, vertScale=0.3)
        suitTrack = getSuitTrack(attack)
        posPoints = [Point3(0.48, 0.11, -0.92), VBase3(20.403, 33.158, 69.511)]
        propTrack = Sequence(
            Wait(1.01),
            Func(__showProp, watercooler, suit.getLeftHand(), posPoints[0], posPoints[1]),
            LerpScaleInterval(watercooler, 0.5, Point3(1.15, 1.15, 1.15)),
            Wait(1.6)
        )
        if dmg > 0:
            propTrack.append(hitSprayTrack)
        else:
            propTrack.append(missSprayTrack)
        propTrack.append(Wait(0.01))
        propTrack.append(LerpScaleInterval(watercooler, 0.5, MovieUtil.PNT3_NEARZERO))
        propTrack.append(Func(MovieUtil.removeProp, watercooler))
        splashTrack = Sequence()
        if dmg > 0:

            def prepSplash(splash, targetPoint):
                splash.reparentTo(render)
                splash.setPos(targetPoint)
                scale = splash.getScale()
                splash.setBillboardPointWorld()
                splash.setScale(scale)

            splash = globalPropPool.getProp('splash-from-splat')
            splash.setColor(0.75, 0.75, 1, 0.8)
            splash.setScale(0.3)
            splashTrack = Sequence(
                Func(battle.movie.needRestoreRenderProp, splash),
                Wait(3.2),
                Func(prepSplash, splash, __toonFacePoint(toon)),
                ActorInterval(splash, 'splash-from-splat'),
                Func(MovieUtil.removeProp, splash),
                Func(battle.movie.clearRenderProp, splash)
            )
        toonTrack = getToonTrack(attack, suitTrack.getDuration() - 1.5, ['cringe'], 2.4, ['sidestep'])
        soundTrack = Sequence(
            Wait(1.1),
            SoundInterval(globalBattleSoundCache.getSound('SA_watercooler_appear_only.ogg'), node=suit, duration=1.4722),
            Wait(0.4),
            SoundInterval(globalBattleSoundCache.getSound('SA_watercooler_spray_only.ogg'), node=suit, duration=2.313)
        )
        return Parallel(suitTrack, toonTrack, propTrack, soundTrack, splashTrack)
    else:
        targets = attack['target']
        watercooler = globalPropPool.getProp('watercooler')

        def getCoolerSpout(watercooler=watercooler):
            spout = watercooler.find('**/joint_toSpray')
            return spout.getPos(render)
        
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        posPoints = [Point3(0.48, 0.11, -0.92), VBase3(20.403, 33.158, 69.511)]
        propTrack = Sequence(
            Wait(1.01),
            Func(__showProp, watercooler, suit.getLeftHand(), posPoints[0], posPoints[1]),
            LerpScaleInterval(watercooler, 0.5, Point3(1.15, 1.15, 1.15)),
            Wait(1.6)
        )
        sprayTracks = Parallel()
        splashTracks = Parallel()
        toonTracks = getToonTracks(attack, suitTrack.getDuration() - 1.5, ['cringe'], 2.4, ['sidestep'])
        soundTrack = Sequence(
            Wait(1.1),
            SoundInterval(globalBattleSoundCache.getSound('SA_watercooler_appear_only.ogg'), node=suit, duration=1.4722),
            Wait(0.4),
            SoundInterval(globalBattleSoundCache.getSound('SA_watercooler_spray_only.ogg'), node=suit, duration=2.313)
        )
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            hitPoint = lambda toon = toon: __toonFacePoint(toon)
            missPoint = lambda prop = watercooler, toon = toon: __toonMissPoint(prop, toon, 0, parent=render)
            hitSprayTrack = MovieUtil.getSprayTrack(battle, Point4(0.75, 0.75, 1.0, 0.8), getCoolerSpout, hitPoint, 0.2, 0.2, 0.2, horizScale=0.3, vertScale=0.3)
            missSprayTrack = MovieUtil.getSprayTrack(battle, Point4(0.75, 0.75, 1.0, 0.8), getCoolerSpout, missPoint, 0.2, 0.2, 0.2, horizScale=0.3, vertScale=0.3)
            if dmg > 0:
                sprayTracks.append(hitSprayTrack)
            else:
                sprayTracks.append(missSprayTrack)
            splashTrack = Sequence()
            if dmg > 0:

                def prepSplash(splash, targetPoint):
                    splash.reparentTo(render)
                    splash.setPos(targetPoint)
                    scale = splash.getScale()
                    splash.setBillboardPointWorld()
                    splash.setScale(scale)

                splash = globalPropPool.getProp('splash-from-splat')
                splash.setColor(0.75, 0.75, 1, 0.8)
                splash.setScale(0.3)
                splashTrack = Sequence(
                    Func(battle.movie.needRestoreRenderProp, splash),
                    Wait(3.2),
                    Func(prepSplash, splash, __toonFacePoint(toon)),
                    ActorInterval(splash, 'splash-from-splat'),
                    Func(MovieUtil.removeProp, splash),
                    Func(battle.movie.clearRenderProp, splash)
                )
            splashTracks.append(splashTrack)
        propTrack.append(sprayTracks)
        propTrack.append(Wait(0.01))
        propTrack.append(LerpScaleInterval(watercooler, 0.5, MovieUtil.PNT3_NEARZERO))
        propTrack.append(Func(MovieUtil.removeProp, watercooler))
        return Parallel(suitTrack, toonTracks, propTrack, soundTrack, splashTracks)


def doPennyPinch(attack):
    suitTrack = getSuitTrack(attack)
    toonTrack = getToonTrack(attack, 0.6, ['cringe'], 0.01, ['sidestep'])
    return Parallel(suitTrack, toonTrack)


def doFired(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        BattleParticles.loadParticles()
        baseFlameEffect = BattleParticles.createParticleEffect(file='firedBaseFlame')
        flameEffect = BattleParticles.createParticleEffect('FiredFlame')
        flecksEffect = BattleParticles.createParticleEffect('SpriteFiredFlecks')
        BattleParticles.setEffectTexture(baseFlameEffect, 'fire')
        BattleParticles.setEffectTexture(flameEffect, 'fire')
        BattleParticles.setEffectTexture(flecksEffect, 'roll-o-dex', color=Vec4(0.8, 0.8, 0.8, 1))
        baseFlameSmall = BattleParticles.createParticleEffect(file='firedBaseFlame')
        flameSmall = BattleParticles.createParticleEffect('FiredFlame')
        flecksSmall = BattleParticles.createParticleEffect('SpriteFiredFlecks')
        BattleParticles.setEffectTexture(baseFlameSmall, 'fire')
        BattleParticles.setEffectTexture(flameSmall, 'fire')
        BattleParticles.setEffectTexture(flecksSmall, 'roll-o-dex', color=Vec4(0.8, 0.8, 0.8, 1))
        baseFlameSmall.setScale(0.7)
        flameSmall.setScale(0.7)
        flecksSmall.setScale(0.7)
        suitTrack = getSuitTrack(attack)
        baseFlameTrack = getPartTrack(baseFlameEffect, 1.0, 1.9, [baseFlameEffect, toon, 0])
        flameTrack = getPartTrack(flameEffect, 1.0, 1.9, [flameEffect, toon, 0])
        flecksTrack = getPartTrack(flecksEffect, 1.8, 1.1, [flecksEffect, toon, 0])
        baseFlameSmallTrack = getPartTrack(baseFlameSmall, 1.0, 1.9, [baseFlameSmall, toon, 0])
        flameSmallTrack = getPartTrack(flameSmall, 1.0, 1.9, [flameSmall, toon, 0])
        flecksSmallTrack = getPartTrack(flecksSmall, 1.8, 1.1, [flecksSmall, toon, 0])
        damageAnims = [['cringe', 0.01, 0.7, 0.62],
         ['slip-forward', 1e-05, 0.4, 1.2]]
        damageAnims.extend(getSplicedLerpAnims('slip-forward', 0.31, 0.8, startTime=1.2))
        toonTrack = getToonTrack(attack, damageDelay=1.5, splicedDamageAnims=damageAnims, dodgeDelay=0.3, dodgeAnimNames=['sidestep'])
        soundTrack = getSoundTrack('SA_hot_air.ogg', delay=1.0, node=suit)
        if dmg > 0:
            colorTrack = getColorTrack(attack, toon, 'all', Vec4(0, 0, 0, 1), 2.0, 3.5)
            return Parallel(suitTrack, baseFlameTrack, flameTrack, flecksTrack, toonTrack, colorTrack, soundTrack)
        else:
            return Parallel(suitTrack, baseFlameSmallTrack, flameSmallTrack, flecksSmallTrack, toonTrack, soundTrack)
    else:
        targets = attack['target']
        BattleParticles.loadParticles()
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        damageAnims = [['cringe', 0.01, 0.7, 0.62],
         ['slip-forward', 1e-05, 0.4, 1.2]]
        baseFlameTracks = Parallel()
        flameTracks = Parallel()
        flecksTracks = Parallel()
        damageAnims.extend(getSplicedLerpAnims('slip-forward', 0.31, 0.8, startTime=1.2))
        toonTracks = getToonTracks(attack, damageDelay=1.5, splicedDamageAnims=damageAnims, dodgeDelay=0.3, dodgeAnimNames=['sidestep'])
        colorTracks = Parallel()
        soundTrack = getSoundTrack('SA_hot_air.ogg', delay=1.0, node=suit)
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            baseFlameEffect = BattleParticles.createParticleEffect(file='firedBaseFlame')
            flameEffect = BattleParticles.createParticleEffect('FiredFlame')
            flecksEffect = BattleParticles.createParticleEffect('SpriteFiredFlecks')
            BattleParticles.setEffectTexture(baseFlameEffect, 'fire')
            BattleParticles.setEffectTexture(flameEffect, 'fire')
            BattleParticles.setEffectTexture(flecksEffect, 'roll-o-dex', color=Vec4(0.8, 0.8, 0.8, 1))
            baseFlameSmall = BattleParticles.createParticleEffect(file='firedBaseFlame')
            flameSmall = BattleParticles.createParticleEffect('FiredFlame')
            flecksSmall = BattleParticles.createParticleEffect('SpriteFiredFlecks')
            BattleParticles.setEffectTexture(baseFlameSmall, 'fire')
            BattleParticles.setEffectTexture(flameSmall, 'fire')
            BattleParticles.setEffectTexture(flecksSmall, 'roll-o-dex', color=Vec4(0.8, 0.8, 0.8, 1))
            baseFlameSmall.setScale(0.7)
            flameSmall.setScale(0.7)
            flecksSmall.setScale(0.7)
            baseFlameTrack = getPartTrack(baseFlameEffect, 1.0, 1.9, [baseFlameEffect, toon, 0])
            flameTrack = getPartTrack(flameEffect, 1.0, 1.9, [flameEffect, toon, 0])
            flecksTrack = getPartTrack(flecksEffect, 1.8, 1.1, [flecksEffect, toon, 0])
            baseFlameSmallTrack = getPartTrack(baseFlameSmall, 1.0, 1.9, [baseFlameSmall, toon, 0])
            flameSmallTrack = getPartTrack(flameSmall, 1.0, 1.9, [flameSmall, toon, 0])
            flecksSmallTrack = getPartTrack(flecksSmall, 1.8, 1.1, [flecksSmall, toon, 0])
            if dmg > 0:
                colorTrack = getColorTrack(attack, toon, 'all', Vec4(0, 0, 0, 1), 2.0, 3.5)
                colorTracks.append(colorTrack)
                baseFlameTracks.append(baseFlameTrack)
                flameTracks.append(flameTrack)
                flecksTracks.append(flecksTrack)
            else:
                baseFlameTracks.append(baseFlameSmallTrack)
                flameTracks.append(flameSmallTrack)
                flecksTracks.append(flecksSmallTrack)
        return Parallel(suitTrack, baseFlameTracks, flameTracks, flecksTracks, toonTracks, colorTracks, soundTrack)


def doAudit(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-one', color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-two', color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-three', color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-four', color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-mult', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        calcPosPoints = [Point3(-0.15, 0.37, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [Point3(0.35, 0.52, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)
    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 1e-06, calcDuration, scaleUpPoint=scaleUpPoint, anim=1, propName='calculator', animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 0.9, ['duck'], showMissedExtraTime=2.2)
    soundTrack = getSoundTrack('SA_audit.ogg', delay=1.9, node=suit)
    return Parallel(suitTrack, toonTrack, calcPropTrack, soundTrack, partTrack, partTrack2, partTrack3, partTrack4, partTrack5)


def doCalculate(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-one', color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-plus', color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-mult', color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-three', color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-div', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        calcPosPoints = [Point3(-0.15, 0.37, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [Point3(0.35, 0.52, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)
    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 1e-06, calcDuration, scaleUpPoint=scaleUpPoint, anim=1, propName='calculator', animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 1.8, ['sidestep'])
    soundTrack = getSoundTrack('SA_audit.ogg', delay=1.9, node=suit)
    return Parallel(suitTrack, toonTrack, calcPropTrack, soundTrack, partTrack, partTrack2, partTrack3, partTrack4, partTrack5)


def doTabulate(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-plus', color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-minus', color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-mult', color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-div', color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-one', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        calcPosPoints = [Point3(-0.15, 0.37, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [Point3(0.35, 0.52, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)
    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 1e-06, calcDuration, scaleUpPoint=scaleUpPoint, anim=1, propName='calculator', animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 1.8, ['sidestep'])
    soundTrack = getSoundTrack('SA_audit.ogg', delay=1.9, node=suit)
    return Parallel(suitTrack, toonTrack, calcPropTrack, soundTrack, partTrack, partTrack2, partTrack3, partTrack4, partTrack5)


def doCrunch(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    throwDuration = 3.03
    suitTrack = getSuitTrack(attack)
    numberNames = ['one',
     'two',
     'three',
     'four',
     'five',
     'six']
    BattleParticles.loadParticles()
    numberSpill1 = BattleParticles.createParticleEffect(file='numberSpill')
    numberSpill2 = BattleParticles.createParticleEffect(file='numberSpill')
    spillTexture1 = random.choice(numberNames)
    spillTexture2 = random.choice(numberNames)
    BattleParticles.setEffectTexture(numberSpill1, 'audit-' + spillTexture1)
    BattleParticles.setEffectTexture(numberSpill2, 'audit-' + spillTexture2)
    numberSpillTrack1 = getPartTrack(numberSpill1, 1.1, 2.2, [numberSpill1, suit, 0])
    numberSpillTrack2 = getPartTrack(numberSpill2, 1.5, 1.0, [numberSpill2, suit, 0])
    numberSprayTracks = Parallel()
    numOfNumbers = random.randint(5, 9)
    for i in range(0, numOfNumbers - 1):
        nextSpray = BattleParticles.createParticleEffect(file='numberSpray')
        nextTexture = random.choice(numberNames)
        BattleParticles.setEffectTexture(nextSpray, 'audit-' + nextTexture)
        nextStartTime = random.random() * 0.6 + throwDuration
        nextDuration = random.random() * 0.4 + 1.4
        nextSprayTrack = getPartTrack(nextSpray, nextStartTime, nextDuration, [nextSpray, suit, 0])
        numberSprayTracks.append(nextSprayTrack)

    numberTracks = Parallel()
    for i in range(0, numOfNumbers):
        texture = random.choice(numberNames)
        next = MovieUtil.copyProp(BattleParticles.getParticle('audit-' + texture))
        next.reparentTo(suit.getRightHand())
        next.setScale(0.01, 0.01, 0.01)
        next.setColor(Vec4(0.0, 0.0, 0.0, 1.0))
        next.setPos(random.random() * 0.6 - 0.3, random.random() * 0.6 - 0.3, random.random() * 0.6 - 0.3)
        next.setHpr(VBase3(-1.15, 86.58, -76.78))
        numberTrack = Sequence(
            Wait(0.9),
            LerpScaleInterval(next, 0.6, MovieUtil.PNT3_ONE),
            Wait(1.7),
            Func(MovieUtil.removeProp, next)
        )
        numberTracks.append(numberTrack)

    damageAnims = [['cringe', 0.01, 0.14, 0.28],
     ['cringe', 0.01, 0.16, 0.3],
     ['cringe', 0.01, 0.13, 0.22],
     ['slip-forward', 0.01, 0.6]]
    toonTrack = getToonTrack(attack, damageDelay=4.7, splicedDamageAnims=damageAnims, dodgeDelay=3.6, dodgeAnimNames=['sidestep'])
    return Parallel(suitTrack, toonTrack, numberSpillTrack1, numberSpillTrack2, numberTracks, numberSprayTracks)


def doLiquidate(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        BattleParticles.loadParticles()
        rainEffect = BattleParticles.createParticleEffect(file='liquidate')
        rainEffect2 = BattleParticles.createParticleEffect(file='liquidate')
        rainEffect3 = BattleParticles.createParticleEffect(file='liquidate')
        cloud = globalPropPool.getProp('stormcloud')
        partDelay = {
            'a': 0.2,
            'b': 0.2,
            'c': 0.2
        }
        damageDelay = {
            'a': 3.5,
            'b': 3.5,
            'c': 3.5
        }
        dodgeDelay = {
            'a': 2.45,
            'b': 2.45,
            'c': 2.45
        }
        suitTrack = getSuitTrack(attack, delay=0.9)
        initialCloudHeight = suit.height + 3
        cloudPosPoints = [Point3(0, 3, initialCloudHeight), VBase3(180, 0, 0)]
        cloudPropTrack = Sequence(
            Func(cloud.pose, 'stormcloud', 0),
            getPropAppearTrack(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7),
            Func(battle.movie.needRestoreRenderProp, cloud),
            Func(cloud.wrtReparentTo, render)
        )
        targetPoint = __toonFacePoint(toon)
        targetPoint.setZ(targetPoint[2] + 3)
        cloudPropTrack.append(Wait(1.1))
        cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
        suitType = getSuitBodyType(attack['suitName'])
        cloudPropTrack.append(Wait(partDelay[suitType]))
        cloudPropTrack.append(
            Parallel(
                Sequence(
                    ParticleInterval(rainEffect, cloud, worldRelative=0, duration=2.1, cleanup=True)
                ),
                Sequence(
                    Wait(0.1),
                    ParticleInterval(rainEffect2, cloud, worldRelative=0, duration=2.0, cleanup=True)
                ),
                Sequence(
                    Wait(0.1),
                    ParticleInterval(rainEffect3, cloud, worldRelative=0, duration=2.0, cleanup=True)
                ),
                Sequence(
                    ActorInterval(cloud, 'stormcloud', startTime=3, duration=0.1),
                    ActorInterval(cloud, 'stormcloud', startTime=1, duration=2.3)
                )
            )
        )
        cloudPropTrack.append(Wait(0.4))
        cloudPropTrack.append(
            LerpScaleInterval(
                cloud,
                0.5,
                MovieUtil.PNT3_NEARZERO))
        cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
        cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))
        damageAnims = [['cringe', 0.01, 0.4, 0.8],
         ['duck', 0.01, 1.6]]
        toonTrack = getToonTrack(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], dodgeAnimNames=['sidestep'])
        soundTrack = getSoundTrack('SA_liquidate.ogg', delay=2.0, node=suit)
        return Parallel(suitTrack, toonTrack, cloudPropTrack, soundTrack)
    else:
        targets = attack['target']
        BattleParticles.loadParticles()
        partDelay = {
            'a': 0.2,
            'b': 0.2,
            'c': 0.2
        }
        damageDelay = {
            'a': 3.5,
            'b': 3.5,
            'c': 3.5
        }
        dodgeDelay = {
            'a': 2.45,
            'b': 2.45,
            'c': 2.45
        }
        suitTrack = getSuitAnimTrack(attack, delay=0.9)
        initialCloudHeight = suit.height + 3
        cloudPosPoints = [Point3(0, 3, initialCloudHeight), VBase3(180, 0, 0)]
        cloudPropTracks = Parallel()
        damageAnims = [['cringe', 0.01, 0.4, 0.8],
         ['duck', 0.01, 1.6]]
        suitType = getSuitBodyType(attack['suitName'])
        toonTracks = getToonTracks(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], dodgeAnimNames=['sidestep'])
        soundTrack = getSoundTrack('SA_liquidate.ogg', delay=2.0, node=suit)
        for t in targets:
            dmg = t['hp']
            toon = t['toon']
            rainEffect = BattleParticles.createParticleEffect(file='liquidate')
            rainEffect2 = BattleParticles.createParticleEffect(file='liquidate')
            rainEffect3 = BattleParticles.createParticleEffect(file='liquidate')
            cloud = globalPropPool.getProp('stormcloud')
            cloudPropTrack = Sequence(
                Func(cloud.pose, 'stormcloud', 0),
                getPropAppearTrack(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7),
                Func(battle.movie.needRestoreRenderProp, cloud),
                Func(cloud.wrtReparentTo, render)
            )
            targetPoint = __toonFacePoint(toon)
            targetPoint.setZ(targetPoint[2] + 3)
            cloudPropTrack.append(Wait(1.1))
            cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
            cloudPropTrack.append(Wait(partDelay[suitType]))
            cloudPropTrack.append(
                Parallel(
                    Sequence(
                        ParticleInterval(rainEffect, cloud, worldRelative=0, duration=2.1, cleanup=True)
                    ),
                    Sequence(
                        Wait(0.1),
                        ParticleInterval(rainEffect2, cloud, worldRelative=0, duration=2.0, cleanup=True)
                    ),
                    Sequence(
                        Wait(0.1),
                        ParticleInterval(rainEffect3, cloud, worldRelative=0, duration=2.0, cleanup=True)
                    ),
                    Sequence(
                        ActorInterval(cloud, 'stormcloud', startTime=3, duration=0.1),
                        ActorInterval(cloud, 'stormcloud', startTime=1, duration=2.3)
                    )
                )
            )
            cloudPropTrack.append(Wait(0.4))
            cloudPropTrack.append(
                LerpScaleInterval(
                    cloud,
                    0.5,
                    MovieUtil.PNT3_NEARZERO))
            cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
            cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))
            cloudPropTracks.append(cloudPropTrack)
        return Parallel(suitTrack, toonTracks, cloudPropTracks, soundTrack)


def doMarketCrash(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    suitDelay = 1.32
    propDelay = 0.6
    throwDuration = 1.5
    paper = globalPropPool.getProp('newspaper')
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(-0.07, 0.17, -0.13), VBase3(161.867, -33.149, -48.086)]
    paperTrack = Sequence(
        getPropAppearTrack(paper, suit.getRightHand(), posPoints, propDelay, Point3(3, 3, 3), scaleUpTime=0.5),
        Wait(suitDelay)
    )
    hitPoint = toon.getPos(battle)
    hitPoint.setX(hitPoint.getX() + 1.2)
    hitPoint.setY(hitPoint.getY() + 1.5)
    if dmg > 0:
        hitPoint.setZ(hitPoint.getZ() + 1.1)
    movePoint = Point3(hitPoint.getX(), hitPoint.getY() - 1.8, hitPoint.getZ() + 0.2)
    paperTrack.append(Func(battle.movie.needRestoreRenderProp, paper))
    paperTrack.append(Func(paper.wrtReparentTo, battle))
    paperTrack.append(getThrowTrack(paper, hitPoint, duration=throwDuration, parent=battle))
    paperTrack.append(Wait(0.6))
    paperTrack.append(LerpPosInterval(paper, 0.4, movePoint))
    spinTrack = Sequence(
        Wait(propDelay + suitDelay + 0.2),
        LerpHprInterval(paper, throwDuration, Point3(-360, 0, 0))
    )
    sizeTrack = Sequence(
        Wait(propDelay + suitDelay + 0.2),
        LerpScaleInterval(paper, throwDuration, Point3(6, 6, 6)),
        Wait(0.95),
        LerpScaleInterval(paper, 0.4, MovieUtil.PNT3_NEARZERO)
    )
    propTrack = Sequence(
        Parallel(paperTrack, spinTrack, sizeTrack),
        Func(MovieUtil.removeProp, paper),
        Func(battle.movie.clearRenderProp, paper)
    )
    damageAnims = [['cringe', 0.01, 0.21, 0.08],
     ['slip-forward', 0.01, 0.6, 0.85]]
    damageAnims.extend(getSplicedLerpAnims('slip-forward', 0.31, 0.95, startTime=1.2))
    damageAnims.append(['slip-forward', 0.01, 1.51])
    toonTrack = getToonTrack(attack, damageDelay=3.8, splicedDamageAnims=damageAnims, dodgeDelay=2.4, dodgeAnimNames=['sidestep'], showDamageExtraTime=0.4, showMissedExtraTime=1.3)
    return Parallel(suitTrack, toonTrack, propTrack)


def doBite(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        teeth = globalPropPool.getProp('teeth')
        propDelay = 0.8
        propScaleUpTime = 0.5
        suitDelay = 1.73
        throwDelay = propDelay + propScaleUpTime + suitDelay
        throwDuration = 0.4
        suitTrack = getSuitTrack(attack)
        posPoints = [Point3(-0.05, 0.41, -0.54), VBase3(4.465, -3.563, 51.479)]
        teethAppearTrack = Sequence(
            getPropAppearTrack(teeth, suit.getRightHand(), posPoints, propDelay, Point3(3, 3, 3), scaleUpTime=propScaleUpTime),
            Wait(suitDelay),
            Func(battle.movie.needRestoreRenderProp, teeth),
            Func(teeth.wrtReparentTo, battle)
        )
        if dmg > 0:
            x = toon.getX(battle)
            y = toon.getY(battle)
            z = toon.getZ(battle)
            toonHeight = z + toon.getHeight()
            flyPoint = Point3(x, y + 2.7, toonHeight * 0.8)
            teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.4, pos=Point3(x, y + 3.2, toonHeight * 0.7)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.3, pos=Point3(x, y + 4.7, toonHeight * 0.5)))
            teethAppearTrack.append(Wait(0.2))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 0.2, toonHeight * 0.9)))
            teethAppearTrack.append(Wait(0.4))
            scaleTrack = Sequence(
                Wait(throwDelay),
                LerpScaleInterval(teeth, throwDuration, Point3(8, 8, 8)),
                Wait(0.9),
                LerpScaleInterval(teeth, 0.2, Point3(14, 14, 14)),
                Wait(1.2),
                LerpScaleInterval(teeth, 0.3, MovieUtil.PNT3_NEARZERO)
            )
            hprTrack = Sequence(
                Wait(throwDelay),
                LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
                Wait(0.2),
                LerpHprInterval(teeth, 0.4, Point3(180, -35, 0), startHpr=Point3(180, 0, 0)),
                Wait(0.6),
                LerpHprInterval(teeth, 0.1, Point3(180, -75, 0), startHpr=Point3(180, -35, 0))
            )
            animTrack = Sequence(
                Wait(throwDelay),
                ActorInterval(teeth, 'teeth', duration=throwDuration),
                ActorInterval(teeth, 'teeth', duration=0.3),
                Func(teeth.pose, 'teeth', 1),
                Wait(0.7),
                ActorInterval(teeth, 'teeth', duration=0.9)
            )
            propTrack = Sequence(
                Parallel(teethAppearTrack, scaleTrack, hprTrack, animTrack),
                Func(MovieUtil.removeProp, teeth),
                Func(battle.movie.clearRenderProp, teeth)
            )
        else:
            flyPoint = __toonFacePoint(toon, parent=battle)
            flyPoint.setY(flyPoint.getY() - 7.1)
            teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
            teethAppearTrack.append(Func(MovieUtil.removeProp, teeth))
            teethAppearTrack.append(Func(battle.movie.clearRenderProp, teeth))
            propTrack = teethAppearTrack
        damageAnims = [['cringe', 0.01, 0.7, 1.2],
         ['conked', 0.01, 0.2, 2.1],
         ['conked', 0.01, 3.2]]
        dodgeAnims = [['cringe', 0.01, 0.7, 0.2],
         ['duck', 0.01, 1.6]]
        toonTrack = getToonTrack(attack, damageDelay=3.2, splicedDamageAnims=damageAnims, dodgeDelay=2.9, splicedDodgeAnims=dodgeAnims, showDamageExtraTime=2.4)
        return Parallel(suitTrack, toonTrack, propTrack)
    else:
        targets = attack['target']
        propDelay = 0.8
        propScaleUpTime = 0.5
        suitDelay = 1.73
        throwDelay = propDelay + propScaleUpTime + suitDelay
        throwDuration = 0.4
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        posPoints = [Point3(-0.05, 0.41, -0.54), VBase3(4.465, -3.563, 51.479)]
        propTracks = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            teeth = globalPropPool.getProp('teeth')
            teethAppearTrack = Sequence(
                getPropAppearTrack(teeth, suit.getRightHand(), posPoints, propDelay, Point3(3, 3, 3), scaleUpTime=propScaleUpTime),
                Wait(suitDelay),
                Func(battle.movie.needRestoreRenderProp, teeth),
                Func(teeth.wrtReparentTo, battle)
            )
            if dmg > 0:
                x = toon.getX(battle)
                y = toon.getY(battle)
                z = toon.getZ(battle)
                toonHeight = z + toon.getHeight()
                flyPoint = Point3(x, y + 2.7, toonHeight * 0.8)
                teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.4, pos=Point3(x, y + 3.2, toonHeight * 0.7)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.3, pos=Point3(x, y + 4.7, toonHeight * 0.5)))
                teethAppearTrack.append(Wait(0.2))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 0.2, toonHeight * 0.9)))
                teethAppearTrack.append(Wait(0.4))
                scaleTrack = Sequence(
                    Wait(throwDelay),
                    LerpScaleInterval(teeth, throwDuration, Point3(8, 8, 8)),
                    Wait(0.9),
                    LerpScaleInterval(teeth, 0.2, Point3(14, 14, 14)),
                    Wait(1.2),
                    LerpScaleInterval(teeth, 0.3, MovieUtil.PNT3_NEARZERO)
                )
                hprTrack = Sequence(
                    Wait(throwDelay),
                    LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
                    Wait(0.2),
                    LerpHprInterval(teeth, 0.4, Point3(180, -35, 0), startHpr=Point3(180, 0, 0)),
                    Wait(0.6),
                    LerpHprInterval(teeth, 0.1, Point3(180, -75, 0), startHpr=Point3(180, -35, 0))
                )
                animTrack = Sequence(
                    Wait(throwDelay),
                    ActorInterval(teeth, 'teeth', duration=throwDuration),
                    ActorInterval(teeth, 'teeth', duration=0.3),
                    Func(teeth.pose, 'teeth', 1),
                    Wait(0.7),
                    ActorInterval(teeth, 'teeth', duration=0.9)
                )
                propTrack = Sequence(
                    Parallel(teethAppearTrack, scaleTrack, hprTrack, animTrack),
                    Func(MovieUtil.removeProp, teeth),
                    Func(battle.movie.clearRenderProp, teeth)
                )
            else:
                flyPoint = __toonFacePoint(toon, parent=battle)
                flyPoint.setY(flyPoint.getY() - 7.1)
                teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
                teethAppearTrack.append(Func(MovieUtil.removeProp, teeth))
                teethAppearTrack.append(Func(battle.movie.clearRenderProp, teeth))
                propTrack = teethAppearTrack
            propTracks.append(propTrack)
        damageAnims = [['cringe', 0.01, 0.7, 1.2],
         ['conked', 0.01, 0.2, 2.1],
         ['conked', 0.01, 3.2]]
        dodgeAnims = [['cringe', 0.01, 0.7, 0.2],
         ['duck', 0.01, 1.6]]
        toonTracks = getToonTracks(attack, damageDelay=3.2, splicedDamageAnims=damageAnims, dodgeDelay=2.9, splicedDodgeAnims=dodgeAnims, showDamageExtraTime=2.4)
        return Parallel(suitTrack, toonTracks, propTracks)


def doChomp(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        teeth = globalPropPool.getProp('teeth')
        propDelay = 0.8
        propScaleUpTime = 0.5
        suitDelay = 1.73
        throwDelay = propDelay + propScaleUpTime + suitDelay
        throwDuration = 0.4
        suitTrack = getSuitTrack(attack)
        posPoints = [Point3(-0.05, 0.41, -0.54), VBase3(4.465, -3.563, 51.479)]
        teethAppearTrack = Sequence(
            getPropAppearTrack(teeth, suit.getRightHand(), posPoints, propDelay, Point3(3, 3, 3), scaleUpTime=propScaleUpTime),
            Wait(suitDelay),
            Func(battle.movie.needRestoreRenderProp, teeth),
            Func(teeth.wrtReparentTo, battle)
        )
        x = toon.getX(battle)
        y = toon.getY(battle)
        z = toon.getZ(battle)
        if dmg > 0:
            toonHeight = z + toon.getHeight()
            flyPoint = Point3(x, y + 2.7, toonHeight * 0.7)
            teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.4, pos=Point3(x, y + 3.2, toonHeight * 0.7)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.3, pos=Point3(x, y + 4.7, toonHeight * 0.5)))
            teethAppearTrack.append(Wait(0.2))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y, toonHeight + 3)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 1.2, toonHeight * 0.7)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 0.7, toonHeight * 0.4)))
            teethAppearTrack.append(Wait(0.4))
            scaleTrack = Sequence(
                Wait(throwDelay),
                LerpScaleInterval(teeth, throwDuration, Point3(6, 6, 6)),
                Wait(0.9),
                LerpScaleInterval(teeth, 0.2, Point3(10, 10, 10)),
                Wait(1.2),
                LerpScaleInterval(teeth, 0.3, MovieUtil.PNT3_NEARZERO)
            )
            hprTrack = Sequence(
                Wait(throwDelay),
                LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
                Wait(0.2),
                LerpHprInterval(teeth, 0.4, Point3(180, -35, 0), startHpr=Point3(180, 0, 0)),
                Wait(0.6),
                LerpHprInterval(teeth, 0.1, Point3(0, -35, 0), startHpr=Point3(180, -35, 0))
            )
            animTrack = Sequence(
                Wait(throwDelay),
                ActorInterval(teeth, 'teeth', duration=throwDuration),
                ActorInterval(teeth, 'teeth', duration=0.3),
                Func(teeth.pose, 'teeth', 1),
                Wait(0.7),
                ActorInterval(teeth, 'teeth', duration=0.9)
            )
            propTrack = Sequence(Parallel(teethAppearTrack, scaleTrack, hprTrack, animTrack))
        else:
            z = z + 0.2
            flyPoint = Point3(x, y - 2.1, z)
            teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
            teethAppearTrack.append(Wait(0.2))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.5, y - 2.5, z)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 1.0, y - 3.0, z + 0.4)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 1.3, y - 3.6, z)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.9, y - 3.1, z + 0.4)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.3, y - 2.6, z)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.1, y - 2.2, z + 0.4)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.4, y - 1.9, z)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.7, y - 2.1, z + 0.4)))
            teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.8, y - 2.3, z)))
            teethAppearTrack.append(LerpScaleInterval(teeth, 0.6, MovieUtil.PNT3_NEARZERO))
            hprTrack = Sequence(
                Wait(throwDelay),
                LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
                Wait(0.5),
                LerpHprInterval(teeth, 0.4, Point3(80, 0, 0), startHpr=Point3(180, 0, 0)),
                LerpHprInterval(teeth, 0.8, Point3(-10, 0, 0), startHpr=Point3(80, 0, 0))
            )
            animTrack = Sequence(
                Wait(throwDelay),
                ActorInterval(teeth, 'teeth', duration=3.6)
            )
            propTrack = Sequence(Parallel(teethAppearTrack, hprTrack, animTrack))
        propTrack.append(Func(MovieUtil.removeProp, teeth))
        propTrack.append(Func(battle.movie.clearRenderProp, teeth))
        damageAnims = [['cringe', 0.01, 0.7, 1.2],
         ['spit', 0.01, 2.95, 1.47],
         ['spit', 0.01, 4.42, 0.07],
         ['spit', 0.08, 4.49, -0.07],
         ['spit', 0.08, 4.42, 0.07],
         ['spit', 0.08, 4.49, -0.07],
         ['spit', 0.08, 4.42, 0.07],
         ['spit', 0.08, 4.49, -0.07],
         ['spit', 0.01, 4.42]]
        dodgeAnims = [['jump', 0.01, 0.01]]
        toonTrack = getToonTrack(attack, damageDelay=3.2, splicedDamageAnims=damageAnims, dodgeDelay=2.75, splicedDodgeAnims=dodgeAnims, showDamageExtraTime=1.4)
        return Parallel(suitTrack, toonTrack, propTrack)
    else:
        targets = attack['target']
        propDelay = 0.8
        propScaleUpTime = 0.5
        suitDelay = 1.73
        throwDelay = propDelay + propScaleUpTime + suitDelay
        throwDuration = 0.4
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        posPoints = [Point3(-0.05, 0.41, -0.54), VBase3(4.465, -3.563, 51.479)]
        propTracks = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            teeth = globalPropPool.getProp('teeth')
            teethAppearTrack = Sequence(
                getPropAppearTrack(teeth, suit.getRightHand(), posPoints, propDelay, Point3(3, 3, 3), scaleUpTime=propScaleUpTime),
                Wait(suitDelay),
                Func(battle.movie.needRestoreRenderProp, teeth),
                Func(teeth.wrtReparentTo, battle)
            )
            x = toon.getX(battle)
            y = toon.getY(battle)
            z = toon.getZ(battle)
            if dmg > 0:
                toonHeight = z + toon.getHeight()
                flyPoint = Point3(x, y + 2.7, toonHeight * 0.7)
                teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.4, pos=Point3(x, y + 3.2, toonHeight * 0.7)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.3, pos=Point3(x, y + 4.7, toonHeight * 0.5)))
                teethAppearTrack.append(Wait(0.2))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y, toonHeight + 3)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 1.2, toonHeight * 0.7)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 0.7, toonHeight * 0.4)))
                teethAppearTrack.append(Wait(0.4))
                scaleTrack = Sequence(
                    Wait(throwDelay),
                    LerpScaleInterval(teeth, throwDuration, Point3(6, 6, 6)),
                    Wait(0.9),
                    LerpScaleInterval(teeth, 0.2, Point3(10, 10, 10)),
                    Wait(1.2),
                    LerpScaleInterval(teeth, 0.3, MovieUtil.PNT3_NEARZERO)
                )
                hprTrack = Sequence(
                    Wait(throwDelay),
                    LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
                    Wait(0.2),
                    LerpHprInterval(teeth, 0.4, Point3(180, -35, 0), startHpr=Point3(180, 0, 0)),
                    Wait(0.6),
                    LerpHprInterval(teeth, 0.1, Point3(0, -35, 0), startHpr=Point3(180, -35, 0))
                )
                animTrack = Sequence(
                    Wait(throwDelay),
                    ActorInterval(teeth, 'teeth', duration=throwDuration),
                    ActorInterval(teeth, 'teeth', duration=0.3),
                    Func(teeth.pose, 'teeth', 1),
                    Wait(0.7),
                    ActorInterval(teeth, 'teeth', duration=0.9)
                )
                propTrack = Sequence(Parallel(teethAppearTrack, scaleTrack, hprTrack, animTrack))
            else:
                z = z + 0.2
                flyPoint = Point3(x, y - 2.1, z)
                teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
                teethAppearTrack.append(Wait(0.2))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.5, y - 2.5, z)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 1.0, y - 3.0, z + 0.4)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 1.3, y - 3.6, z)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.9, y - 3.1, z + 0.4)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.3, y - 2.6, z)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.1, y - 2.2, z + 0.4)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.4, y - 1.9, z)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.7, y - 2.1, z + 0.4)))
                teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.8, y - 2.3, z)))
                teethAppearTrack.append(LerpScaleInterval(teeth, 0.6, MovieUtil.PNT3_NEARZERO))
                hprTrack = Sequence(
                    Wait(throwDelay),
                    LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
                    Wait(0.5),
                    LerpHprInterval(teeth, 0.4, Point3(80, 0, 0), startHpr=Point3(180, 0, 0)),
                    LerpHprInterval(teeth, 0.8, Point3(-10, 0, 0), startHpr=Point3(80, 0, 0))
                )
                animTrack = Sequence(
                    Wait(throwDelay),
                    ActorInterval(teeth, 'teeth', duration=3.6)
                )
                propTrack = Sequence(Parallel(teethAppearTrack, hprTrack, animTrack))
            propTrack.append(Func(MovieUtil.removeProp, teeth))
            propTrack.append(Func(battle.movie.clearRenderProp, teeth))
            propTracks.append(propTrack)
        damageAnims = [['cringe', 0.01, 0.7, 1.2],
         ['spit', 0.01, 2.95, 1.47],
         ['spit', 0.01, 4.42, 0.07],
         ['spit', 0.08, 4.49, -0.07],
         ['spit', 0.08, 4.42, 0.07],
         ['spit', 0.08, 4.49, -0.07],
         ['spit', 0.08, 4.42, 0.07],
         ['spit', 0.08, 4.49, -0.07],
         ['spit', 0.01, 4.42]]
        dodgeAnims = [['jump', 0.01, 0.01]]
        toonTracks = getToonTracks(attack, damageDelay=3.2, splicedDamageAnims=damageAnims, dodgeDelay=2.75, splicedDodgeAnims=dodgeAnims, showDamageExtraTime=1.4)
        return Parallel(suitTrack, toonTracks, propTracks)


def doFiveOClockShadow(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    damageDelay = 1.1
    shadow = toon.dropShadow
    fakeShadow = MovieUtil.copyProp(shadow)
    fakeShadow.wrtReparentTo(battle)
    suitTrack = getSuitTrack(attack)
    shadowTrack = Sequence(
        Func(battle.movie.needRestoreRenderProp, fakeShadow),
        Wait(damageDelay - 0.7),
        Func(fakeShadow.hide),
        Func(fakeShadow.setScale, MovieUtil.PNT3_NEARZERO),
        Func(fakeShadow.reparentTo, toon),
        Func(fakeShadow.setPos, MovieUtil.PNT3_ZERO),
        Func(fakeShadow.wrtReparentTo, battle),
        Func(fakeShadow.show),
        LerpScaleInterval(fakeShadow, 1.0, Point3(1.7), startScale=MovieUtil.PNT3_NEARZERO)
    )
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=[['melt'], ['jump', 1.5, 0.4]], dodgeAnimNames=['sidestep'])
    if dmg > 0:
        shadowTrack.append(Wait(3.2))
    else:
        shadowTrack.append(Wait(0.3))
    shadowTrack.append(LerpColorScaleInterval(fakeShadow, 0.5, Vec4(0, 0, 0, 0)))
    shadowTrack.append(Func(MovieUtil.removeProp, fakeShadow))
    shadowTrack.append(Func(battle.movie.clearRenderProp, fakeShadow))
    return Parallel(suitTrack, shadowTrack, toonTrack)


def doUndergroundLiquidity(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    BattleParticles.loadParticles()
    rainEffect = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect2 = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect3 = BattleParticles.createParticleEffect(file='liquidate')
    cloud = globalPropPool.getProp('stormcloud')
    partDelay = {
        'a': 0.2,
        'b': 0.2,
        'c': 0.2
    }
    damageDelay = {
        'a': 3.5,
        'b': 3.5,
        'c': 3.5
    }
    dodgeDelay = {
        'a': 2.45,
        'b': 2.45,
        'c': 2.45
    }
    suitTrack = getSuitTrack(attack, delay=0.9)
    initialCloudHeight = suit.height + 3
    cloudPosPoints = [Point3(0, 3, initialCloudHeight), VBase3(180, 0, 0)]
    cloudPropTrack = Sequence()
    cloudPropTrack.append(Func(cloud.pose, 'stormcloud', 0))
    cloudPropTrack.append(getPropAppearTrack(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7))
    cloudPropTrack.append(Func(battle.movie.needRestoreRenderProp, cloud))
    cloudPropTrack.append(Func(cloud.wrtReparentTo, render))
    targetPoint = __toonFacePoint(toon)
    targetPoint.setZ(targetPoint[2] + 3)
    cloudPropTrack.append(Wait(1.1))
    cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
    suitType = getSuitBodyType(attack['suitName'])
    cloudPropTrack.append(Wait(partDelay[suitType]))
    cloudPropTrack.append(
        Parallel(
            Sequence(ParticleInterval(rainEffect, cloud, worldRelative=0, duration=2.1, cleanup=True)),
            Sequence(
                Wait(0.1),
                ParticleInterval(rainEffect2, cloud, worldRelative=0, duration=2.0, cleanup=True)
            ),
            Sequence(
                Wait(0.1),
                ParticleInterval(rainEffect3, cloud, worldRelative=0, duration=2.0, cleanup=True)
            ),
            Sequence(
                ActorInterval(cloud, 'stormcloud', startTime=3, duration=0.1),
                ActorInterval(cloud, 'stormcloud', startTime=1, duration=2.3)
            )
        )
    )
    cloudPropTrack.append(Wait(0.4))
    cloudPropTrack.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
    cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
    cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))
    damageAnims = [['melt'], ['jump', 1.5, 0.4]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay[suitType], splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay[suitType], dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_liquidate.ogg', delay=2.0, node=suit)
    multiTrackList = Parallel(suitTrack, toonTrack, cloudPropTrack, soundTrack)
    if dmg > 0:
        puddle = globalPropPool.getProp('quicksand')
        puddle.setColor(Vec4(0.0, 0.0, 1.0, 1))
        puddle.setHpr(Point3(120, 0, 0))
        puddle.setScale(0.01)
        puddleTrack = Sequence(
            Func(battle.movie.needRestoreRenderProp, puddle),
            Wait(damageDelay[suitType] - 0.7),
            Func(puddle.reparentTo, battle),
            Func(puddle.setPos, toon.getPos(battle)),
            LerpScaleInterval(puddle, 1.7, Point3(1.7, 1.7, 1.7), startScale=MovieUtil.PNT3_NEARZERO),
            Wait(3.2),
            LerpFunctionInterval(puddle.setAlphaScale, fromData=1, toData=0, duration=0.8),
            Func(MovieUtil.removeProp, puddle),
            Func(battle.movie.clearRenderProp, puddle)
        )
        multiTrackList.append(puddleTrack)
    return multiTrackList


def doEvictionNotice(attack):
    # TODO: Attack should make a Toon get launched from the battle, evicting them.
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    paper = globalPropPool.getProp('shredder-paper')
    suitTrack = getSuitTrack(attack, playRate=1.5)
    posPoints = [Point3(-0.04, 0.15, -1.38), VBase3(10.584, -11.945, 18.316)]
    propTrack = Sequence(
        getPropAppearTrack(paper, suit.getRightHand(), posPoints, 0.6, MovieUtil.PNT3_ONE, scaleUpTime=0.375),
        Wait(1.2975)
    )
    hitPoint = __toonFacePoint(toon, parent=battle)
    hitPoint.setX(hitPoint.getX() - 1.4)
    missPoint = __toonGroundPoint(attack, toon, 0.7, parent=battle)
    missPoint.setX(missPoint.getX() - 1.1)
    propTrack.append(getPropThrowTrack(attack, paper, [hitPoint], [missPoint], hitDuration=0.375, missDuration=0.375, parent=battle))
    if dmg > 0:
        # Will work on the eviction part later.
        toonTrack = getToonTakeDamageTrack(toon, target['died'], dmg, 2.55, ['conked'], None, 0.01)
    else:
        toonTrack = getToonDodgeTrack(target, 2.1, ['jump'], None, 0.5)
    return Parallel(suitTrack, toonTrack, propTrack)


def doWithdrawal(attack):
    suit = attack['suit']
    battle = attack['battle']
    targets = attack['target']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Withdrawal')
    BattleParticles.setEffectTexture(particleEffect, 'snow-particle')
    suitTrack = getSuitAnimTrack(attack)
    partTrack = getPartTrack(particleEffect, 1e-05, suitTrack.getDuration() + 1.2, [particleEffect, suit, 0])
    toonTracks = getToonTracks(attack, 1.2, ['cringe'], 0.2, splicedDodgeAnims=[['duck', 1e-05, 0.8]], showMissedExtraTime=0.8)
    soundTrack = getSoundTrack('SA_withdrawl.ogg', delay=1.4, node=suit)
    colorTracks = Parallel()
    for t in targets:
        toon = t['toon']
        dmg = t['hp']
        if dmg > 0:
            colorTrack = getColorTrack(attack, toon, 'all', Vec4(0, 0, 0, 1), 1.6, 2.9)
            colorTracks.append(colorTrack)
    return Parallel(suitTrack, partTrack, toonTracks, soundTrack, colorTracks)

def doJargon(attack):
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect2 = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect3 = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect4 = BattleParticles.createParticleEffect(file='jargonSpray')
    BattleParticles.setEffectTexture(particleEffect, 'jargon-brow', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'jargon-deep', color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect3, 'jargon-hoop', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect4, 'jargon-ipo', color=Vec4(0, 0, 0, 1))
    damageDelay = 2.2
    dodgeDelay = 1.5
    partDelay = 1.1
    partInterval = 1.2
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, partDelay + partInterval * 0, 2, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, partDelay + partInterval * 1, 2, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, partDelay + partInterval * 2, 2, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, partDelay + partInterval * 3, 1.0, [particleEffect4, suit, 0])
    damageAnims = [['conked', 0.0001, 0, 0.4],
     ['conked', 0.0001, 2.7, 0.85],
     ['conked', 0.0001, 0.4, 0.09],
     ['conked', 0.0001, 0.4, 0.09],
     ['conked', 0.0001, 0.4, 0.66],
     ['conked', 0.0001, 0.4, 0.09],
     ['conked', 0.0001, 0.4, 0.09],
     ['conked', 0.0001, 0.4, 0.86],
     ['conked', 0.0001, 0.4, 0.14],
     ['conked', 0.0001, 0.4, 0.14],
     ['conked', 0.0001, 0.4]]
    dodgeAnims = [['duck', 0.0001, 1.2],
     ['duck', 0.0001, 1.3]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.6, showDamageExtraTime=0.7)
    soundTrack = getSoundTrack('SA_jargon.ogg', delay=2.1, node=suit)
    return Parallel(suitTrack, toonTrack, soundTrack, partTrack, partTrack2, partTrack3, partTrack4)


def doMumboJumbo(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect(file='mumboJumboSpray')
    particleEffect2 = BattleParticles.createParticleEffect(file='mumboJumboSpray')
    particleEffect3 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    particleEffect4 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    particleEffect5 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    BattleParticles.setEffectTexture(particleEffect, 'mumbojumbo-boiler', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'mumbojumbo-creative', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect3, 'mumbojumbo-deben', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect4, 'mumbojumbo-high', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect5, 'mumbojumbo-iron', color=Vec4(1, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.5, 2, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.5, 2, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 3.3, 1.7, [particleEffect3, toon, 0])
    partTrack4 = getPartTrack(particleEffect4, 3.3, 1.7, [particleEffect4, toon, 0])
    partTrack5 = getPartTrack(particleEffect5, 3.3, 1.7, [particleEffect5, toon, 0])
    toonTrack = getToonTrack(attack, 3.2, ['cringe'], 2.2, ['sidestep'])
    soundTrack = getSoundTrack('SA_mumbo_jumbo.ogg', delay=2.5, node=suit)
    multiTrackList = Parallel(suitTrack, toonTrack, soundTrack, partTrack, partTrack2)
    if dmg != 0:
        multiTrackList.append(partTrack3)
        multiTrackList.append(partTrack4)
        multiTrackList.append(partTrack5)
    return multiTrackList


def doGuiltTrip(attack):
    suit = attack['suit']
    battle = attack['battle']
    centerColor = Vec4(1.0, 0.2, 0.2, 0.9)
    edgeColor = Vec4(0.9, 0.9, 0.9, 0.4)
    powerBar1 = BattleParticles.createParticleEffect(file='guiltTrip')
    powerBar2 = BattleParticles.createParticleEffect(file='guiltTrip')
    powerBar1.setPos(0, 6.1, 0.4)
    powerBar1.setHpr(-90, 0, 0)
    powerBar2.setPos(0, 6.1, 0.4)
    powerBar2.setHpr(90, 0, 0)
    powerBar1.setScale(5)
    powerBar2.setScale(5)
    powerBar1Particles = powerBar1.getParticlesNamed('particles-1')
    powerBar2Particles = powerBar2.getParticlesNamed('particles-1')
    powerBar1Particles.renderer.setCenterColor(centerColor)
    powerBar1Particles.renderer.setEdgeColor(edgeColor)
    powerBar2Particles.renderer.setCenterColor(centerColor)
    powerBar2Particles.renderer.setEdgeColor(edgeColor)
    waterfallEffect = BattleParticles.createParticleEffect('Waterfall')
    waterfallEffect.setScale(11)
    waterfallParticles = waterfallEffect.getParticlesNamed('particles-1')
    waterfallParticles.renderer.setCenterColor(centerColor)
    waterfallParticles.renderer.setEdgeColor(edgeColor)
    suitTrack = getSuitAnimTrack(attack)

    def getPowerTrack(effect, suit=suit, battle=battle):
        partTrack = Sequence(
            Wait(0.7),
            Func(battle.movie.needRestoreParticleEffect, effect),
            Func(effect.start, suit),
            Wait(0.4),
            LerpPosInterval(effect, 1.0, Point3(0, 15, 0.4)),
            LerpFunctionInterval(effect.setAlphaScale, fromData=1, toData=0, duration=0.4),
            Func(effect.cleanup),
            Func(battle.movie.clearRestoreParticleEffect, effect)
        )
        return partTrack

    partTrack1 = getPowerTrack(powerBar1)
    partTrack2 = getPowerTrack(powerBar2)
    waterfallTrack = getPartTrack(waterfallEffect, 0.6, 0.6, [waterfallEffect, suit, 0])
    toonTracks = getToonTracks(attack, 1.5, ['slip-forward'], 0.86, ['jump'])
    soundTrack = getSoundTrack('SA_guilt_trip.ogg', delay=1.1, node=suit)
    return Parallel(suitTrack, partTrack1, partTrack2, soundTrack, waterfallTrack, toonTracks)


def doRestrainingOrder(attack):
    suit = attack['suit']
    battle = attack['battle']
    if attack['group'] == ATK_TGT_SINGLE:
        target = attack['target']
        toon = target[0]['toon']
        dmg = target[0]['hp']
        paper = globalPropPool.getProp('shredder-paper')
        suitTrack = getSuitTrack(attack)
        posPoints = [Point3(-0.04, 0.15, -1.38), VBase3(10.584, -11.945, 18.316)]
        propTrack = Sequence(
            getPropAppearTrack(paper, suit.getRightHand(), posPoints, 0.8, MovieUtil.PNT3_ONE, scaleUpTime=0.5),
            Wait(1.73)
        )
        hitPoint = __toonFacePoint(toon, parent=battle)
        hitPoint.setX(hitPoint.getX() - 1.4)
        missPoint = __toonGroundPoint(attack, toon, 0.7, parent=battle)
        missPoint.setX(missPoint.getX() - 1.1)
        propTrack.append(getPropThrowTrack(attack, paper, [hitPoint], [missPoint], parent=battle))
        damageAnims = [['conked', 0.01, 0.3, 0.2],
         ['struggle', 0.01, 0.2]]
        toonTrack = getToonTrack(attack, damageDelay=3.4, splicedDamageAnims=damageAnims, dodgeDelay=2.8, dodgeAnimNames=['sidestep'])
        if dmg > 0:
            restraintCloud = BattleParticles.createParticleEffect(file='restrainingOrderCloud')
            restraintCloud.setPos(hitPoint.getX(), hitPoint.getY() + 0.5, hitPoint.getZ())
            cloudTrack = getPartTrack(restraintCloud, 3.5, 0.2, [restraintCloud, battle, 0])
            return Parallel(suitTrack, cloudTrack, toonTrack, propTrack)
        else:
            return Parallel(suitTrack, toonTrack, propTrack)
    else:
        targets = attack['target']
        suitTrack = getSuitAnimTrack(attack, delay=1e-06)
        posPoints = [Point3(-0.04, 0.15, -1.38), VBase3(10.584, -11.945, 18.316)]
        propTracks = Parallel()
        damageAnims = [['conked', 0.01, 0.3, 0.2],
         ['struggle', 0.01, 0.2]]
        toonTracks = getToonTracks(attack, damageDelay=3.4, splicedDamageAnims=damageAnims, damageDelay=2.8, dodgeAnimNames=['sidestep'])
        cloudTracks = Parallel()
        for t in targets:
            toon = t['toon']
            dmg = t['hp']
            paper = globalPropPool.getProp('shredder-paper')
            propTrack = Sequence(
                getPropAppearTrack(paper, suit.getRightHand(), posPoints, 0.8, MovieUtil.PNT3_ONE, scaleUpTime=0.5),
                Wait(1.73)
            )
            hitPoint = __toonFacePoint(toon, parent=battle)
            hitPoint.setX(hitPoint.getX() - 1.4)
            missPoint = __toonGroundPoint(attack, toon, 0.7, parent=battle)
            missPoint.setX(missPoint.getX() - 1.1)
            propTrack.append(getPropThrowTrack(attack, paper, [hitPoint], [missPoint], parent=battle))
            propTracks.append(propTrack)
            if dmg > 0:
                restraintCloud = BattleParticles.createParticleEffect(file='restrainingOrderCloud')
                restraintCloud.setPos(hitPoint.getX(), hitPoint.getY() + 0.5, hitPoint.getZ())
                cloudTrack = getPartTrack(restraintCloud, 3.5, 0.2, [restraintCloud, battle, 0])
                cloudTracks.append(cloudTrack)
        return Parallel(suitTrack, cloudTracks, toonTracks, propTracks)


def doSpin(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    damageDelay = 1.7
    sprayEffect = BattleParticles.createParticleEffect(file='spinSpray')
    spinEffect1 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect2 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect3 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect1.reparentTo(toon)
    spinEffect2.reparentTo(toon)
    spinEffect3.reparentTo(toon)
    height1 = toon.getHeight() * (random.random() * 0.2 + 0.7)
    height2 = toon.getHeight() * (random.random() * 0.2 + 0.4)
    height3 = toon.getHeight() * (random.random() * 0.2 + 0.1)
    spinEffect1.setPos(0.8, -0.7, height1)
    spinEffect1.setHpr(0, 0, -random.random() * 10 - 85)
    spinEffect1.setHpr(spinEffect1, 0, 50, 0)
    spinEffect2.setPos(0.8, -0.7, height2)
    spinEffect2.setHpr(0, 0, -random.random() * 10 - 85)
    spinEffect2.setHpr(spinEffect2, 0, 50, 0)
    spinEffect3.setPos(0.8, -0.7, height3)
    spinEffect3.setHpr(0, 0, -random.random() * 10 - 85)
    spinEffect3.setHpr(spinEffect3, 0, 50, 0)
    spinEffect1.wrtReparentTo(battle)
    spinEffect2.wrtReparentTo(battle)
    spinEffect3.wrtReparentTo(battle)
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])
    spinTrack1 = getPartTrack(spinEffect1, 2.1, 3.9, [spinEffect1, battle, 0])
    spinTrack2 = getPartTrack(spinEffect2, 2.1, 3.9, [spinEffect2, battle, 0])
    spinTrack3 = getPartTrack(spinEffect3, 2.1, 3.9, [spinEffect3, battle, 0])
    damageAnims = [['duck', 0.01, 0.01, 1.1]]
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.1, startTime=2.26))
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.1, startTime=2.26))
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=0.91, dodgeAnimNames=['sidestep'], showDamageExtraTime=2.1, showMissedExtraTime=1.0)
    multiTrackList = Parallel(suitTrack, sprayTrack, toonTrack)
    if dmg > 0:
        toonSpinTrack = Sequence(
            Wait(damageDelay + 0.9),
            LerpHprInterval(toon, 0.7, Point3(-10, 0, 0)),
            LerpHprInterval(toon, 0.5, Point3(-30, 0, 0)),
            LerpHprInterval(toon, 0.2, Point3(-60, 0, 0)),
            LerpHprInterval(toon, 0.7, Point3(-700, 0, 0)),
            LerpHprInterval(toon, 1.0, Point3(-1310, 0, 0)),
            LerpHprInterval(toon, 0.4, toon.getHpr()),
            Wait(0.5)
        )
        multiTrackList.append(toonSpinTrack)
        multiTrackList.append(spinTrack1)
        multiTrackList.append(spinTrack2)
        multiTrackList.append(spinTrack3)
    return multiTrackList


def doLegalese(attack):
    suit = attack['suit']
    BattleParticles.loadParticles()
    sprayEffect1 = BattleParticles.createParticleEffect(file='legaleseSpray')
    sprayEffect2 = BattleParticles.createParticleEffect(file='legaleseSpray')
    sprayEffect3 = BattleParticles.createParticleEffect(file='legaleseSpray')
    color = Vec4(0.4, 0, 0, 1)
    BattleParticles.setEffectTexture(sprayEffect1, 'legalese-hc', color=color)
    BattleParticles.setEffectTexture(sprayEffect2, 'legalese-qpq', color=color)
    BattleParticles.setEffectTexture(sprayEffect3, 'legalese-vd', color=color)
    partDelay = 1.3
    partDuration = 1.15
    damageDelay = 1.9
    dodgeDelay = 1.1
    suitTrack = getSuitTrack(attack)
    sprayTrack1 = getPartTrack(sprayEffect1, partDelay, partDuration, [sprayEffect1, suit, 0])
    sprayTrack2 = getPartTrack(sprayEffect2, partDelay + 0.8, partDuration, [sprayEffect2, suit, 0])
    sprayTrack3 = getPartTrack(sprayEffect3, partDelay + 1.6, partDuration, [sprayEffect3, suit, 0])
    damageAnims = [['cringe', 1e-05, 0.3, 0.8],
     ['cringe', 1e-05, 0.3, 0.8],
     ['cringe', 1e-05, 0.3]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'], showMissedExtraTime=0.8)
    return Parallel(suitTrack, toonTrack, sprayTrack1, sprayTrack2, sprayTrack3)


def doPeckingOrder(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    dmg = target[0]['hp']
    throwDuration = 3.03
    throwDelay = 3.2
    suitTrack = getSuitTrack(attack)
    numBirds = random.randint(4, 7)
    birdTracks = Parallel()
    propDelay = 1.5
    for i in range(0, numBirds):
        next = globalPropPool.getProp('bird')
        next.setScale(0.01)
        next.reparentTo(suit.getRightHand())
        next.setPos(random.random() * 0.6 - 0.3, random.random() * 0.6 - 0.3, random.random() * 0.6 - 0.3)
        if dmg > 0:
            hitPoint = Point3(random.random() * 5 - 2.5, random.random() * 2 - 1 - 6, random.random() * 3 - 1.5 + toon.getHeight() - 0.9)
        else:
            hitPoint = Point3(random.random() * 2 - 1, random.random() * 4 - 2 - 15, random.random() * 4 - 2 + 2.2)
        birdTrack = Sequence(
            Wait(throwDelay),
            Func(battle.movie.needRestoreRenderProp, next),
            Func(next.wrtReparentTo, battle),
            Func(next.setHpr, Point3(90, 20, 0)),
            LerpPosInterval(next, 1.1, hitPoint)
        )
        scaleTrack = Sequence(
            Wait(throwDelay),
            LerpScaleInterval(next, 0.15, Point3(9, 9, 9)))
        birdTracks.append(
            Sequence(
                Parallel(birdTrack, scaleTrack),
                Func(MovieUtil.removeProp, next)
            )
        )

    damageAnims = []
    damageAnims.append(['cringe',
                        0.01,
                        0.14,
                        0.21])
    damageAnims.append(['cringe',
                        0.01,
                        0.14,
                        0.13])
    damageAnims.append(['cringe', 0.01, 0.43])
    toonTrack = getToonTrack(
        attack,
        damageDelay=4.2,
        splicedDamageAnims=damageAnims,
        dodgeDelay=2.8,
        dodgeAnimNames=['sidestep'],
        showMissedExtraTime=1.1)
    return Parallel(suitTrack, toonTrack, birdTracks)


def doGavel(attack):
    battle = attack['battle']
    target = attack['target']
    toon = target[0]['toon']
    gavel = loader.loadModel('phase_11/models/lawbotHQ/LB_gavel')
    suitTrack = getSuitTrack(attack)
    toonPos = toon.getPos(battle)
    gavelPos = Point3(toonPos.getX(), toonPos.getY() + 8, 0)
    propTrack = Sequence(
        getPropAppearTrack(gavel, battle, [gavelPos, VBase3(0, 0, 0)], 0.0, scaleUpPoint=Point3(1), scaleUpTime=1.5),
        LerpHprInterval(gavel, 0.5, VBase3(0, 90, 0)),
        Parallel(
            SoundInterval(base.loader.loadSfx('phase_11/audio/sfx/LB_gavel.ogg'), node=toon),
            Sequence(
                Wait(0.1),
                LerpHprInterval(gavel, 0.5, VBase3(0, 0, 0)),
                LerpScaleInterval(gavel, 1.5, Point3(0.0, 0.0, 0.0))
            )
        ),
        Func(MovieUtil.removeProp, gavel)
    )
    toonTrack = getToonTrack(attack, 2.0, ['Squish'], 0.9, ['sidestep'])
    return Parallel(suitTrack, propTrack, toonTrack)


def doTrip(attack):
    suit = attack['suit']
    battle = attack['battle']
    powerBar1 = BattleParticles.createParticleEffect(file='powertrip')
    powerBar2 = BattleParticles.createParticleEffect(file='powertrip2')
    powerBar1.setPos(0, 6.1, 0.4)
    powerBar1.setHpr(-60, 0, 0)
    powerBar2.setPos(0, 6.1, 0.4)
    powerBar2.setHpr(60, 0, 0)
    waterfallEffect = BattleParticles.createParticleEffect('Waterfall')
    waterfallEffect.setScale(11)
    suitTrack = getSuitAnimTrack(attack)

    def getPowerTrack(effect, suit=suit, battle=battle):
        partTrack = Sequence(
            Wait(1.0),
            Func(battle.movie.needRestoreParticleEffect, effect),
            Func(effect.start, suit),
            Wait(0.4),
            LerpPosInterval(effect, 1.0, Point3(0, 15, 0.4)),
            LerpFunctionInterval(effect.setAlphaScale, fromData=1, toData=0, duration=0.4),
            Func(effect.cleanup), Func(battle.movie.clearRestoreParticleEffect, effect)
        )
        return partTrack

    partTrack1 = getPowerTrack(powerBar1)
    partTrack2 = getPowerTrack(powerBar2)
    waterfallTrack = getPartTrack(waterfallEffect, 0.6, 1.3, [waterfallEffect, suit, 0])
    toonTracks = getToonTracks(attack, 1.8, ['slip-forward'], 1.29, ['jump'])
    return Parallel(suitTrack, partTrack1, partTrack2, waterfallTrack, toonTracks)
