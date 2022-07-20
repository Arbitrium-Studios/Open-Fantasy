from . import TownLoader
from . import BRStreet
from toontown.suit import Suit


class BRTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = BRStreet.BRStreet
        self.musicFile = '../../user/default/resources/default/phase_8/audio/bgm/TB_SZ.ogg'
        self.activityMusicFile = '../../user/default/resources/default/phase_8/audio/bgm/TB_SZ_activity.ogg'
        self.townStorageDNAFile = '../../user/default/resources/default/phase_8/dna/storage_BR_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(3)
        dnaFile = '../../user/default/resources/default/phase_8/dna/the_burrrgh_' + \
            str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        Suit.unloadSuits(3)
        TownLoader.TownLoader.unload(self)
