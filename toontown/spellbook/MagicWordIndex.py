##################################################
# The Toontown Offline Magic Word Manager
##################################################
# Author: Benjamin Frisby
# Copyright: Copyright 2020, Toontown Offline
# Credits: Benjamin Frisby, John Cote, Ruby Lord, Frank, Nick, Little Cat, Ooowoo
# License: MIT
# Version: 1.0.0
# Email: belloqzafarian@gmail.com
##################################################

import collections
import types

from direct.distributed.ClockDelta import *
from direct.distributed import MsgTypes

from direct.interval.IntervalGlobal import *

from panda3d.otp import NametagGroup, WhisperPopup

from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
import os
from . import MagicWordConfig
import time
import datetime
import random
import re
import json
from panda3d.core import *
from toontown.toon import Experience
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.golf import GolfGlobals
from toontown.racing import RaceGlobals
from toontown.shtiker import CogPageGlobals
from toontown.coghq import CogDisguiseGlobals
from toontown.quest import Quests
from toontown.fishing import FishGlobals
from toontown.racing.KartDNA import *
from toontown.suit import SuitDNA
from direct.showbase.InputStateGlobal import inputState
from toontown.toonbase import ToontownBattleGlobals
from toontown.hood import ZoneUtil
from toontown.toon import ToonDNA, NPCToons
from toontown.parties import PartyGlobals
from toontown.suit import DistributedSuitPlanner
from toontown.battle import SuitBattleGlobals
# from toontown.suit import DistributedBossCog

# from otp.ai.AIBaseGlobal import *

magicWordIndex = collections.OrderedDict()


class MagicWord:
    notify = DirectNotifyGlobal.directNotify.newCategory('MagicWord')

    # Whether this Magic word should be considered "hidden"
    # If your Toontown source has a page for Magic Words in the Sthickerbook,
    # this will be useful for that
    hidden = False

    # Whether this Magic Word is an administrative command or not
    # Good for config settings where you want to disable cheaty Magic Words,
    # but still want moderation ones
    administrative = False

    # List of names that will also invoke this word - a setHp magic word might have "hp", for example
    # A Magic Word will always be callable with its class name, so you don't
    # have to put that in the aliases
    aliases = None

    # Description of the Magic Word
    # If your Toontown source has a page for Magic Words in the Sthickerbook,
    # this will be useful for that
    desc = MagicWordConfig.MAGIC_WORD_DEFAULT_DESC

    # Advanced description that gives the user a lot more information than normal
    # If your Toontown source has a page for Magic Words in the Sthickerbook,
    # this will be useful for that
    advancedDesc = MagicWordConfig.MAGIC_WORD_DEFAULT_ADV_DESC

    # Default example with for commands with no arguments set
    # If your Toontown source has a page for Magic Words in the Sthickerbook,
    # this will be useful for that
    example = ""

    # The minimum access level required to use this Magic Word
    accessLevel = 'USER'

    # A restriction on the Magic Word which sets what kind or set of Distributed Objects it can be used on
    # By default, a Magic Word can affect everyone
    affectRange = [
        MagicWordConfig.AFFECT_SELF,
        MagicWordConfig.AFFECT_OTHER,
        MagicWordConfig.AFFECT_BOTH]

    # Where the magic word will be executed -- EXEC_LOC_CLIENT or
    # EXEC_LOC_SERVER
    execLocation = MagicWordConfig.EXEC_LOC_INVALID

    # List of all arguments for this word, with the format [(type, isRequired), (type, isRequired)...]
    # If the parameter is not required, you must provide a default argument:
    # (type, False, default)
    arguments = None

    # True if executes differently based on the alias
    useAlias = False

    # is it a safezone?

    Str2szId = {
        'ttc': ToontownGlobals.ToontownCenter,
        'tt': ToontownGlobals.ToontownCenter,
        'tc': ToontownGlobals.ToontownCenter,
        'dd': ToontownGlobals.ToontownShipyards,
        'dg': ToontownGlobals.FloweringGrove,
        'mml': ToontownGlobals.TheLandOfMusic,
        'mm': ToontownGlobals.TheLandOfMusic,
        'br': ToontownGlobals.TundraWonderland,
        'ddl': ToontownGlobals.TwilightDreamland,
        'dl': ToontownGlobals.TwilightDreamland,
    }

    def __init__(self):
        if self.__class__.__name__ != "MagicWord":
            self.aliases = self.aliases if self.aliases is not None else []
            self.aliases.insert(0, self.__class__.__name__)
            self.aliases = [x.lower() for x in self.aliases]
            self.arguments = self.arguments if self.arguments is not None else []

            if len(self.arguments) > 0:
                for arg in self.arguments:
                    argInfo = ""
                    if not arg[MagicWordConfig.ARGUMENT_REQUIRED]:
                        argInfo += "(default: {0})".format(
                            arg[MagicWordConfig.ARGUMENT_DEFAULT])
                    self.example += "[{0}{1}] ".format(
                        arg[MagicWordConfig.ARGUMENT_NAME], argInfo)

            self.__register()
        self.texViewer = None

    def __register(self):
        for wordName in self.aliases:
            if wordName in magicWordIndex:
                self.notify.error(
                    'Duplicate Magic Word name or alias detected! Invalid name: {}'.format(wordName))
            magicWordIndex[wordName] = {'class': self,
                                        'classname': self.__class__.__name__,
                                        'hidden': self.hidden,
                                        'administrative': self.administrative,
                                        'aliases': self.aliases,
                                        'desc': self.desc,
                                        'advancedDesc': self.advancedDesc,
                                        'example': self.example,
                                        'execLocation': self.execLocation,
                                        'access': self.accessLevel,
                                        'affectRange': self.affectRange,
                                        'args': self.arguments}

    def loadWord(self, air=None, cr=None, invokerId=None,
                 targets=None, args=None):
        self.air = air
        self.cr = cr
        self.invokerId = invokerId
        self.targets = targets
        self.args = args

    def executeWord(self, usedAlias=None):
        executedWord = None
        validTargets = len(self.targets)
        now = time.strftime("%c")
        if not os.path.exists('users/logs/magic-words/'):
            os.makedirs('users/logs/magic-words/')
        for avId in self.targets:
            invoker = None
            toon = None
            if self.air:
                invoker = self.air.doId2do.get(self.invokerId)
                toon = self.air.doId2do.get(avId)
            elif self.cr:
                invoker = self.cr.doId2do.get(self.invokerId)
                toon = self.cr.doId2do.get(avId)
            if hasattr(toon, "getName"):
                name = toon.getName()
            else:
                name = avId

            if not self.validateTarget(toon):
                if len(self.targets) > 1:
                    validTargets -= 1
                    continue
                return "{} is not a valid target!".format(name)
            # TODO check also if toon is locked
            #                if len(self.targets) > 1:
            #                   validTargets -= 1
            #                  continue
            # return "{} is currently locked. You can only use administrative commands
            # on them.".format(name)

            if invoker.getAccessLevel() <= toon.getAccessLevel() and toon != invoker:
                if len(self.targets) > 1:
                    validTargets -= 1
                    continue
                targetAccess = OTPGlobals.AccessLevelDebug2Name.get(
                    OTPGlobals.AccessLevelInt2Name.get(toon.getAccessLevel()))
                invokerAccess = OTPGlobals.AccessLevelDebug2Name.get(
                    OTPGlobals.AccessLevelInt2Name.get(invoker.getAccessLevel()))
                return "You don't have a high enough Access Level to target {0}! Their Access Level: {1}. Your Access Level: {2}.".format(
                    name, targetAccess, invokerAccess)

            if self.execLocation == MagicWordConfig.EXEC_LOC_CLIENT:
                self.args = json.loads(self.args)

            if not usedAlias:
                executedWord = self.handleWord(invoker, avId, toon, *self.args)
            else:
                executedWord = self.handleWordWithAlias(
                    invoker, avId, toon, usedAlias, *self.args)
            # make sure the process is an ai process before writing a server
            # event
            if game.process == 'ai':
                self.air.writeServerEvent('magic-word-excuted',
                                          self.invokerId, invoker.getAccessLevel(),
                                          toon.getAccessLevel(),
                                          self.__class__.__name__,
                                          executedWord)

        # darth you do know this thing is clientside right o_O
        with open('users/logs/magic-words/magic-words-log.txt', 'a') as magicWordLogFile:
            magicWordLogFile.write(
                f"{now} | {self.invokerId}: {self.__class__.__name__}\n")
        # If you're only using the Magic Word on one person and there is a
        # response, return that response
        if executedWord and len(self.targets) == 1:
            return executedWord
        # If the amount of targets is higher than one...
        elif validTargets > 0:
            # And it's only 1, and that's yourself, return None
            if validTargets == 1 and self.invokerId in self.targets:
                return None
            # Otherwise, state how many targets you executed it on

            return "Magic Word successfully executed on %s target(s)." % validTargets
        else:
            return "Magic Word unable to execute on any targets."

    def validateTarget(self, target):
        if self.air:
            from toontown.toon.DistributedToonAI import DistributedToonAI
            return isinstance(target, DistributedToonAI)
        elif self.cr:
            from toontown.toon.DistributedToon import DistributedToon
            return isinstance(target, DistributedToon)
        return False

    def handleWord(self, invoker, avId, toon, *args):
        if self.useAlias:
            self.handleWordWithAlias(invoker, avId, toon, None, *args)

    def handleWordWithAlias(self, invoker, avId, toon, alias, *args):
        self.handleWord(invoker, avId, toon, *args)

    def doNpcFriend(self, av, npcId, numCalls):
        return av.attemptAddNPCFriend(npcId, numCalls) == 1

    def getDepts(self, args):
        # Returns a list of the dept indices specified by args[1], or
        # all depts if nothing is specified.  If a dept is specified,
        # args[1] is removed from the list.

        depts = []
        if len(args) > 0:
            if args[0] == 'all':
                depts = [0, 1, 2, 3]
                del args[0]
            else:
                allLettersGood = 1
                for letter in args[0]:
                    if letter in SuitDNA.suitDepts:
                        dept = SuitDNA.suitDepts.index(letter)
                        depts.append(dept)
                    else:
                        allLettersGood = 0
                        break

                if allLettersGood:
                    del args[0]
                else:
                    depts = []

        if depts:
            return depts
        else:
            return [0, 1, 2, 3]


class SetHP(MagicWord):
    aliases = ["hp", "setlaff", "laff"]
    desc = "Sets the target's current laff."
    advancedDesc = "This Magic Word will change the current amount of laff points the target has to whichever " \
                   "value you specify. You are only allowed to specify a value between -1 and the target's maximum " \
                   "laff points. If you specify a value less than 1, the target will instantly go sad unless they " \
                   "are in Immortal Mode."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [("hp", int, True)]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        hp = args[0]

        if not -100 <= hp <= toon.getMaxHp():
            return "Can't set {0}'s laff to {1}! Specify a value between -100 and {0}'s max laff ({2}).".format(
                toon.getName(), hp, toon.getMaxHp())

        if hp <= 0 and (toon.immortalMode):
            return "Can't set {0}'s laff to {1} because they are in Immortal Mode!".format(
                toon.getName(), hp)

        toon.b_setHp(hp)
        return "{}'s laff has been set to {}.".format(toon.getName(), hp)


class SetGMIcon(MagicWord):
    aliases = ['gm', 'gmicon', 'setgm', 'icons', 'setIcons', 'icon', 'staffIcon', 'si']
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [("id", int, True)]
    accessLevel = 'MODERATOR'
    desc = "Sets the target's GM Icon."

    def handleWord(self, invoker, avId, toon, *args):
        id = args[0]
        if not 0 <= id <= 8:
            return "Invalid GM Icon given."

        AccessLevel = toon.getAccessLevel()
        if id > 3 and AccessLevel < 600:
            return "Your access level is too low to use this GM icon."
        else:
            if (AccessLevel < 400 and id > 2) or (
                    AccessLevel < 500 and id > 3):
                return "Your access level is too low to use this GM icon."

        if toon.isGM() and id != 0:
            toon.b_setGM(0)
        elif toon.isGM() and id == 0:
            toon.b_setGM(0)

        toon.b_setGM(id)

        return "You have set {0} to GM type {1}".format(toon.getName(), id)


class ToggleGM(MagicWord):
    desc = 'Toggles GM icon.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'COMMUNITY'

    def handleWord(self, invoker, avId, toon, *args):
        access = invoker.getAccessLevel()
        if invoker.isGM():
            invoker.b_setGM(0)
            return "You have disabled your GM icon."
        else:
            if access >= 700:
                invoker.b_setGM(1)
            elif access >= 600:
                invoker.b_setGM(1)
            elif access >= 500:
                invoker.b_setGM(1)
            elif access >= 400:
                invoker.b_setGM(2)
            elif access >= 200:
                invoker.b_setGM(3)
            return 'You have enabled your GM icon.'


class SetMaxHP(MagicWord):
    aliases = ["maxhp", "setmaxlaff", "maxlaff"]
    desc = "Sets the target's max laff."
    advancedDesc = "This Magic Word will change the maximum amount of laff points the target has to whichever value " \
                   "you specify. You are only allowed to specify a value between 1 and 137 laff points."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [("maxhp", int, True)]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        maxhp = args[0]

        if not 1 <= maxhp <= 137:
            return f"Can't set {toon.getName()}'s max laff to {maxHp}! " \
                   f"Specify a value between 1 and 137."

        toon.setMaxHp(maxhp)
        toon.toonUp(maxhp)
        return "{}'s max laff has been set to {}.".format(
            toon.getName(), maxhp)


class ToggleSellbotCutscene(MagicWord):
    aliases = ['ToggleSC']
    desc = 'Will set whether you have seen the VP cutscene for the first time or not.'
    advancedDesc = 'Sets the sellbot cutscene first time variable. If already set to true will set to false, etc'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    affectRange = [MagicWordConfig.AFFECT_SELF]

    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        if invoker.getSellbotCutSceneFirstTime():
            invoker.b_setSellbotCutSceneFirstTime(False)
            return 'Set sellbot cutscene first time to false'
        else:
            invoker.b_setSellbotCutSceneFirstTime(True)
            return 'Set sellbot cutscene first time to true'


class ToggleCashbotCutscene(MagicWord):
    aliases = ['ToggleCC']
    desc = 'Will set whether you have seen the CFO cutscene for the first time or not.'
    advancedDesc = 'Sets the cashbot cutscene first time variable. If already set to true will set to false, etc'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    affectRange = [MagicWordConfig.AFFECT_SELF]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        if invoker.getCashbotCutSceneFirstTime():
            invoker.b_setCashbotCutSceneFirstTime(False)
            return 'Set cashbot cutscene first time to false'
        else:
            invoker.b_setCashbotCutSceneFirstTime(True)
            return 'Set cashbot cutscene first time to true'


class ToonUp(MagicWord):
    aliases = ["tu", "toon-up", "heal"]
    desc = "Heals the toon to full laff."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        toon.toonUp(toon.maxHp)
        return 'Successfully healed the target.'


class Unlocks(MagicWord):
    desc = "Unlocks the target's teleport access, emotions, and pet trick phrases."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'COMMUNITY'

    def handleWord(self, invoker, avId, av, *args):
        # Unlocks the target's teleport access, emotions, and pet trick
        # phrases.
        av.b_setTeleportAccess(ToontownGlobals.HoodsForTeleportAll)
        av.b_setEmoteAccess(range(len(OTPLocalizer.EmoteFuncDict)))
        av.b_setPetTrickPhrases(range(len(OTPLocalizer.PetTrickPhrases)))
        return 'Successfully unlocked teleport access, emotions, and pet trick phrases.'


class MaxGags(MagicWord):
    desc = "Gives your toon the max amount of every gag."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, av, *args):
        av.b_setMaxCarry(255)
        experience = Experience.Experience(av.getExperience(), av)
        for i, track in enumerate(av.getTrackAccess()):
            if track:
                experience.experience[i] = (
                    Experience.MaxSkill - Experience.UberSkill)
        av.b_setExperience(experience.makeNetString())
        av.inventory.maxOutInv(filterUberGags=0, filterPaidGags=0)
        av.b_setInventory(av.inventory.makeNetString())
        # TODO give 255 of each gag
        return 'Successfully gave your toon the max amount of gags.'


class MaxToon(MagicWord):
    desc = "Maxes the toon to unlock everything."
    arguments = [("actuallyMaxGags", int, False, 0)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, av, actuallyMaxGags=0, *args):
        av.b_setTrackAccess([1, 1, 1, 1, 1, 1, 1])
        av.b_setMaxCarry(255)

        experience = Experience.Experience(av.getExperience(), av)
        for i, track in enumerate(av.getTrackAccess()):
            if track:
                experience.experience[i] = (
                    Experience.MaxSkill - Experience.UberSkill)
        av.b_setExperience(experience.makeNetString())

        av.inventory.zeroInv()
        av.inventory.maxOutInv(filterUberGags=0, filterPaidGags=0)
        av.b_setInventory(av.inventory.makeNetString())

        av.b_setMaxMoney(Quests.RewardDict[707][1])
        av.b_setMoney(av.getMaxMoney())
        av.b_setBankMoney(30000)

        av.b_setMaxHp(137)
        laff = av.getMaxHp() - av.getHp()
        if laff < 15:
            laff = 15
        av.toonUp(laff)

        av.b_setHoodsVisited(ToontownGlobals.Hoods)
        av.b_setTeleportAccess(ToontownGlobals.HoodsForTeleportAll)

        av.b_setCogParts([
            CogDisguiseGlobals.PartsPerSuitBitmasks[0],
            CogDisguiseGlobals.PartsPerSuitBitmasks[1],
            CogDisguiseGlobals.PartsPerSuitBitmasks[2],
            CogDisguiseGlobals.PartsPerSuitBitmasks[3],
        ])
        av.b_setCogLevels([ToontownGlobals.MaxCogSuitLevel] * 4 + [0])
        av.b_setCogTypes([7] * 4 + [0])

        av.b_setCogCount(list(CogPageGlobals.COG_QUOTAS[1]) * 4)
        cogStatus = [CogPageGlobals.COG_COMPLETE2] * SuitDNA.suitsPerDept
        av.b_setCogStatus(cogStatus * 4)
        av.b_setCogRadar([1] * 4)
        av.b_setBuildingRadar([1] * 4)

        for id in av.getQuests():
            av.removeQuest(id)
        av.b_setQuestCarryLimit(ToontownGlobals.MaxQuestCarryLimit)
        av.b_setRewardHistory(
            Quests.LOOPING_FINAL_TIER,
            av.getRewardHistory()[1])

        allFish = TTLocalizer.FishSpeciesNames
        fishLists = [[], [], []]
        for genus in allFish.keys():
            for species in range(len(allFish[genus])):
                fishLists[0].append(genus)
                fishLists[1].append(species)
                fishLists[2].append(
                    FishGlobals.getRandomWeight(
                        genus, species))
        av.b_setFishCollection(*fishLists)
        av.b_setFishingRod(FishGlobals.MaxRodId)
        av.b_setFishingTrophies(list(FishGlobals.TrophyDict.keys()))

        if not av.hasKart():
            av.b_setKartBodyType(list(KartDict.keys())[1])
        av.b_setTickets(RaceGlobals.MaxTickets)
        maxTrophies = RaceGlobals.NumTrophies + RaceGlobals.NumCups
        av.b_setKartingTrophies(range(1, maxTrophies + 1))
        av.b_setTickets(99999)

        av.b_setGolfHistory([600] * (GolfGlobals.MaxHistoryIndex * 2))
        return 'Successfully maxed your Toon.'


class SkipMazeGame(MagicWord):
    aliases = ["skipmaze", "endmaze"]
    desc = "Skips the sellbot field office minigame."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        mazeGame = None
        from toontown.cogdominium.DistCogdoMazeGameAI import DistCogdoMazeGameAI
        for do in simbase.air.doId2do.values():
            if isinstance(do, DistCogdoMazeGameAI):
                if invoker.doId in do.getToonIds():
                    mazeGame = do
                    break

        if mazeGame:
            mazeGame.openDoor()
            return "Skipped SBFO Maze Minigame!"
        else:
            return "You are not in the SBFO maze minigame!"


class SkipFlyingGame(MagicWord):
    aliases = ['skipfly', 'endfly']
    desc = 'Skips the lawbot field office minigame.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        from toontown.cogdominium.DistCogdoFlyingGameAI import DistCogdoFlyingGameAI
        flyingGame = None
        for do in simbase.air.doId2do.values():
            if isinstance(do, DistCogdoFlyingGameAI):
                if toon.doId in do.getToonIds():
                    flyingGame = do
                    break

        if flyingGame:
            flyingGame._handleGameFinished()
            response = 'Finished lawbot field office flying game!'
        else:
            response = 'Not in a lawbot field office'
        return response


class ainotify(MagicWord):
    desc = 'Sets the ai notification level'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'ADMIN'
    arguments = [('categoryName', str, True), ('serverity', int, True)]

    def handleWord(self, invoker, avId, toon, *args):
        n = Notify.ptr().getCategory(args[0])
        serverityDict = {'error': NSError,
                         'warning': NSWarning,
                         'info': NSInfo,
                         'debug': NSDebug,
                         'spam': NSSpam}
        n.setSeverity(
            {'error': NSError,
             'warning': NSWarning,
             'info': NSInfo,
             'debug': NSDebug,
             'spam': NSSpam, }[args[1]])
        return 'Set severity to {0}'.format(n.getSeverity())


class Rename(MagicWord):
    aliases = ['name', 'setname']
    desc = "Sets the target's name."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('name', str, True)]
    accessLevel = 'MODERATOR'

    def handleWord(self, invoker, avId, toon, *args):
        word = args[0]
        name = word.strip()
        pastName = toon.getName()
        if name == "":
            response = "Invalid name: Name can't be blank."
        elif ':' in word:
            response = 'Invalid name: Cannot have : in name.'
        else:
            toon.b_setName(name)
            response = 'Changed {0} name to {1}'.format(pastName, name)
        return response


class BadName(MagicWord):
    aliases = ['setbad', 'setbadname']
    desc = "Set's the target's name back to color + animal."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'MODERATOR'

    def handleWord(self, invoker, avId, toon, *args):
        self.notify.info(
            "Renaming inappropriately named toon %s (doId %d)." %
            (toon._name, avId))
        pastName = toon.getName()
        color = TTLocalizer.NumToColor[toon.dna.headColor]
        animal = TTLocalizer.AnimalToSpecies[toon.dna.getAnimal()]
        toon.b_setName(color + ' ' + animal)
        toon.sendUpdate('WishNameState', 4)  # rejected state
        return 'Changed {0} name to {1}'.format(pastName, toon.getName())


class fix(MagicWord):
    aliases = ['fixavatar', 'fixtoon']
    desc = "Fix whatever might be out-of-whack for the avatar."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'MODERATOR'

    def handleWord(self, invoker, avId, toon, *args):
        anyChanged = toon.fixAvatar()
        if anyChanged:
            response = "avatar fixed."
        else:
            response = "avatar does not need fixing."
        return response


class ToggleGhost(MagicWord):
    aliases = [
        'invisible',
        'ghostmode',
        'setghost',
        'setghostmode',
        'ghost',
        'toggleghostmode']
    desc = "Toggles ghost mode for the invoker."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'COMMUNITY'
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        if toon.ghostMode:
            toon.b_setGhostMode(0)
            response = 'Ghost mode disabled'
        else:
            # we want staff to be invisible to the players if they want to spy
            toon.b_setGhostMode(1)
            response = 'Ghost mode enabled'
        return response


class ToggleFPS(MagicWord):
    aliases = ['fps', 'framerate', 'fpsmeter']
    desc = 'Toggles the fps meter for the invoker'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'COMMUNITY'
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        base.setFrameRateMeter(not base.frameRateMeter)

        if base.frameRateMeter:
            response = 'frame rate ON'
        else:
            response = 'frame rate OFF'
        return response

class allstuff(MagicWord):
    aliases = [
        'restockinventory',
        'restockinv',
        'maxinv',
        'maxinventory',
        'restock',
        'restockall',
        'inventoryRestock',
        'invRestock',
        'inventoryall',
        'inventory']
    desc = 'Gives target all the inventory they can carry.'

    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, av, *args):
        av.b_setMaxCarry(255)
        experience = Experience.Experience(av.getExperience(), av)
        for i, track in enumerate(av.getTrackAccess()):
            if track:
                experience.experience[i] = (
                    Experience.MaxSkill - Experience.UberSkill)
        av.b_setExperience(experience.makeNetString())
        av.inventory.maxOutInv(filterUberGags=0, filterPaidGags=0)
        av.b_setInventory(av.inventory.makeNetString())
        # TODO give 255 of each gag
        return 'Successfully gave your toon the max amount of gags.'


class nostuff(MagicWord):
    aliases = ['emptyinventory', 'emptyinv', 'zeroinv', 'zeroinventory', 'inventoryzero']
    desc = 'Gives target all the inventory they can carry.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        toon.inventory.zeroInv()
        toon.d_setInventory()
        return ("Zeroing inventory for " + toon._name)


class rich(MagicWord):
    desc = 'Gives the target full bank jellybeans'
    aliases = ['maxjbs', 'maxjellybeans', 'maxbankjellybeans']
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        av = toon
        av.b_setMoney(toon.maxMoney)
        av.b_setBankMoney(toon.maxBankMoney)
        return (toon._name + " is now rich")


class SetMoney(MagicWord):
    desc = "Sets the target's carrying jellybeans."
    advancedDesc = "Sets the target's carrying jellybeans. If no args are given give max beans."
    aliases = ['setjellybeans', 'jellybeans', 'setjbs', 'jbs']
    arguments = [('money', int, False, 250)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        if len(args) >= 1:
            count = int(args[0])
            # this will just fill up the pocketbook,
            # but wont add to the bank
            toon.b_setMoney(min(count, toon.getMaxMoney()))
        else:
            toon.b_setMoney(toon.getMaxMoney())
        return 'Set money to {0}.'.format(toon.getMoney())


class SetBankMoney(MagicWord):
    desc = "Sets the target's current amount of jellybeans in the bank."
    advancedDesc = "Sets the target's current amount of jellybeans in the bank. If no args are given give max beans."
    aliases = ['setbank', 'bank', 'bankmoney', ]
    arguments = [('money', int, False, 30000)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        if len(args) >= 1:
            count = int(args[0])
            toon.b_setBankMoney(count)
        else:
            toon.b_setBankMoney(toon.getMaxBankMoney())
        return 'Set bank money to {0}'.format(toon.getBankMoney())


class SetMaxBankMoney(MagicWord):
    desc = "Sets the target's max amount of jellybeans in the bank."
    advancedDesc = "Sets the target's max amount of jellybeans in the bank."
    aliases = ['setmaxbank', 'maxbank', 'maxbankmoney', ]
    arguments = [('money', int, True)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):

        if len(args) >= 1:
            count = int(args[0])
            toon.b_setMaxBankMoney(count)
            response = "Max bank money set to %s" % (count)

        else:
            response = "Max bank money is %s" % (toon.getMaxBankMoney())
        return response


class GivePies(MagicWord):
    desc = 'Gives the target the specified pie type.'
    aliases = ['pie', 'pies', 'givepie']
    arguments = [('type', str, True)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        # Give ourselves a pie.  Or four.
        count = 0
        _type = None
        if len(args) == 1:
            count = 1
        for arg in args[1:]:
            from toontown.toonbase import ToontownBattleGlobals
            if arg in ToontownBattleGlobals.pieNames:
                _type = ToontownBattleGlobals.pieNames.index(arg)
            else:
                try:
                    count = int(arg)
                except BaseException:
                    response = "Invalid pie argument: %s" % (arg)

        if _type is not None:
            toon.b_setPieType(_type)
        toon.b_setNumPies(toon.numPies + count)
        response = 'Set pies to {0} with num of {1}'.format(
            toon.getPieType(), toon.getNumPies())
        return response


class SetExp(MagicWord):
    aliases = ['exp', 'experience', 'setexperience']
    desc = 'Sets the experience of the target.'
    advancedDesc = "Sets the experience of the target. If no args are specified set all tracks to next level."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('track', str, False, 'all'), ('increment', int, False, -1)]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, av, *args):
        track = None
        trackIndex = -1
        increment = 0
        gotIncrement = 0

        if len(args) > 0:
            trackStr = args[0]
            if trackStr != "all":
                trackIndex = ToontownBattleGlobals.Tracks.index(trackStr)

        if len(args) > 1:
            increment = int(args[1])
            if increment == -1:
                gotIncrement = 0
            else:
                gotIncrement = 1

        if trackIndex == -1:
            for trackIndex in range(ToontownBattleGlobals.MAX_TRACK_INDEX + 1):
                if av.hasTrackAccess(trackIndex):
                    if not gotIncrement:
                        # No increment specified; the default is whatever
                        # it takes to get to the next track.
                        increment = av.experience.getNextExpValue(
                            trackIndex) - av.experience.getExp(trackIndex)

                    response = ("Adding %d to %s track for %s." % (
                        increment, ToontownBattleGlobals.Tracks[trackIndex], av._name))
                    av.experience.addExp(trackIndex, increment)
        else:
            if not gotIncrement:
                # No increment specified; the default is whatever
                # it takes to get to the next track.
                increment = av.experience.getNextExpValue(
                    trackIndex) - av.experience.getExp(trackIndex)

            response = ("Adding %d to %s track for %s." % (
                increment, ToontownBattleGlobals.Tracks[trackIndex], av._name))
            av.experience.addExp(trackIndex, increment)

        av.d_setExperience(av.experience.makeNetString())
        return response


class SetTrophyScore(MagicWord):
    aliases = ['trophy', 'settrophy']
    desc = 'Sets the trophy score of the target.'
    advancedDesc = 'Set the trophy score of the target. If no args specified, restore the actual trophy score.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('score', int, False, -1)]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        if args[0] != -1:
            score = int(args[0])

            response = "Set trophy score to %s." % (score)
        else:
            # No score specified; restore the actual trophy score.
            score = self.air.trophyMgr.getTrophyScore(avId)

            response = "Trophy score is %s." % (score)

        toon.d_setTrophyScore(score)
        return response


class SetCheesyEffect(MagicWord):
    aliases = ['setce', 'ce', 'effect', 'cheesyeffect', 'seteffect']
    desc = 'Sets the cheesy effect of the target.'
    advancedDesc = """These are the list of effects:Normal, BigHead,
     SmallHead, BigLegs,
      SmallLegs, BigToon,
      SmallToon, FlatPortrait,
       FlatProfile, Transparent,
        NoColor, Invisible,
         Pumpkin, BigWhite,
         SnowMan"""
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('ce', str, True), ('zoneId', int, False, 0),
                 ('expiretime', int, False, 0)]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        effect = None
        zoneId = args[1]
        if zoneId >= ToontownGlobals.DynamicZonesBegin:
            hoodId = 1
        else:
            hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        timeLimit = 10
        try:
            effect = eval("ToontownGlobals.CE" + args[0])
        except BaseException:
            try:
                effect = eval(args[0])
            except BaseException:
                effect = None

        if effect is None:
            response = "Unknown effect %s." % (args[0])
            return response
        if len(args) > 1:
            timeLimit = int(args[2])

        # Let it expire in timeLimit minutes.
        expireTime = (int)(time.time() / 60 + 0.5) + timeLimit
        toon.b_setCheesyEffect(effect, hoodId, expireTime)
        response = 'Set cheesy effect {0} for amount of time {1}'.format(
            effect, expireTime)


class CogTakeOver(MagicWord):
    aliases = ['building', 'spawnbuilding', 'spawnbldg', 'bldg']
    desc = 'Takes over a building with a cog.'
    advancedDesc = "If no argument is specified spawn a random cog building."

    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('track', str, False, 'x')]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        if args[0] != 'x':
            name = args[0]
        else:
            name = random.choice(SuitDNA.suitHeadTypes)
        if name not in SuitDNA.suitHeadTypes:
            return "Invalid cog specified. {0}".format(name)
        if invoker.doBuildingTakeover(name) == 'success':
            return 'Spawned building successfully with cog {0}'.format(name)
        else:
            return "Couldn't spawn building with cog {0}".format(name)


class CogDoTakeOver(MagicWord):
    aliases = ['fieldoffice', 'cogdo', 'cogdominium']
    desc = 'Takes over a toon building with a field office'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('track', str, False, 'x'), ('difficulty', int, False, -1)]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        from toontown.building import SuitBuildingGlobals
        level = None

        if len(args) > 0:
            track = args[0]
            if track not in ['s', 'l', 'x']:
                return 'Invalid track for field office. Must be s, l or x .'
            if track == 'x':
                track = random.choice(['s', 'l'])
        else:
            track = random.choice(['s', 'l'])

        if len(args) > 1:
            if args[1] != -1:
                level = int(args[1])
                if not 0 <= level < len(SuitBuildingGlobals.SuitBuildingInfo):
                    "Invalid difficulty: {0}".format(args[1])
            else:
                level = random.choice(SuitBuildingGlobals.SuitBuildingInfo)
        try:
            invoker.findClosestDoor().cogdoTakeOver(level, 2, track)
            return "Spawned a %s Field Office with a difficulty of %d!" % (
                track, level)
        except BaseException:
            return "Unable to spawn a %s Field Office with a difficulty of %d." % (
                track, level)


class ToonTakeOver(MagicWord):
    aliases = ['freebuilding', 'freebldg']
    desc = 'Takes over a cog building, or cogdo with a toon building.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        streetId = invoker.getLocation()[1]
        # Just the buildings on this street.
        try:
            bm = self.air.buildingManagers[streetId]
        except KeyError:
            return str(streetId) + \
                " is not buildingManagers list for some reason :/"

        blocks = None

        if blocks is None:
            # Try to figure out what doors we're standing in front
            # of.
            blocks = []
            for i in bm.getSuitBlocks():
                building = bm.getBuilding(i)
                if hasattr(building, "elevator"):
                    if building.elevator.fsm.getCurrentState().getName() == 'waitEmpty':
                        blocks.append(i)
            blockMap = {bm: blocks}

        total = 0
        for bm, blocks in list(blockMap.items()):
            total += len(blocks)
            for i in blocks:
                building = bm.getBuilding(i)
                building.b_setVictorList([0, 0, 0, 0])
                building.updateSavedBy(
                    [(toon.doId, toon._name, toon.dna.asTuple())])
                building.toonTakeOver()
                self.notify.debug("Toon take over %s %s" % (i, streetId))

        response = "%d buildings." % (total)
        return response


class FinishTutorial(MagicWord):
    aliases = ['skiptutorial']
    desc = 'Skips the tutorial.'
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        av.b_setTutorialAck(1)
        av.b_setQuests([])
        av.b_setQuestHistory([])
        av.b_setRewardHistory(2, [])
        av.fixAvatar()
        return "Finished tutorial."


class FinishQuests(MagicWord):
    desc = 'Finishes quests magically.'
    aliases = ['finishtasks', 'finishToonTasks']
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, toon, *args):
        self.air.questManager.completeAllQuestsMagically(toon)
        return "Finished quests."


class FinishQuest(MagicWord):
    aliases = [
            'finishtask',
            'finishToonTask'
            'skipTask',
            'skipQuest']
    desc = 'Finishes specific quest magically.'
    accessLevel = 'DEVELOPER'
    arguments = [('index', int, True)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, toon, *args):
        index = int(args[0])
        result = self.air.questManager.completeQuestMagically(toon, index)
        if result:
            return ("Finished quest %s." % (index))
        else:
            return ("Quest %s not found." % (index))


class SetQuestTier(MagicWord):
    aliases = ['setqt', 'questtier', 'settasktier']
    desc = 'Sets the quest tier of the target'
    accessLevel = 'DEVELOPER'
    arguments = [('tier', int, True)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        tier = int(args[0])
        tier = min(tier, Quests.getNumTiers())
        av.b_setQuestHistory([])
        av.b_setRewardHistory(tier, [])
        av.fixAvatar()


class ClearQuests(MagicWord):
    aliases = ['cleartasks']
    desc = 'Reset all quest fields as if this were a new toon.'
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        av.b_setQuests([])
        av.b_setQuestHistory([])
        currentTier = av.getRewardTier()
        av.b_setRewardHistory(currentTier, [])
        return "Cleared quests."


class SetNextQuest(MagicWord):
    aliases = ['nextquest']
    desc = 'Forces NPCs to offer you a particular quest'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'
    arguments = [('questid', str, False, '')]

    def handleWord(self, invoker, avId, av, *args):
        if args[0] == '':
            # clear any existing request
            questId = self.air.questManager.cancelNextQuest(av.doId)
            if questId:
                return "Cancelled request for quest %s" % (questId)

        questId = int(args[0])

        # Make sure this quest exists
        questDesc = Quests.QuestDict.get(questId)
        if questDesc is None:
            return "Quest %s not found" % (questId)

        # Make sure the av is in that tier
        avTier = av.getRewardTier()
        tier = questDesc[Quests.QuestDictTierIndex]
        if tier != avTier:
            return "Avatar not in that tier: %s. You can ~setQuestTier %s, if you want." % (
                tier, tier)

        # Make sure the av does not already have this quest
        for questDesc in av.quests:
            if questId == questDesc[0]:
                return "Already has quest: %s" % (questId)

        self.air.questManager.setNextQuest(av.doId, questId)
        return "Quest %s queued" % (questId)


class GetQuestTier(MagicWord):
    desc = 'Gets the quest tier of the target.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'COMMUNITY'

    def handleWord(self, invoker, avId, av, *args):
        response = "tier %d" % (av.getRewardTier())
        return response


class SetAssignedQuest(MagicWord):
    aliases = ['assignquest', 'assigntask']
    desc = 'Intelligently assigns a quest'
    arguments = [('questId', str, True)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, av, *args):
        questId = int(args[0])

        # Make sure this quest exists
        questDesc = Quests.QuestDict.get(questId)
        if questDesc is None:
            return "Quest %s not found" % (questId)

        # Make sure the av is in that tier
        avTier = av.getRewardTier()
        tier = questDesc[Quests.QuestDictTierIndex]
        if tier != avTier:
            return "Avatar not in that tier: %s. You can ~setQuestTier %s, if you want." % (
                tier, tier)

        # Make sure the av has room for this quest
        if not self.air.questManager.needsQuest(av):
            return "Quests are already full"

        # Make sure the av does not already have this quest
        for questDesc in av.quests:
            if questId == questDesc[0]:
                return "Already has quest: %s" % (questId)

        # Should we check your reward history too?

        fromNpcId = Quests.ToonHQ  # A reasonable default

        rewardId = Quests.getQuestReward(questId, av)
        # Some quests do not have a reward specified. Instead they have
        # the keyword <Any> which tells the quest system to try to
        # match something up. In our case, we are not going through
        # normal channels, so just pick some reward so things do not
        # crash. How about some jellybeans?
        if rewardId == Quests.Any:
            # Just give 100 jellybeans (rewardId = 604 from Quests.py)
            rewardId = 604

        toNpcId = Quests.getQuestToNpcId(questId)
        # Account for some trickery in the quest description
        # If the toNpcId is marked <Any> or <Same> let's just use ToonHQ
        if toNpcId == Quests.Any:
            toNpcId = Quests.ToonHQ
        elif toNpcId == Quests.Same:
            toNpcId = Quests.ToonHQ

        startingQuest = Quests.isStartingQuest(questId)
        self.air.questManager.assignQuest(av.doId,
                                          fromNpcId,
                                          questId,
                                          rewardId,
                                          toNpcId,
                                          startingQuest,
                                          )
        return "Quest %s assigned" % (questId)


class GetBuildings(MagicWord):
    aliases = ['buildings']
    accessLevel = 'COMMUNITY'
    desc = 'Gets suit buildings info.'
    advancedDesc = """Reports the number of cog buildings vs. total buildings, and
    the target number of cog buildings, in the indicated zone (or
    overall).  If <zone> is omitted, the default is your current zone.
    "where" is a special keyword to list the distribution of buildings
    across the various zones."""
    arguments = [('word', str, False, ''), ('streetId', 'str', False, 'this')]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def __sortBuildingDist(self, a, b):
        return a[0] - b[0]

    def handleWord(self, invoker, avId, av, *args):
        zoneId = invoker.getLocation()[1]
        streetId = ZoneUtil.getBranchZone(zoneId)

        if args[0] == "where":
            # "~buildings where": report the distribution of buildings.
            dist = {}
            for sp in list(self.air.suitPlanners.values()):
                if sp.buildingMgr:
                    numActual = len(sp.buildingMgr.getSuitBlocks())
                    if numActual not in dist:
                        dist[numActual] = []
                    dist[numActual].append(sp.zoneId)

            # Sort the distribution by number of buildings.
            sorted = []
            for tuple in list(dist.items()):
                sorted.append(tuple)
            sorted.sort(self.__sortBuildingDist)

            # Now format the distribution into a text response.
            response = ""
            for numActual, zones in sorted:
                if numActual != 0:
                    response += "\n%s: %d" % (zones, numActual)

            if response == "":
                response = "No cog buildings."
            else:
                response = response[1:]

        else:
            # "~buildings zoneId" or "~buildings all"

            if len(args) > 1:
                if args[1] == "all":
                    streetId = "all"
                elif args[1] == 'this':
                    streetId = streetId
                else:
                    streetId = int(args[1])

            if streetId == "all":
                numTarget = 0
                numActual = 0
                numTotalBuildings = 0
                numAttempting = 0
                numPerTrack = {}
                numPerHeight = {}
                for sp in list(self.air.suitPlanners.values()):
                    numTarget += sp.targetNumSuitBuildings
                    if sp.buildingMgr:
                        numActual += len(sp.buildingMgr.getSuitBlocks())
                    numTotalBuildings += len(sp.frontdoorPointList)
                    numAttempting += sp.numAttemptingTakeover
                    sp.countNumBuildingsPerTrack(numPerTrack)
                    sp.countNumBuildingsPerHeight(numPerHeight)

                response = "Overall, %d cog buildings (%s, %s) out of %d; target is %d.  %d cogs are attempting takeover." % (
                    numActual, sp.formatNumSuitsPerTrack(numPerTrack),
                    sp.formatNumSuitsPerTrack(numPerHeight),
                    numTotalBuildings, numTarget, numAttempting)

            elif streetId not in self.air.suitPlanners:
                response = "Street %d is not known." % (streetId)

            else:
                sp = self.air.suitPlanners[streetId]

                numTarget = sp.targetNumSuitBuildings
                if sp.buildingMgr:
                    numActual = len(sp.buildingMgr.getSuitBlocks())
                else:
                    numActual = 0
                numTotalBuildings = len(sp.frontdoorPointList)
                numAttempting = sp.numAttemptingTakeover
                numPerTrack = {}
                numPerHeight = {}
                sp.countNumBuildingsPerTrack(numPerTrack)
                sp.countNumBuildingsPerHeight(numPerHeight)

                response = "Street %d has %d cog buildings (%s, %s) out of %d; target is %d.  %d cogs are attempting takeover." % (
                    streetId, numActual,
                    sp.formatNumSuitsPerTrack(numPerTrack),
                    sp.formatNumSuitsPerTrack(numPerHeight),
                    numTotalBuildings, numTarget, numAttempting)
        return response


class GetInvasion(MagicWord):
    aliases = ['getsuitinvasion', 'getcoginvasion', 'setsuitinvasion', 'setcoginvasion']
    desc = 'Get the current invasion thats happening.'
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        invMgr = self.air.suitInvasionManager

        if invMgr.getInvading():
            cogType, skeleton = invMgr.getCogType()
            numRemaining = invMgr.getNumCogsRemaining()
            cogName = SuitBattleGlobals.SuitAttributes[cogType]['name']
            if skeleton:
                cogName = TTLocalizer.Skeleton + " " + cogName
            response = (
                "Invasion is in progress: %s, %s remaining" %
                (cogName, numRemaining))
        else:
            response = ("No invasion found.")
        return response


class StartInvasion(MagicWord):
    desc = 'Starts a cog invasion.'
    accessLevel = 'MODERATOR'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('cogType', str, True), ('numCogs', int, True),
                 ('skelecog', bool, False, False)]

    def handleWord(self, invoker, avId, av, *args):
        invMgr = self.air.suitInvasionManager

        if invMgr.getInvading():
            cogType = invMgr.getCogType()
            numRemaining = invMgr.getNumCogsRemaining()
            cogName = SuitBattleGlobals.SuitAttributes[cogType[0]]['name']
            response = (
                "Invasion already in progress: %s, %s" %
                (cogName, numRemaining))
        else:
            if len(args) < 2 or len(args) > 3:
                response = "Error: Must specify cogType and numCogs"
            else:
                cogType = args[0]
                numCogs = int(args[1])
                if len(args) == 3:
                    skeleton = args[2]
                else:
                    skeleton = 0
                cogNameDict = SuitBattleGlobals.SuitAttributes.get(cogType)
                if cogNameDict:
                    cogName = cogNameDict['name']
                    if skeleton:
                        cogName = TTLocalizer.Skeleton + " " + cogName
                    if invMgr.startInvasion(cogType, numCogs, skeleton):
                        response = (
                            "Invasion started: %s, %s" %
                            (cogName, numCogs))
                    else:
                        response = (
                            "Invasion failed: %s, %s" %
                            (cogName, numCogs))
                else:
                    response = ("Unknown cogType: %s" % (cogType))
        return response


class StopInvasion(MagicWord):
    accessLevel = 'DEVELOPER'
    desc = 'Stops current invasion'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        invMgr = self.air.suitInvasionManager

        if invMgr.getInvading():
            self.air.suitInvasionManager.stopInvasion()
            response = ("Invasion stopped.")
        else:
            response = ("No invasion found.")
        return response


class StartAllFireworks(MagicWord):
    accessLevel = 'ADMIN'
    desc = 'Starts a show in all zones.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        fMgr = self.air.fireworkManager
        fMgr.stopAllShows()
        fMgr.startAllShows(None)
        response = "Shows started in all hoods."
        return response


class StartFireworks(MagicWord):
    accessLevel = 'ADMIN'
    desc = 'Starts a show in current zones'
    arguments = [('showType', int, False, 1)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        zoneId = invoker.getLocation()[1]
        fMgr = self.air.fireworkManager
        if fMgr.isShowRunning(zoneId):
            response = ("Show already running in zone: %s" % (zoneId))
        else:
            if len(args) == 1:
                showType = int(args[0])
                if fMgr.startShow(zoneId, showType, 1):
                    response = ("Show started, showType: %s" % showType)
                else:
                    response = ("Show failed, showType: %s" % showType)
            else:
                # Default to showType 0
                response = (TTLocalizer.startFireworksResponse
                            % (ToontownGlobals.NEWYEARS_FIREWORKS,
                               PartyGlobals.FireworkShows.Summer,
                               ToontownGlobals.JULY4_FIREWORKS))
        return response


class StopFireworks(MagicWord):
    accessLevel = 'ADMIN'
    desc = 'Stops show in current zone.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        zoneId = invoker.getLocation()[1]
        if self.air.fireworkManager.stopShow(zoneId):
            response = ("Show stopped, zoneId: %s" % zoneId)
        else:
            response = ("Show stop failed, zoneId: %s" % zoneId)
        return response


class StopAllFireworks(MagicWord):
    accessLevel = 'ADMIN'
    desc = 'Stops all shows in all zones.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        numStopped = self.air.fireworkManager.stopAllShows()
        response = ("Stopped %s firework show(s)" % (numStopped))
        return response


class DoMinigame(MagicWord):
    aliases = ['minigame']
    accessLevel = 'DEVELOPER'
    desc = 'Requests minigame'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('name or id', str, False, 0), ('keep', bool, False, False), ('difficulty', int, False, 0),
                 ('safezone', str, False, 0)]
    advancedDesc = """    Requests the indicated minigame for the current avatar.  The
    indicated minigame will be the next one chosen by the trolley
    for the next game that involves this avatar.
    difficulty (float) and safezone (string:tt,dd,dg,mm,br,dl) are
    optional difficulty setting overrides.
    'keep' will cause settings to 'stick' on the AI, for current
    avatar, until they are cancelled.
    With no arguments, will cancel any outstanding minigame request.
   """

    def handleWord(self, invoker, avId, av, *args):
        from toontown.minigame import MinigameCreatorAI
        if len(args) == 0:
            # No minigame parameter specified: clear the request.
            mgRequest = MinigameCreatorAI.RequestMinigame.get(av.doId)
            if mgRequest is not None:
                mgId = mgRequest[0]
                del MinigameCreatorAI.RequestMinigame[av.doId]
                response = "Request for minigame %d cleared." % (mgId)
            else:
                response = "Usage: ~minigame [<name|id> [difficulty] [safezone]]"
        else:
            # Try to determine the minigame id, keep flag, and the difficulty
            # and safezone overrides, if any
            name = args[0]
            mgId = None
            mgKeep = 0
            mgDiff = None
            mgSzId = None

            try:
                mgId = int(name)
                numMgs = len(ToontownGlobals.MinigameIDs)
                if mgId < 1 or mgId > numMgs or mgId not in ToontownGlobals.MinigameIDs:
                    response = "minigame ID '%s' is out of range" % mgId
                    mgId = None
            except BaseException:
                name = name.lower()
                if name[-4:] == "game":
                    name = name[:-4]
                if name[:11] == "distributed":
                    name = name[11:]
                mgId = ToontownGlobals.MinigameNames.get(name)
                if mgId is None:
                    response = "Unknown minigame '%s'." % (name)

            if args[1]:
                # it's either a difficulty (float), 'keep',
                # or a safezone (string)
                # is it 'keep'?
                mgKeep = 1
                # is it a difficulty?
            if args[2] != 0:
                try:
                    mgDiff = args[2]
                except BaseException:
                    pass
            if args[3] != 0:
                mgSzId = self.Str2szId.get(args[3])
            if mgId is not None:
                # mdId must be the first element
                MinigameCreatorAI.RequestMinigame[av.doId] = (
                    mgId, mgKeep, mgDiff, mgSzId)
                response = "Selected minigame %d" % mgId
                if mgDiff is not None:
                    response += ", difficulty %s" % mgDiff
                if mgSzId is not None:
                    response += ", safezone %s" % mgSzId
                if mgKeep:
                    response += ", keep=true"

        return response

# TO DO AllSummons MagicWord command to get ALL summons in your Shtiker Book.

class SummonSuit(MagicWord):
    aliases = ['call', 'summoncog']
    arguments = [('type', str, True, 'x'), ('level', int, True), ('skelecog', bool, False, False),
                 ('revives', int, False, 0)]
    accessLevel = 'DEVELOPER'
    desc = 'Summons a suit.'
    advancedDesc = """Calls in a cog from the sky.  If type is specified, it should be a
    one- or two-letter string describing the type of cog, e.g. pp for
    a Penny Pincher or f for a Flunky.  Level is the numeric level of
    the cog, 1 - 9. True or false for skelecog.. You can set the number of revives as well."""
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        zoneId = invoker.getLocation()[1]
        streetId = ZoneUtil.getBranchZone(zoneId)

        name = None
        level = None
        skelecog = None
        revives = None

        if len(args) > 0:
            try:
                int(name)
                return 'Argument 1 cannot be an integer.'
            except BaseException:

                name = args[0]
                if name == 'x':
                    name = None
                if name not in SuitDNA.suitHeadTypes:
                    return 'Not a valid cog head type.'

        if len(args) > 1:
            level = int(args[1])
            if level <= 0:
                return 'Invalid level specified.'
        if len(args) > 2:
            skelecog = args[2]

        if len(args) > 3:
            revives = int(args[3])

        if streetId not in self.air.suitPlanners:
            response = "Street %d is not known." % (streetId)

        else:
            sp = self.air.suitPlanners[streetId]
            map = sp.getZoneIdToPointMap()
            canonicalZoneId = ZoneUtil.getCanonicalZoneId(zoneId)
            if canonicalZoneId not in map:
                response = "Zone %d isn't near a suit point." % (
                    canonicalZoneId)
            else:
                points = map[canonicalZoneId][:]
                suit = sp.createNewSuit([], points,
                                        suitName=name,
                                        suitLevel=level,
                                        skelecog=skelecog,
                                        revives=revives)
                if suit:
                    response = "Here comes %s." % (
                        SuitBattleGlobals.SuitAttributes[suit.dna.name]['name'])
                else:
                    response = "Could not create suit."

        return response


class TeleportAll(MagicWord):
    aliases = ['teleportaccess', 'tpaccess']
    desc = 'Gives invoker teleport access everywhere.'
    affectRange = [MagicWordConfig.AFFECT_SELF]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, av, *args):
        av.b_setHoodsVisited(ToontownGlobals.HoodsForTeleportAll)
        av.b_setTeleportAccess(ToontownGlobals.HoodsForTeleportAll)
        return 'You can now teleport anywhere.'

# TODO God Mode MagicWord command to become Immortal to damage, have unlimited gags, have unlimited unites, fires, etc.!

class ToggleImmortality(MagicWord):
    aliases = ['immortal', 'toggleimmortal', 'invincible', 'toggleinvincible']
    desc = "Toggles immortal mode for the invoker."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        immortal = not toon.immortalMode
        toon.setImmortalMode(immortal)
        if toon.immortalMode:
            response = 'immortality ON'
        else:
            response = 'immortality OFF'
        return response


class AIObjects(MagicWord):
    aliases = ['getaiobjects']
    desc = 'Gets AI objects.'
    advancedDesc = 'This magic words gets AI objects. Either all or baseline.'
    arguments = [('word', str, True)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        from direct.showbase import ObjectReport
        report = ObjectReport.ObjectReport('AI ~objects')

        if 'all' in args:
            self.notify.info('printing full object set...')
            report.getObjectPool().printObjsByType(printReferrers='ref' in args)

        if hasattr(self, 'baselineObjReport'):
            self.notify.info('calculating diff from baseline ObjectReport...')
            self.lastDiff = self.baselineObjReport.diff(report)
            self.lastDiff.printOut(full=('diff' in args or 'dif' in args))

        if 'baseline' in args or not hasattr(self, 'baselineObjReport'):
            self.notify.info('recording baseline ObjectReport...')
            if hasattr(self, 'baselineObjReport'):
                self.baselineObjReport.destroy()
            self.baselineObjReport = report

        return 'objects logged'


class RequestDeleted(MagicWord):
    aliases = [
        'requestdeletedobjects',
        'getdeletedobjects',
        'getdeleted',
        'deletedobjects']
    desc = 'Gets deleted AI objects.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        requestDeletedDOs = self.air.getRequestDeletedDOs()
        response = '%s requestDeleted AI objects%s' % (
            len(requestDeletedDOs), choice(len(requestDeletedDOs), ', logging...', ''))
        s = '~requestDeleted: ['
        for do, age in requestDeletedDOs:
            s += '[%s, %s]' % (do.__class__.__name__, age)
        s += ']'
        self.notify.info(s)
        if len(requestDeletedDOs):
            response += '\noldest: %s, %s' % (
                requestDeletedDOs[0][0].__class__.__name__,
                formatTimeCompact(requestDeletedDOs[0][1]))
        return response


class AIMessenger(MagicWord):
    aliases = ['logaimessenger']
    desc = 'Logs AI Messenger.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'SYSTEM ADMIN'

    def handleWord(self, invoker, avId, toon, *args):
        print(messenger)
        return 'logging AI messenger'


class StartHoliday(MagicWord):
    desc = 'Starts a holiday based on the id specified'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'ADMIN'
    arguments = [('holidayId', int, False, 0)]

    def handleWord(self, invoker, avId, toon, *args):
        holidayId = args[0]
        if holidayId in self.air.holidayManager.holidaysCommon:
            self.air.holidayManager.startHoliday(holidayId)
            return f'Holiday successfully started {holidayId}'
        else:
            return f'Invalid holiday {holidayId}'


class StopHoliday(MagicWord):
    desc = 'Starts a holiday based on the id specified'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'ADMIN'
    arguments = [('holidayId', int, False, 0)]

    def handleWord(self, invoker, avId, toon, *args):
        holidayId = args[0]
        if holidayId in self.air.holidayManager.holidaysCommon:
            self.air.holidayManager.endHoliday(holidayId)
            return f'Holiday successfully ended {holidayId}'
        else:
            return f'Invalid holiday {holidayId}'


class DNA(MagicWord):
    aliases = ['dodna']
    desc = 'Modifies a DNA part for the invoker.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('part', str, True), ('value', str, True)]
    accessLevel = 'CREATIVE'

    def handleWord(self, invoker, avId, toon, *args):
        dna = ToonDNA.ToonDNA()
        dna.makeFromNetString(invoker.getDNAString())
        part = args[0]
        value = args[1]
        if part.endswith('size') or part.endswith(
                'color') or part.endswith('tex'):
            value = int(value)
        if part in ('species', 'head', 'animal'):
            animalsList = ('dog', 'cat', 'horse', 'mouse', 'rabbit', 'duck', 'monkey', 'bear',
                           'pig')
            if value not in animalsList:
                return 'Invalid species: {0}'.format(value)
            if value in animalsList:
                animalsIndex = animalsList.index(value)
                value = ToonDNA.toonSpeciesTypes[animalsIndex]
            dna.head = value + dna.head[1:3]
            invoker.b_setDNAString(dna.makeNetString())
            return 'Species is now: {0}'.format(dna.head[0])
        if part == 'headsize':
            sizes = ('ss', 'sl', 'ls', 'll')
            if not 0 <= value <= len(sizes):
                return 'Invalid head size index: {0}'.format(value)
            dna.head = sizes[value] + dna.head[0]
            invoker.b_setDNAString(dna.makeNetString())
            return 'Head size index is now: {0}'.format(dna.head[1:])
        if part == 'torso':
            # if dna.gender not in ('m', 'f'):
            #    return 'Invalid gender.'
            # return 'torso modification is in WIP due to gender'
            value = int(value)
            # if (not 0 <= value <= 2) and (dna.gender == 'm'):
            # return 'Male torso index out of range (0-2).'
            # if (not 3 <= value <= 8) and (dna.gender == 'f') :
            #   return 'Female torso index out of range (3-8).'
            if (not 0 <= value <= 8):
                return 'Torso index out of range '
            dna.torso = ToonDNA.toonTorsoTypes[value]
            invoker.b_setDNAString(dna.makeNetString())
            return 'Torso is now: {0}'.format(dna.torso)

        if part == 'legs':
            value = int(value)
            if not 0 <= value <= len(ToonDNA.toonLegTypes):
                return 'Legs index out of range (0-{0d}).'.format(
                    len(ToonDNA.toonLegTypes))
            dna.legs = ToonDNA.toonLegTypes[value]
            invoker.b_setDNAString(dna.makeNetString())
            return 'Legs are now: {0}'.format(dna.legs)

        if part == 'headcolor':
            # if dna.gender not in ('m', 'f'):
            #    return 'Invalid gender.'
            if (value not in ToonDNA.defaultColorList):
                return f'Invalid head color index: {dna.headColor}'
            dna.headColor = value
            invoker.b_setDNAString(dna.makeNetString())
            return f'Head color index is now: {dna.headColor} '

        if part == 'armcolor':
            # if dna.gender not in ('m', 'f'):
            #     return 'Invalid gender.'
            # if (value not in ToonDNA.defaultBoyColorList) and (dna.gender == 'm'):
            #   return 'Invalid male arm color index: {0}'.format(str(value))
            # if (value not in ToonDNA.defaultGirlColorList) and (dna.gender == 'f'):
            # return 'Invalid female arm color index: {0}'.format(str(value))
            if value not in ToonDNA.defaultColorList:
                return f'Invalid arm color index : {value}'
            dna.armColor = value
            invoker.b_setDNAString(dna.makeNetString())
            return f'Arm color index is now: {dna.armColor}'

        if part == 'legcolor':
            # if dna.gender not in ('m', 'f'):
            # return 'Invalid gender.'
            # if (value not in ToonDNA.defaultBoyColorList) and (dna.gender == 'm'):
            #       return 'Invalid male leg color index: {0}'.format(str(value))
            #   if (value not in ToonDNA.defaultGirlColorList) and (dna.gender == 'f'):
            # return 'Invalid female leg color index: {0}'.format(str(value))
            if value not in ToonDNA.defaultColorList:
                return f'Invalid leg color index : {value}'
            dna.legColor = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Leg color index is now: {0}'.format(str(dna.legColor))
        if part == 'color':
            # if dna.gender not in ('m', 'f'):
            #     return 'Invalid gender.'
            #    if (value not in ToonDNA.defaultBoyColorList) and (dna.gender == 'm'):
            #        return 'Invalid male color index: {0}'.format(str(value))
            #    if (value not in ToonDNA.defaultGirlColorList) and (dna.gender == 'f'):
            # return 'Invalid female  color index: {0}'.format(str(value))
            if value not in ToonDNA.defaultColorList:
                return f'Invalid  color index : {value}'
            dna.headColor = value
            dna.armColor = value
            dna.legColor = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Color index is now: {0}'.format(str(dna.headColor))
        if part == 'eyelashes':
            if value not in [0, 1] or value not in [True, False]:
                return 'Invalid eyelash values'
            if value == True:
                dna.eyelashes = 1
            elif value == False:
                dna.eyelashes = 0
            else:
                dna.eyelashes = value
        if part == 'gloves':
            value = int(value)
            if value not in ToonDNA.defaultGloveColorList:
                return 'Invalid glove color: ' + str(value)
            dna.gloveColor = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Glove color set to: ' + str(dna.gloveColor)

        if part == 'toptex':
            if not -1 < value <= len(ToonDNA.Shirts):
                return 'Top texture index out of range (0-{0}).'.format(
                    len(ToonDNA.Shirts))
            dna.topTex = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Top texture index set to: {0}'.format(str(dna.topTex))

        if part == 'toptexcolor':
            if not -1 < value <= len(ToonDNA.ClothesColors):
                return 'Top texture color index out of range(0-{0}).'.format(
                    len(ToonDNA.ClothesColors))
            dna.topTexColor = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Top texture color index set to: {0}'.format(
                str(dna.topTexColor))

        if part == 'sleevetex':
            if not -1 < value <= len(ToonDNA.Sleeves):
                return 'Sleeve texture index out of range(0-{0}).'.format(
                    len(ToonDNA.Sleeves))
            dna.sleeveTex = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Sleeve texture index set to: {0}'.format(
                str(dna.sleeveTex))

        if part == 'sleevetexcolor':
            if not -1 <= value <= len(ToonDNA.ClothesColors):
                return 'Sleeve texture color index out of range(0-{0}).'.format(
                    len(ToonDNA.ClothesColors))
            dna.sleeveTexColor = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Sleeve texture color index set to: {0}'.format(
                (dna.sleeveTexColor))

        if part == 'bottex':
            bottoms = ToonDNA.Bottoms
            if not -1 <= value <= len(bottoms):
                return 'Bottom texture index out of range (0-{0}).'.format(
                    len(bottoms))
            dna.botTex = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Bottom texture index set to:{0}'.format(str(dna.botTex))
        if part == 'hatModel':
            hatModels = ToonDNA.HatModels
            try:
                value = int(value)
            except BaseException:
                return 'value must be an int '
            if not -1 <= int(value) <= len(hatModels):
                return f"Hat model index out of range(0-{len(hatModels)}"
            dna.hatModel = value
            invoker.b_setDNAString(dna.makeNetString())
            return f'Hat model index set to : {str(dna.hatModel)}'
        if part == 'hatTex':
            hatTextures = ToonDNA.HatTextures
            try:
                value = int(value)
            except BaseException:
                return 'value must be an int '
            if not -1 <= int(value) <= len(hatTextures):
                return f"Hat texture index out of range(0-{len(hatTextures)}"
            dna.hatTex = value
            invoker.b_setDNAString(dna.makeNetString())
            return f'Hat texture index set to : {str(dna.hatTex)}'
        if part == 'glassesModel':
            glassesModels = ToonDNA.GlassesModels
            try:
                value = int(value)
            except BaseException:
                return 'value must be an int '
            if not -1 <= int(value) <= len(glassesModels):
                return f"Glasses model index out of range(0-{len(glassesModels)}"
            dna.glassesModel = value
            invoker.b_setDNAString(dna.makeNetString())
            return f'Glasses model index set to : {str(dna.glassesModel)}'
        if part == 'glassesTex':
            glassesTextures = ToonDNA.GlassesTextures
            try:
                value = int(value)
            except BaseException:
                return 'value must be an int '
            if not -1 <= int(value) <= len(glassesTextures):
                return f"Glasses texture index out of range(0-{len(glassesTextures)}"
            dna.glassesTex = value
            invoker.b_setDNAString(dna.makeNetString())
            return f'Glasses model index set to : {str(dna.glassesTex)}'
        if part == 'backpackModel':
            backpackModels = ToonDNA.BackpackModels
            try:
                value = int(value)
            except BaseException:
                return 'value must be an int '
            if not -1 <= int(value) <= len(backpackModels):
                return f"Backpack model index out of range(0-{len(backpackModels)}"
            dna.backpackModel = value
            invoker.b_setDNAString(dna.makeNetString())
            return f'Backpack model index set to : {str(dna.backpackModel)}'
        if part == 'shoesModel':
            shoesModels = ToonDNA.ShoesModels
            try:
                value = int(value)
            except BaseException:
                return 'value must be an int '
            if not -1 <= int(value) <= len(shoesModels):
                return f"Shoes model index out of range(0-{len(shoesModels)}"
            dna.shoesModel = value
            invoker.b_setDNAString(dna.makeNetString())
            return f'Shoes model index set to : {str(dna.shoesModel)}'

            # TODO textures and colors for accessories
        if part == 'bottexcolor':
            if not -1 < value <= len(ToonDNA.ClothesColors):
                return 'Bottom texture color index out of range(0-{0}).'.format(
                    len(ToonDNA.ClothesColors))
            dna.botTexColor = value
            invoker.b_setDNAString(dna.makeNetString())
            return 'Bottom texture color index set to: {0}'.format(
                str(dna.botTexColor))

        if part == 'save':
            backup = simbase.backups.load('toon', (invoker.doId,), default={})
            backup.setdefault('dna', {})[value] = invoker.getDNAString()
            simbase.backups.save('toon', (invoker.doId,), backup)
            return 'Saved a DNA backup for {0} under : {1}'.format(
                (invoker.getName(), value))

        if part == 'load':
            backup = simbase.backups.load('toon', (invoker.doId,), default={})
            if value not in backup.get('dna', {}):
                return "Couldn't find a DNA backup for {0} under: {1}".format(
                    (invoker.getName(), value))
            invoker.b_setDNAString(backup['dna'][value])
            return 'Restored a DNA backup for {0} under : {1}'.format(
                (invoker.getName(), value))

        return 'Invalid part: ' + part


# class WhoAll(MagicWord):
#   aliases = ['allonline', 'alltoons']
#  desc = 'Reports everyone online.'
# advancedDesc = """Reports everyone online.  Listed with accountName and avatarName."""
# execLocation = MagicWordConfig.EXEC_LOC_SERVER
# accessLevel = 'MODERATOR'

# def handleWord(self, invoker, avId, toon, *args):
#  str = ''
# for obj in list(self.air.doId2do.values()):
#      if hasattr(obj, "accountName"):
#            str += '%s %s\n' % (obj.accountName, obj.name)
#  if not str:
#        str = "No avatars."

#    return str


class ToggleOobe(MagicWord):
    aliases = ["oobe"]
    desc = "Toggles the out of body experience mode, which lets you move the camera freely."
    advancedDesc = "This Magic Word will toggle what is known as 'Out Of Body Experience' Mode, hence the name " \
                   "'Oobe'. When this mode is active, you are able to move the camera around with your mouse- " \
                   "though your camera will still follow your Toon. You can also toggle this mode by pressing the " \
                   "'F4' key, or whichever other keybind you have set."
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'COMMUNITY'
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        base.oobe()
        return "Oobe mode has been toggled."


class ToggleOobeCull(MagicWord):
    aliases = ['oobecull']
    desc = "Toggles out of body experience view with culling debugging"
    advancedDesc = """While in OOBE mode , cull the viewing frustum as if
        it were still attached to our original camera.  This allows us
        to visualize the effectiveness of our bounding volumes."""
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'COMMUNITY'
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        base.oobeCull()
        return "Oobe cull has been toggled."


class ToggleTex(MagicWord):
    aliases = ['tex']
    desc = """Toggles texturing."""
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'COMMUNITY'
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        # No parameters, and now texture viewer: toggle texture.
        base.toggleTexture()

        return 'texturing has been toggled.'


class ToggleTexMemory(MagicWord):
    aliases = ['texmem', 'toggletexmem']
    desc = 'Toggles a handy texture memory watcher utility.'
    advancedDesc = 'Toggles a handy texture memory watcher utility.'
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        base.toggleTexMem()
        return 'Tex memory has been toggled.'


class ToggleShowVertices(MagicWord):
    aliases = ['showvertices', 'toggleverts', 'verts']
    # TODO desc
    advancedDesc = """Toggles a mode that visualizes vertex density per screen
        area."""
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        base.toggleShowVertices()
        return 'Vertices have been toggled.'


class ToggleWireframe(MagicWord):
    aliases = ['wireframe', 'wire', 'togglewire']
    desc = 'Toggles the wireframe'
    advancedDesc = """Toggles between `wireframeOn()` and `wireframeOff()"""
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def handleWord(self, invoker, avId, toon, *args):
        base.toggleWireframe()
        return 'Wireframe has been toggled.'


class ToggleRun(MagicWord):
    aliases = ["run", 'sprint', 'fast', 'speed']
    desc = "Toggles run mode, which gives you a faster running speed."
    advancedDesc = "This Magic Word will toggle Run Mode. When this mode is active, the target can run around at a " \
                   "very fast speed. This running speed stacks with other speed multipliers, such as the one given" \
                   "by the 'SetSpeed' Magic Word. You will automatically toggle Run Mode by using the 'EnableGod' " \
                   "Magic Word."
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    affectRange = [MagicWordConfig.AFFECT_SELF]

    def toggleRun(self):
        inputState.set("debugRunning",
                       inputState.isSet("debugRunning") != True)

    def handleWord(self, invoker, avId, toon, *args):
        self.toggleRun()
        return "Run mode has been toggled."


class SpawnFanfare(MagicWord):
    aliases = ['fanfare']
    desc = 'Spawns a fanfare over the invoker.'
    accessLevel = 'CREATIVE'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT

    def handleWord(self, invoker, avId, av, *args):
        from toontown.battle import Fanfare
        go = Fanfare.makeFanfareWithMessageImage(0, base.localAvatar, 1, "You just did a ~fanfare.  Here's a rake.",
                                                 Vec2(
                                                     0, 0.2), 0.08, base.localAvatar.inventory.buttonLookup(
                                                     1, 1),
                                                 Vec3(0, 0, 0), 4)
        Sequence(go[0], Func(go[1].show),
                 LerpColorScaleInterval(go[1], duration=.5, startColorScale=Vec4(1, 1, 1, 0),
                                        colorScale=Vec4(1, 1, 1, 1)), Wait(2),
                 LerpColorScaleInterval(go[1], duration=.5, startColorScale=Vec4(1, 1, 1, 1),
                                        colorScale=Vec4(1, 1, 1, 0)),
                 Func(go[1].remove)).start()
        return "Fanfare spawned."


class skipMinigame(MagicWord):
    aliases = ['abortminigame', 'endgame']
    desc = 'Skips the current minigame'
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT

    def handleWord(self, invoker, avId, av, *args):
        messenger.send("minigameAbort")
        return "aborting minigame"


class WinMinigame(MagicWord):
    aliases = ['winmg', 'wingame']
    desc = 'Sets current minigame to the win state.'
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT

    def handleWord(self, invoker, avId, av, *args):
        messenger.send("minigameVictory")
        return 'AND A SWEET SWEET SWEET VICTORY YEAH!'


class SkipBattleMovie(MagicWord):
    aliases = ['skipmovie', 'sbm']
    desc = 'Skips the battle movie.'
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT

    def handleWord(self, invoker, avId, av, *args):
        ToontownBattleGlobals.SkipMovie = not ToontownBattleGlobals.SkipMovie
        if ToontownBattleGlobals.SkipMovie:
            response = "battle movies will be skipped"
        else:
            response = "battle movies will be played"
        return response


class MintWarp(MagicWord):
    desc = "Takes you to the room 'roomId', if it exists in the mint floor you're in."
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    arguments = [('roomId', int, True)]

    def handleWord(self, invoker, avId, av, *args):
        if len(args) < 1:
            return ('Usage: ~mintWarp roomId')
        try:
            roomNum = int(args[0])
        except BaseException:
            return ('roomId not found: %s' % args[1])
        if not bboard.has('mint'):
            return ('not in a mint')
        mint = bboard.get('mint')
        if not mint.warpToRoom(roomNum):
            return 'invalid roomId or roomId not in this mint: %s' % args[0]


class MintLayouts(MagicWord):
    desc = "Logs the layout of all mints"
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    arguments = [('roomId', int, True)]

    def handleWord(self, invoker, avId, av, *args):
        from toontown.coghq import MintLayout
        MintLayout.printAllCashbotInfo()
        return 'logged mint layouts'


class SetFactoryZone(MagicWord):
    aliases = ['fzone', 'factoryzone']
    desc = 'Warp to a certain factory zone'
    arguments = [('zoneId', int, True)]
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT

    def handleWord(self, invoker, avId, av, *args):
        if len(args) < 1:
            return ('Usage: ~fzone <zoneNum>')
        zoneId = int(args[0])

        from toontown.coghq import DistributedFactory
        factories = base.cr.doFindAll("DistributedFactory")
        factory = None
        for f in factories:
            if isinstance(f, DistributedFactory.DistributedFactory):
                factory = f
                break
        if factory is None:
            return ('factory not found')
        factory.warpToZone(zoneId)


class Catalog(MagicWord):
    desc = 'Handles management of catalog'
    advancedDesc = """    next - generate the next weeks catalog
    week # - generate the catalog for week number #
    season ##/## - present the seasonal catalog items for day ## / month ##
    clear - reset to initial week
    deliver - cause all pending deliveries to be sent to mailbox
    after - optional parameter to delay specified action by # minutes"""
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('command', str, False, ''), ('n', str, False, '0')]

    def handleWord(self, invoker, avId, av, *args):
        now = time.time()

        # There may be an optional "after" parameter on many of these
        # commands, which specifies the number of minutes to delay
        # before doing the action.
        afterMinutes = 0
        if "after" in args:
            a = args.index("after")
            afterMinutes = int(args[a + 1])
            del args[a + 1]
            del args[a]

        if args[0] == '':
            # No parameter: report the current catalog.
            duration = (av.catalogScheduleNextTime * 60) - time.time()
            response = "Week %d, next catalog in %s." % \
                       (av.catalogScheduleCurrentWeek,
                        PythonUtil.formatElapsedSeconds(duration))

        elif args[0] == "next":
            # ~catalog next: advance to the next catalog.
            week = av.catalogScheduleCurrentWeek + 1
            self.air.catalogManager.forceCatalog(av, week, afterMinutes)
            response = "Issued catalog for week %s." % (week)

        elif args[0] == "week":
            # ~catalog week n: force to the catalog of the nth week.
            # Note: need to have catalog-skip-seeks set to true to jump
            # more than one week
            week = int(args[1])
            if week > 0:
                self.air.catalogManager.forceCatalog(av, week, afterMinutes)
                response = "Forced to catalog week %s." % (week)
            else:
                response = "Invalid catalog week %s." % (week)

        elif args[0] == "season":
            # ~catalog season mm/dd: regenerate the monthly catalog
            # items as if it were the indicated month and day.
            if len(args) == 2:
                mmdd = args[1].split('/')
                mm = int(mmdd[0])
                dd = int(mmdd[1])
            else:
                mm = int(args[2])
                dd = int(args[3])

            self.air.catalogManager.forceMonthlyCatalog(av, mm, dd)
            response = "%s items for %d/%0d." % (
                len(av.monthlyCatalog), mm, dd)

        elif (args[0] == "clear") or (args[0] == "reset"):
            # ~catalog clear: reset the catalog (and the back catalog)
            # to its initial state.
            av.b_setCatalog(CatalogItemList.CatalogItemList(),
                            CatalogItemList.CatalogItemList(),
                            CatalogItemList.CatalogItemList())
            av.catalogScheduleCurrentWeek = 0
            av.catalogScheduleNextTime = 0
            self.air.catalogManager.deliverCatalogFor(av)
            response = "Catalog reset."

        elif args[0] == "deliver":
            # ~catalog deliver: force the immediate delivery of all
            # of the on-order item(s).

            now = (int)(time.time() / 60 + 0.5)
            deliveryTime = now + afterMinutes

            for item in av.onOrder:
                item.deliveryDate = deliveryTime
            av.onOrder.markDirty()
            av.b_setDeliverySchedule(av.onOrder)

            response = "Delivered %s item(s)." % (len(av.onOrder))

        else:
            response = "Invalid catalog command: %s" % (args[1])

        return response


class ResetFurniture(MagicWord):
    desc = "Resets the invoker's furniture"
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, toon, *args):
        av = invoker
        house = None
        if av.houseId:
            house = self.air.doId2do.get(av.houseId)
        if house:
            house.setInitialFurniture()
            house.resetFurniture()
            response = "Furniture reset."
        else:
            response = "Could not find house."
        return response


class SetFishingRod(MagicWord):
    desc = "Sets the target's fishing rod."
    aliases = ['rod', 'fishingrod']
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        # Sets reward tier and optionally index
        rodId = int(args[0])
        if ((rodId > FishGlobals.MaxRodId) or
                (rodId < 0)):
            return ("Invalid rod: %s" % (rodId))
        else:
            av.b_setFishingRod(rodId)
            return ("New fishing rod: %s" % (rodId))


class SetNPCFriend(MagicWord):
    aliases = ['setsoscard', 'sos', 'setsos']
    desc = "Modifies the target's specified sos card amount"
    advancedDesc = 'List of sos cards ids to names will be in discord.'
    arguments = [('npcName', str, True), ('amount', int, False, 1)]
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        npcName = str(args[0])
        numCalls = int(args[1])
        if numCalls > 100 or numCalls <= 0:
            return 'Invalid amount for sos card'
        for npcId, sosName in TTLocalizer.NPCToonNames.items():
            if sosName.lower() == npcName.lower():
                if npcId not in NPCToons.npcFriends:
                    continue
                break
        else:
            return 'Invalid sos name'

        if (numCalls == 0) and (npcId in av.NPCFriendsDict):
            del av.NPCFriendsDict[npcId]
        else:
            av.NPCFriendsDict[npcId] = numCalls
        av.d_setNPCFriendsDict(av.NPCFriendsDict)
        return "Added sos card {0}".format(npcName)


class GiveBessies(MagicWord):
    aliases = ['uberdrop', 'pianos', 'bessies', 'barnaclebessies']
    desc = 'Gives 100 barnacle bessies to invoker.'
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, av, *args):
        if self.doNpcFriend(invoker, 1116, 100):
            return "got bessies"
        else:
            return "error getting bessies"


# class BossBattle(MagicWord):
#   desc = 'Takes the toon to a common bossBattle arena.'
#  advancedDesc = """Takes the toon to a common bossBattle arena, or sets the
# bossBattle state to one of the indicated tokens."""
# arguments = [('dept', str, False , ''), ()]

class ToggleDisguisePage(MagicWord):
    aliases = ['disguisepage']
    desc = 'Turns on or off the disguise page flag.  The default is on (1).'
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('flag', bool, False, True)]

    def handleWord(self, invoker, avId, av, *args):
        flag = args[0]
        av.b_setDisguisePageFlag(flag)
        return "Disguise page = %s" % (flag)


class GiveAllParts(MagicWord):
    aliases = ['allparts']
    desc = 'Gives the toon all cog suit parts in the indicated depts.'
    advancedDesc = """Gives the toon all cog suit parts in the indicated depts.  [depts]
    may be one or more of the letters c, l, m, or s, with no spaces or
    punctuation between, or the string "all" to indicate all depts.
    If omitted, the default is "all"."""

    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('dept', str, False, 'all')]

    def handleWord(self, invoker, avId, toon, *args):
        for dept in self.getDepts(args[0]):
            parts = toon.getCogParts()
            parts[dept] = CogDisguiseGlobals.PartsPerSuitBitmasks[dept]

        toon.b_setCogParts(parts)
        return "Set cog parts: %s" % (parts)


class GivePart(MagicWord):
    advancedDesc = """Gives one cog suit part as if from the indicated factory type.
    [depts] as above.  factoryType may be one of leg, arm, torso, or
    fullSuit; the default is fullSuit."""
    desc = "Gives cog suit part to toon."
    aliases = ['part']
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('dept', str, False, 'all'),
                 ('factoryType', str, False, 'fullSuit')]

    def handleWord(self, invoker, avId, toon, *args):
        depts = self.getDepts(args[0])
        if args[1] != 'fullSuit':
            # trust that user typed the factory type correctly...
            try:
                factoryType = args[1]
            except BaseException:
                return 'Invalid part specified'
        else:
            factoryType = ToontownGlobals.FT_FullSuit

        for dept in depts:
            toon.giveGenericCogPart(factoryType, dept)

        return "Set cog parts: %s" % (toon.getCogParts())


class SetMerits(MagicWord):
    aliases = ['merits']
    accessLevel = 'DEVELOPER'
    desc = "Sets the toon's cog merits for the indicated depts to the given integer value."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('dept', str, False, 'all'), ('merits', int, False, 32767)]

    def handleWord(self, invoker, avId, av, *args):
        depts = self.getDepts(args[0])
        if args[1]:
            numMerits = int(args[1])
            if numMerits > 32767:
                numMerits = 32767
        else:
            return "Specify number of merits to set."

        merits = av.getCogMerits()[:]
        for dept in depts:
            merits[dept] = numMerits
        av.b_setCogMerits(merits)

        return "Set cog merits: %s" % (merits)


class Promote(MagicWord):
    accessLevel = 'DEVELOPER'
    desc = "Promotes the toon in the indicated dept(s)."
    advancedDesc = """Promotes the toon in the indicated dept(s).  The promotion occurs
    regardless of whether the toon has earned sufficient merits."""
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('dept', str, False, 'all')]

    def handleWord(self, invoker, avId, av, *args):
        depts = self.getDepts(args[0])

        for dept in depts:
            av.b_promote(dept)

        return "Set cogTypes: %s and cogLevels: %s" % (
            av.getCogTypes(), av.getCogLevels())


class SetCogSuit(MagicWord):
    aliases = ['cogsuit', 'setcogdisguise', 'disguise', 'setsuitdisguise']
    accessLevel = 'DEVELOPER'
    desc = "Sets the toon to the indicated cog type."
    advancedDesc = """Sets the toon to the indicated cog type (e.g. 'gh' for Glad
    Hander) and level for the appropriate dept. If no arg is specified for cogtype, reset cog suits in all depts to the initial level."""
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('cogtype', str, False, 'clear'),
                 ('dept', str, False, ''), ('level', int, False, 0)]

    def handleWord(self, invoker, avId, av, *args):
        if len(args) > 0:
            cogType = args[0]
        else:
            return "Specify cog type, or 'clear'."

        if cogType == 'clear':
            av.b_setCogTypes([0, 0, 0, 0])
            av.b_setCogLevels([0, 0, 0, 0])

        elif cogType == 'on':
            if len(args) > 1 and args[1] in SuitDNA.suitDepts:
                dept = SuitDNA.suitDepts.index(args[1])
                av.b_setCogIndex(dept)
            else:
                return "Specify dept."
            return

        elif cogType == 'off':
            av.b_setCogIndex(-1)
            return

        else:
            if cogType not in SuitDNA.suitHeadTypes:
                return 'Invalid cogType'
            if dept not in SuitDNA.suitDepts:
                return 'Invalid department'

            dept = SuitDNA.getSuitDept(cogType)
            if dept is None:
                return "Unknown cog type: %s" % (cogType)

            deptIndex = SuitDNA.suitDepts.index(dept)
            _type = SuitDNA.getSuitType(cogType)
            minLevel = SuitBattleGlobals.SuitAttributes[cogType]['level']

            # determine max level (usually minLevel + 4, but 50 for last cog)
            if _type >= (SuitDNA.suitsPerDept - 1):
                maxLevel = ToontownGlobals.MaxCogSuitLevel + 1
            else:
                maxLevel = minLevel + 4

            if args[2] != 0:
                level = int(args[2]) - 1
                if level < minLevel or level > maxLevel:
                    return "Invalid level for %s (should be %s to %s)" % (
                        cogType, minLevel + 1, minLevel + 5)
            else:
                level = minLevel

            cogTypes = av.getCogTypes()[:]
            cogLevels = av.getCogLevels()[:]
            cogTypes[deptIndex] = _type - 1
            cogLevels[deptIndex] = level
            av.b_setCogTypes(cogTypes)
            av.b_setCogLevels(cogLevels)

        return "Set cogTypes: %s and cogLevels: %s" % (
            av.getCogTypes(), av.getCogLevels())


class SetPinkSlips(MagicWord):
    aliases = ['fires', 'pinkslips', 'setfires']
    accessLevel = 'DEVELOPER'
    desc = "Gives the target a certain amount of pink slips."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('pinkslips', int, False, '255')]

    def handleWord(self, invoker, avId, av, *args):
        if len(args) > 0:
            numSlips = int(args[0])
            if numSlips > 255:
                numSlips = 255
            if numSlips <= 0:
                numSlips = 1

        else:
            return ("Specify number of pinkSlips to set.")

        av.b_setPinkSlips(numSlips)

        return ("Set PinkSlips: %s" % (numSlips))


class ToggleHoliday(MagicWord):
    aliases = ['holiday']
    desc = 'Start or stop a holiday'
    advancedDesc = """Specify a holiday id number. For the second argument use
                      a command like start, end or list.
                   """
    accessLevel = 'ADMIN'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [('holidayId', int, True), ('command', 'str',
                                            False, ''), ('extra', str, False, '')]

    def handleWord(self, invoker, avId, av, *args):
        holiday = 5
        fStart = 1
        if args[1] != '':
            if args[1] == 'list':
                return (
                    "1: July 4\n2: New Years\n3: Halloween\n4: Winter Decorations\n5: Skelecog Invades\n6: Mr. Holly Invades\n7: Fish Bingo\n8: Species Election\n9: Black Cat\n10: Resistance Event\n11: Reset Daily Recs\n12: Reset Weekly Recs\n13: Trick-or-Treat\n14: Grand Prix\n17: Trolley Metagame")
        holiday = int(args[0])
        doPhase = None
        stopForever = False
        if args[1] != '':
            if args[1] == 'start':
                fStart = 1
            elif args[1] == 'end':
                fStart = 0
                if args[2] != '':
                    if args[2] == 'forever':
                        stopForever = True
            elif args[1] == 'phase':
                if args[2] != '':
                    doPhase = args[2]
                else:
                    return ("need a number after phase")
            else:
                return (
                    'Arg 2 should be "start" or "end" or "end forever" or "phase"')
        if doPhase:
            result = self.air.holidayManager.forcePhase(holiday, doPhase)
            return "succeeded=%s forcing holiday %d to phase %s" % (
                result, holiday, doPhase)
        elif fStart:
            self.air.holidayManager.startHoliday(holiday)
            return (
                senderId, "Starting holiday %d" % holiday)
        else:
            self.air.holidayManager.endHoliday(holiday, stopForever)
            return (
                "Ending holiday %d stopForever=%s" % (holiday, stopForever))


class DamageCFO(MagicWord):
    desc = 'Damages the cfo'
    aliases = ['hitcfo']
    arguments = [("damage", int, False, 1)]
    accessLevel = 'DEVELOPER'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER

    def handleWord(self, invoker, avId, toon, *args):
        dmg = args[0]
        from toontown.suit.DistributedCashbotBossAI import DistributedCashbotBossAI
        boss = None
        for do in simbase.air.doId2do.values():
            if isinstance(do, DistributedCashbotBossAI):
                if invoker.doId in do.involvedToons:
                    boss = do
                    break
        if not boss:
            return "You aren't in a CFO!"

        boss.magicWordHit(dmg, invoker.doId)
        return 'Damaged cfo for {0} damage'.format(dmg)


class kickplayer(MagicWord):
    desc = 'Kicks the targeted player with a given reason.'
    aliases = ['kicktoon', 'kick']
    arguments = [('reason', str, True)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'MODERATOR'

    def handleWord(self, invoker, avId, toon, *args):
        reason = args[0]
        if invoker == toon:
            return 'Imagine trying to kick yourself smh use ~~'
        if reason == '' or reason is None:
            return 'Need a reason to kick this person'
        dg = PyDatagram()
        # CLIENTAGENT_EJECT is a global set in direct.distributed.MsgTypes,
        # why does p3d like messing with globals so much :grief:
        dg.addServerHeader(self.GetPuppetConnectionChannel(avId), simbase.air.ourChannel,
                           MsgTypes.MsgName2Id['CLIENTAGENT_EJECT'])
        dg.addUint16(168)
        dg.addString(reason)
        simbase.air.send(dg)
        return f'Successfully kicked {toon.getName()}'


class warntoon(MagicWord):
    desc = 'Warns the targeted toon with a given reason.'
    arguments = [('reason', str, True)]
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    accessLevel = 'MODERATOR'
    aliases = ['warn', 'warnplayer']

    def handleWord(self, invoker, avId, toon, *args):
        reason = args[0]
        if toon == invoker:
            return 'You can\'t warn yourself!'

        toon.sendUpdate('warnToon', [reason])
        return f'Warned {toon.getName()} for {reason}!'


class StunAllGoons(MagicWord):
    aliases = ['disablegoons', 'stungoons']
    desc = 'stun all of the goons in the CFO battle.'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        from toontown.suit import DistributedBossCog
        bossCog = None
        for distObj in list(self.cr.doId2do.values()):
            if isinstance(distObj, DistributedBossCog.DistributedBossCog):
                bossCog = distObj
                break
        if not bossCog:
            return "You aren't in a CFO!"
        bossCog.stunAllGoons()
        return 'Stunned all goons'


class DestroyAllGoons(MagicWord):
    aliases = ['destroygoons']
    desc = 'Destroys all of the goons in the CFO.'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        from toontown.suit import DistributedBossCog
        bossCog = None
        for distObj in list(self.cr.doId2do.values()):
            if isinstance(distObj, DistributedBossCog.DistributedBossCog):
                bossCog = distObj
                break
        if not bossCog:
            return "You aren't in a CFO!"
        bossCog.destroyAllGoons
        return 'Destroyed all goons'


class leaveRace(MagicWord):
    desc = 'Leaves current race'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'COMMUNITY'

    def handleWord(self, invoker, avId, toon, *args):
        messenger.send('leaveRace')
        return 'Left race'


class ShowSuitPaths(MagicWord):
    aliases = ['showpaths']
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT

    def handleWord(self, invoker, avId, av, *args):
        for obj in list(self.cr.doId2do.values()):
            if isinstance(obj, DistributedSuitPlanner.DistributedSuitPlanner):
                obj.showPaths()
        place = base.cr.playGame.getPlace()
        if hasattr(place, "showPaths"):
            place.showPaths()


class HideSuitPaths(MagicWord):
    aliases = ['hidepaths']
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT

    def handleWord(self, invoker, avId, av, *args):
        for obj in list(self.cr.doId2do.values()):
            if isinstance(obj, DistributedSuitPlanner.DistributedSuitPlanner):
                obj.hidePaths()
        place = base.cr.playGame.getPlace()
        if hasattr(place, "hidePaths"):
            place.hidePaths()


class Listen(MagicWord):
    desc = 'unfilters the chat for the client'
    accessLevel = 'COMMUNITY'
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT

    def handleWord(self, invoker, avId, av, *args):
        base.localAvatar.garbleChat = 0


class ToggleCollisionsOn(MagicWord):
    aliases = ['clip', 'collisionson']
    desc = "Enables collisions for the invoker."
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'COMMUNITY'

    def handleWord(self, invoker, avId, toon, *args):
        toon.collisionsOn()


class ToggleCollisionsOff(MagicWord):
    aliases = ['noclip', 'CollisionsOff']
    desc = "Disables collisions for the target."
    execLocation = MagicWordConfig.EXEC_LOC_CLIENT
    accessLevel = 'COMMUNITY'

    def handleWord(self, invoker, avId, toon, *args):
        toon.collisionsOff()


class SetUnites(MagicWord):
    aliases = ['unites']
    desc = 'Restock all resistance messages.'
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [("amount", int, False, 32767)]
    accessLevel = 'DEVELOPER'

    def handleWord(self, invoker, avId, toon, *args):
        value = min(args[0], 32767)
        invoker.restockAllResistanceMessages(value)
        return "Restocked {0} unites!".format(value)


class SkipVP(MagicWord):
    desc = "Skips to the indicated round of the VP."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [("round", str, False, "next")]
    accessLevel = "DEVELOPER"

    def handleWord(self, invoker, avId, toon, *args):
        round = args[0]
        from toontown.suit.DistributedSellbotBossAI import DistributedSellbotBossAI
        boss = None
        for do in simbase.air.doId2do.values():
            if isinstance(do, DistributedSellbotBossAI):
                if invoker.doId in do.involvedToons:
                    boss = do
                    break
        if not boss:
            return "You aren't in a VP!"

        round = round.lower()

        if round == 'three':
            if boss.state in ('PrepareBattleThree', 'BattleThree'):
                return "You can not return to previous rounds!"
            else:
                boss.exitIntroduction()
                boss.b_setState('PrepareBattleThree')
                return "Skipping to final round."
        elif round == 'two':
            if boss.state in ('PrepareBattleThree', 'BattleThree'):
                return "You can not return to previous rounds!"
            else:
                boss.exitIntroduction()
                boss.b_setState('RollToBattleTwo')
                return 'Skipping to 2nd round.'
        if round == 'next':
            if boss.state in ('PrepareBattleOne', 'BattleOne'):
                boss.exitIntroduction()
                boss.b_setState('RollToBattleTwo')
                return "Skipping current round..."
            elif boss.state in ('PrepareBattleTwo', 'BattleTwo'):
                boss.b_setState('PrepareBattleThree')
                return 'Skipping to final round.'

            elif boss.state in ('PrepareBattleThree', 'BattleThree'):
                boss.exitIntroduction()
                boss.b_setState('Victory')
                return "Killing the vp. :O "


class SkipCFO(MagicWord):
    desc = "Skips to the indicated round of the CFO."
    execLocation = MagicWordConfig.EXEC_LOC_SERVER
    arguments = [("round", str, False, "next")]
    accessLevel = "DEVELOPER"

    def handleWord(self, invoker, avId, toon, *args):
        battle = args[0]

        from toontown.suit.DistributedCashbotBossAI import DistributedCashbotBossAI
        boss = None
        for do in simbase.air.doId2do.values():
            if isinstance(do, DistributedCashbotBossAI):
                if invoker.doId in do.involvedToons:
                    boss = do
                    break
        if not boss:
            return "You aren't in a CFO!"

        battle = battle.lower()

        if battle == 'two':
            if boss.state in ('PrepareBattleThree', 'BattleThree'):
                return "You can not return to previous rounds!"
            else:
                boss.exitIntroduction()
                boss.b_setState('PrepareBattleThree')
                return "Skipping to last round..."

        if battle == 'next':
            if boss.state in ('PrepareBattleOne', 'BattleOne'):
                boss.exitIntroduction()
                boss.b_setState('PrepareBattleThree')
                return "Skipping current round..."
            elif boss.state in ('PrepareBattleThree', 'BattleThree'):
                boss.exitIntroduction()
                boss.b_setState('Victory')
                return "Skipping final round..."

# TODO add skipcj and skipcfo


# Instantiate all classes defined here to register them.
# A bit hacky, but better than the old system
for item in list(globals().values()):
    if isinstance(item, type) and issubclass(item, MagicWord):
        i = item()
