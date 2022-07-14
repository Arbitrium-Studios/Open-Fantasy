import time 
from ctypes import *
from direct.task import Task 
from pypresence import Presence
class DiscordRPC(object):

    zone2imgdesc = { # A dict of ZoneID -> An image and a description
        1000: ["toontown-docks", "In Toontown Docks"],
        1100: ["toontown-docks", "On Barnacle Boulevard"],
        1200: ["toontown-docks", "On Seaweed Street"],
        1300: ["toontown-docks", "On Lighthouse Lane"],

        2000: ["toontown-central", "In Toontown Central"],
        2100: ["toontown-central", "On Silly Street"],
        2200: ["toontown-central", "On Loopy Lane"],
        2300: ["toontown-central", "On Punchline Place"],

        3000: ["tundra-wonderland", "In Tundra Wonderland"],
        3100: ["tundra-wonderland", "On Walrus Way"],
        3200: ["tundra-wonderland", "On Sleet Street"],
        3300: ["tundra-wonderland", "On Polar Place"],

        4000: ["the-land-of-music", "In The Land of Music"],
        4100: ["the-land-of-music", "On Alto Avenue"],
        4200: ["the-land-of-music", "On Baritone Boulevard"],
        4300: ["the-land-of-music", "On Tenor Terrace"],

        5000: ["flowering-grove", "In the Flovering Grove"],
        5100: ["flowering-grove", "On Elm Street"],
        5200: ["flowering-grove", "On Maple Street"],
        5300: ["flowering-grove", "On Oak Street"],

        6000: ["acorn-acres", "At Acorn Acres"],


        8000: ["toontown-stadium", "In Toontown Stadium"],

        9000: ["twlight-dreamland", "In Twlight Dreamland"],
        9100: ["twlight-dreamland", "On Lullaby Lane"],
        9200: ["twlight-dreamland", "On Pajama Place"],
        # 9300: ["twlight-dreamland", "On Twilight Terrace"],

        10000: ["bossbot-hq", "At Bossbot Headquarters"],
        10100: ["bossbot-hq", "In The Chief Executive Officer's Clubhouse"],
        10200: ["bossbot-hq", "In The Chief Executive Officer's Clubhouse"],
        10500: ["bossbot-hq", "In The Front Three"],
        10600: ["bossbot-hq", "In The Middle Six"],
        10700: ["bossbot-hq", "In The Back Nine"],

        11000: ["sellbot-hq", "At Sellbot Headquarters"],
        11100: ["sellbot-hq", "In The Vice President's Lobby"],
        11200: ["sellbot-hq", "In The Sellbot HQ Factory Exterior"],
        11500: ["sellbot-hq", "In The Sellbot Factory"],

        12000: ["cashbot-hq", "At Cashbot Headquarters"],
        12100: ["cashbot-hq", "In The Chief Financial Officer's Lobby"],
        12500: ["cashbot-hq", "In The Cashbot Coin Mint"],
        12600: ["cashbot-hq", "In The Cashbot Dollar Mint"],
        12700: ["cashbot-hq", "In The Cashbot Bullion Mint"],

        13000: ["lawbot-hq", "At Lawbot Headquarters"],
        13100: ["lawbot-hq", "In The Chief Justice's Lobby"],
        13200: ["lawbot-hq", "In The DA's Office Lobby"],
        13300: ["lawbot-hq", "In The Lawbot Office A"],
        13400: ["lawbot-hq", "In The Lawbot Office B"],
        13500: ["lawbot-hq", "In The Lawbot Office C"],
        13600: ["lawbot-hq", "In The Lawbot Office D"],

        14000: ["tutorial", "In The Toontorial"],

        16000: ["estate", "At A Toon Estate"],

        17000: ['golf', "In Acorn Acres's Mini-Golf"], # Remove this once we've begun merging Goofy Speedway and the Mini-Golf Area into Toontown Stadium

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
            self.state = 'In a boarding group'
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
            self.details = 'In a building.'
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


