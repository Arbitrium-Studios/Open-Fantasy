from panda3d.core import ConfigVariableString
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.launcher.QuickLauncher import QuickLauncher
import time
import random
import os
from ctypes import *
from direct.task import Task
import threading
import ast
import pypresence
from pypresence.exceptions import PipeClosed, ServerError, PyPresenceException, DiscordNotFound

clientId = '1384706254978420816' # This is also called the Application ID on the Discord Developer Portal
gameLogo = 'toontown-logo'
gameName = TTLocalizer.setGameName
canEnableRichPresence = bool(False)

zone2imgdesc = { # A dict of ZoneID -> An image and a description

    ToontownGlobals.FoggyFjord: ['foggy_fjord_playground', f'Sailing around the {TTLocalizer.lFoggyFjord} playground'],
    ToontownGlobals.BarnacleBoulevard: ['foggy_fjord_street_barnacle_boulevard', f'Sailing through {TTLocalizer.GlobalStreetNames[ToontownGlobals.BarnacleBoulevard][-1]} in {TTLocalizer.lFoggyFjord}'],
    ToontownGlobals.SeaweedStreet: ['foggy_fjord_street_seaweed_street', f'Sailing through {TTLocalizer.GlobalStreetNames[ToontownGlobals.SeaweedStreet][-1]} in {TTLocalizer.lFoggyFjord}'],
    ToontownGlobals.LighthouseLane: ['foggy_fjord_street_lighthouse_lane', f'Sailing through {TTLocalizer.GlobalStreetNames[ToontownGlobals.LighthouseLane][-1]} in {TTLocalizer.lFoggyFjord}'],

    ToontownGlobals.ToontownCentral: ['toontown_central_playground', f'Hanging around the {TTLocalizer.lToontownCentral} playground'],
    ToontownGlobals.SillyStreet: ['toontown_central_street_silly_street', f'Walking through {TTLocalizer.GlobalStreetNames[ToontownGlobals.SillyStreet][-1]} in {TTLocalizer.lToontownCentral}'],
    ToontownGlobals.LoopyLane: ['toontown_central_street_loopy_lane', f'Walking through {TTLocalizer.GlobalStreetNames[ToontownGlobals.LoopyLane][-1]} in {TTLocalizer.lToontownCentral}'],
    ToontownGlobals.PunchlinePlace: ['toontown_central_street_punchline_place', f'Walking through {TTLocalizer.GlobalStreetNames[ToontownGlobals.PunchlinePlace][-1]} in {TTLocalizer.lToontownCentral}'],
    ToontownGlobals.TutorialTerrace: ['toontown_central_street_toontorial_terrace', f'Walking through {TTLocalizer.GlobalStreetNames[ToontownGlobals.TutorialTerrace][-1]}'.title()],

    ToontownGlobals.TundraWonderland: ['tundra_wonderland_playground', f'Chilling in {TTLocalizer.lTundraWonderland} playground'],
    ToontownGlobals.WalrusWay: ['tundra_wonderland_street_walrus_way', f'Freezing all the way through {TTLocalizer.GlobalStreetNames[ToontownGlobals.WalrusWay][-1]} in {TTLocalizer.lTundraWonderland}'],
    ToontownGlobals.SleetStreet: ['tundra_wonderland_street_sleet_street', f'Freezing all the way through {TTLocalizer.GlobalStreetNames[ToontownGlobals.SleetStreet][-1]} in {TTLocalizer.lTundraWonderland}'],
    ToontownGlobals.PolarPlace: ['tundra_wonderland_street_polar_place', f'Freezing all the way through {TTLocalizer.GlobalStreetNames[ToontownGlobals.PolarPlace][-1]} in {TTLocalizer.lTundraWonderland}'],

    ToontownGlobals.HarmoniousHaven: ['harmonious_haven_playground', f'Feeling the flow of the music in {TTLocalizer.lHarmoniousHaven} playground'],
    ToontownGlobals.AltoAvenue: ['harmonious_haven_street_alto_avenue', f'Skipping through {TTLocalizer.GlobalStreetNames[ToontownGlobals.AltoAvenue][-1]} in {TTLocalizer.lHarmoniousHaven}'],
    ToontownGlobals.BaritoneBoulevard: ['harmonious_haven_street_baritone_boulevard', f'Skipping through {TTLocalizer.GlobalStreetNames[ToontownGlobals.BaritoneBoulevard][-1]} in {TTLocalizer.lHarmoniousHaven}'],
    ToontownGlobals.TenorTerrace: ['harmonious_haven_street_tenor_terrace', f'Skipping through {TTLocalizer.GlobalStreetNames[ToontownGlobals.TenorTerrace][-1]} in {TTLocalizer.lHarmoniousHaven}'],

    ToontownGlobals.FloweringGrove: ['flowering_grove_playground', f'Smelling the flowers in the {TTLocalizer.lFloweringGrove} playground'],
    ToontownGlobals.ElmStreet: ['flowering_grove_street_elm_street', f'Strolling through {TTLocalizer.GlobalStreetNames[ToontownGlobals.ElmStreet][-1]} in {TTLocalizer.lFloweringGrove}'],
    ToontownGlobals.MapleStreet: ['flowering_grove_street_maple_street', f'Strolling through {TTLocalizer.GlobalStreetNames[ToontownGlobals.MapleStreet][-1]} in {TTLocalizer.lFloweringGrove}'],
    ToontownGlobals.OakStreet: ['flowering_grove_street_oak_street', f'Strolling through {TTLocalizer.GlobalStreetNames[ToontownGlobals.OakStreet][-1]} in {TTLocalizer.lFloweringGrove}'],

    ToontownGlobals.AcornAcres: ['acorn_acres_playground', f'Hiking through {TTLocalizer.lAcornAcres}'],

    ToontownGlobals.ToontownStadium: ['toontown_stadium_racing', f'Drifting through {TTLocalizer.lToontownStadium}'],
    ToontownGlobals.GolfZone: ['toontown_stadium_minigolf', f'Putting around {TTLocalizer.lGolfZone}'], # Remove this once we've begun merging Goofy Speedway and the Mini-Golf Area into Toontown Stadium
    # ToontownGlobals.FunnyFarms: ['funny_farms_playground', f'Uncovering the mysteries of {TTLocalizer.lFunnyFarms}']

    ToontownGlobals.TwilightDreamland: ['twilight_dreamland_playground', f'Dreaming {TTLocalizer.GlobalStreetNames[ToontownGlobals.TwilightDreamland][-2]} {TTLocalizer.lTwilightDreamland} playground'],
    ToontownGlobals.LullabyLane: ['twilight_dreamland_street_lullaby_lane', f'Sleepwalking through {TTLocalizer.GlobalStreetNames[ToontownGlobals.LullabyLane][-1]} in {TTLocalizer.lTwilightDreamland}'],
    ToontownGlobals.PajamaPlace: ['twilight_dreamland_street_pajama_place', f'Sleepwalking through {TTLocalizer.GlobalStreetNames[ToontownGlobals.PajamaPlace][-1]} in {TTLocalizer.lTwilightDreamland}'],
    ToontownGlobals.TwilightTerrace: ['twilight_dreamland_street_twilight_terrace', f'Sleepwalking through {TTLocalizer.GlobalStreetNames[ToontownGlobals.TwilightTerrace][-1]} in {TTLocalizer.lTwilightDreamland}'],

    ToontownGlobals.BossbotHQ: ['bossbot_hq_country_club', f'Snooping around the {TTLocalizer.GlobalStreetNames[ToontownGlobals.BossbotHQ][-1]} {TTLocalizer.lInBossbotHQ}'],
    ToontownGlobals.BossbotLobby: ['bossbot_hq_clubhouse_lobby', f'Waiting {TTLocalizer.GlobalStreetNames[ToontownGlobals.BossbotLobby][-2]} {TTLocalizer.GlobalStreetNames[ToontownGlobals.BossbotLobby][-1]} {TTLocalizer.lInBossbotHQ}'],
    ToontownGlobals.BossbotCountryClubIntA: ['bossbot_hq_the_front_three', f'Infiltrating {TTLocalizer.GlobalStreetNames[ToontownGlobals.BossbotCountryClubIntA][-1]} {TTLocalizer.lInBossbotHQ}'],
    ToontownGlobals.BossbotCountryClubIntB: ['bossbot_hq_the_middle_six', f'Infiltrating {TTLocalizer.GlobalStreetNames[ToontownGlobals.BossbotCountryClubIntB][-1]} {TTLocalizer.lInBossbotHQ}'],
    ToontownGlobals.BossbotCountryClubIntC: ['bossbot_hq_the_back_nine', f'Infiltrating {TTLocalizer.GlobalStreetNames[ToontownGlobals.BossbotCountryClubIntC][-1]} {TTLocalizer.lInBossbotHQ}'],

    ToontownGlobals.SellbotHQ: ['sellbot_hq_courtyard', f'Waltzing around the {TTLocalizer.GlobalStreetNames[ToontownGlobals.SellbotHQ][-1]} {TTLocalizer.lInSellbotHQ}'],
    ToontownGlobals.SellbotLobby: ['sellbot_hq_towers_lobby', f'Waiting {TTLocalizer.GlobalStreetNames[ToontownGlobals.SellbotLobby][-2]} {TTLocalizer.GlobalStreetNames[ToontownGlobals.SellbotLobby][-1]} {TTLocalizer.lInSellbotHQ}'],
    ToontownGlobals.SellbotFactoryExt: ['sellbot_hq_factory_exterior', f'Sneaking around the {TTLocalizer.GlobalStreetNames[ToontownGlobals.SellbotFactoryExt][-1]} Exterior {TTLocalizer.lInSellbotHQ}'],
    ToontownGlobals.SellbotFactoryInt: ['sellbot_hq_factory_interior', f'Infiltrating the {TTLocalizer.GlobalStreetNames[ToontownGlobals.SellbotFactoryInt][-1]} {TTLocalizer.lInSellbotHQ}'],

    ToontownGlobals.CashbotHQ: ['cashbot_hq_trainyard', f'Dodging Trains {TTLocalizer.GlobalStreetNames[ToontownGlobals.CashbotHQ][-2]} {TTLocalizer.GlobalStreetNames[ToontownGlobals.CashbotHQ][-1]} {TTLocalizer.lInCashbotHQ}'],
    ToontownGlobals.CashbotLobby: ['cashbot_hq_lobby', f'Waiting {TTLocalizer.GlobalStreetNames[ToontownGlobals.CashbotLobby][-2]} {TTLocalizer.lCashbotVaultLobby} {TTLocalizer.lInCashbotHQ}'],
    ToontownGlobals.CashbotMintIntA: ['cashbot_hq_mint_coin', f'Infiltrating the {TTLocalizer.GlobalStreetNames[ToontownGlobals.CashbotMintIntA][-1]} {TTLocalizer.lInCashbotHQ}'],
    ToontownGlobals.CashbotMintIntB: ['cashbot_hq_mint_dollar', f'Infiltrating the {TTLocalizer.GlobalStreetNames[ToontownGlobals.CashbotMintIntB][-1]} {TTLocalizer.lInCashbotHQ}'],
    ToontownGlobals.CashbotMintIntC: ['cashbot_hq_mint_bullion', f'Infiltrating the {TTLocalizer.GlobalStreetNames[ToontownGlobals.CashbotMintIntC][-1]} {TTLocalizer.lInCashbotHQ}'],

    ToontownGlobals.LawbotHQ: ['lawbot_hq_courtyard', f'Wandering around the {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotHQ][-1]} {TTLocalizer.lInLawbotHQ}'],
    ToontownGlobals.LawbotLobby: ['lawbot_hq_courthouse_lobby', f'Waiting {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotLobby][-2]} Lawbot {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotLobby][-1]} {TTLocalizer.lInLawbotHQ}'],
    ToontownGlobals.LawbotOfficeExt: ['lawbot_hq_da_office_lobby', f'Strolling through the {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotOfficeExt][-1]} {TTLocalizer.lInLawbotHQ}'],
    ToontownGlobals.LawbotStageIntA: ['lawbot_hq_da_office_a', f'Infiltrating the {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotStageIntA][-1]} {TTLocalizer.lInLawbotHQ}'],
    ToontownGlobals.LawbotStageIntB: ['lawbot_hq_da_office_b', f'Infiltrating the {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotStageIntB][-1]} {TTLocalizer.lInLawbotHQ}'],
    ToontownGlobals.LawbotStageIntC: ['lawbot_hq_da_office_c', f'Infiltrating the {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotStageIntC][-1]} {TTLocalizer.lInLawbotHQ}'],
    ToontownGlobals.LawbotStageIntD: ['lawbot_hq_da_office_d', f'Infiltrating the {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotStageIntD][-1]} {TTLocalizer.lInLawbotHQ}'],

    ToontownGlobals.MyEstate: ['toon-estate', f'Hanging out {TTLocalizer.lAtHome}'],
}

class DiscordRPC(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('DiscordRPC')
    hasFinishedCoolDownToggle = bool(False)

    def __init__(self):
        self.RPC = None
        self.avatarNameKey = 'AVATAR_NAME'
        self.zoneIdKey = 'ZONE_ID'
        self.currentDetailsKey = 'CURRENT_DETAILS'
        self.previousDetailsKey = 'PREVIOUS_DETAILS'

        if base.wantRichPresence:
            self.enable()
        else:
            self.disable()

        self.gameName = str(gameName)

        toontownPlayTokenKey = QuickLauncher.getToontownFantasyPlayTokenKey(self)
        self.username = QuickLauncher.getUsername(self)

        self.hasFinishedCoolDownKey = ToontownGlobals.hasFinishedCoolDownKey
        self.canEnableRichPresenceKey = ToontownGlobals.canEnableRichPresenceKey

        toontownPlayTokenKeyStrQuotated = f'"toontownPlayTokenKey"'
        toontownPlayTokenKeyQuotated = f'"{toontownPlayTokenKey}"'

        DiscordRPC.notify.debug(f'The {toontownPlayTokenKeyStrQuotated} is set to {toontownPlayTokenKeyQuotated}.\n')
        self.toggle_cooldown_time = 30.0

        self.hasBeenEnabledBefore = bool(False)
        self.canEnableRichPresenceBool = bool(True)
        QuickLauncher.setValue(self, key=self.canEnableRichPresenceKey, value=f'{self.canEnableRichPresenceBool}')
        self.canEnableRichPresence = QuickLauncher.getValue(self, key=self.canEnableRichPresenceKey, default=None)
        self.canEnableRichPresence = ast.literal_eval(self.canEnableRichPresence.strip().title())

        self.updateTask = None
        self.details = '   ' # text next to photo
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        self.large_image = gameLogo # Sets the main image displayed on the Discord profile
        self.large_text = self.gameName # Hover text for main image 
        self.smallLogo = 'game-icon' # Set the image that appears in the bottom-right corner of the main image
        self.state = '   ' # Set the text that appears underneath the details (used for boarding groups)
        self.serverVersion = ConfigVariableString('server-version', '').value
        self.smallTxt = f'{self.serverVersion}' # Sets the text that appears when you hover over the smaller logo
        self.discordTaskLoop = None

    def stopBoarding(self):
        if not base.wantRichPresence:
            return

        self.state = '  '
        self.setData()

    def allowBoarding(self, size):
        if not base.wantRichPresence:
            return

        self.state = str(TTLocalizer.lInBoardingGroup)
        self.setData()

    def setBoarding(self, size):
        if not base.wantRichPresence:
            return

        self.setData()

    def setData(self, details=None, large_image=None, large_text=None, smallLogo=None, smallTxt=None):
        if details is None:
            details = self.details

        if large_image is None:
            large_image = self.large_image

        if large_text is None:
            large_text = self.large_text

        if smallLogo is None:
            smallLogo = self.smallLogo # Set the image that appears in the bottom-right corner of the main image

        if smallTxt is None:
            smallTxt = self.smallTxt # Sets the text that appears when you hover over the smaller logo

        if self.RPC is not None:
            try:
                self.RPC.update(name=f'{self.gameName}', state=self.state, details=details, large_image=large_image, large_text=large_text, small_image=smallLogo, small_text=smallTxt)

            except (PipeClosed, BrokenPipeError, ServerError):
                self.disable()
                DiscordRPC.notify.warning('Warning: Lost connection to DiscordRPC, trying to reconnect in 30 seconds.')
                self.RPC = None

                self.discordTaskLoop = threading.Timer(30, self.reconnectDiscord)
                self.discordTaskLoop.start()
            except RuntimeError as e:
                if str(e) == 'This event loop is already running':
                    DiscordRPC.notify.warning(f'DiscordRPC:\n\n{e}')
                else:
                    DiscordRPC.notify.warning(f'DiscordRPC Runtime Error:\n\n{e}')

    def setLaff(self, hp, maxHp):
        if not base.wantRichPresence:
            return

        self.state = '({0}/{1}) {2}'.format(hp, maxHp, base.localAvatar.getName())
        self.setData()

    def updateTasks(self, task):
        if not base.wantRichPresence:
            return

        self.updateTask = True
        self.setData()
        return task.again

    def avChoice(self):
        if not base.wantRichPresence:
            return

        self.large_image = gameLogo
        self.details = str(TTLocalizer.lPickingAToon)
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        self.state = '  '
        DiscordRPC.notify.info(f'{self.username} is choosing an avatar!')
        self.setData()

    def launching(self):
        if not base.wantRichPresence:
            return

        self.large_image = gameLogo
        startingGameList = [f'{TTLocalizer.lStartingGame}', f'{TTLocalizer.lBootingUpGame}', f'{TTLocalizer.lLoadingIntoGame}']
        self.details = f'{random.choice(startingGameList)}'.format(f'Toontown')

        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        DiscordRPC.notify.info(f'{self.username} is starting {gameName}!')
        self.setData()

    def making(self):
        if not base.wantRichPresence:
            return

        self.large_image = gameLogo
        self.details = str(TTLocalizer.lMakingAToon)
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        DiscordRPC.notify.info(f'{self.username} is making a Toon!')
        self.setData()

    def loading(self, avatarName):
        if not base.wantRichPresence:
            return

        QuickLauncher.setValue(self, key=self.avatarNameKey, value=f'{avatarName}')

        self.avatarName = QuickLauncher.getValue(self, key=self.avatarNameKey, default=None)

        self.large_image = gameLogo
        self.details = f'{TTLocalizer.lLoadingIntoGame}'.format('Toontown')
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        self.state = '  '
        if self.avatarName is not None:
            self.smallTxt = f'Playing as {self.avatarName}'
            DiscordRPC.notify.info(f'{self.username} is loading into {gameName} as {self.avatarName}!')
        else:
            DiscordRPC.notify.info(f'{self.username} is loading into {gameName}!')
        self.setData()

    def vp(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'sellbot_hq_towers' # sellbot_hq_vp
        self.details = f'{TTLocalizer.lSellbotTowersRPC}' # TTLocalizer.lFightingTheVP
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        DiscordRPC.notify.info(f'{self.username} is fighting the V.P.!')
        self.setData()

    def cfo(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'cashbot_hq_vault'
        self.details = f'{TTLocalizer.lCashbotVaultRPC}' # TTLocalizer.lFightingTheCFO
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        DiscordRPC.notify.info(f'{self.username} is fighting the C.F.O.!')
        self.setData()

    def cj(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'lawbot_hq_courthouse' # lawbot_hq_cj
        # self.details = str(TTLocalizer.lFightingTheCJ)
        self.details = f'{TTLocalizer.lLawbotCourthouseRPC}' # TTLocalizer.lFightingTheCJ
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        DiscordRPC.notify.info(f'{self.username} is fighting the C.J.!')
        self.setData()

    def ceo(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'bossbot_hq_clubhouse' # bossbot_hq_ceo
        self.details = f'{TTLocalizer.lBossbotClubhouseRPC}' # TTLocalizer.lFightingTheCEO
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        DiscordRPC.notify.info(f'{self.username} is fighting the C.E.O.!')
        self.setData()

    def building(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'cog-building'
        self.details = str(TTLocalizer.lInACogBuilding)
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        self.avatarName = QuickLauncher.getValue(self, key=self.avatarNameKey, default=None)
        DiscordRPC.notify.info(f'{self.avatarName} has entered a C.O.G. building!')
        self.setData()

    def sleeping(self):
        if not base.wantRichPresence:
            return

        self.grabbedCurrentDetails = QuickLauncher.getValue(self, key=self.currentDetailsKey, default=None)
        if self.grabbedCurrentDetails is not None:
            QuickLauncher.setValue(self, key=self.previousDetailsKey, value=f'{self.grabbedCurrentDetails}')

        self.details = f'{TTLocalizer.lSleeping}...'
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
        self.smallLogo = f'sleeping'

        self.avatarName = QuickLauncher.getValue(self, key=self.avatarNameKey, default=None)
        DiscordRPC.notify.info(f'{self.avatarName} has fallen asleep!')
        self.setData()

    def reawaken(self):
        if not base.wantRichPresence:
            return

        self.grabbedPreviousDetailsKey = QuickLauncher.getValue(self, key=self.previousDetailsKey, default=None)
        if self.grabbedPreviousDetailsKey is not None:
            QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.grabbedPreviousDetailsKey}')
            self.details = QuickLauncher.getValue(self, key=self.currentDetailsKey, default=None)
        else:
            self.details = '  '
        QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')

        self.avatarName = QuickLauncher.getValue(self, key=self.avatarNameKey, default=None)
        DiscordRPC.notify.info(f'{self.avatarName} has reawoken from falling asleep!')
        self.smallLogo = 'game-icon'
        self.setData()

    def startTasks(self):
        if not base.wantRichPresence:
            return

        taskMgr.doMethodLater(10, self.updateTasks, 'UpdateTask')

    def setServerVersion(self, serverVersion):
        if not base.wantRichPresence:
            return

        self.smallTxt = serverVersion
        DiscordRPC.notify.debug(f'Current server version is "{serverVersion}".')
        self.setData()

    def setZone(self, zone): # Set image and text based on the zone
        if not isinstance(zone, int) or not base.wantRichPresence:
            return
        QuickLauncher.setValue(self, key=self.zoneIdKey, value=f'{zone}')

        zone -= zone % 100
        DiscordRPC.notify.info(f'The zone is set to "{zone}"')
        data = zone2imgdesc.get(zone, None)
        if not data:
            DiscordRPC.notify.error(f'Error: Zone Not Found!: {zone}')
        else:
            self.large_image = data[0]
            # self.details = '  '
            self.details = data[1]
            QuickLauncher.setValue(self, key=self.currentDetailsKey, value=f'{self.details}')
            self.large_text = data[1]
            self.setData()

    def reconnectDiscord(self):
        self.enable()
        self.discordTaskLoop = None

    def enable(self):
        try:
            if self.RPC is None:
                self.RPC = pypresence.Presence(clientId)

                try:
                    self.RPC.connect()
                    DiscordRPC.notify.info(f'DiscordRPC has been connected!')

                except PermissionError as permError:
                    DiscordRPC.notify.error(f'Error: Failed to connect to DiscordRPC for the following reason:\n\n{permError}')
                    self.RPC = None
                except ConnectionError:
                    DiscordRPC.notify.error('Error: Lost connection to DiscordRPC, trying to reconnect in 30 seconds.')
                    self.RPC = None

                    self.discordTaskLoop = threading.Timer(30, self.reconnectDiscord)
                    self.discordTaskLoop.start()

        except PyPresenceException as discordPresenceExceptionError:
            DiscordRPC.notify.error(f'Error: DiscordRPC could not be disabled for the following reason:\n\n{discordPresenceExceptionError}')
            self.RPC = None
        except BaseException as enableExceptionError:
            DiscordRPC.notify.error(f'Error: DiscordRPC could not be disabled for the following reason:\n\n{enableExceptionError}')
            self.RPC = None

    def disable(self):
        try:
            if self.RPC is not None:
                self.RPC.clear()
                self.RPC.close()
                DiscordRPC.notify.info(f'DiscordRPC has been disabled.')
        except DiscordNotFound:
            DiscordRPC.notify.error(f'Error: Discord could not be found for this client.')
        except PyPresenceException as PyPresenceExceptionError:
            DiscordRPC.notify.warning(f'Error: DiscordRPC could not be disabled for the following reason:\n\n{PyPresenceExceptionError}')
        except BaseException as disableExceptionError:
            DiscordRPC.notify.error(f'Error: DiscordRPC could not be disabled for the following reason:\n\n{disableExceptionError}')
        self.RPC = None
        self.updateTask = None
