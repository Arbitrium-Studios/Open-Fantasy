import time
import random
from ctypes import *
from direct.task import Task 
from pypresence import Presence
class DiscordRPC(object):

    zone2imgdesc = { # A dict of ZoneID -> An image and a description
        
        # Add Doodlevania

        1000: ["toontown-shipyard", "in Toontown Shipyard"],
        1100: ["toontown-shipyard", "on Barnacle Boulevard"],
        1200: ["toontown-shipyard", "on Seaweed Street"],
        1300: ["toontown-shipyard", "on Lighthouse Lane"],

        2000: ["toontown-central", "in Toontown Central"],
        2100: ["toontown-central", "on Silly Street"],
        2200: ["toontown-central", "on Loopy Lane"],
        2300: ["toontown-central", "on Punchline Place"],

        3000: ["tundra-wonderland", "in Tundra Wonderland"],
        3100: ["tundra-wonderland", "on Walrus Way"],
        3200: ["tundra-wonderland", "on Sleet Street"],
        3300: ["tundra-wonderland", "on Polar Place"],

        4000: ["the-land-of-music", "in the Land of Music"],
        4100: ["the-land-of-music", "on Alto Avenue"],
        4200: ["the-land-of-music", "on Baritone Boulevard"],
        4300: ["the-land-of-music", "on Tenor Terrace"],

        5000: ["flowering-grove", "in the Flovering Grove"],
        5100: ["flowering-grove", "on Elm Street"],
        5200: ["flowering-grove", "on Maple Street"],
        5300: ["flowering-grove", "on Oak Street"],

        6000: ["acorn-acres", "in Acorn Acres"],


        8000: ["toontown-stadium", "in Toontown Stadium"],

        9000: ["twlight-dreamland", "in Twlight Dreamland"],
        9100: ["twlight-dreamland", "on Lullaby Lane"],
        9200: ["twlight-dreamland", "on Pajama Place"],
        # 9300: ["twlight-dreamland", "on Twilight Terrace"],

        10000: ["bossbot-hq", "at Bossbot Headquarters"],
        10100: ["bossbot-hq", "in The Chief Executive Officer's Clubhouse"],
        10200: ["bossbot-hq", "in The Chief Executive Officer's Clubhouse"],
        10500: ["bossbot-hq", "in The Front Three"],
        10600: ["bossbot-hq", "in The Middle Six"],
        10700: ["bossbot-hq", "in The Back Nine"],

        11000: ["sellbot-hq", "at Sellbot Headquarters"],
        11100: ["sellbot-hq", "in The Vice President's Lobby"],
        11200: ["sellbot-hq", "in The Sellbot HQ Factory Exterior"],
        11500: ["sellbot-hq", "in The Sellbot Factory"],

        12000: ["cashbot-hq", "at Cashbot Headquarters"],
        12100: ["cashbot-hq", "in The Chief Financial Officer's Lobby"],
        12500: ["cashbot-hq", "in The Cashbot Coin Mint"],
        12600: ["cashbot-hq", "in The Cashbot Dollar Mint"],
        12700: ["cashbot-hq", "in The Cashbot Bullion Mint"],

        13000: ["lawbot-hq", "at Lawbot Headquarters"],
        13100: ["lawbot-hq", "in The Chief Justice's Lobby"],
        13200: ["lawbot-hq", "in The DA's Office Lobby"],
        13300: ["lawbot-hq", "in The Lawbot Office A"],
        13400: ["lawbot-hq", "in The Lawbot Office B"],
        13500: ["lawbot-hq", "in The Lawbot Office C"],
        13600: ["lawbot-hq", "in The Lawbot Office D"],

        14000: ["toontorial-terrace", "in The Toontorial"],

        16000: ["toon-estate", "at A Toon Estate"],

        17000: ['mini-golf', "in the Toontown Mini-Golf Area"], # Remove this once we've begun merging Goofy Speedway and the Mini-Golf Area into Toontown Stadium

    }

    def __init__(self):
        self.RPC = None
        self.enable()
        self.updateTask = None
        self.details = "Loading" # text next to photo
        self.image = 'toontown-logo' #Main image
        self.imageTxt = 'Toontown Fantasy' #Hover text for main image 
        self.smallLogo = 'game-icon' #small image in corner
        self.state = '   ' #Displayed underneath details, used for boarding groups
        self.smallTxt = 'Loading'
        self.partySize = 1
        self.maxParty = 1


    def stopBoarding(self):
        if base.wantRichPresence:
            self.partySize = 1
            self.state = '  '
            self.maxParty = 1
            self.setData()

    def allowBoarding(self, size):
        if base.wantRichPresence:
            self.state = 'in a boarding group'
            self.partySize = 1
            self.maxParty = size
            self.setData()

    def setBoarding(self, size):
        if base.wantRichPresence:
            self.PartySize = size
            self.setData()

    def setData(self, details=None, image=None, imageTxt=None):
        if details is None:
            details = self.details
        if image is None:
            image = self.image
        if imageTxt is None:
            imageTxt = self.imageTxt
        smallLogo = self.smallLogo
        smallTxt = self.smallTxt
        state = self.state
        party = self.partySize
        maxSize = self.maxParty
        if self.RPC is not None and base.wantRichPresence:
            self.RPC.update(state=state,details=details , large_image=image, large_text=imageTxt,  small_image=smallLogo, small_text=smallTxt, party_size=[party, maxSize])

    def setLaff(self, hp, maxHp):
        if base.wantRichPresence:
            self.state = '{0}: {1}/{2}'.format(base.localAvatar.name, hp, maxHp)
            self.setData()

    def updateTasks(self, task):
        if base.wantRichPresence:
            self.updateTask = True
            self.setData()
            return task.again
    
    def avChoice(self):
        if base.wantRichPresence:
            self.image = 'toontown-logo'
            self.details = 'Picking a Toon.'
            self.state = '  '
            self.setData()

    def launching(self):
        if base.wantRichPresence:
            self.image = 'toontown-logo'
            self.details = 'Loading...'
            self.setData()

    def making(self):
        if base.wantRichPresence:
            self.image = 'toontown-logo'
            self.details = 'Making a Toon.'

    def vp(self):
        if base.wantRichPresence:
            self.image = 'vp'
            self.details = 'Fighting the V.P..'
            self.setData()

    def cfo(self):
        if base.wantRichPresence:
            self.image = 'cfo'
            self.details = 'Fighting the C.F.O.'
            self.setData()

    def cj(self):
        if base.wantRichPresence:
            self.image = 'cj'
            self.details = 'Fighting the C.J.'
            self.setData()

    def ceo(self):
        if base.wantRichPresence:
            self.image = 'ceo'
            self.details = 'Fighting the CEO.'

    def building(self):
        if base.wantRichPresence:
            self.image = 'building'
            self.details = 'in a building.'
            self.setData()


    

    def startTasks(self):
        if base.wantRichPresence:
            taskMgr.doMethodLater(10, self.updateTasks, 'UpdateTask')

    def setDistrict(self, name):
        if base.wantRichPresence:
            self.smallTxt = name

    def setZone(self,zone): # Set image and text based on the zone
        if not isinstance(zone, int) or not base.wantRichPresence:
            return
        zone -= zone % 100
        data = self.zone2imgdesc.get(zone,None)
        if data:
            self.image = data[0]
            self.details = data[1]
            self.setData()
        else:
            print("Error: Zone Not Found!")

    def disable(self):
        try:
            self.RPC.clear()
            if self.RPC is not None:
                self.RPC.close()
        except BaseException:
            print('DiscordRPC: Warning: Discord not open or invalid client id')
        self.RPC = None
        self.updateTask = None

    def enable(self):
        clientId = "994119909929914419"
        try:
            if self.RPC is None:
                self.RPC = Presence(clientId)
        except BaseException:
            print("DiscordRPC: Warning : Discord not found for this client.")
            self.RPC = None
        try:
            if base.wantRichPresence and self.RPC is not None:
                self.RPC.connect()
        except BaseException:
            print("DiscordRPC: Warning: Failed to connect to discord client.")


