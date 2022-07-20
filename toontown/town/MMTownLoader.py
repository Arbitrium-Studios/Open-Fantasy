
from . import TownLoader
from . import MMStreet
from toontown.suit import Suit
if __debug__:
    from direct.directnotify import DirectNotifyGlobal

class MMTownLoader(TownLoader.TownLoader):
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory("MMTownLoader")
    
    def __init__(self, hood, parentFSM, doneEvent):
        assert self.notify.debug("__init__()")
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = MMStreet.MMStreet
        self.musicFile = "phase_6/audio/bgm/MM_SZ.ogg"
        self.activityMusicFile = "phase_6/audio/bgm/MM_SZ_activity.ogg"
        self.townStorageDNAFile = "phase_6/dna/storage_MM_town.dna"

    def load(self, zoneId):
        assert self.notify.debug("__init__()")
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(2)
        dnaFile = ("phase_6/dna/minnies_melody_land_" + str(self.canonicalBranchZone) + ".dna")
        self.createHood(dnaFile)

    def unload(self):
        assert self.notify.debug("__init__()")
        Suit.unloadSuits(2)
        TownLoader.TownLoader.unload(self)

