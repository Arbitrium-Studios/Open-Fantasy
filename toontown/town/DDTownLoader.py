from . import TownLoader
from . import DDStreet
from toontown.suit import Suit


class DDTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = DDStreet.DDStreet
        self.musicFile = 'user/resources/default/phase_6/audio/bgm/DD_SZ.ogg'
        self.activityMusicFile = 'user/resources/default/phase_6/audio/bgm/DD_SZ_activity.ogg'
        self.townStorageDNAFile = 'user/resources/default/phase_6/dna/storage_DD_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(2)
        dnaFile = 'user/resources/default/phase_6/dna/donalds_dock_' + \
            str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        Suit.unloadSuits(2)
        TownLoader.TownLoader.unload(self)

    def enter(self, requestStatus):
        TownLoader.TownLoader.enter(self, requestStatus)

    def exit(self):
        TownLoader.TownLoader.exit(self)
