from typing import Literal

from re import M
from .BattleBase import *
import random
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from . import StatusEffects
notify = DirectNotifyGlobal.directNotify.newCategory('SuitBattleGlobals')
debugAttackSequence = {}


class Targeting:
    '''
    Use this class to replace the constants and better determine how the attacks will target a Toon.
    '''

    def __init__(self, side: Literal['toon', 'suit'], numTargets: int | Literal['all'], selfTarget: Literal['can', 'must', 'cannot'] = 'can'):
        '''
        Parameters:
            side (str): Which side the Cog will choose to aim for, either 'toon' or 'suit'.
            numTargets (int|str): The number of targets that will be affected by the attack, which is either an int or 'all'.\n
                                  This parameter is only really relevant if side is 'suit', as Toontown Fantasy is single-player, but it can be used for determining camera angles.
            selfTarget (str): Whether or not an attacker can target themselves with an attack.  Valid choices are 'can', which means the attacker can target themselves if given the chance, 'must', which means the attacker must be one of the targets, or 'cannot', which means the attacker cannot be selected.\n
                              This is ignored if side is 'toon'.
        
        Raises:
            TypeError: Raise a TypeError if the arguments are not the correct type.
        '''
        if not isinstance(side, str):
            raise TypeError
        if side not in ('toon', 'suit'):
            raise ValueError("side is supposed to be either 'toon' or 'suit', but it's '{}' here!".format(side))
        # Here, numTargets can alternatively be 'all' rather than an int.
        if isinstance(numTargets, int):
            if numTargets < 0:
                raise ValueError("numTargets int must be greater than or equal to 0 (it's {} here)!".format(numTargets))
        elif numTargets != 'all':
            raise TypeError
        if not isinstance(selfTarget, str):
            raise TypeError
        if selfTarget not in ('can', 'must', 'cannot'):
            raise ValueError("selfTarget is supposed to be 'can', 'must', or 'cannot', but it's '{}' here!".format(selfTarget))
        self.side: Literal['toon', 'suit'] = side
        self.numTargets: int | Literal['all'] = numTargets
        self.selfTarget: Literal['can', 'must', 'cannot'] = selfTarget


class SuitAttack:
    '''
    Instead of using tuples, we will use this object for a Cog's attack.
    '''

    def __init__(self, name: str, /, hp: tuple[int, ...], acc: tuple[int, ...], freq: tuple[int, ...], effects: tuple[StatusEffects.StatusEffect, ...] = (), targets: int | Targeting | None = None) -> None:
        '''
        Parameters:
            name (str): The Cog attack that will be displayed via the movie.
            hp (tuple): The hit points of the attack by level.
            acc (tuple): The accuracy of the attack by level.
            freq (tuple): The frequency of the attack by level.
            effects (tuple): A list of effects that will be applied if the attack lands.  They must be a StatusEffect!
            targets (Targeting|None): Who will be affected by the attack.
        '''
        if not isinstance(name, str):
            raise TypeError
        if not isinstance(hp, tuple):
            raise TypeError
        if not isinstance(acc, tuple):
            raise TypeError
        if not isinstance(freq, tuple):
            raise TypeError
        if not isinstance(effects, tuple):
            raise TypeError
        if targets in (ATK_TGT_UNKNOWN, ATK_TGT_SINGLE, ATK_TGT_GROUP):
            pass # TODO: Stop relying on constants for targeting.
        elif not isinstance(targets, (Targeting, type(None))):
            raise TypeError
        self.name: str = name
        self.hp: tuple[int, ...] = hp
        self.acc: tuple[int, ...] = acc
        self.freq: tuple[int, ...] = freq
        self.effects: tuple[StatusEffects.StatusEffect, ...] = effects
        self.targets: Targeting | int
        if targets == None:
            self.targets = SuitAttacks[self.name][1] # If it's None, then we can have a default.
        else:
            self.targets = targets


class SuitAttributes:
    
    def __init__(self, *, name: str, singularname: str, pluralname: str, level: int, hp: tuple[int, ...], defense: tuple[int, ...], freq: tuple[int, ...], acc: tuple[int, ...], attacks: tuple[SuitAttack, ...]) -> None:
        '''
        Parameters:
            name (str): The Cog's name.
            singularname (str): How the Cog is referred to singularly (e.g. "a Flunky", "an Ambulance Chaser").
            pluralname (str): How the Cog is referred to plurally (e.g. "Telemarketers", "Flunkies", "Movers & Shakers").
            level (int): The minimum level of the Cog.  NOTE: Levels are zero-based and will be one more than listed in-game.
            hp (tuple): A list of health points for a Cog based on level.  NOTE: The standard formula for a Cog's health is: <i>x</i><sup>2</sup> + 3<i>x</i> + 2, where <i>x</i> is the Cog's level.
            defense (tuple): A list of values that affect a Cog's ability to dodge based on level.
            freq (tuple): If a level for the Cog cannot be returned, fall back to a random level with values from this list.
            acc (tuple): The accuracy of this Cog and their attack's accuracy are averaged.  TODO: Remove, since this is outdated and the accuracies we should want are already listed in the Cog's attack.
            attacks (tuple): A list of Cog attacks for the Cog to use.
        '''
        self.name: str = name
        self.singularname: str = singularname
        self.pluralname: str = pluralname
        self.level: int = level
        self.hp: tuple[int, ...] = hp
        self.defense: tuple[int, ...] = defense
        self.freq: tuple[int, ...] = freq
        self.acc: tuple[int, ...] = acc
        self.attacks: tuple[SuitAttack, ...] = attacks


def pickFromFreqList(freqList):
    randNum = random.randint(0, 99)
    count = 0
    index = 0
    level = None
    for f in freqList:
        count = count + f
        if randNum < count:
            level = index
            break
        index = index + 1

    return level


def getActualFromRelativeLevel(name: str, relLevel):
    data: SuitAttributes = SuitAttributesDict[name]
    actualLevel = data.level + relLevel
    return actualLevel


def getSuitVitals(name: str, level=-1):
    data: SuitAttributes = SuitAttributesDict[name]
    if level == -1:
        level = pickFromFreqList(data.freq)
    dict = {}
    dict['level'] = getActualFromRelativeLevel(name, level)
    if dict['level'] == 11:
        level = 0
    dict['hp'] = data.hp[level]
    dict['def'] = data.defense[level]
    attacks: tuple[SuitAttack, ...] = data.attacks
    alist = []
    for a in attacks:
        adict = {}
        name: str = a.name
        adict['name'] = name
        adict['animName'] = SuitAttacks[name][0]
        adict['hp'] = a.hp[level]
        adict['acc'] = a.acc[level]
        adict['freq'] = a.freq[level]
        adict['group'] = a.targets
        alist.append(adict)

    dict['attacks'] = alist
    return dict


def pickSuitAttack(attacks: tuple[SuitAttack, ...], suitLevel: int):
    attackNum = None
    randNum = random.randint(0, 99)
    notify.debug('pickSuitAttack: rolled %d' % randNum)
    count = 0
    index = 0
    total = 0
    for c in attacks:
        total = total + c.freq[suitLevel]

    for c in attacks:
        count = count + c.freq[suitLevel]
        if randNum < count:
            attackNum = index
            notify.debug('picking attack %d' % attackNum)
            break
        index = index + 1

    configAttackName = simbase.config.GetString('attack-type', 'random')
    if configAttackName == 'random':
        return attackNum
    elif configAttackName == 'sequence':
        for i in range(len(attacks)):
            if attacks[i] not in debugAttackSequence:
                debugAttackSequence[attacks[i]] = 1
                return i

        return attackNum
    else:
        for i in range(len(attacks)):
            if attacks[i].name == configAttackName:
                return i

        return attackNum
    return


def getSuitAttack(suitName: str, suitLevel: int, attackNum: int = -1) -> dict:
    attackChoices: tuple[SuitAttack, ...] = SuitAttributesDict[suitName].attacks
    if attackNum == -1:
        notify.debug('getSuitAttack: picking attacking for %s' % suitName)
        attackNum = pickSuitAttack(attackChoices, suitLevel)
    attack: SuitAttack = attackChoices[attackNum]
    adict = {}
    adict['suitName'] = suitName
    name: str = attack.name
    adict['name'] = name
    adict['id'] = list(SuitAttacks.keys()).index(name)
    adict['animName'] = SuitAttacks[name][0]
    # TODO: Get around to adding status effects.
    adict['hp'] = attack.hp[suitLevel]
    adict['acc'] = attack.acc[suitLevel]
    adict['freq'] = attack.freq[suitLevel]
    adict['group'] = attack.targets
    return adict


ATK_TGT_UNKNOWN: Literal[1] = 1
ATK_TGT_SINGLE: Literal[2] = 2
ATK_TGT_GROUP: Literal[3] = 3
SuitAttributesDict: dict[str, SuitAttributes] = {'f': SuitAttributes(name=TTLocalizer.SuitFlunky,
                     singularname=TTLocalizer.SuitFlunkyS,
                     pluralname=TTLocalizer.SuitFlunkyP,
                     level=0,
                     hp=(6, 12, 20, 30, 42),
                     defense=(2, 5, 10, 15, 20),
                     freq=(50, 30, 10, 5, 5),
                     acc=(35, 40, 45, 50, 55),
                     attacks=(SuitAttack('PoundKey',
                                            hp=(2, 2, 3, 4, 6),
                                            acc=(75, 75, 80, 80, 90),
                                            freq=(30, 35, 40, 45, 50),
                                            targets=ATK_TGT_SINGLE),
                                 SuitAttack('Shred',
                                            hp=(3, 4, 5, 6, 7),
                                            acc=(50, 55, 60, 65, 70),
                                            freq=(10, 15, 20, 25, 30),
                                            targets=ATK_TGT_SINGLE),
                                 SuitAttack('ClipOnTie',
                                            hp=(1, 1, 2, 2, 3),
                                            acc=(75, 80, 85, 90, 95),
                                            freq=(60, 50, 40, 30, 20),
                                            targets=ATK_TGT_SINGLE))),
 'p': SuitAttributes(name=TTLocalizer.SuitPencilPusher,
                     singularname=TTLocalizer.SuitPencilPusherS,
                     pluralname=TTLocalizer.SuitPencilPusherP,
                     level=1,
                     hp=(12, 20, 30, 42, 56),
                     defense=(5, 10, 15, 20, 25),
                     freq=(50, 30, 10, 5, 5),
                     acc=(45, 50, 55, 60, 65),
                     attacks=(SuitAttack('FountainPen',
                                         hp=(2, 3, 4, 6, 9),
                                         acc=(75, 75, 75, 75, 75),
                                         freq=(20, 20, 20, 20, 20),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('RubOut',
                                         hp=(4, 5, 6, 8, 11),
                                         acc=(75, 75, 75, 75, 75),
                                         freq=(20, 20, 20, 20, 20),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('FingerWag',
                                         hp=(1, 2, 2, 3, 4),
                                         acc=(75, 75, 75, 75, 75),
                                         freq=(35, 30, 25, 20, 15),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('WriteOff',
                                         hp=(4, 6, 8, 10, 12),
                                         acc=(75, 75, 75, 75, 75),
                                         freq=(5, 10, 15, 20, 25),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('FillWithLead',
                                         hp=(3, 4, 5, 6, 7),
                                         acc=(75, 75, 75, 75, 75),
                                         freq=(20, 20, 20, 20, 20),
                                         targets=ATK_TGT_SINGLE))),
 'ym': SuitAttributes(name=TTLocalizer.SuitYesman,
                      singularname=TTLocalizer.SuitYesmanS,
                      pluralname=TTLocalizer.SuitYesmanP,
                      level=2,
                      hp=(20, 30, 42, 56, 72),
                      defense=(10, 15, 20, 25, 30),
                      freq=(50, 30, 10, 5, 5),
                      acc=(65, 70, 75, 80, 85),
                      attacks=(SuitAttack('RubberStamp',
                                          hp=(3, 4, 6, 8, 9),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('RazzleDazzle',
                                          hp=(3, 5, 7, 9, 11),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(25, 20, 15, 10, 5),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Synergy',
                                          hp=(4, 5, 6, 7, 8),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(5, 10, 15, 20, 25),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('TeeOff',
                                          hp=(3, 5, 8, 11, 14),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE))),
 'mm': SuitAttributes(name=TTLocalizer.SuitMicromanager,
                      singularname=TTLocalizer.SuitMicromanagerS,
                      pluralname=TTLocalizer.SuitMicromanagerP,
                      level=3,
                      hp=(30, 42, 56, 72, 90),
                      defense=(15, 20, 25, 30, 35),
                      freq=(50, 30, 10, 5, 5),
                      acc=(70, 75, 80, 82, 85),
                      attacks=(SuitAttack('Demotion',
                                          hp=(6, 8, 12, 15, 18),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FingerWag',
                                          hp=(4, 6, 9, 12, 15),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(10, 10, 10, 10, 10),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FountainPen',
                                          hp=(3, 4, 6, 8, 10),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('BrainStorm',
                                          hp=(4, 6, 9, 12, 15),
                                          acc=(5, 5, 5, 5, 5),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('BuzzWord',
                                          hp=(4, 6, 9, 12, 15),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE))),
 'ds': SuitAttributes(name=TTLocalizer.SuitDownsizer,
                      singularname=TTLocalizer.SuitDownsizerS,
                      pluralname=TTLocalizer.SuitDownsizerP,
                      level=4,
                      hp=(42, 56, 72, 90, 110),
                      defense=(20, 25, 30, 35, 40),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('Canned',
                                          hp=(5, 6, 8, 10, 12),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Downsize',
                                          hp=(7, 9, 11, 14, 17),
                                          acc=(50, 65, 70, 75, 80),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PinkSlip',
                                          hp=(4, 5, 6, 8, 10),
                                          acc=(60, 65, 75, 80, 85),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Fired',
                                          hp=(6, 8, 10, 12, 14),
                                          acc=(70, 75, 80, 85, 90),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Sacked',
                                          hp=(5, 6, 8, 10, 12),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(10, 10, 10, 10, 10),
                                          targets=ATK_TGT_SINGLE))),
 'hh': SuitAttributes(name=TTLocalizer.SuitHeadHunter,
                      singularname=TTLocalizer.SuitHeadHunterS,
                      pluralname=TTLocalizer.SuitHeadHunterP,
                      level=5,
                      hp=(56, 72, 90, 110, 132),
                      defense=(25, 30, 35, 40, 45),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('FountainPen',
                                          hp=(5, 6, 8, 10, 12),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('GlowerPower',
                                          hp=(7, 8, 10, 12, 13),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('HalfWindsor',
                                          hp=(8, 10, 12, 14, 16),
                                          acc=(60, 65, 70, 75, 80),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('HeadShrink',
                                          hp=(10, 12, 15, 18, 21),
                                          acc=(65, 75, 80, 85, 95),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Rolodex',
                                          hp=(6, 7, 8, 9, 10),
                                          acc=(60, 65, 70, 75, 80),
                                          freq=(10, 10, 10, 10, 10),
                                          targets=ATK_TGT_SINGLE))),
 'cr': SuitAttributes(name=TTLocalizer.SuitCorporateRaider,
                      singularname=TTLocalizer.SuitCorporateRaiderS,
                      pluralname=TTLocalizer.SuitCorporateRaiderP,
                      level=6,
                      hp=(72, 90, 110, 132, 156),
                      defense=(30, 35, 40, 45, 50),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('Canned',
                                          hp=(6, 7, 8, 9, 10),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('EvilEye',
                                          hp=(12, 15, 18, 21, 24),
                                          acc=(60, 70, 75, 80, 90),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PlayHardball',
                                          hp=(7, 8, 12, 15, 16),
                                          acc=(60, 65, 70, 75, 80),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PickPocket',
                                          hp=(10, 12, 14, 16, 18),
                                          acc=(65, 75, 80, 85, 95),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE))),
 'tbc': SuitAttributes(name=TTLocalizer.SuitTheBigCheese,
                       singularname=TTLocalizer.SuitTheBigCheeseS,
                       pluralname=TTLocalizer.SuitTheBigCheeseP,
                       level=7,
                       hp=(90, 110, 132, 156, 182, 210, 240, 272, 306, 342, 380, 420, 462),
                       defense=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 80, 80, 80),
                       freq=(50, 30, 10, 5, 5),
                       acc=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95),
                       attacks=(SuitAttack('CigarSmoke',
                                           hp=(10, 12, 15, 18, 20, 20, 20, 20, 21, 21, 21, 21, 22),
                                           acc=(55, 65, 75, 85, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                           freq=(20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20),
                                           targets=ATK_TGT_SINGLE),
                                SuitAttack('GlowerPower',
                                           hp=(14, 16, 18, 20, 22, 22, 22, 22, 23, 23, 23, 23, 24),
                                           acc=(70, 75, 85, 90, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                           freq=(20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20),
                                           targets=ATK_TGT_SINGLE),
                                SuitAttack('PowerTrip',
                                           hp=(14, 15, 17, 19, 20, 20, 20, 20, 21, 21, 21, 21, 22),
                                           acc=(60, 65, 70, 75, 80, 80, 80, 80, 80, 80, 80, 80, 80),
                                           freq=(50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50),
                                           targets=ATK_TGT_GROUP),
                                SuitAttack('TeeOff',
                                           hp=(12, 15, 18, 21, 24, 24, 24, 24, 25, 25, 25, 25, 26),
                                           acc=(55, 65, 70, 75, 80, 80, 80, 80, 80, 80, 80, 80, 80),
                                           freq=(10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10),
                                           targets=ATK_TGT_SINGLE))),
 'cp': SuitAttributes(name=TTLocalizer.President,
                      singularname=TTLocalizer.APresident,
                      pluralname=TTLocalizer.PresidentP,
                      # Either level 11 or 12.  In the case one is desired over the other, data for both will exist.
                      level=10,
                      hp=(156, 182),
                      defense=(50, 55),
                      freq=(50, 50),
                      acc=(35, 40),
                      attacks=(SuitAttack('TeeOff',
                                          hp=(21, 24),
                                          acc=(75, 75),
                                          freq=(35, 35),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('SandTrap',
                                          hp=(20, 23),
                                          acc=(70, 70),
                                          freq=(20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PowerTrip',
                                          hp=(19, 21),
                                          acc=(50, 50),
                                          freq=(15, 15),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('Filibuster',
                                          hp=(16, 17),
                                          acc=(75, 75),
                                          freq=(15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('BuzzWord', # Write Off would be nice in this attack's place, but there's no 'hold-pencil' animation for suitA Cogs.
                                          hp=(20, 22),
                                          acc=(75, 75),
                                          freq=(15, 15),
                                          targets=ATK_TGT_SINGLE))),
 'cc': SuitAttributes(name=TTLocalizer.SuitColdCaller,
                      singularname=TTLocalizer.SuitColdCallerS,
                      pluralname=TTLocalizer.SuitColdCallerP,
                      level=0,
                      hp=(6, 12, 20, 30, 42),
                      defense=(2, 5, 10, 15, 20),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('FreezeAssets',
                                          hp=(3, 4, 6, 8, 10),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(45, 40, 35, 30, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PoundKey',
                                          hp=(2, 2, 3, 4, 5),
                                          acc=(75, 80, 85, 90, 95),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('MumboJumbo',
                                          hp=(2, 3, 4, 5, 7),
                                          acc=(50, 55, 60, 65, 70),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Watercooler',
                                          hp=(1, 1, 1, 1, 1),
                                          acc=(90, 90, 90, 90, 90),
                                          freq=(5, 10, 15, 20, 25),
                                          targets=ATK_TGT_SINGLE))),
 'tm': SuitAttributes(name=TTLocalizer.SuitTelemarketer,
                      singularname=TTLocalizer.SuitTelemarketerS,
                      pluralname=TTLocalizer.SuitTelemarketerP,
                      level=1,
                      hp=(12, 20, 30, 42, 56),
                      defense=(5, 10, 15, 20, 25),
                      freq=(50, 30, 10, 5, 5),
                      acc=(45, 50, 55, 60, 65),
                      attacks=(SuitAttack('MumboJumbo',
                                          hp=(2, 2, 3, 3, 4),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PickPocket',
                                          hp=(1, 1, 1, 1, 1),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Rolodex',
                                          hp=(4, 6, 8, 10, 12),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PoundKey',
                                          hp=(4, 6, 7, 9, 12),
                                          acc=(75, 80, 85, 90, 95),
                                          freq=(40, 40, 40, 40, 40),
                                          targets=ATK_TGT_SINGLE))),
 'nd': SuitAttributes(name=TTLocalizer.SuitNameDropper,
                      singularname=TTLocalizer.SuitNameDropperS,
                      pluralname=TTLocalizer.SuitNameDropperP,
                      level=2,
                      hp=(20, 30, 42, 56, 72),
                      defense=(10, 15, 20, 25, 30),
                      freq=(50, 30, 10, 5, 5),
                      acc=(65, 70, 75, 80, 85),
                      attacks=(SuitAttack('RazzleDazzle',
                                             hp=(4, 5, 6, 8, 11),
                                             acc=(75, 80, 85, 90, 95),
                                             freq=(30, 30, 30, 30, 30),
                                             targets=ATK_TGT_SINGLE),
                                  SuitAttack('Rolodex',
                                             hp=(5, 6, 7, 9, 12),
                                             acc=(95, 95, 95, 95, 95),
                                             freq=(40, 40, 40, 40, 40),
                                             targets=ATK_TGT_SINGLE),
                                  SuitAttack('Synergy',
                                             hp=(3, 4, 6, 9, 10),
                                             acc=(50, 50, 50, 50, 50),
                                             freq=(15, 15, 15, 15, 15),
                                             targets=ATK_TGT_GROUP),
                                  SuitAttack('SpeedDial',
                                             hp=(2, 3, 4, 5, 7),
                                             acc=(95, 95, 95, 95, 95),
                                             freq=(15, 15, 15, 15, 15),
                                             targets=ATK_TGT_SINGLE))),
 'gh': SuitAttributes(name=TTLocalizer.SuitGladHander,
                      singularname=TTLocalizer.SuitGladHanderS,
                      pluralname=TTLocalizer.SuitGladHanderP,
                      level=3,
                      hp=(30, 42, 56, 72, 90),
                      defense=(15, 20, 25, 30, 35),
                      freq=(50, 30, 10, 5, 5),
                      acc=(70, 75, 80, 82, 85),
                      attacks=(SuitAttack('RubberStamp',
                                          hp=(4, 5, 5, 6, 7),
                                          acc=(90, 70, 50, 30, 10),
                                          freq=(40, 30, 20, 10, 5),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FountainPen',
                                          hp=(3, 3, 4, 5, 5),
                                          acc=(70, 60, 50, 40, 30),
                                          freq=(40, 30, 20, 10, 5),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Filibuster',
                                          hp=(4, 6, 8, 10, 13),
                                          acc=(30, 40, 50, 60, 70),
                                          freq=(10, 20, 30, 40, 45),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Schmooze',
                                          hp=(5, 7, 10, 13, 15),
                                          acc=(55, 65, 75, 85, 95),
                                          freq=(10, 20, 30, 40, 45),
                                          targets=ATK_TGT_SINGLE))),
 'ms': SuitAttributes(name=TTLocalizer.SuitMoverShaker,
                      singularname=TTLocalizer.SuitMoverShakerS,
                      pluralname=TTLocalizer.SuitMoverShakerP,
                      level=4,
                      hp=(42, 56, 72, 90, 110),
                      defense=(20, 25, 30, 35, 40),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('BrainStorm',
                                          hp=(5, 6, 8, 10, 12),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Schmooze',
                                          hp=(5, 7, 9, 11, 13),
                                          acc=(50, 65, 70, 75, 80),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Quake',
                                          hp=(6, 9, 11, 13, 16),
                                          acc=(60, 65, 75, 80, 85),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('Shake',
                                          hp=(6, 8, 10, 12, 14),
                                          acc=(70, 75, 80, 85, 90),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('Tremor',
                                          hp=(5, 6, 7, 8, 9),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_GROUP))),
 'tf': SuitAttributes(name=TTLocalizer.SuitTwoFace,
                      singularname=TTLocalizer.SuitTwoFaceS,
                      pluralname=TTLocalizer.SuitTwoFaceP,
                      level=5,
                      hp=(56, 72, 90, 110, 132),
                      defense=(25, 30, 35, 40, 45),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('EvilEye',
                                          hp=(10, 12, 14, 16, 18),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('HangUp',
                                          hp=(7, 8, 10, 12, 13),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('DoubleWindsor',
                                          hp=(8, 10, 12, 14, 16),
                                          acc=(60, 65, 70, 75, 80),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('RedTape',
                                          hp=(6, 7, 8, 9, 10),
                                          acc=(60, 65, 75, 85, 90),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('SensoryOverload',  # This move would reduce a Toon's accuracy.
                                          hp=(0, 0, 0, 0, 0), # This is where the accuracy reduction should probably go.
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(0, 0, 0, 0, 0),
                                          targets=ATK_TGT_SINGLE))),
 'm': SuitAttributes(name=TTLocalizer.SuitTheMingler,
                     singularname=TTLocalizer.SuitTheMinglerS,
                     pluralname=TTLocalizer.SuitTheMinglerP,
                     level=6,
                     hp=(72, 90, 110, 132, 156),
                     defense=(30, 35, 40, 45, 50),
                     freq=(50, 30, 10, 5, 5),
                     acc=(35, 40, 45, 50, 55),
                     attacks=(SuitAttack('BuzzWord',
                                         hp=(10, 11, 13, 15, 16),
                                         acc=(60, 75, 80, 85, 90),
                                         freq=(20, 20, 20, 20, 20),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('Schmooze',
                                         hp=(12, 15, 18, 21, 24),
                                         acc=(60, 70, 75, 80, 90),
                                         freq=(25, 25, 25, 25, 25),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('RazzleDazzle',
                                         hp=(10, 13, 14, 15, 18),
                                         acc=(60, 65, 70, 75, 80),
                                         freq=(15, 15, 15, 15, 15),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('ParadigmShift',
                                         hp=(7, 8, 12, 15, 16),
                                         acc=(55, 65, 75, 85, 95),
                                         freq=(30, 30, 30, 30, 30),
                                         targets=ATK_TGT_GROUP),
                              SuitAttack('TeeOff',
                                         hp=(8, 9, 10, 11, 12),
                                         acc=(70, 75, 80, 85, 95),
                                         freq=(10, 10, 10, 10, 10),
                                         targets=ATK_TGT_SINGLE))),
 'mh': SuitAttributes(name=TTLocalizer.SuitMrHollywood,
                      singularname=TTLocalizer.SuitMrHollywoodS,
                      pluralname=TTLocalizer.SuitMrHollywoodP,
                      level=7,
                      hp=(90, 110, 132, 156, 182, 210, 240, 272, 306, 342, 380, 420, 462),
                      defense=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 80, 80, 80),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95),
                      attacks=(SuitAttack('PowerTrip',
                                          hp=(10, 12, 15, 18, 20, 20, 20, 20, 21, 21, 21, 21, 22),
                                          acc=(55, 65, 75, 85, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                          freq=(25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('RazzleDazzle',
                                          hp=(8, 11, 14, 17, 20, 20, 20, 20, 21, 21, 21, 21, 22),
                                          acc=(70, 75, 85, 90, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                          freq=(25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('TeeOff',
                                          hp=(14, 15, 17, 19, 20, 20, 20, 20, 21, 21, 21, 21, 22),
                                          acc=(60, 65, 70, 75, 80, 80, 80, 80, 80, 80, 80, 80, 80),
                                          freq=(25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('SongAndDance',
                                          hp=(12, 14, 16, 18, 20, 20, 20, 20, 21, 21, 21, 21, 22),
                                          acc=(65, 75, 80, 85, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                          freq=(25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25),
                                          targets=ATK_TGT_GROUP))),
 'ff': SuitAttributes(name=TTLocalizer.Foreman,
                      singularname=TTLocalizer.AForeman,
                      pluralname=TTLocalizer.ForemanP,
                      level=8,
                      hp=(110,),
                      defense=(40,),
                      freq=(100,),
                      acc=(35,),
                      attacks=(SuitAttack('CigarSmoke',
                                          hp=(8,),
                                          acc=(70,),
                                          freq=(20,),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Stomper',
                                          hp=(10,),
                                          acc=(90,),
                                          freq=(15,),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('ReOrg',
                                          hp=(7,),
                                          acc=(75,),
                                          freq=(30,),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('TeeOff',
                                          hp=(6,),
                                          acc=(60,),
                                          freq=(15,),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Canned',
                                          hp=(7,),
                                          acc=(50,),
                                          freq=(20,),
                                          targets=ATK_TGT_SINGLE))),
 'sc': SuitAttributes(name=TTLocalizer.SuitShortChange,
                      singularname=TTLocalizer.SuitShortChangeS,
                      pluralname=TTLocalizer.SuitShortChangeP,
                      level=0,
                      hp=(6, 12, 20, 30, 42),
                      defense=(2, 5, 10, 15, 20),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('FreezeAssets',
                                          hp=(2, 2, 3, 4, 6),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('BounceCheck',
                                          hp=(3, 5, 7, 9, 11),
                                          acc=(75, 80, 85, 90, 95),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('ClipOnTie',
                                          hp=(1, 1, 2, 2, 3),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PickPocket',
                                          hp=(2, 2, 3, 4, 6),
                                          acc=(95, 95, 95, 95, 95),
                                          freq=(40, 40, 40, 40, 40),
                                          targets=ATK_TGT_SINGLE))),
 'pp': SuitAttributes(name=TTLocalizer.SuitPennyPincher,
                      singularname=TTLocalizer.SuitPennyPincherS,
                      pluralname=TTLocalizer.SuitPennyPincherP,
                      level=1,
                      hp=(12, 20, 30, 42, 56),
                      defense=(5, 10, 15, 20, 25),
                      freq=(50, 30, 10, 5, 5),
                      acc=(45, 50, 55, 60, 65),
                      attacks=(SuitAttack('BounceCheck',
                                          hp=(4, 5, 6, 8, 12),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(40, 40, 40, 40, 40),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FreezeAssets',
                                          hp=(2, 3, 4, 6, 9),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FingerWag',
                                          hp=(1, 2, 3, 4, 6),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PennyPinch',
                                          hp=(5, 7, 9, 11, 13),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE))),
 'tw': SuitAttributes(name=TTLocalizer.SuitTightwad,
                      singularname=TTLocalizer.SuitTightwadS,
                      pluralname=TTLocalizer.SuitTightwadP,
                      level=2,
                      hp=(20, 30, 42, 56, 72),
                      defense=(10, 15, 20, 25, 30),
                      freq=(50, 30, 10, 5, 5),
                      acc=(65, 70, 75, 80, 85),
                      attacks=(SuitAttack('PickPocket',
                                          hp=(3, 4, 5, 5, 6),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(75, 5, 5, 5, 5),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('GlowerPower',
                                          hp=(3, 4, 6, 9, 12),
                                          acc=(95, 95, 95, 95, 95),
                                          freq=(10, 15, 20, 25, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FingerWag',
                                          hp=(3, 3, 4, 4, 5),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(5, 70, 5, 5, 5),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('BounceCheck',
                                          hp=(3, 4, 6, 9, 12),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(5, 5, 65, 5, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FreezeAssets',
                                          hp=(5, 6, 9, 13, 18),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(5, 5, 5, 60, 30),
                                          targets=ATK_TGT_SINGLE))),
 'bc': SuitAttributes(name=TTLocalizer.SuitBeanCounter,
                      singularname=TTLocalizer.SuitBeanCounterS,
                      pluralname=TTLocalizer.SuitBeanCounterP,
                      level=3,
                      hp=(30, 42, 56, 72, 90),
                      defense=(15, 20, 25, 30, 35),
                      freq=(50, 30, 10, 5, 5),
                      acc=(70, 75, 80, 82, 85),
                      attacks=(SuitAttack('Audit',
                                          hp=(4, 6, 7, 8, 10),
                                          acc=(55, 65, 75, 85, 95),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Calculate',
                                          hp=(3, 6, 9, 12, 15),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Tabulate',
                                          (5, 6, 8, 10, 13),
                                          (55, 60, 70, 75, 85),
                                          (25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('WriteOff',
                                          (6, 7, 9, 12, 14),
                                          (60, 70, 75, 80, 90),
                                          (30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE))),
 'nc': SuitAttributes(name=TTLocalizer.SuitNumberCruncher,
                      singularname=TTLocalizer.SuitNumberCruncherS,
                      pluralname=TTLocalizer.SuitNumberCruncherP,
                      level=4,
                      hp=(42, 56, 72, 90, 110),
                      defense=(20, 25, 30, 35, 40),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('Audit',
                                          hp=(5, 6, 8, 10, 12),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Calculate',
                                          hp=(6, 7, 9, 11, 13),
                                          acc=(50, 65, 70, 75, 80),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Crunch',
                                          hp=(8, 9, 11, 13, 15),
                                          acc=(60, 65, 75, 80, 85),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Tabulate',
                                          hp=(5, 6, 7, 8, 9),
                                          acc=(50, 50, 50, 50, 50),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE))),
 'mb': SuitAttributes(name=TTLocalizer.SuitMoneyBags,
                      singularname=TTLocalizer.SuitMoneyBagsS,
                      pluralname=TTLocalizer.SuitMoneyBagsP,
                      level=5,
                      hp=(56, 72, 90, 110, 132),
                      defense=(25, 30, 35, 40, 45),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('MarketCrash',
                                          hp=(10, 12, 14, 16, 18),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FloodTheMarket',
                                          hp=(8, 10, 12, 14, 16),
                                          acc=(60, 65, 70, 75, 80),
                                          freq=(45, 45, 45, 45, 45),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('Liquidate',
                                          hp=(6, 7, 8, 9, 10),
                                          acc=(60, 65, 75, 85, 90),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE))),
 'ls': SuitAttributes(name=TTLocalizer.SuitLoanShark,
                      singularname=TTLocalizer.SuitLoanSharkS,
                      pluralname=TTLocalizer.SuitLoanSharkP,
                      level=6,
                      hp=(72, 90, 110, 132, 156),
                      defense=(30, 35, 40, 45, 50),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('Bite',
                                          hp=(10, 11, 13, 15, 16),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Chomp',
                                          hp=(12, 15, 18, 21, 24),
                                          acc=(60, 70, 75, 80, 90),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PlayHardball',
                                          hp=(9, 11, 12, 13, 15),
                                          acc=(55, 65, 75, 85, 95),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('WriteOff',
                                          hp=(6, 8, 10, 12, 14),
                                          acc=(70, 75, 80, 85, 95),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE))),
 'rb': SuitAttributes(name=TTLocalizer.SuitRobberBaron,
                      singularname=TTLocalizer.SuitRobberBaronS,
                      pluralname=TTLocalizer.SuitRobberBaronP,
                      level=7,
                      hp=(90, 110, 132, 156, 182, 210, 240, 272, 306, 342, 380, 420, 462),
                      defense=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 80, 80, 80),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95),
                      attacks=(SuitAttack('UndergroundLiquidity',
                                          hp=(14, 17, 19, 21, 24, 24, 24, 24, 25, 25, 25, 25, 26),
                                          acc=(55, 65, 75, 85, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                          freq=(25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FloodTheMarket',
                                          hp=(12, 15, 18, 21, 24, 24, 24, 24, 25, 25, 25, 25, 26),
                                          acc=(70, 75, 85, 90, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                          freq=(25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('PowerTrip',
                                          hp=(11, 14, 16, 18, 21, 21, 21, 21, 22, 22, 22, 22, 23),
                                          acc=(60, 65, 70, 75, 80, 80, 80, 80, 80, 80, 80, 80, 80),
                                          freq=(25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('PickPocket',
                                          hp=(10, 12, 14, 16, 18, 18, 18, 18, 19, 19, 19, 19, 20),
                                          acc=(60, 65, 75, 85, 90, 90, 90, 90, 90, 90, 90, 90, 90),
                                          freq=(25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE))),
 'msv': SuitAttributes(name=TTLocalizer.Supervisor,
                       singularname=TTLocalizer.ASupervisor,
                       pluralname=TTLocalizer.SupervisorP,
                       level=11,
                       hp=(182,),
                       defense=(55,),
                       freq=(100,),
                       acc=(35,),
                       attacks=(SuitAttack('FreezeAssets',
                                           hp=(15,),
                                           acc=(70,),
                                           freq=(20,),
                                           targets=ATK_TGT_SINGLE),
                                SuitAttack('EvilEye',
                                           hp=(12,),
                                           acc=(85,),
                                           freq=(20,),
                                           targets=ATK_TGT_SINGLE),
                                SuitAttack('GlowerPower',
                                           hp=(12,),
                                           acc=(50,),
                                           freq=(30,),
                                           targets=ATK_TGT_SINGLE),
                                SuitAttack('Stomper',
                                           hp=(15,),
                                           acc=(75,),
                                           freq=(30,),
                                           targets=ATK_TGT_SINGLE))),
 'bf': SuitAttributes(name=TTLocalizer.SuitBottomFeeder,
                      singularname=TTLocalizer.SuitBottomFeederS,
                      pluralname=TTLocalizer.SuitBottomFeederP,
                      level=0,
                      hp=(6, 12, 20, 30, 42),
                      defense=(2, 5, 10, 15, 20),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('Canned',
                                          hp=(2, 3, 4, 5, 6),
                                          acc=(75, 80, 85, 90, 95),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Shred',
                                          hp=(2, 4, 6, 8, 10),
                                          acc=(50, 55, 60, 65, 70),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Watercooler',
                                          hp=(3, 4, 5, 6, 7),
                                          acc=(95, 95, 95, 95, 95),
                                          freq=(10, 10, 10, 10, 10),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PickPocket',
                                          hp=(1, 1, 2, 2, 3),
                                          acc=(25, 30, 35, 40, 45),
                                          freq=(50, 50, 50, 50, 50),
                                          targets=ATK_TGT_SINGLE))),
 'b': SuitAttributes(name=TTLocalizer.SuitBloodsucker,
                     singularname=TTLocalizer.SuitBloodsuckerS,
                     pluralname=TTLocalizer.SuitBloodsuckerP,
                     level=1,
                     hp=(12, 20, 30, 42, 56),
                     defense=(5, 10, 15, 20, 25),
                     freq=(50, 30, 10, 5, 5),
                     acc=(45, 50, 55, 60, 65),
                     attacks=(SuitAttack('Bite',
                                         hp=(1, 2, 3, 3, 4),
                                         acc=(75, 75, 75, 75, 75),
                                         freq=(20, 20, 20, 20, 20),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('PickPocket',
                                         hp=(2, 3, 4, 6, 9),
                                         acc=(75, 75, 75, 75, 75),
                                         freq=(20, 20, 20, 20, 20),
                                         targets=ATK_TGT_SINGLE),
                              SuitAttack('Withdrawal',
                                         hp=(6, 8, 10, 12, 14),
                                         acc=(95, 95, 95, 95, 95),
                                         freq=(10, 10, 10, 10, 10),
                                         targets=ATK_TGT_GROUP),
                              SuitAttack('Liquidate',
                                         hp=(2, 3, 4, 6, 9),
                                         acc=(50, 60, 70, 80, 90),
                                         freq=(50, 50, 50, 50, 50),
                                         targets=ATK_TGT_SINGLE))),
 'dt': SuitAttributes(name=TTLocalizer.SuitDoubleTalker,
                      singularname=TTLocalizer.SuitDoubleTalkerS,
                      pluralname=TTLocalizer.SuitDoubleTalkerP,
                      level=2,
                      hp=(20, 30, 42, 56, 72),
                      defense=(10, 15, 20, 25, 30),
                      freq=(50, 30, 10, 5, 5),
                      acc=(65, 70, 75, 80, 85),
                      attacks=(SuitAttack('RubberStamp',
                                          hp=(1, 1, 1, 1, 1),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(10, 10, 10, 10, 10),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('DoubleWindsor',
                                          hp=(1, 2, 3, 5, 6),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('DoubleTalk',
                                          hp=(6, 6, 9, 13, 18),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Jargon',
                                          hp=(3, 4, 6, 9, 12),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('MumboJumbo',
                                          hp=(3, 4, 6, 9, 12),
                                          acc=(50, 60, 70, 80, 90),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE))),
 'ac': SuitAttributes(name=TTLocalizer.SuitAmbulanceChaser,
                      singularname=TTLocalizer.SuitAmbulanceChaserS,
                      pluralname=TTLocalizer.SuitAmbulanceChaserP,
                      level=3,
                      hp=(30, 42, 56, 72, 90),
                      defense=(15, 20, 25, 30, 35),
                      freq=(50, 30, 10, 5, 5),
                      acc=(65, 70, 75, 80, 85),
                      attacks=(SuitAttack('Shake',
                                          hp=(4, 6, 9, 12, 15),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('RedTape',
                                          hp=(6, 8, 12, 15, 19),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Rolodex',
                                          hp=(3, 4, 5, 6, 7),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('SpeedDial',
                                          hp=(2, 3, 4, 5, 6),
                                          acc=(75, 75, 75, 75, 75),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE))),
 'bs': SuitAttributes(name=TTLocalizer.SuitBackStabber,
                      singularname=TTLocalizer.SuitBackStabberS,
                      pluralname=TTLocalizer.SuitBackStabberP,
                      level=4,
                      hp=(42, 56, 72, 90, 110),
                      defense=(20, 25, 30, 35, 40),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('GuiltTrip',
                                          hp=(8, 11, 13, 15, 18),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(40, 40, 40, 40, 40),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('GlowerPower',
                                          hp=(6, 7, 9, 11, 13),
                                          acc=(50, 65, 70, 75, 90),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('FingerWag',
                                          hp=(5, 6, 7, 8, 9),
                                          acc=(50, 55, 65, 75, 80),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE))),
 'sd': SuitAttributes(name=TTLocalizer.SuitSpinDoctor,
                      singularname=TTLocalizer.SuitSpinDoctorS,
                      pluralname=TTLocalizer.SuitSpinDoctorP,
                      level=5,
                      hp=(56, 72, 90, 110, 132),
                      defense=(25, 30, 35, 40, 45),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('ReOrg',
                                          hp=(9, 10, 13, 16, 17),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('ParadigmShift',
                                          hp=(8, 10, 12, 14, 16),
                                          acc=(60, 65, 70, 75, 80),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('Spin',
                                          hp=(10, 12, 15, 18, 20),
                                          acc=(70, 75, 80, 85, 90),
                                          freq=(35, 35, 35, 35, 35),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('WriteOff',
                                          hp=(6, 7, 8, 9, 10),
                                          acc=(60, 65, 75, 85, 90),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE))),
 'le': SuitAttributes(name=TTLocalizer.SuitLegalEagle,
                      singularname=TTLocalizer.SuitLegalEagleS,
                      pluralname=TTLocalizer.SuitLegalEagleP,
                      level=6,
                      hp=(72, 90, 110, 132, 156),
                      defense=(30, 35, 40, 45, 50),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55),
                      attacks=(SuitAttack('EvilEye',
                                          hp=(10, 11, 13, 15, 16),
                                          acc=(60, 75, 80, 85, 90),
                                          freq=(15, 15, 15, 15, 15),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Jargon',
                                          hp=(7, 9, 11, 13, 15),
                                          acc=(60, 70, 75, 80, 90),
                                          freq=(10, 10, 10, 10, 10),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Legalese',
                                          hp=(11, 13, 16, 19, 21),
                                          acc=(55, 65, 75, 85, 95),
                                          freq=(30, 30, 30, 30, 30),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PeckingOrder',
                                          hp=(12, 15, 18, 21, 24),
                                          acc=(70, 75, 80, 85, 95),
                                          freq=(25, 25, 25, 25, 25),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('LegalStorm',
                                          hp=(8, 10, 12, 14, 16),
                                          acc=(70, 75, 80, 85, 90),
                                          freq=(20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE))),
 'bw': SuitAttributes(name=TTLocalizer.SuitBigWig,
                      singularname=TTLocalizer.SuitBigWigS,
                      pluralname=TTLocalizer.SuitBigWigP,
                      level=7,
                      hp=(90, 110, 132, 156, 182, 210, 240, 272, 306, 342, 380, 420, 462),
                      defense=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 80, 80, 80),
                      freq=(50, 30, 10, 5, 5),
                      acc=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95),
                      attacks=(SuitAttack('FingerWag',
                                          hp=(12, 14, 16, 18, 20, 20, 20, 20, 21, 21, 21, 21, 22),
                                          acc=(65, 75, 85, 90, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                          freq=(20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Gavel',
                                          hp=(14, 16, 19, 22, 24, 24, 24, 24, 25, 25, 25, 25, 26),
                                          acc=(70, 75, 85, 90, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                          freq=(10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('PowerTrip',
                                          hp=(10, 11, 13, 15, 16, 16, 16, 16, 17, 17, 17, 17, 18),
                                          acc=(75, 80, 85, 90, 95, 95, 95, 95, 95, 95, 95, 95, 95),
                                          freq=(50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50),
                                          targets=ATK_TGT_GROUP),
                               SuitAttack('ThrowBook',
                                          hp=(13, 15, 17, 19, 21, 21, 21, 21, 22, 22, 22, 22, 23),
                                          acc=(80, 85, 85, 85, 90, 90, 90, 90, 90, 90, 90, 90, 90),
                                          freq=(20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20),
                                          targets=ATK_TGT_SINGLE))),
 'lc': SuitAttributes(name=TTLocalizer.Clerk,
                      singularname=TTLocalizer.AClerk,
                      pluralname=TTLocalizer.ClerkP,
                      level=11,
                      hp=(182,),
                      defense=(55,),
                      freq=(100,),
                      acc=(35),
                      attacks=(SuitAttack('Jargon',
                                          hp=(12,),
                                          acc=(75,),
                                          freq=(15,),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('RestrainingOrder',
                                          hp=(14,),
                                          acc=(60,),
                                          freq=(30,),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('ReOrg',
                                          hp=(16,),
                                          acc=(90,),
                                          freq=(25,),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('EvictionNotice',
                                          hp=(13,),
                                          acc=(75,),
                                          freq=(15,),
                                          targets=ATK_TGT_SINGLE),
                               SuitAttack('Stomper',
                                          hp=(14,),
                                          acc=(70,),
                                          freq=(15,),
                                          targets=ATK_TGT_SINGLE)))}
SuitAttacks = {'Audit': ('phone', ATK_TGT_SINGLE),
               'Bite': ('throw-paper', ATK_TGT_SINGLE),
               'BounceCheck': ('throw-paper', ATK_TGT_SINGLE),
               'BrainStorm': ('effort', ATK_TGT_SINGLE),
               'BuzzWord': ('speak', ATK_TGT_SINGLE),
               'Calculate': ('phone', ATK_TGT_SINGLE),
               'Canned': ('throw-paper', ATK_TGT_SINGLE),
               'Chomp': ('throw-paper', ATK_TGT_SINGLE),
               'CigarSmoke': ('cigar-smoke', ATK_TGT_SINGLE),
               'ClipOnTie': ('throw-paper', ATK_TGT_SINGLE),
               'Crunch': ('throw-object', ATK_TGT_SINGLE),
               'Demotion': ('magic1', ATK_TGT_SINGLE),
               'DoubleTalk': ('speak', ATK_TGT_SINGLE),
               'DoubleWindsor': ('throw-paper', ATK_TGT_SINGLE),
               'Downsize': ('magic2', ATK_TGT_SINGLE),
               'EvictionNotice': ('throw-paper', ATK_TGT_SINGLE),
               'EvilEye': ('glower', ATK_TGT_SINGLE),
               'Filibuster': ('speak', ATK_TGT_SINGLE),
               'FillWithLead': ('pencil-sharpener', ATK_TGT_SINGLE),
               'FingerWag': ('finger-wag', ATK_TGT_SINGLE),
               'Fired': ('magic2', ATK_TGT_SINGLE),
               'FiveOClockShadow': ('effort', ATK_TGT_SINGLE),
               'FloodTheMarket': ('effort', ATK_TGT_GROUP),
               'FountainPen': ('pen-squirt', ATK_TGT_SINGLE),
               'FreezeAssets': ('glower', ATK_TGT_SINGLE),
               'Gavel': ('effort', ATK_TGT_SINGLE),
               'GlowerPower': ('glower', ATK_TGT_SINGLE),
               'GuiltTrip': ('magic1', ATK_TGT_GROUP),
               'HalfWindsor': ('throw-paper', ATK_TGT_SINGLE),
               'HangUp': ('phone', ATK_TGT_SINGLE),
               'HeadShrink': ('magic1', ATK_TGT_SINGLE),
               'HotAir': ('speak', ATK_TGT_SINGLE),
               'Jargon': ('speak', ATK_TGT_SINGLE),
               'Kickback': ('effort', ATK_TGT_SINGLE),
               'Legalese': ('speak', ATK_TGT_SINGLE),
               'LegalStorm': ('effort', ATK_TGT_SINGLE),
               'Liquidate': ('magic1', ATK_TGT_SINGLE),
               'MarketCrash': ('throw-paper', ATK_TGT_SINGLE),
               'MumboJumbo': ('speak', ATK_TGT_SINGLE),
               'ParadigmShift': ('magic2', ATK_TGT_GROUP),
               'PeckingOrder': ('throw-object', ATK_TGT_SINGLE),
               'PennyPinch': ('pickpocket', ATK_TGT_SINGLE),
               'PickPocket': ('pickpocket', ATK_TGT_SINGLE),
               'PinkSlip': ('throw-paper', ATK_TGT_SINGLE),
               'PlayHardball': ('throw-paper', ATK_TGT_SINGLE),
               'PoundKey': ('phone', ATK_TGT_SINGLE),
               'PowerTie': ('throw-paper', ATK_TGT_SINGLE),
               'PowerTrip': ('magic1', ATK_TGT_GROUP),
               'Quake': ('quick-jump', ATK_TGT_GROUP),
               'RazzleDazzle': ('smile', ATK_TGT_SINGLE),
               'RedTape': ('throw-object', ATK_TGT_SINGLE),
               'ReOrg': ('magic3', ATK_TGT_SINGLE),
               'RestrainingOrder': ('throw-paper', ATK_TGT_SINGLE),
               'Rolodex': ('roll-o-dex', ATK_TGT_SINGLE),
               'RubberStamp': ('rubber-stamp', ATK_TGT_SINGLE),
               'RubOut': ('hold-eraser', ATK_TGT_SINGLE),
               'Sacked': ('throw-paper', ATK_TGT_SINGLE),
               'SandTrap': ('effort', ATK_TGT_SINGLE),
               'Schmooze': ('speak', ATK_TGT_SINGLE),
               'SensoryOverload': ('speak', ATK_TGT_SINGLE),
               'Shake': ('stomp', ATK_TGT_GROUP),
               'Shred': ('shredder', ATK_TGT_SINGLE),
               'SongAndDance': ('song-and-dance', ATK_TGT_GROUP),
               'SpeedDial': ('phone', ATK_TGT_SINGLE),
               'Spin': ('magic3', ATK_TGT_SINGLE),
               'Stomper': ('effort', ATK_TGT_SINGLE),
               'Synergy': ('magic3', ATK_TGT_GROUP),
               'Tabulate': ('phone', ATK_TGT_SINGLE),
               'TeeOff': ('golf-club-swing', ATK_TGT_SINGLE),
               'ThrowBook': ('throw-object', ATK_TGT_SINGLE),
               'Tremor': ('stomp', ATK_TGT_GROUP),
               'Trip': ('magic1', ATK_TGT_GROUP),
               'UndergroundLiquidity': ('magic1', ATK_TGT_SINGLE),
               'Watercooler': ('watercooler', ATK_TGT_SINGLE),
               'Withdrawal': ('magic1', ATK_TGT_GROUP),
               'WriteOff': ('hold-pencil', ATK_TGT_SINGLE),
               'WriteUp': ('hold-pencil', ATK_TGT_SINGLE)}
AUDIT = list(SuitAttacks.keys()).index('Audit')
BITE = list(SuitAttacks.keys()).index('Bite')
BOUNCE_CHECK = list(SuitAttacks.keys()).index('BounceCheck')
BRAIN_STORM = list(SuitAttacks.keys()).index('BrainStorm')
BUZZ_WORD = list(SuitAttacks.keys()).index('BuzzWord')
CALCULATE = list(SuitAttacks.keys()).index('Calculate')
CANNED = list(SuitAttacks.keys()).index('Canned')
CHOMP = list(SuitAttacks.keys()).index('Chomp')
CIGAR_SMOKE = list(SuitAttacks.keys()).index('CigarSmoke')
CLIPON_TIE = list(SuitAttacks.keys()).index('ClipOnTie')
CRUNCH = list(SuitAttacks.keys()).index('Crunch')
DEMOTION = list(SuitAttacks.keys()).index('Demotion')
DOUBLE_TALK = list(SuitAttacks.keys()).index('DoubleTalk')
DOUBLE_WINDSOR = list(SuitAttacks.keys()).index('DoubleWindsor')
DOWNSIZE = list(SuitAttacks.keys()).index('Downsize')
EVICTION_NOTICE = list(SuitAttacks.keys()).index('EvictionNotice')
EVIL_EYE = list(SuitAttacks.keys()).index('EvilEye')
FILIBUSTER = list(SuitAttacks.keys()).index('Filibuster')
FILL_WITH_LEAD = list(SuitAttacks.keys()).index('FillWithLead')
FINGER_WAG = list(SuitAttacks.keys()).index('FingerWag')
FIRED = list(SuitAttacks.keys()).index('Fired')
FIVE_O_CLOCK_SHADOW = list(SuitAttacks.keys()).index('FiveOClockShadow')
FLOOD_THE_MARKET = list(SuitAttacks.keys()).index('FloodTheMarket')
FOUNTAIN_PEN = list(SuitAttacks.keys()).index('FountainPen')
FREEZE_ASSETS = list(SuitAttacks.keys()).index('FreezeAssets')
GAVEL = list(SuitAttacks.keys()).index('Gavel')
GLOWER_POWER = list(SuitAttacks.keys()).index('GlowerPower')
GUILT_TRIP = list(SuitAttacks.keys()).index('GuiltTrip')
HALF_WINDSOR = list(SuitAttacks.keys()).index('HalfWindsor')
HANG_UP = list(SuitAttacks.keys()).index('HangUp')
HEAD_SHRINK = list(SuitAttacks.keys()).index('HeadShrink')
HOT_AIR = list(SuitAttacks.keys()).index('HotAir')
JARGON = list(SuitAttacks.keys()).index('Jargon')
KICKBACK = list(SuitAttacks.keys()).index('Kickback')
LEGALESE = list(SuitAttacks.keys()).index('Legalese')
LEGAL_STORM = list(SuitAttacks.keys()).index('LegalStorm')
LIQUIDATE = list(SuitAttacks.keys()).index('Liquidate')
MARKET_CRASH = list(SuitAttacks.keys()).index('MarketCrash')
MUMBO_JUMBO = list(SuitAttacks.keys()).index('MumboJumbo')
PARADIGM_SHIFT = list(SuitAttacks.keys()).index('ParadigmShift')
PECKING_ORDER = list(SuitAttacks.keys()).index('PeckingOrder')
PENNY_PINCH = list(SuitAttacks.keys()).index('PennyPinch')
PICK_POCKET = list(SuitAttacks.keys()).index('PickPocket')
PINK_SLIP = list(SuitAttacks.keys()).index('PinkSlip')
PLAY_HARDBALL = list(SuitAttacks.keys()).index('PlayHardball')
POUND_KEY = list(SuitAttacks.keys()).index('PoundKey')
POWER_TIE = list(SuitAttacks.keys()).index('PowerTie')
POWER_TRIP = list(SuitAttacks.keys()).index('PowerTrip')
QUAKE = list(SuitAttacks.keys()).index('Quake')
RAZZLE_DAZZLE = list(SuitAttacks.keys()).index('RazzleDazzle')
RED_TAPE = list(SuitAttacks.keys()).index('RedTape')
RE_ORG = list(SuitAttacks.keys()).index('ReOrg')
RESTRAINING_ORDER = list(SuitAttacks.keys()).index('RestrainingOrder')
ROLODEX = list(SuitAttacks.keys()).index('Rolodex')
RUBBER_STAMP = list(SuitAttacks.keys()).index('RubberStamp')
RUB_OUT = list(SuitAttacks.keys()).index('RubOut')
SACKED = list(SuitAttacks.keys()).index('Sacked')
SANDTRAP = list(SuitAttacks.keys()).index('SandTrap')
SCHMOOZE = list(SuitAttacks.keys()).index('Schmooze')
SENSORY_OVERLOAD = list(SuitAttacks.keys()).index('SensoryOverload')
SHAKE = list(SuitAttacks.keys()).index('Shake')
SHRED = list(SuitAttacks.keys()).index('Shred')
SONG_AND_DANCE = list(SuitAttacks.keys()).index('SongAndDance')
SPEED_DIAL = list(SuitAttacks.keys()).index('SpeedDial')
SPIN = list(SuitAttacks.keys()).index('Spin')
STOMPER = list(SuitAttacks.keys()).index('Stomper')
SYNERGY = list(SuitAttacks.keys()).index('Synergy')
TABULATE = list(SuitAttacks.keys()).index('Tabulate')
TEE_OFF = list(SuitAttacks.keys()).index('TeeOff')
THROW_BOOK = list(SuitAttacks.keys()).index('ThrowBook')
TREMOR = list(SuitAttacks.keys()).index('Tremor')
TRIP = list(SuitAttacks.keys()).index('Trip')
UNDERGROUND_LIQUIDITY = list(SuitAttacks.keys()).index('UndergroundLiquidity')
WATERCOOLER = list(SuitAttacks.keys()).index('Watercooler')
WITHDRAWAL = list(SuitAttacks.keys()).index('Withdrawal')
WRITE_OFF = list(SuitAttacks.keys()).index('WriteOff')
WRITE_UP = list(SuitAttacks.keys()).index('WriteUp')


def getFaceoffTaunt(suitName: str, doId):
    if suitName in SuitFaceoffTaunts:
        taunts = SuitFaceoffTaunts[suitName]
    else:
        taunts = TTLocalizer.SuitFaceoffDefaultTaunts
    return taunts[doId % len(taunts)]


SuitFaceoffTaunts = OTPLocalizer.SuitFaceoffTaunts


def getAttackTauntIndexFromIndex(suit, attackIndex):
    adict: dict = getSuitAttack(suit.getStyleName(), suit.getLevel(), attackIndex)
    return getAttackTauntIndex(adict['name'])


def getAttackTauntIndex(attackName: str) -> int:
    if attackName in SuitAttackTaunts:
        taunts = SuitAttackTaunts[attackName]
        return random.randint(0, len(taunts) - 1)
    else:
        return 1


def getAttackTaunt(attackName, index=None, suitName=None):
    if attackName in SuitAttackTaunts:
        try:
            taunts = SuitAttackTaunts[attackName][suitName if suitName in SuitAttackTaunts[attackName] else None]
        except:
            taunts = SuitAttackTaunts[attackName]
    else:
        taunts = TTLocalizer.SuitAttackDefaultTaunts
    if index is not None:
        if index >= len(taunts):
            notify.warning(
                'index exceeds length of taunts list in getAttackTaunt')
            return TTLocalizer.SuitAttackDefaultTaunts[0]
        return taunts[index]
    else:
        return random.choice(taunts)
    return


SuitAttackTaunts = TTLocalizer.SuitAttackTaunts
