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

playgroundZoneID = ToontownGlobals.ToontownCentral
streetZoneID = ToontownGlobals.BarnacleBoulevard

lInThePlayground = f'{TTLocalizer.GlobalStreetNames[playgroundZoneID][-2]}'.capitalize()
lOnStreet = f'{TTLocalizer.GlobalStreetNames[streetZoneID][-2]}'.capitalize()
lFoggyFjord = f'{TTLocalizer.FoggyFjord[2]}'.title()
lInAcornAcres = f'{TTLocalizer.AcornAcres[1]} {TTLocalizer.AcornAcres[2]}'.title()
lInToontownStadium = f'{TTLocalizer.ToontownStadium[1]} {TTLocalizer.ToontownStadium[2]}'.title()
lOnToontorialTerrace = f'{TTLocalizer.GlobalStreetNames[ToontownGlobals.TutorialTerrace][-2]} {TTLocalizer.GlobalStreetNames[ToontownGlobals.TutorialTerrace][-1]}'.title()
lInTheBossbotHQ = f'{TTLocalizer.GlobalStreetNames[ToontownGlobals.BossbotHQ][-2]}'.capitalize()
lInTheSellbotHQ = f'{TTLocalizer.GlobalStreetNames[ToontownGlobals.SellbotHQ][-2]}'.capitalize()
lInTheCashbotHQ = f'{TTLocalizer.GlobalStreetNames[ToontownGlobals.CashbotHQ][-2]}'.capitalize()
lInTheLawbotHQ = f'{TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotHQ][-2]}'.capitalize()

zone2imgdesc = { # A dict of ZoneID -> An image and a description

    1000: ["foggy-fjord", f"{lInThePlayground} {TTLocalizer.GlobalStreetNames[playgroundZoneID][-1]}, {lFoggyFjord}"],
    1100: ["foggy-fjord", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.BarnacleBoulevard][-1]}, {lFoggyFjord}"],
    1200: ["foggy-fjord", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.SeaweedStreet][-1]}, {lFoggyFjord}"],
    1300: ["foggy-fjord", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.LighthouseLane][-1]}, {lFoggyFjord}"],

    2000: ["toontown-central", f"{lInThePlayground} {TTLocalizer.GlobalStreetNames[playgroundZoneID][-1]}, {TTLocalizer.lToontownCentral}"],
    2100: ["toontown-central", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.SillyStreet][-1]}, {TTLocalizer.lToontownCentral}"],
    2200: ["toontown-central", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.LoopyLane][-1]}, {TTLocalizer.lToontownCentral}"],
    2300: ["toontown-central", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.PunchlinePlace][-1]}, {TTLocalizer.lToontownCentral}"],

    3000: ["tundra-wonderland", f"{lInThePlayground} {TTLocalizer.GlobalStreetNames[playgroundZoneID][-1]}, {TTLocalizer.lTundraWonderland}"],
    3100: ["tundra-wonderland", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.WalrusWay][-1]}, {TTLocalizer.lTundraWonderland}"],
    3200: ["tundra-wonderland", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.SleetStreet][-1]}, {TTLocalizer.lTundraWonderland}"],
    3300: ["tundra-wonderland", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.PolarPlace][-1]}, {TTLocalizer.lTundraWonderland}"],

    4000: ["harmony-haven", f"{lInThePlayground} {TTLocalizer.GlobalStreetNames[playgroundZoneID][-1]}, {TTLocalizer.lHarmoniousHaven}"],
    4100: ["harmony-haven", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.AltoAvenue][-1]}, {TTLocalizer.lHarmoniousHaven}"],
    4200: ["harmony-haven", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.BaritoneBoulevard][-1]}, {TTLocalizer.lHarmoniousHaven}"],
    4300: ["harmony-haven", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.TenorTerrace][-1]}, {TTLocalizer.lHarmoniousHaven}"],

    5000: ["flowering-grove", f"{lInThePlayground} {TTLocalizer.GlobalStreetNames[playgroundZoneID][-1]}, {TTLocalizer.lFloweringGrove}"],
    5100: ["flowering-grove", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.ElmStreet][-1]}, {TTLocalizer.lFloweringGrove}"],
    5200: ["flowering-grove", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.MapleStreet][-1]}, {TTLocalizer.lFloweringGrove}"],
    5300: ["flowering-grove", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.OakStreet][-1]}, {TTLocalizer.lFloweringGrove}"],

    6000: ["acorn-acres", f"{lInAcornAcres}"],

    8000: ["toontown-stadium", f"{lInToontownStadium}"],

    9000: ["twlight-dreamland", f"{lInThePlayground} {TTLocalizer.GlobalStreetNames[playgroundZoneID][-1]}, {TTLocalizer.lTwilightDreamland}"],
    9100: ["twlight-dreamland", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.LullabyLane][-1]}, {TTLocalizer.lTwilightDreamland}"],
    9200: ["twlight-dreamland", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.PajamaPlace][-1]}, {TTLocalizer.lTwilightDreamland}"],
    9300: ["twlight-dreamland", f"{lOnStreet} {TTLocalizer.GlobalStreetNames[ToontownGlobals.TwilightTerrace][-1]}, {TTLocalizer.lTwilightDreamland}"],

    10000: ["bossbot-hq", f"{lInTheBossbotHQ} {TTLocalizer.GlobalStreetNames[ToontownGlobals.BossbotHQ][-1]}, {TTLocalizer.lBossbotHQ}"],
    10100: ["bossbot-hq", f"The Chief Executive Officer's Clubhouse"],
    10200: ["bossbot-hq", f"The Chief Executive Officer's Clubhouse"],
    10500: ["bossbot-hq", f"The Front Three"],
    10600: ["bossbot-hq", f"The Middle Six"],
    10700: ["bossbot-hq", f"The Back Nine"],

    11000: ["sellbot-hq", f"{lInTheSellbotHQ} {TTLocalizer.GlobalStreetNames[ToontownGlobals.SellbotHQ][-1]}, {TTLocalizer.lSellbotHQ}"],
    11100: ["sellbot-hq", f"The Vice President's Lobby, {TTLocalizer.lSellbotHQ}"],
    11200: ["sellbot-hq", f"The Sellbot HQ Factory Exterior, {TTLocalizer.lSellbotHQ}"],
    11500: ["sellbot-hq", f"The Sellbot Factory, {TTLocalizer.lSellbotHQ}"],

    12000: ["cashbot-hq", f"{lInTheCashbotHQ} {TTLocalizer.GlobalStreetNames[ToontownGlobals.CashbotHQ][-1]}, {TTLocalizer.lCashbotHQ}"],
    12100: ["cashbot-hq", f"The Chief Financial Officer's Lobby"],
    12500: ["cashbot-hq", f"The Cashbot Coin Mint"],
    12600: ["cashbot-hq", f"The Cashbot Dollar Mint"],
    12700: ["cashbot-hq", f"The Cashbot Bullion Mint"],

    13000: ["lawbot-hq", f"{lInTheLawbotHQ} {TTLocalizer.GlobalStreetNames[ToontownGlobals.LawbotHQ][-1]}, {TTLocalizer.lLawbotHQ}"],
    13100: ["lawbot-hq", f"The Chief Justice's Lobby"],
    13200: ["lawbot-hq", f"The DA's Office Lobby"],
    13300: ["lawbot-hq", f"The Lawbot Office A"],
    13400: ["lawbot-hq", f"The Lawbot Office B"],
    13500: ["lawbot-hq", f"The Lawbot Office C"],
    13600: ["lawbot-hq", f"The Lawbot Office D"],

    14000: ["toontorial", f"{lOnToontorialTerrace}"],

    16000: ["toon-estate", f"A Toon Estate"],

    17000: ['mini-golf', f"{TTLocalizer.lGolfZone}"], # Remove this once we've begun merging Goofy Speedway and the Mini-Golf Area into Toontown Stadium
}

class DiscordRPC(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('DiscordRPC')
    hasFinishedCoolDownToggle = bool(False)

    def __init__(self):
        self.RPC = None

        if base.wantRichPresence:
            self.enable()
        else:
            self.disable()

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
        self.large_image = gameLogo # Sets the main image displayed on the Discord profile
        self.large_text = gameName # Hover text for main image 
        self.smallLogo = 'game-icon' # Set the image that appears in the bottom-right corner of the main image
        self.state = '   ' # Set the text that appears underneath the details (used for boarding groups)
        self.smallTxt = '   ' # Sets the text that appears when you hover over the smaller logo
        self.discordTaskLoop = None

    def stopBoarding(self):
        if not base.wantRichPresence:
            return

        self.state = '  '
        self.setData()

    def allowBoarding(self, size):
        if not base.wantRichPresence:
            return

        self.state = 'in a boarding group'
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
                self.RPC.update(name=gameName, state=self.state, details=details, large_image=large_image, large_text=large_text, small_image=smallLogo, small_text=smallTxt)

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

        self.state = '{0}: {1}/{2}'.format(base.localAvatar.getName(), hp, maxHp)
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
        self.details = 'Picking a Toon'
        self.state = '  '
        DiscordRPC.notify.info(f'{self.username} is choosing an avatar!')
        self.setData()

    def launching(self):
        if not base.wantRichPresence:
            return

        self.large_image = gameLogo
        self.details = 'Starting Toontown...'
        self.smallTxt = 'Starting...'
        DiscordRPC.notify.info(f'{self.username} is starting {gameName}!')
        self.setData()

    def making(self):
        if not base.wantRichPresence:
            return

        self.large_image = gameLogo
        self.details = 'Making a Toon...'
        DiscordRPC.notify.info(f'{self.username} is making a Toon!')
        self.setData()

    def loading(self):
        if not base.wantRichPresence:
            return

        self.large_image = gameLogo
        self.details = 'Loading into Toontown...'
        self.smallTxt = 'Loading...'
        self.state = '  '
        DiscordRPC.notify.info(f'{self.username} is loading into {gameName}!')
        self.setData()

    def vp(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'sellbot_hq_vp'
        self.details = 'Fighting the V.P.'
        DiscordRPC.notify.info(f'{self.username} is fighting the V.P.!')
        self.setData()

    def cfo(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'cashbot_hq_cfo'
        self.details = 'Fighting the C.F.O.'
        DiscordRPC.notify.info(f'{self.username} is fighting the C.F.O.!')
        self.setData()

    def cj(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'lawbot_hq_cj'
        self.details = 'Fighting the C.J.'
        DiscordRPC.notify.info(f'{self.username} is fighting the C.J.!')
        self.setData()

    def ceo(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'bossbot_hq_ceo'
        self.details = 'Fighting the C.E.O.'
        DiscordRPC.notify.info(f'{self.username} is fighting the C.E.O.!')
        self.setData()

    def building(self):
        if not base.wantRichPresence:
            return

        self.large_image = 'cog-building'
        self.details = 'in a Cog Building'
        DiscordRPC.notify.info(f'Player has entered a cog building!')
        self.setData()

    def sleeping(self):
        if not base.wantRichPresence:
            return

        self.smallLogo = 'sleeping'
        self.details = f'{self.smallLogo}'.capitalize()
        DiscordRPC.notify.info(f'Player has fallen asleep!')
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

        zone -= zone % 100
        DiscordRPC.notify.debug(f'The zone is set to "{zone}"')
        data = zone2imgdesc.get(zone, None)
        if not data:
            DiscordRPC.notify.debug(f'Error: Zone Not Found!: {zone}')
        else:
            self.large_image = data[0]
            self.details = data[1]
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

    def disable(self):
        try:
            if self.RPC is not None:
                self.RPC.clear()
                self.RPC.close()
                DiscordRPC.notify.info(f'DiscordRPC has been disabled.')
        except DiscordNotFound:
            DiscordRPC.notify.error(f'Error: Discord could not be found for this client.')
        except Exception as disableExceptionError:
            DiscordRPC.notify.error(f'Error: DiscordRPC could not be disabled for the following reason:\n\n{disableExceptionError}')
        except PyPresenceException as PyPresenceExceptionError:
            DiscordRPC.notify.warning(f'Error: DiscordRPC could not be disabled for the following reason:\n\n{PyPresenceExceptionError}')
        self.RPC = None
        self.updateTask = None
