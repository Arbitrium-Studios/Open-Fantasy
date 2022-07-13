from . import TownLoader
from . import DGStreet
from toontown.suit import Suit


class DGTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = DGStreet.DGStreet
        self.musicFile = 'user/resources/default/phase_8/audio/bgm/DG_SZ.ogg'
        self.activityMusicFile = 'user/resources/default/phase_8/audio/bgm/DG_SZ.ogg'
        self.townStorageDNAFile = 'user/resources/default/phase_8/dna/storage_DG_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(3)
        dnaFile = 'user/resources/default/phase_8/dna/daisys_garden_' + \
            str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        Suit.unloadSuits(3)
        TownLoader.TownLoader.unload(self)
